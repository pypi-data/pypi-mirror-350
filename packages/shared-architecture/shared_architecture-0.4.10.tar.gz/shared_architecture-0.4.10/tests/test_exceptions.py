import pytest
from shared_architecture.exceptions import (
    SharedArchitectureError,
    ConfigurationError,
    ConnectionError,
    ValidationError,
    RetryLimitExceededError,
    BatchProcessingError,
    UnsupportedOperationError
)

def test_shared_architecture_error():
    with pytest.raises(SharedArchitectureError):
        raise SharedArchitectureError("Test error")

def test_configuration_error():
    with pytest.raises(ConfigurationError):
        raise ConfigurationError("Configuration error")

def test_connection_error():
    with pytest.raises(ConnectionError):
        raise ConnectionError("Connection error")

def test_validation_error():
    with pytest.raises(ValidationError):
        raise ValidationError("Validation error")

def test_retry_limit_exceeded_error():
    with pytest.raises(RetryLimitExceededError):
        raise RetryLimitExceededError("Retry limit exceeded")

def test_batch_processing_error():
    with pytest.raises(BatchProcessingError):
        raise BatchProcessingError("Batch processing failed")

def test_unsupported_operation_error():
    with pytest.raises(UnsupportedOperationError):
        raise UnsupportedOperationError("Unsupported operation")
