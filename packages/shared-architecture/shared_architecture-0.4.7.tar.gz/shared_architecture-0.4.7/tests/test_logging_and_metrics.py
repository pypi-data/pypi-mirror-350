from shared_architecture.logging.logger import get_logger
from shared_architecture.metrics.metrics_collector import (
    record_request,
    set_service_health,
    REQUEST_COUNT,
    SERVICE_HEALTH
)

def test_logger_outputs_messages(caplog):
    logger = get_logger("test_service")
    logger.info("Test info message")
    logger.error("Test error message")

    assert any("Test info message" in message for message in caplog.text.splitlines())
    assert any("Test error message" in message for message in caplog.text.splitlines())

def test_record_request_increments_counter():
    initial_count = REQUEST_COUNT.labels(method="GET", endpoint="/test")._value.get()
    record_request("GET", "/test", 0.1)
    new_count = REQUEST_COUNT.labels(method="GET", endpoint="/test")._value.get()
    assert new_count == initial_count + 1

def test_set_service_health_sets_gauge():
    set_service_health(True)
    assert SERVICE_HEALTH._value.get() == 1.0

    set_service_health(False)
    assert SERVICE_HEALTH._value.get() == 0.0
