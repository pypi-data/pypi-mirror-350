from typing import Any


__all__ = (
    'DatabaseConfig',
)


class DatabaseConfig:
    def __init__(self):
        self._config_data = {}

    def set_db_url(self, db_url: str):
        self._config_data["db_url"] = db_url
        return self

    def set_db_url_read(self, db_url_read: str):
        self._config_data["db_url_read"] = db_url_read
        return self

    def set_db_user(self, db_user: str):
        self._config_data["db_user"] = db_user
        return self

    def set_db_password(self, db_password: str):
        self._config_data["db_password"] = db_password
        return self

    def set_db_host(self, db_host: str):
        self._config_data["db_host"] = db_host
        return self

    def set_db_host_read(self, db_host_read: str):
        self._config_data["db_host_read"] = db_host_read
        return self

    def set_db_port(self, db_port: int):
        self._config_data["db_port"] = db_port
        return self

    def set_db_name(self, db_name: str):
        self._config_data["db_name"] = db_name
        return self

    def set_db_ssl(self, db_ssl: bool):
        self._config_data["db_ssl"] = db_ssl
        return self

    def set_db_pool_size(self, db_pool_size: int):
        self._config_data["db_pool_size"] = db_pool_size
        return self

    def set_db_max_overflow(self, db_max_overflow: int):
        self._config_data["db_max_overflow"] = db_max_overflow
        return self

    def get(self, key: str, default: Any = None):
        return self._config_data.get(key, default)
