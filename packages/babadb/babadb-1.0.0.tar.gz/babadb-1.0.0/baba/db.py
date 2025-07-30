import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Type, Optional, Dict, Any, List, AsyncIterator, Union
from pydantic import BaseModel
from .encrypt import encode_bytes, decode_bytes

class Logger:
    def __init__(self, to_file: bool = False) -> None:
        self.to_file: bool = to_file
        if self.to_file:
            self.log_dir: Path = Path("baba_logs")
            self.log_dir.mkdir(exist_ok=True)
            date_str: str = datetime.now().strftime("%Y-%m-%d")
            self.log_file: Path = self.log_dir / f"baba_log_{date_str}.log"
        else:
            self.log_file = None

    def _log(self, level: str, msg: str) -> None:
        full_msg: str = f"[BABA ({level.upper()})] LOG: {msg}"
        if self.to_file and self.log_file:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(full_msg + "\n")
        else:
            print(full_msg)

    def info(self, msg: str) -> None:
        self._log("info", msg)

    def error(self, msg: str) -> None:
        self._log("error", msg)

class AsyncSession:
    def __init__(self, db: 'BabaDB') -> None:
        self.db: BabaDB = db
        self._pending: Dict[str, BaseModel] = {}
        self._loop = asyncio.get_event_loop()

    async def __aenter__(self) -> 'AsyncSession':
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc is None:
            await self.commit()
        else:
            self.db.logger.error(f"Session exited with exception: {exc}")
            self._pending.clear()

    async def add(self, obj: BaseModel, filename: Optional[str] = None) -> None:
        if filename is None:
            if hasattr(obj, "id"):
                filename = f"{obj.id}.baba"
            else:
                raise ValueError("Filename or obj.id required for saving")
        self._pending[filename] = obj
        self.db.logger.info(f"Queued for saving: '{filename}'")

    async def get(self, cls: Type[BaseModel], filename: str) -> Optional[BaseModel]:
        try:
            encoded = await self._read_file(filename)
            decoded_bytes = decode_bytes(encoded)
            data = json.loads(decoded_bytes.decode("utf-8"))
            obj = cls(**data)
            self.db.logger.info(f"File loaded: '{filename}'")
            return obj
        except Exception as e:
            self.db.logger.error(f"Error loading file '{filename}': {e}")
            return None

    async def update(self, obj: BaseModel, filename: Optional[str] = None) -> None:
        await self.add(obj, filename)

    async def delete(self, filename: str) -> bool:
        try:
            def del_file() -> None:
                Path(filename).unlink()
            await self._loop.run_in_executor(None, del_file)
            self.db.logger.info(f"File deleted: '{filename}'")
            if filename in self._pending:
                del self._pending[filename]
            return True
        except Exception as e:
            self.db.logger.error(f"Error deleting file '{filename}': {e}")
            return False

    async def all(self, folder: Union[str, Path], cls: Type[BaseModel]) -> List[BaseModel]:
        folder_path = Path(folder)
        results = []
        for file_path in folder_path.glob("*.baba"):
            obj = await self.get(cls, str(file_path))
            if obj is not None:
                results.append(obj)
        self.db.logger.info(f"Loaded all objects from '{folder_path}' count={len(results)}")
        return results

    async def filter(self, folder: Union[str, Path], cls: Type[BaseModel], **kwargs) -> List[BaseModel]:
        all_objs = await self.all(folder, cls)
        filtered = []
        for obj in all_objs:
            if all(getattr(obj, k, None) == v for k, v in kwargs.items()):
                filtered.append(obj)
        self.db.logger.info(f"Filtered {len(filtered)} objects with criteria {kwargs}")
        return filtered

    async def exists(self, filename: str) -> bool:
        exists = Path(filename).exists()
        self.db.logger.info(f"Exists check '{filename}': {exists}")
        return exists

    async def count(self, folder: Union[str, Path]) -> int:
        folder_path = Path(folder)
        count = len(list(folder_path.glob("*.baba")))
        self.db.logger.info(f"Count in '{folder_path}': {count}")
        return count

    async def commit(self) -> None:
        tasks = []
        for filename, obj in self._pending.items():
            tasks.append(self._write_file(filename, obj))
        await asyncio.gather(*tasks)
        self._pending.clear()

    async def _write_file(self, filename: str, obj: BaseModel) -> None:
        try:
            json_bytes: bytes = json.dumps(obj.dict(), ensure_ascii=False).encode("utf-8")
            encoded: str = encode_bytes(json_bytes)
            def write_file() -> None:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(encoded)
            await self._loop.run_in_executor(None, write_file)
            self.db.logger.info(f"File saved: '{filename}'")
        except Exception as e:
            self.db.logger.error(f"Error saving file '{filename}': {e}")

    async def _read_file(self, filename: str) -> str:
        def read_file_sync() -> str:
            with open(filename, "r", encoding="utf-8") as f:
                return f.read()
        return await self._loop.run_in_executor(None, read_file_sync)

class BabaDB:
    def __init__(self, model_cls: Type[BaseModel], logging: bool = False) -> None:
        self.model_cls: Type[BaseModel] = model_cls
        self.logger: Logger = Logger(to_file=logging)

    def async_session(self) -> AsyncSession:
        return AsyncSession(self)
