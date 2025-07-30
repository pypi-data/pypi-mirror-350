# import pytest
# from metaworkflows import CONNECTION_MANAGER

# def test_connections_loaded():
#     connections = CONNECTION_MANAGER._load_connections()  # Use the method to load connections
#     assert connections, "Connections should be loaded from the configuration file."
#     assert "my_postgres_db" in connections, "Expected 'my_postgres_db' in connections."
#     assert connections["my_postgres_db"]["type"] == "postgresql", "Connection type should be 'postgresql'."