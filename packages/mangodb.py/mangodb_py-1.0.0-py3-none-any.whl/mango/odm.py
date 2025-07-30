from typing import Optional, Type, Any
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClientSession
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, info=None) -> ObjectId:

        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class MangoModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class MangoODM:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.models: dict[str, Type[MangoModel]] = {}

    def register_model(self, model: Type[MangoModel]):
        self.models[model.__name__] = model

    def get_collection(self, model_name: str):
        model = self.models.get(model_name)
        if not model:
            raise RuntimeError(f"Model {model_name} not registered")
        return self.db[model_name.lower()]

    def get_model(self, model_name: str) -> Type[MangoModel]:
        model = self.models.get(model_name)
        if not model:
            raise RuntimeError(f"Model {model_name} not registered")
        return model

    async def insert_one(self, model_name: str, session: Optional[AsyncIOMotorClientSession] = None, **kwargs):
        model = self.get_model(model_name)
        doc = model(**kwargs)
        result = await self.get_collection(model_name).insert_one(doc.model_dump(by_alias=True), session=session)
        return result

    async def find_one(self, model_name: str, session: Optional[AsyncIOMotorClientSession] = None, **query):
        model = self.get_model(model_name)
        doc = await self.get_collection(model_name).find_one(query, session=session)
        if doc:
            return model.model_validate(doc)
        return None

    async def find_all(self, model_name: str, session: Optional[AsyncIOMotorClientSession] = None):
        model = self.get_model(model_name)
        cursor = self.get_collection(model_name).find({}, session=session)
        docs = []
        async for doc in cursor:
            docs.append(model.model_validate(doc))
        return docs

    async def update_one(self, model_name: str, session: Optional[AsyncIOMotorClientSession] = None, query: dict = None, update: dict = None):
        if query is None or update is None:
            raise ValueError("Query and update parameters required")
        result = await self.get_collection(model_name).update_one(query, update, session=session)
        return result

    async def delete_one(self, model_name: str, session: Optional[AsyncIOMotorClientSession] = None, **query):
        result = await self.get_collection(model_name).delete_one(query, session=session)
        return result
