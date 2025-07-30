import asyncio
from typing import TypeVar, Generic, List, Optional, Callable, Type, AsyncIterator
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class BabaSession(Generic[T]):
    def __init__(self, engine, model: Type[T], key_field: str = "id"):
        self.engine = engine
        self.model = model
        self.key_field = key_field
        self._cache: dict = {}

    async def __aenter__(self) -> "BabaSession[T]":
        await self._load_cache()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.clear_cache()

    async def _load_cache(self):
        lines = await self.engine.read_all()
        for line in lines:
            try:
                obj = self.model.parse_raw(line)
                key = getattr(obj, self.key_field)
                self._cache[key] = obj
            except Exception:
                pass

    async def add(self, instance: T) -> None:
        line = instance.json()
        await self.engine.write(line)
        key = getattr(instance, self.key_field)
        self._cache[key] = instance

    async def get_all(self) -> List[T]:
        if not self._cache:
            await self._load_cache()
        return list(self._cache.values())

    async def get(self, key) -> Optional[T]:
        if key in self._cache:
            return self._cache[key]
        await self._load_cache()
        return self._cache.get(key)

    async def update(self, key, **kwargs) -> bool:
        if key not in self._cache:
            await self._load_cache()
            if key not in self._cache:
                return False
        old = self._cache[key]
        data = old.dict()
        data.update(kwargs)
        updated = self.model(**data)
        self._cache[key] = updated
        await self._rewrite_cache()
        return True

    async def delete(self, key) -> bool:
        if key not in self._cache:
            await self._load_cache()
            if key not in self._cache:
                return False
        self._cache.pop(key)
        await self._rewrite_cache()
        return True

    async def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        if not self._cache:
            await self._load_cache()
        return [obj for obj in self._cache.values() if predicate(obj)]

    async def count(self) -> int:
        if not self._cache:
            await self._load_cache()
        return len(self._cache)

    async def exists(self, key) -> bool:
        if key in self._cache:
            return True
        await self._load_cache()
        return key in self._cache

    async def clear_cache(self) -> None:
        self._cache.clear()

    async def _rewrite_cache(self) -> None:
        await self.engine.clear()
        for obj in self._cache.values():
            await self.engine.write(obj.json())
