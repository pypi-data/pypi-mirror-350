from shared_architecture.connection_manager import connection_manager

def test_get_all_connections_returns_expected_keys():
    connections = connection_manager.get_all_connections()
    assert isinstance(connections, dict)
    assert "redis" in connections
    assert "timescaledb" in connections
    assert "rabbitmq" in connections
    assert "mongodb" in connections

def test_create_timescaledb_session_returns_session():
    session = connection_manager.create_timescaledb_session()
    assert session is not None
    session.close()

def test_health_check_returns_all_keys():
    health_status = connection_manager.health_check()
    assert isinstance(health_status, dict)
    assert "redis" in health_status
    assert "timescaledb" in health_status
    assert "rabbitmq" in health_status
    assert "mongodb" in health_status
