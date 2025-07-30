from pydantic import BaseModel
from typing import Type, TypeVar, List
from .engine import BabaEngine
from .db import BabaTable, Baba

ModelType = TypeVar("ModelType", bound=BaseModel)

class BabaSession:
    def __init__(self, engine: BabaEngine) -> None:
        self.engine = engine
        self.db = Baba(engine.filepath)

    async def __aenter__(self) -> "BabaSession":
        self.engine.log("Session started", "INFO")
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.db.save()
        self.engine.log("Session ended", "INFO")
        if hasattr(self.engine, "close"):
            self.engine.close()

    async def insert(self, table: BabaTable, obj: BaseModel) -> None:
        self.db.insert(table, obj)
        values = ' ; '.join(f"{k}={v}" for k, v in obj.dict().items())
        self.engine.log(f"Inserted into {table.name}: {values}", "INFO")

    async def all(self, table: BabaTable) -> List[str]:
        self.engine.log(f"Fetching all from {table.name}", "INFO")
        return self.db.all(table)
