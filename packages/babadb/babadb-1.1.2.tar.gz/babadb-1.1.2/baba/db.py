from pydantic import BaseModel
from typing import Type, TypeVar, List
from .crypto import sha256_hash

ModelType = TypeVar("ModelType", bound=BaseModel)

class BabaTable:
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model
        self.name = model.__name__

class Baba:
    def __init__(self, path: str) -> None:
        self.path = path
        self.data: List[str] = []
        self._load()

    def _load(self) -> None:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    print("[INFO] Loaded hash from file, data not restored (write only)")
        except FileNotFoundError:
            pass

    def insert(self, table: BabaTable, obj: BaseModel) -> None:
        values = ", ".join(f"{k}={v}" for k, v in obj.dict().items())
        record = f"{table.name} | {values}"
        self.data.append(record)

    def all(self, table: BabaTable) -> List[str]:
        prefix = f"{table.name} |"
        return [r for r in self.data if r.startswith(prefix)]

    def save(self) -> None:
        data_str = "\n".join(self.data)
        hashed = sha256_hash(data_str)
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(hashed)
