from typing import Type, List
from pydantic import BaseModel
from .engine.engine import BabaEngine
from .session.session import BabaSession

class Baba:
    def __init__(self, filename: str, logging=None):
        self.engine = BabaEngine(filename, logging)
        self.session = BabaSession(self.engine)

    async def add(self, model: BaseModel):
        await self.session.add(model)

    async def get_all_raw(self) -> List[str]:
        return await self.session.get_all()

    async def clear(self):
        await self.session.clear()

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.clear()
