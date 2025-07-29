from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from toolbox.schemes import SensitiveDataScheme
from toolbox.sqlalchemy.models import BaseDatabaseModel

AnyPydanticModel = Annotated[SensitiveDataScheme, Depends(SensitiveDataScheme)]
AnySQLAlchemyModel = Annotated[BaseDatabaseModel, Depends(BaseDatabaseModel)]


class AbstractDatabaseCrudManager:
    _alchemy_model = type[AnySQLAlchemyModel]
    _pydantic_model = type[AnyPydanticModel]

    @classmethod
    def to_alchemy_model(cls, pydantic_model: AnyPydanticModel) -> AnySQLAlchemyModel:
        encripted_data = pydantic_model.encrypt_fields()
        obj = cls._alchemy_model(**encripted_data.model_dump())
        return obj

    @classmethod
    def to_pydantic_model(cls, alchemy_model: AnySQLAlchemyModel) -> AnyPydanticModel:
        new_model = cls._pydantic_model.model_validate(alchemy_model.__dict__)
        decrypted_model = new_model.decrypt_fields()
        return decrypted_model

    @classmethod
    async def add_one(cls, conn: AsyncSession, data_model: AnyPydanticModel) -> AnyPydanticModel:
        obj = cls.to_alchemy_model(data_model)
        conn.add(obj)
        await conn.commit()
        await conn.refresh(obj)
        return obj

    @classmethod
    async def get_all(cls, conn: AsyncSession, limit: int = 100, offset: int = 0) -> list[AnyPydanticModel]:
        query = select(cls._alchemy_model).limit(limit).offset(offset)
        raw_data = (await conn.execute(query)).all()
        result = [cls.to_pydantic_model(v[0]) for v in raw_data]
        return result
