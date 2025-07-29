import pytest

from toolbox.sqlalchemy.connection import DatabaseConnectionSettings


@pytest.fixture(autouse=True, scope="session")
def db_settings():
    data = DatabaseConnectionSettings(
        POSTGRES_USER="postgres",
        POSTGRES_PASSWORD = "postgres",
        POSTGRES_HOST = "0.0.0.0",
        POSTGRES_PORT = 5432,
        POSTGRES_DB = "postgres"
    )
    return data


@pytest.fixture(autouse=True, scope="session")
async def temp_db(db_settings):
    from toolbox.testing import temporary_database
    from toolbox.sqlalchemy.models import BaseDatabaseModel
    async with temporary_database(settings=db_settings, base_model=BaseDatabaseModel):
        yield
        pass
