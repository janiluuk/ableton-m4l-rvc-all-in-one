# server/stemxtract_client.py
"""
StemXtract API client wrapper for integration with the RVC Max4Live device.
Provides a Python interface to the StemXtract Gradio API for stem separation with effects.
"""

import os
import tempfile
from typing import Optional, Tuple
from gradio_client import Client, handle_file


class StemXtractClient:
    """Client for interfacing with StemXtract Gradio API."""
    
    def __init__(self, server_url: str = "http://192.168.2.12:60000"):
        """
        Initialize StemXtract client.
        
        Args:
            server_url: Base URL of the StemXtract Gradio server
        """
        self.server_url = server_url
        self.client = None
    
    def _get_client(self) -> Client:
        """Lazy load and return the Gradio client."""
        if self.client is None:
            self.client = Client(self.server_url)
        return self.client
    
    def process_track(
        self,
        audio_file_path: str,
        task: str = "remove_vocals",
        model_name: str = "htdemucs",
        drums_vol: float = 1.0,
        bass_vol: float = 1.0,
        other_vol: float = 1.0,
        vocals_vol: float = 1.0,
        instrumental_volume: float = 1.0,
        instrumental_low_gain: float = 0.0,
        instrumental_high_gain: float = 0.0,
        instrumental_reverb: float = 0.0,
        vocal_volume: float = 1.0,
        vocal_low_gain: float = 0.0,
        vocal_high_gain: float = 0.0,
        vocal_reverb: float = 0.0,
        trim_silence_chk: bool = False
    ) -> Tuple[str, str, str, str, str, str]:
        """
        Process audio track with StemXtract API using the /process_track_wrapper endpoint.
        
        Args:
            audio_file_path: Path to input audio file
            task: Task type - 'remove_vocals', 'isolate_vocals', or 'mix_stems'
            model_name: AI model - 'htdemucs', 'mdx', 'mdx_extra', or 'mdx_q'
            drums_vol: Drums volume (0.0 to 2.0)
            bass_vol: Bass volume (0.0 to 2.0)
            other_vol: Other instruments volume (0.0 to 2.0)
            vocals_vol: Vocals volume (0.0 to 2.0)
            instrumental_volume: Instrumental volume (0.0 to 2.0)
            instrumental_low_gain: Instrumental low frequency gain in dB
            instrumental_high_gain: Instrumental high frequency gain in dB
            instrumental_reverb: Instrumental reverb amount (0.0 to 1.0)
            vocal_volume: Vocal volume (0.0 to 2.0)
            vocal_low_gain: Vocal low frequency gain in dB
            vocal_high_gain: Vocal high frequency gain in dB
            vocal_reverb: Vocal reverb amount (0.0 to 1.0)
            trim_silence_chk: Whether to trim silence
        
        Returns:
            Tuple of (final_output_path, processing_time, drums_path, bass_path, other_path, vocals_path)
        """
        client = self._get_client()
        
        result = client.predict(
            audio_file=handle_file(audio_file_path),
            task=task,
            model_name=model_name,
            drums_vol=drums_vol,
            bass_vol=bass_vol,
            other_vol=other_vol,
            vocals_vol=vocals_vol,
            instrumental_volume=instrumental_volume,
            instrumental_low_gain=instrumental_low_gain,
            instrumental_high_gain=instrumental_high_gain,
            instrumental_reverb=instrumental_reverb,
            vocal_volume=vocal_volume,
            vocal_low_gain=vocal_low_gain,
            vocal_high_gain=vocal_high_gain,
            vocal_reverb=vocal_reverb,
            trim_silence_chk=trim_silence_chk,
            api_name="/process_track_wrapper"
        )
        
        # Result is a tuple: (final_output, processing_time, drums, bass, other, vocals)
        return result
    
    def blend_audio(
        self,
        track1_source: str = "Upload New Track",
        track1_upload_path: Optional[str] = None,
        track1_vol: float = 1.0,
        track1_low_gain: float = 0.0,
        track1_high_gain: float = 0.0,
        track1_threshold: float = -20.0,
        track1_ratio: float = 1.0,
        track1_attack: float = 5.0,
        track1_release: float = 50.0,
        track1_reverb_room: float = 0.0,
        track1_reverb_decay: float = 1.0,
        track1_reverb_wetdry: float = 0.0,
        track1_delay_time: float = 0.25,
        track1_delay_feedback: float = 0.3,
        track1_delay_wetdry: float = 0.0,
        track2_source: str = "Upload New Track",
        track2_upload_path: Optional[str] = None,
        track2_vol: float = 1.0,
        track2_low_gain: float = 0.0,
        track2_high_gain: float = 0.0,
        track2_threshold: float = -20.0,
        track2_ratio: float = 1.0,
        track2_attack: float = 5.0,
        track2_release: float = 50.0,
        track2_reverb_room: float = 0.0,
        track2_reverb_decay: float = 1.0,
        track2_reverb_wetdry: float = 0.0,
        track2_delay_time: float = 0.25,
        track2_delay_feedback: float = 0.3,
        track2_delay_wetdry: float = 0.0,
        match_tempo_chk: bool = True,
        offset_ms: float = 0.0
    ) -> Tuple[str, str]:
        """
        Blend two audio tracks using the StemXtract API.
        
        Args:
            track1_source: Source for track 1 - 'Upload New Track', 'Use Processed Vocals', or 'Use Processed Instrumental'
            track1_upload_path: Path to track 1 audio file (required if track1_source is 'Upload New Track')
            track1_vol: Track 1 volume
            track1_low_gain: Track 1 low frequency gain
            track1_high_gain: Track 1 high frequency gain
            track1_threshold: Track 1 compression threshold
            track1_ratio: Track 1 compression ratio
            track1_attack: Track 1 compression attack (ms)
            track1_release: Track 1 compression release (ms)
            track1_reverb_room: Track 1 reverb room size
            track1_reverb_decay: Track 1 reverb damping
            track1_reverb_wetdry: Track 1 reverb amount
            track1_delay_time: Track 1 delay time (seconds)
            track1_delay_feedback: Track 1 delay feedback
            track1_delay_wetdry: Track 1 delay amount
            track2_source: Source for track 2 (same options as track1_source)
            track2_upload_path: Path to track 2 audio file
            track2_vol: Track 2 volume
            track2_low_gain: Track 2 low frequency gain
            track2_high_gain: Track 2 high frequency gain
            track2_threshold: Track 2 compression threshold
            track2_ratio: Track 2 compression ratio
            track2_attack: Track 2 compression attack (ms)
            track2_release: Track 2 compression release (ms)
            track2_reverb_room: Track 2 reverb room size
            track2_reverb_decay: Track 2 reverb damping
            track2_reverb_wetdry: Track 2 reverb amount
            track2_delay_time: Track 2 delay time (seconds)
            track2_delay_feedback: Track 2 delay feedback
            track2_delay_wetdry: Track 2 delay amount
            match_tempo_chk: Whether to time-stretch track 2 to match track 1
            offset_ms: Manual offset for track 2 in milliseconds
        
        Returns:
            Tuple of (final_output_path, processing_time)
        """
        client = self._get_client()
        
        # Handle file uploads
        track1_file = handle_file(track1_upload_path) if track1_upload_path else None
        track2_file = handle_file(track2_upload_path) if track2_upload_path else None
        
        result = client.predict(
            track1_source=track1_source,
            track1_upload=track1_file,
            track1_vol=track1_vol,
            track1_low_gain=track1_low_gain,
            track1_high_gain=track1_high_gain,
            track1_threshold=track1_threshold,
            track1_ratio=track1_ratio,
            track1_attack=track1_attack,
            track1_release=track1_release,
            track1_reverb_room=track1_reverb_room,
            track1_reverb_decay=track1_reverb_decay,
            track1_reverb_wetdry=track1_reverb_wetdry,
            track1_delay_time=track1_delay_time,
            track1_delay_feedback=track1_delay_feedback,
            track1_delay_wetdry=track1_delay_wetdry,
            track2_source=track2_source,
            track2_upload=track2_file,
            track2_vol=track2_vol,
            track2_low_gain=track2_low_gain,
            track2_high_gain=track2_high_gain,
            track2_threshold=track2_threshold,
            track2_ratio=track2_ratio,
            track2_attack=track2_attack,
            track2_release=track2_release,
            track2_reverb_room=track2_reverb_room,
            track2_reverb_decay=track2_reverb_decay,
            track2_reverb_wetdry=track2_reverb_wetdry,
            track2_delay_time=track2_delay_time,
            track2_delay_feedback=track2_delay_feedback,
            track2_delay_wetdry=track2_delay_wetdry,
            match_tempo_chk=match_tempo_chk,
            offset_ms=offset_ms,
            api_name="/blend_audio"
        )
        
        # Result is a tuple: (final_output_path, processing_time)
        return result
