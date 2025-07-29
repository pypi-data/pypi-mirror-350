import pytest
from sqlalchemy import Column, Integer, String, orm, LargeBinary

from toolbox.schemes import SensitiveDataScheme, SensitiveFieldData
from toolbox.sqlalchemy.connection import DatabaseConnectionManager, DatabaseConnectionSettings
from toolbox.sqlalchemy.repositories import AbstractDatabaseCrudManager


class BaseDatabaseModel(orm.DeclarativeBase):
    pass


class TestSQLAlchemyModel(BaseDatabaseModel):
    __tablename__ = "test_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sensitive_field = Column(LargeBinary)


class TestPydanticModel(SensitiveDataScheme):
    _sensitive_attributes = ["sensitive_field"]

    name: str
    sensitive_field: SensitiveFieldData


class TestItemRepository(AbstractDatabaseCrudManager):
    _alchemy_model = TestSQLAlchemyModel
    _pydantic_model = TestPydanticModel


@pytest.fixture(autouse=True, scope="session")
def db_settings():
    data = DatabaseConnectionSettings(
        POSTGRES_USER="postgres",
        POSTGRES_PASSWORD="postgres",
        POSTGRES_HOST="0.0.0.0",
        POSTGRES_PORT="5432",
        POSTGRES_DB="postgres"
    )
    return data


@pytest.fixture(autouse=True, scope="session")
async def temp_db(db_settings):
    from toolbox.testing import temporary_database
    from toolbox.sqlalchemy.models import BaseDatabaseModel
    async with temporary_database(settings=db_settings, base_model=BaseDatabaseModel) as db_connection:
        yield db_connection
        pass


@pytest.fixture(autouse=True, scope="session")
def database_connection(db_settings):
    dc = DatabaseConnectionManager(settings=db_settings)
    return dc

class MockCipherManager:
    def encrypt(self, value):
        return f"{value}_secret".encode()

    def decrypt(self, value):
        return value.decode()[:-7]


async def test_add_one_sensitive_field(temp_db, database_connection):
    new_obj = TestPydanticModel(
        name="test_item",
        sensitive_field="test_sensitive_field"
    )

    TestPydanticModel.set_cipher_suite_manager(MockCipherManager())
    async with database_connection.get_db_session() as conn:
        from sqlalchemy.schema import CreateTable
        try:
            await conn.execute(CreateTable(TestSQLAlchemyModel.__table__))
        except:
            pass

        all_ = await TestItemRepository.get_all(conn)
        assert len(all_) == 0

        await TestItemRepository.add_one(conn, new_obj)

        import asyncpg
        another_conn = await asyncpg.connect(dsn=database_connection._get_settings().get_dsn())
        raw_results = await another_conn.fetch(f"SELECT * FROM {TestSQLAlchemyModel.__table__}")
        await another_conn.close()

        assert len(raw_results) == 1
        result = dict(zip(raw_results[0].keys(), raw_results[0].values()))

        assert result["sensitive_field"] == "test_sensitive_field_secret".encode()

        all_ = await TestItemRepository.get_all(conn)
        assert len(all_) == 1
        obj = all_[0]
        assert obj.sensitive_field == "test_sensitive_field"
