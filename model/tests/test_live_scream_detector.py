"""
Unit tests for live_scream_detector.py

Tests the scream detection model loading and prediction logic.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from live_scream_detector import load_models, predict_scream


class TestLoadModels:
    """Test suite for load_models function"""

    @patch('live_scream_detector.hub.load')
    @patch('live_scream_detector.tf.keras.layers.TFSMLayer')
    @patch('live_scream_detector.os.path.exists')
    def test_load_models_success(self, mock_exists, mock_tfsm, mock_hub_load):
        """Test successful model loading"""
        mock_exists.return_value = True
        mock_hub_load.return_value = Mock()
        mock_tfsm.return_value = Mock()
        
        yamnet, classifier = load_models()
        
        assert yamnet is not None
        assert classifier is not None

    @patch('live_scream_detector.hub.load')
    @patch('live_scream_detector.os.path.exists')
    def test_load_models_missing_saved_model(self, mock_exists, mock_hub_load):
        """Test model loading when saved model doesn't exist"""
        mock_exists.return_value = False
        mock_hub_load.return_value = Mock()
        
        yamnet, classifier = load_models("nonexistent_path")
        
        assert yamnet is not None
        assert classifier is None

    @patch('live_scream_detector.hub.load')
    def test_load_models_yamnet_failure(self, mock_hub_load):
        """Test handling of YAMNet loading failure"""
        mock_hub_load.side_effect = Exception("Network error")
        
        yamnet, classifier = load_models()
        
        assert yamnet is None
        assert classifier is None

    @patch('live_scream_detector.hub.load')
    @patch('live_scream_detector.os.path.exists')
    def test_load_models_custom_path(self, mock_exists, mock_hub_load):
        """Test loading models from custom path"""
        mock_exists.return_value = False
        mock_hub_load.return_value = Mock()
        
        custom_path = "custom/model/path"
        _, _ = load_models(custom_path)
        
        mock_exists.assert_called_with(custom_path)


class TestPredictScream:
    """Test suite for predict_scream function"""

    def test_predict_scream_no_models(self):
        """Test prediction when models are not loaded"""
        waveform = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        
        label, prob = predict_scream(None, None, waveform_data=waveform)
        
        assert "Error" in label
        assert prob == 0.0

    def test_predict_scream_no_waveform(self):
        """Test prediction with no waveform data"""
        mock_yamnet = Mock()
        mock_classifier = Mock()
        
        label, prob = predict_scream(mock_yamnet, mock_classifier, waveform_data=None)
        
        assert "Error" in label
        assert prob == 0.0

    def test_predict_scream_invalid_waveform_type(self):
        """Test prediction with invalid waveform type"""
        mock_yamnet = Mock()
        mock_classifier = Mock()
        
        # Pass list instead of numpy array
        label, _ = predict_scream(mock_yamnet, mock_classifier, waveform_data=[1, 2, 3])
        
        assert "Error" in label

    def test_predict_scream_empty_waveform(self):
        """Test prediction with empty waveform"""
        mock_yamnet = Mock()
        mock_classifier = Mock()
        waveform = np.array([], dtype=np.float32)
        
        label, _ = predict_scream(mock_yamnet, mock_classifier, waveform_data=waveform)
        
        assert "Error" in label

    def test_predict_scream_multidimensional_waveform(self):
        """Test prediction with multidimensional waveform"""
        mock_yamnet = Mock()
        mock_classifier = Mock()
        waveform = np.array([[1, 2], [3, 4]], dtype=np.float32)
        
        label, _ = predict_scream(mock_yamnet, mock_classifier, waveform_data=waveform)
        
        assert "Error" in label

    @patch('live_scream_detector.tf.constant')
    @patch('live_scream_detector.tf.reduce_mean')
    @patch('live_scream_detector.tf.expand_dims')
    @patch('live_scream_detector.tf.size')
    def test_predict_scream_success_scream(self, mock_size, mock_expand, mock_mean, _mock_constant):
        """Test successful prediction for scream"""
        # Setup mocks
        mock_yamnet = Mock()
        mock_embeddings = Mock()
        mock_yamnet.return_value = (None, mock_embeddings, None)
        
        mock_size.return_value = 1024
        mock_mean.return_value = Mock()
        mock_expand.return_value = Mock()
        
        mock_classifier = Mock()
        mock_classifier.predict.return_value = {"dense_2": np.array([[0.9]])}
        
        waveform = np.random.randn(16000).astype(np.float32)
        
        label, prob = predict_scream(mock_yamnet, mock_classifier, threshold=0.5, waveform_data=waveform)
        
        assert label == "Scream"
        assert prob == 0.9

    @patch('live_scream_detector.tf.constant')
    @patch('live_scream_detector.tf.reduce_mean')
    @patch('live_scream_detector.tf.expand_dims')
    @patch('live_scream_detector.tf.size')
    def test_predict_scream_success_non_scream(self, mock_size, mock_expand, mock_mean, _mock_constant):
        """Test successful prediction for non-scream"""
        # Setup mocks
        mock_yamnet = Mock()
        mock_embeddings = Mock()
        mock_yamnet.return_value = (None, mock_embeddings, None)
        
        mock_size.return_value = 1024
        mock_mean.return_value = Mock()
        mock_expand.return_value = Mock()
        
        mock_classifier = Mock()
        mock_classifier.predict.return_value = {"dense_2": np.array([[0.2]])}
        
        waveform = np.random.randn(16000).astype(np.float32)
        
        label, prob = predict_scream(mock_yamnet, mock_classifier, threshold=0.5, waveform_data=waveform)
        
        assert label == "Non-Scream"
        assert prob == 0.2

    @patch('live_scream_detector.tf.constant')
    def test_predict_scream_yamnet_failure(self, _mock_constant):
        """Test handling of YAMNet embedding failure"""
        mock_yamnet = Mock()
        mock_yamnet.side_effect = Exception("YAMNet error")
        mock_classifier = Mock()
        
        waveform = np.random.randn(16000).astype(np.float32)
        
        label, _ = predict_scream(mock_yamnet, mock_classifier, waveform_data=waveform)
        
        assert "Error" in label

    @patch('live_scream_detector.tf.constant')
    @patch('live_scream_detector.tf.size')
    def test_predict_scream_empty_embeddings(self, mock_size, _mock_constant):
        """Test handling of empty embeddings"""
        mock_yamnet = Mock()
        mock_embeddings = Mock()
        mock_yamnet.return_value = (None, mock_embeddings, None)
        mock_size.return_value = 0
        
        mock_classifier = Mock()
        waveform = np.random.randn(16000).astype(np.float32)
        
        label, prob = predict_scream(mock_yamnet, mock_classifier, waveform_data=waveform)
        
        assert label == "Non-Scream"
        assert prob == 0.0

    @patch('live_scream_detector.tf.constant')
    @patch('live_scream_detector.tf.reduce_mean')
    @patch('live_scream_detector.tf.expand_dims')
    @patch('live_scream_detector.tf.size')
    def test_predict_scream_custom_threshold(self, mock_size, mock_expand, mock_mean, _mock_constant):
        """Test prediction with custom threshold"""
        mock_yamnet = Mock()
        mock_embeddings = Mock()
        mock_yamnet.return_value = (None, mock_embeddings, None)
        
        mock_size.return_value = 1024
        mock_mean.return_value = Mock()
        mock_expand.return_value = Mock()
        
        mock_classifier = Mock()
        mock_classifier.predict.return_value = {"dense_2": np.array([[0.6]])}
        
        waveform = np.random.randn(16000).astype(np.float32)
        
        # With threshold 0.7, probability 0.6 should be Non-Scream
        label, prob = predict_scream(mock_yamnet, mock_classifier, threshold=0.7, waveform_data=waveform)
        
        assert label == "Non-Scream"
        assert prob == 0.6

    def test_predict_scream_waveform_type_conversion(self):
        """Test that waveform is converted to float32 if needed"""
        mock_yamnet = Mock()
        mock_classifier = Mock()
        
        # Provide int16 waveform
        waveform = np.array([100, 200, 300], dtype=np.int16)
        
        # Should not crash due to type conversion
        label, _ = predict_scream(mock_yamnet, mock_classifier, waveform_data=waveform)
        
        # Will error for other reasons but should handle type conversion
        assert isinstance(label, str)


class TestModelConstants:
    """Test suite for model constants"""

    def test_sample_rate_defined(self):
        """Test that SAMPLE_RATE is defined"""
        from live_scream_detector import SAMPLE_RATE
        assert SAMPLE_RATE == 16000

    def test_chunk_duration_defined(self):
        """Test that CHUNK_DURATION is defined"""
        from live_scream_detector import CHUNK_DURATION
        assert CHUNK_DURATION > 0
        assert isinstance(CHUNK_DURATION, int)

    def test_channels_defined(self):
        """Test that CHANNELS is defined"""
        from live_scream_detector import CHANNELS
        assert CHANNELS == 1

    def test_model_dir_defined(self):
        """Test that MODEL_DIR is defined"""
        from live_scream_detector import MODEL_DIR
        assert MODEL_DIR is not None
        assert isinstance(MODEL_DIR, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])