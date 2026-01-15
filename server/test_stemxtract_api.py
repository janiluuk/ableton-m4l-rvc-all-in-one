"""
Test suite for StemXtract API integration
Tests the /stemxtract/process endpoint
"""
import sys
import pytest
import os
import tempfile
import wave
import numpy as np
from unittest.mock import Mock, patch, MagicMock

# Mock heavy dependencies before importing main
sys.modules['torch'] = MagicMock()
sys.modules['librosa'] = MagicMock()
sys.modules['librosa.core'] = MagicMock()
sys.modules['scipy'] = MagicMock()
sys.modules['scipy.io'] = MagicMock()
sys.modules['scipy.io.wavfile'] = MagicMock()
sys.modules['uvr5_pack'] = MagicMock()
sys.modules['uvr5_pack.lib_v5'] = MagicMock()
sys.modules['uvr5_pack.lib_v5.spec_utils'] = MagicMock()
sys.modules['uvr5_pack.utils'] = MagicMock()
sys.modules['uvr5_pack.lib_v5.model_param_init'] = MagicMock()
sys.modules['gradio_client'] = MagicMock()

from fastapi.testclient import TestClient
from main import app

# Test constants
TEST_STEMXTRACT_SERVER = "http://localhost:60000"


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_audio_file():
    """Create a sample WAV file for testing"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        # Create a simple mono WAV file (1 second, 44100 Hz)
        sample_rate = 44100
        duration = 1.0
        frequency = 440.0
        
        with wave.open(f.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            
            # Generate a simple sine wave
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio = np.sin(2 * np.pi * frequency * t)
            audio = (audio * 32767).astype(np.int16)
            wf.writeframes(audio.tobytes())
        
        yield f.name
        
        # Cleanup
        if os.path.exists(f.name):
            os.remove(f.name)


class TestStemXtractEndpoint:
    """Test cases for /stemxtract/process endpoint"""
    
    def test_stemxtract_endpoint_exists(self, client):
        """Test that /stemxtract/process endpoint is accessible"""
        response = client.post("/stemxtract/process")
        # Should return 422 (validation error) not 404
        assert response.status_code == 422
    
    @patch('main.StemXtractClient')
    def test_stemxtract_basic_request(self, mock_client_class, client, sample_audio_file):
        """Test basic StemXtract request with default parameters"""
        # Create a mock instance and mock the process_track method
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance
        
        # Create temporary output files
        mock_output_files = []
        for name in ['final', 'drums', 'bass', 'other', 'vocals']:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            tmp.close()
            mock_output_files.append(tmp.name)
        
        # Mock the return value (final_output, processing_time, drums, bass, other, vocals)
        mock_client_instance.process_track.return_value = (
            mock_output_files[0],  # final_output
            "5.2 seconds",          # processing_time
            mock_output_files[1],  # drums
            mock_output_files[2],  # bass
            mock_output_files[3],  # other
            mock_output_files[4]   # vocals
        )
        
        try:
            with open(sample_audio_file, 'rb') as f:
                response = client.post(
                    "/stemxtract/process",
                    files={"file": ("test.wav", f, "audio/wav")},
                    data={
                        "stemxtract_server": TEST_STEMXTRACT_SERVER,
                        "task": "remove_vocals",
                        "model_name": "htdemucs"
                    }
                )
            
            assert response.status_code == 200
            assert response.headers['content-type'] == 'application/zip'
            assert mock_client_instance.process_track.called
            
            # Verify the parameters passed to process_track
            call_kwargs = mock_client_instance.process_track.call_args[1]
            assert call_kwargs['task'] == 'remove_vocals'
            assert call_kwargs['model_name'] == 'htdemucs'
        finally:
            # Cleanup mock output files
            for tmp_file in mock_output_files:
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)
    
    @patch('main.StemXtractClient')
    def test_stemxtract_with_volume_controls(self, mock_client_class, client, sample_audio_file):
        """Test StemXtract request with custom volume controls"""
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance
        
        # Create temporary output files
        mock_output_files = []
        for name in ['final', 'drums', 'bass', 'other', 'vocals']:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            tmp.close()
            mock_output_files.append(tmp.name)
        
        mock_client_instance.process_track.return_value = (
            mock_output_files[0], "5.2 seconds", mock_output_files[1],
            mock_output_files[2], mock_output_files[3], mock_output_files[4]
        )
        
        try:
            with open(sample_audio_file, 'rb') as f:
                response = client.post(
                    "/stemxtract/process",
                    files={"file": ("test.wav", f, "audio/wav")},
                    data={
                        "task": "isolate_vocals",
                        "drums_vol": "0.5",
                        "bass_vol": "0.8",
                        "other_vol": "1.2",
                        "vocals_vol": "1.5",
                        "instrumental_volume": "0.9",
                        "vocal_volume": "1.1"
                    }
                )
            
            assert response.status_code == 200
            
            call_kwargs = mock_client_instance.process_track.call_args[1]
            assert call_kwargs['task'] == 'isolate_vocals'
            assert call_kwargs['drums_vol'] == 0.5
            assert call_kwargs['bass_vol'] == 0.8
            assert call_kwargs['other_vol'] == 1.2
            assert call_kwargs['vocals_vol'] == 1.5
            assert call_kwargs['instrumental_volume'] == 0.9
            assert call_kwargs['vocal_volume'] == 1.1
        finally:
            for tmp_file in mock_output_files:
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)
    
    @patch('main.StemXtractClient')
    def test_stemxtract_with_effects(self, mock_client_class, client, sample_audio_file):
        """Test StemXtract request with EQ and reverb effects"""
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance
        
        mock_output_files = []
        for name in ['final', 'drums', 'bass', 'other', 'vocals']:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            tmp.close()
            mock_output_files.append(tmp.name)
        
        mock_client_instance.process_track.return_value = (
            mock_output_files[0], "5.2 seconds", mock_output_files[1],
            mock_output_files[2], mock_output_files[3], mock_output_files[4]
        )
        
        try:
            with open(sample_audio_file, 'rb') as f:
                response = client.post(
                    "/stemxtract/process",
                    files={"file": ("test.wav", f, "audio/wav")},
                    data={
                        "task": "mix_stems",
                        "instrumental_low_gain": "-3.0",
                        "instrumental_high_gain": "2.0",
                        "instrumental_reverb": "0.3",
                        "vocal_low_gain": "1.5",
                        "vocal_high_gain": "-1.0",
                        "vocal_reverb": "0.5",
                        "trim_silence_chk": "true"
                    }
                )
            
            assert response.status_code == 200
            
            call_kwargs = mock_client_instance.process_track.call_args[1]
            assert call_kwargs['task'] == 'mix_stems'
            assert call_kwargs['instrumental_low_gain'] == -3.0
            assert call_kwargs['instrumental_high_gain'] == 2.0
            assert call_kwargs['instrumental_reverb'] == 0.3
            assert call_kwargs['vocal_low_gain'] == 1.5
            assert call_kwargs['vocal_high_gain'] == -1.0
            assert call_kwargs['vocal_reverb'] == 0.5
            assert call_kwargs['trim_silence_chk'] is True
        finally:
            for tmp_file in mock_output_files:
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)
    
    @patch('main.StemXtractClient')
    def test_stemxtract_error_handling(self, mock_client_class, client, sample_audio_file):
        """Test error handling in StemXtract endpoint"""
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance
        mock_client_instance.process_track.side_effect = RuntimeError("StemXtract API error")
        
        with open(sample_audio_file, 'rb') as f:
            response = client.post(
                "/stemxtract/process",
                files={"file": ("test.wav", f, "audio/wav")}
            )
        
        assert response.status_code == 500
        assert "error" in response.json()
        assert "StemXtract API error" in response.json()["error"]
    
    def test_stemxtract_endpoint_schema(self, client):
        """Test StemXtract endpoint has correct schema"""
        response = client.get("/openapi.json")
        schema = response.json()
        
        assert "/stemxtract/process" in schema["paths"]
        stemxtract_schema = schema["paths"]["/stemxtract/process"]["post"]
        assert "requestBody" in stemxtract_schema


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
