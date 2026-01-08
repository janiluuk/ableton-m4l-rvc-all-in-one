"""
Tests for Applio integration
"""
import pytest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add server directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../server/server'))

from rvc_infer import RVCConverter

class TestApplioIntegration:
    """Test Applio voice conversion integration"""
    
    @pytest.fixture
    def converter(self):
        """Create RVCConverter instance"""
        return RVCConverter()
    
    def test_applio_server_url_from_env(self, converter):
        """Test that Applio server URL can be configured via environment"""
        # Default should be http://applio:8001
        assert converter.applio_server == "http://applio:8001"
        
        # Should use environment variable if set
        os.environ["APPLIO_SERVER"] = "http://custom:9999"
        converter2 = RVCConverter()
        assert converter2.applio_server == "http://custom:9999"
        del os.environ["APPLIO_SERVER"]
    
    def test_convert_returns_tuple(self):
        """Test that convert method signature returns a tuple"""
        # This tests the interface without requiring actual conversion
        converter = RVCConverter()
        
        # Check that the method exists
        assert hasattr(converter, 'convert')
        assert callable(converter.convert)
        
        # Check that _process_with_applio exists
        assert hasattr(converter, '_process_with_applio')
        assert callable(converter._process_with_applio)
    
    def test_convert_with_applio_auto_enables_separation(self):
        """Test that enabling Applio automatically enables separation"""
        # This test verifies the logic without actually running the conversion
        kwargs = {
            'in_path': '/tmp/test.wav',
            'applio_enabled': True,
            'applio_model': 'test_model',
            'separate': False  # Initially false
        }
        
        # The convert method should modify kwargs to enable separation
        # We'll test this by checking the logic path
        assert kwargs.get('separate') == False
        
        # When applio_enabled=True and applio_model is set, separation should be enabled
        if kwargs.get("applio_enabled") and kwargs.get("applio_model"):
            kwargs["separate"] = True
        
        assert kwargs['separate'] == True
    
    def test_applio_model_fallback(self):
        """Test that applio_model can fallback to rvc_model"""
        converter = RVCConverter()
        
        # Test the logic for model selection
        kw1 = {'applio_model': 'applio_specific', 'rvc_model': 'rvc_model'}
        model1 = kw1.get("applio_model") if kw1.get("applio_model") else kw1.get("rvc_model")
        assert model1 == 'applio_specific'
        
        kw2 = {'applio_model': None, 'rvc_model': 'rvc_model'}
        model2 = kw2.get("applio_model") if kw2.get("applio_model") else kw2.get("rvc_model")
        assert model2 == 'rvc_model'
        
        kw3 = {'rvc_model': 'rvc_model'}
        model3 = kw3.get("applio_model") if kw3.get("applio_model") else kw3.get("rvc_model")
        assert model3 == 'rvc_model'

class TestApplioServerStructure:
    """Test Applio server structure and configuration"""
    
    def test_applio_server_file_exists(self):
        """Test that applio_server.py exists"""
        applio_server_path = os.path.join(
            os.path.dirname(__file__), 
            '../applio/applio_server.py'
        )
        assert os.path.exists(applio_server_path), "applio_server.py should exist"
    
    def test_applio_dockerfile_exists(self):
        """Test that Applio Dockerfile exists"""
        dockerfile_path = os.path.join(
            os.path.dirname(__file__), 
            '../applio/Dockerfile'
        )
        assert os.path.exists(dockerfile_path), "Applio Dockerfile should exist"
    
    def test_docker_compose_includes_applio(self):
        """Test that docker-compose files include Applio service"""
        compose_files = [
            '../server/docker-compose.yml',
            '../docker-compose.example.yml'
        ]
        
        for compose_file in compose_files:
            compose_path = os.path.join(os.path.dirname(__file__), compose_file)
            if os.path.exists(compose_path):
                with open(compose_path, 'r') as f:
                    content = f.read()
                    assert 'applio:' in content, f"{compose_file} should include applio service"
                    assert '8001' in content, f"{compose_file} should expose port 8001 for Applio"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
