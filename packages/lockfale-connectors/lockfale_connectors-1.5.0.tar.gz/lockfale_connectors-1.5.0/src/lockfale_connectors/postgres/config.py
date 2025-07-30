import os

from pydantic_settings import BaseSettings


class PGDBSettingsFromEnvironment(BaseSettings):
    db_host: str = os.getenv("PG_DB_HOST")
    db_port: str = os.getenv("PG_DB_CKC_POOL_PORT")
    db_database: str = os.getenv("PG_DB_CKC_POOL")
    db_connection_limit: str = os.getenv("PG_DB_CONNECTION_LIMIT")


class PGDBSettingsFromEnvironmentAdmin(PGDBSettingsFromEnvironment):
    db_user: str = os.getenv("PG_DB_USER")
    db_password: str = os.getenv("PG_DB_PASSWORD")


class PGDBSettingsFromEnvironmentMQTTUser(PGDBSettingsFromEnvironment):
    db_user: str = os.getenv("PG_DB_MQTT_USER_READONLY")
    db_password: str = os.getenv("PG_DB_MQTT_USER_READONLY_PW")
