import os
from datetime import datetime
from typing import Optional
import asyncio

class BabaEngine:
    def __init__(self, filename: str, logging: Optional[bool] = None):
        self.filename = filename
        self.logging = logging
        if logging is True:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            os.makedirs("baba_logs", exist_ok=True)
            self.log_path = f"baba_logs/{now}.log"
            self._log_file = open(self.log_path, "a", encoding="utf-8")
        else:
            self._log_file = None
        self._log("info", f"Engine initialized with file {filename}")

    def _log(self, level: str, message: str):
        text = f"[BABA LOG] ({level}): {message}"
        if self.logging is False:
            return
        if self.logging is None:
            print(text)
        elif self.logging is True and self._log_file:
            self._log_file.write(text + "\n")
            self._log_file.flush()

    async def write(self, data: str):
        try:
            await asyncio.to_thread(self._write_sync, data)
            self._log("info", f"Data written: {data[:30]}...")
        except Exception as e:
            self._log("error", f"Write error: {str(e)}")

    def _write_sync(self, data: str):
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(data + "\n")

    async def read_all(self) -> list[str]:
        if not os.path.exists(self.filename):
            self._log("info", "Read all called but file does not exist, returning empty list")
            return []
        try:
            lines = await asyncio.to_thread(self._read_all_sync)
            self._log("info", f"Read {len(lines)} lines")
            return lines
        except Exception as e:
            self._log("error", f"Read error: {str(e)}")
            return []

    def _read_all_sync(self) -> list[str]:
        with open(self.filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]