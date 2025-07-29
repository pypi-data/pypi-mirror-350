"""Tests for ServifAI library"""

import pytest
from unittest.mock import Mock, patch
from servifai import ServifAI, ServifAIConfig, SubscriptionTier
from servifai.exceptions import AuthenticationError, ValidationError

class TestServifAIConfig:
    
    def test_valid_config(self):
        config = ServifAIConfig(
            api_key="sai_test_key_12345",
            api_url="https://api.syntheialabs.ai"
        )
        assert config.api_key == "sai_test_key_12345"
        assert config.timeout == 300
    
    def test_invalid_api_key(self):
        with pytest.raises(ValueError, match="Valid ServifAI API key required"):
            ServifAIConfig(api_key="invalid_key")
    
    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("SERVIFAI_API_KEY", "sai_test_key")
        monkeypatch.setenv("SERVIFAI_TIMEOUT", "600")
        
        config = ServifAIConfig.from_env()
        assert config.api_key == "sai_test_key"
        assert config.timeout == 600

class TestServifAI:
    
    @pytest.fixture
    def mock_config(self):
        return ServifAIConfig(
            api_key="sai_test_key_12345",
            api_url="https://api.syntheialabs.ai"
        )
    
    @pytest.fixture
    def client(self, mock_config):
        return ServifAI(config=mock_config)
    
    @patch('servifai.client.httpx.AsyncClient')
    def test_initialization(self, mock_httpx, mock_config):
        client = ServifAI(config=mock_config)
        assert client.config.api_key == "sai_test_key_12345"
        mock_httpx.assert_called_once()
    
    def test_validate_pdf_files(self):
        from servifai.utils import validate_pdf_files
        
        # Test with non-existent file
        with pytest.raises(FileNotFoundError):
            validate_pdf_files(["nonexistent.pdf"])

if __name__ == "__main__":
    pytest.main([__file__])
