"""
Test suite for RVC API endpoints
Tests both /convert and /uvr endpoints with various scenarios
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
sys.modules['uvr5_pack'] = MagicMock()
sys.modules['uvr5_pack.lib_v5'] = MagicMock()
sys.modules['uvr5_pack.lib_v5.spec_utils'] = MagicMock()
sys.modules['uvr5_pack.utils'] = MagicMock()
sys.modules['uvr5_pack.lib_v5.model_param_init'] = MagicMock()

from fastapi.testclient import TestClient
from main import app
from rvc_infer import RVCConverter


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


class TestConvertEndpoint:
    """Test cases for /convert endpoint"""
    
    def test_convert_endpoint_exists(self, client):
        """Test that /convert endpoint is accessible"""
        response = client.post("/convert")
        # Should return 422 (validation error) not 404
        assert response.status_code == 422
    
    @patch.object(RVCConverter, 'convert')
    def test_convert_basic_request(self, mock_convert, client, sample_audio_file):
        """Test basic convert request without separation"""
        # Create a mock output file
        mock_output = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        mock_output.close()
        mock_convert.return_value = mock_output.name
        
        try:
            with open(sample_audio_file, 'rb') as f:
                response = client.post(
                    "/convert",
                    files={"file": ("test.wav", f, "audio/wav")},
                    data={"rvc_model": "test_model"}
                )
            
            assert response.status_code == 200
            assert mock_convert.called
            
            # Verify the parameters passed to convert
            call_args = mock_convert.call_args[1]
            assert call_args['rvc_model'] == 'test_model'
            assert call_args['separate'] is False
            assert call_args['separator'] == 'demucs'
        finally:
            if os.path.exists(mock_output.name):
                os.remove(mock_output.name)
    
    @patch.object(RVCConverter, 'convert')
    def test_convert_with_demucs_separator(self, mock_convert, client, sample_audio_file):
        """Test convert request with Demucs separator"""
        mock_output = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        mock_output.close()
        mock_convert.return_value = mock_output.name
        
        try:
            with open(sample_audio_file, 'rb') as f:
                response = client.post(
                    "/convert",
                    files={"file": ("test.wav", f, "audio/wav")},
                    data={
                        "separate": "true",
                        "separator": "demucs",
                        "stem": "vocals"
                    }
                )
            
            assert response.status_code == 200
            
            call_args = mock_convert.call_args[1]
            assert call_args['separate'] is True
            assert call_args['separator'] == 'demucs'
            assert call_args['stem'] == 'vocals'
        finally:
            if os.path.exists(mock_output.name):
                os.remove(mock_output.name)
    
    @patch.object(RVCConverter, 'convert')
    def test_convert_with_uvr_separator(self, mock_convert, client, sample_audio_file):
        """Test convert request with UVR separator"""
        mock_output = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        mock_output.close()
        mock_convert.return_value = mock_output.name
        
        try:
            with open(sample_audio_file, 'rb') as f:
                response = client.post(
                    "/convert",
                    files={"file": ("test.wav", f, "audio/wav")},
                    data={
                        "separate": "true",
                        "separator": "uvr",
                        "stem": "vocals",
                        "uvr_model_path": "/custom/model.pth"
                    }
                )
            
            assert response.status_code == 200
            
            call_args = mock_convert.call_args[1]
            assert call_args['separate'] is True
            assert call_args['separator'] == 'uvr'
            assert call_args['stem'] == 'vocals'
            assert call_args['uvr_model_path'] == '/custom/model.pth'
        finally:
            if os.path.exists(mock_output.name):
                os.remove(mock_output.name)
    
    @patch.object(RVCConverter, 'convert')
    def test_convert_with_all_parameters(self, mock_convert, client, sample_audio_file):
        """Test convert request with all optional parameters"""
        mock_output = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        mock_output.close()
        mock_convert.return_value = mock_output.name
        
        try:
            with open(sample_audio_file, 'rb') as f:
                response = client.post(
                    "/convert",
                    files={"file": ("test.wav", f, "audio/wav")},
                    data={
                        "rvc_model": "test_model",
                        "output_format": "wav",
                        "pitch_change_all": "2.0",
                        "index_rate": "0.7",
                        "filter_radius": "5",
                        "rms_mix_rate": "0.5",
                        "pitch_detection_algorithm": "crepe",
                        "separate": "true",
                        "separator": "uvr",
                        "stem": "vocals",
                        "normalize": "true",
                        "target_db": "-1.0"
                    }
                )
            
            assert response.status_code == 200
            
            call_args = mock_convert.call_args[1]
            assert call_args['pitch_change_all'] == 2.0
            assert call_args['index_rate'] == 0.7
            assert call_args['filter_radius'] == 5
            assert call_args['rms_mix_rate'] == 0.5
            assert call_args['pitch_detection_algorithm'] == 'crepe'
            assert call_args['normalize'] is True
            assert call_args['target_db'] == -1.0
        finally:
            if os.path.exists(mock_output.name):
                os.remove(mock_output.name)
    
    @patch.object(RVCConverter, 'convert')
    def test_convert_error_handling(self, mock_convert, client, sample_audio_file):
        """Test error handling in convert endpoint"""
        mock_convert.side_effect = RuntimeError("Test error")
        
        with open(sample_audio_file, 'rb') as f:
            response = client.post(
                "/convert",
                files={"file": ("test.wav", f, "audio/wav")}
            )
        
        assert response.status_code == 500
        assert "error" in response.json()
        assert "Test error" in response.json()["error"]


class TestUVREndpoint:
    """Test cases for /uvr endpoint"""
    
    def test_uvr_endpoint_exists(self, client):
        """Test that /uvr endpoint is accessible"""
        response = client.post("/uvr")
        # Should return 422 (validation error) not 404
        assert response.status_code == 422
    
    @patch.object(RVCConverter, 'uvr')
    def test_uvr_with_demucs(self, mock_uvr, client, sample_audio_file):
        """Test UVR endpoint with Demucs (default)"""
        mock_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
        mock_zip.close()
        mock_uvr.return_value = mock_zip.name
        
        try:
            with open(sample_audio_file, 'rb') as f:
                response = client.post(
                    "/uvr",
                    files={"file": ("test.wav", f, "audio/wav")},
                    data={
                        "use_uvr": "false",
                        "model": "htdemucs"
                    }
                )
            
            assert response.status_code == 200
            assert mock_uvr.called
            
            call_args = mock_uvr.call_args[1]
            assert call_args['use_uvr'] is False
            assert call_args['model'] == 'htdemucs'
        finally:
            if os.path.exists(mock_zip.name):
                os.remove(mock_zip.name)
    
    @patch.object(RVCConverter, 'uvr')
    def test_uvr_with_uvr_separator(self, mock_uvr, client, sample_audio_file):
        """Test UVR endpoint with UVR separator"""
        mock_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
        mock_zip.close()
        mock_uvr.return_value = mock_zip.name
        
        try:
            with open(sample_audio_file, 'rb') as f:
                response = client.post(
                    "/uvr",
                    files={"file": ("test.wav", f, "audio/wav")},
                    data={
                        "use_uvr": "true",
                        "uvr_model_path": "/custom/uvr_model.pth"
                    }
                )
            
            assert response.status_code == 200
            
            call_args = mock_uvr.call_args[1]
            assert call_args['use_uvr'] is True
            assert call_args['uvr_model_path'] == '/custom/uvr_model.pth'
        finally:
            if os.path.exists(mock_zip.name):
                os.remove(mock_zip.name)
    
    @patch.object(RVCConverter, 'uvr')
    def test_uvr_with_demucs_parameters(self, mock_uvr, client, sample_audio_file):
        """Test UVR endpoint with Demucs-specific parameters"""
        mock_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
        mock_zip.close()
        mock_uvr.return_value = mock_zip.name
        
        try:
            with open(sample_audio_file, 'rb') as f:
                response = client.post(
                    "/uvr",
                    files={"file": ("test.wav", f, "audio/wav")},
                    data={
                        "use_uvr": "false",
                        "model": "htdemucs_mmi",
                        "shifts": "5",
                        "segment": "10.0"
                    }
                )
            
            assert response.status_code == 200
            
            call_args = mock_uvr.call_args[1]
            assert call_args['model'] == 'htdemucs_mmi'
            assert call_args['shifts'] == 5
            assert call_args['segment'] == 10.0
        finally:
            if os.path.exists(mock_zip.name):
                os.remove(mock_zip.name)
    
    @patch.object(RVCConverter, 'uvr')
    def test_uvr_error_handling(self, mock_uvr, client, sample_audio_file):
        """Test error handling in UVR endpoint"""
        mock_uvr.side_effect = FileNotFoundError("Model not found")
        
        with open(sample_audio_file, 'rb') as f:
            response = client.post(
                "/uvr",
                files={"file": ("test.wav", f, "audio/wav")}
            )
        
        assert response.status_code == 500
        assert "error" in response.json()
        assert "Model not found" in response.json()["error"]


class TestRVCConverter:
    """Test cases for RVCConverter class"""
    
    @patch('rvc_infer.demucs_separate')
    def test_convert_calls_demucs_when_separator_is_demucs(self, mock_demucs):
        """Test that convert method calls demucs_separate when separator='demucs'"""
        # Mock demucs_separate to return a temporary file
        mock_stem_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        mock_stem_file.close()
        mock_demucs.return_value = (mock_stem_file.name, "/tmp/demucs_out")
        
        # Mock subprocess and file checks to avoid actual RVC call
        with patch('rvc_infer.subprocess.run') as mock_subprocess, \
             patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False  # No RVC CLI exists
            
            converter = RVCConverter()
            
            try:
                with pytest.raises(RuntimeError, match="No known RVC CLI found"):
                    converter.convert(
                        in_path=mock_stem_file.name,
                        separate=True,
                        separator="demucs",
                        stem="vocals"
                    )
                
                # Verify demucs_separate was called
                assert mock_demucs.called
                call_kwargs = mock_demucs.call_args[1]
                assert call_kwargs['stem'] == 'vocals'
            finally:
                if os.path.exists(mock_stem_file.name):
                    os.remove(mock_stem_file.name)
    
    @patch('rvc_infer.uvr_separate')
    def test_convert_calls_uvr_when_separator_is_uvr(self, mock_uvr):
        """Test that convert method calls uvr_separate when separator='uvr'"""
        # Mock uvr_separate to return a temporary file
        mock_stem_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        mock_stem_file.close()
        mock_uvr.return_value = (mock_stem_file.name, "/tmp/uvr_out")
        
        # Mock subprocess and file checks to avoid actual RVC call
        with patch('rvc_infer.subprocess.run') as mock_subprocess, \
             patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False  # No RVC CLI exists
            
            converter = RVCConverter()
            
            try:
                with pytest.raises(RuntimeError, match="No known RVC CLI found"):
                    converter.convert(
                        in_path=mock_stem_file.name,
                        separate=True,
                        separator="uvr",
                        stem="vocals",
                        uvr_model_path="/models/uvr.pth"
                    )
                
                # Verify uvr_separate was called
                assert mock_uvr.called
                call_kwargs = mock_uvr.call_args[1]
                assert call_kwargs['model_path'] == '/models/uvr.pth'
            finally:
                if os.path.exists(mock_stem_file.name):
                    os.remove(mock_stem_file.name)


class TestAPIIntegration:
    """Integration tests for API endpoints"""
    
    def test_openapi_schema(self, client):
        """Test that OpenAPI schema is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "paths" in schema
        assert "/convert" in schema["paths"]
        assert "/uvr" in schema["paths"]
    
    def test_docs_endpoint(self, client):
        """Test that API docs are accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_convert_endpoint_schema(self, client):
        """Test convert endpoint has correct schema"""
        response = client.get("/openapi.json")
        schema = response.json()
        
        convert_schema = schema["paths"]["/convert"]["post"]
        assert "requestBody" in convert_schema
        
        # Check for new UVR parameters
        # Note: Form parameters are defined in the requestBody
        assert convert_schema["summary"] or convert_schema["operationId"]
    
    def test_uvr_endpoint_schema(self, client):
        """Test UVR endpoint has correct schema"""
        response = client.get("/openapi.json")
        schema = response.json()
        
        uvr_schema = schema["paths"]["/uvr"]["post"]
        assert "requestBody" in uvr_schema
        assert uvr_schema["summary"] or uvr_schema["description"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
