from ..repository import BaseRepository
from ..schema import ListFilter,FindUniqueByFieldInput,ListFilter

class BaseService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def create(self, data: dict, collection_name: str = None) -> any:
        return await self.repository.create(data, collection_name)
    
    async def bulk_create(self, data: list[any], collection_name: str = None) -> list[any]:
        return await self.repository.bulk_create(data, collection_name)
    
    async def get_by_attr(self, attr: str, value: any, collection_name: str = None) -> any:
        return await self.repository.get_by_attr(attr, value, collection_name)

    async def update(self, _id: str, data: dict, collection_name: str = None) -> any:
        return await self.repository.update(_id, data, collection_name)
    
    async def delete(self, _id: str, collection_name: str = None) -> any:
        return await self.repository.delete(_id, collection_name)

    async def get_unique_values(self, schema: FindUniqueByFieldInput, collection_name: str = None) -> list[any]:
        return await self.repository.get_unique_values(schema, collection_name)
    
    async def get_all(self,find:ListFilter,collection_name:str=None)->list[any]:
        return await self.repository.get_all(find,collection_name)