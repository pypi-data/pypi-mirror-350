# BabaDB — Encrypted Async File-Based Database for Pydantic Models

## Overview

BabaDB is a lightweight asynchronous database system designed to store Pydantic models securely in encrypted files with a custom encoding format. It provides an easy-to-use API inspired by SQLModel, enabling you to save, load, update, delete, and query your data objects asynchronously while keeping all stored data encrypted and obfuscated.

---

## Architecture and Design

- **File Storage:**  
  Each database record is saved as an individual `.baba` file on disk. Files contain encrypted and encoded binary data representing the JSON-serialized form of your Pydantic models.

- **Custom Encoding and Encryption:**  
  Data is serialized into JSON bytes, then encoded using a custom ternary-like (base-3) scheme combined with random digits and letters. This encoding transforms the binary data into a format that is obfuscated and not trivially reversible without the decoding algorithm. The encoding introduces spaces between encoded trinary parts for added complexity.

- **Asynchronous API:**  
  All file operations (reading, writing, deleting) are performed asynchronously using Python's `asyncio` event loop, wrapped around synchronous file IO executed in thread executors to avoid blocking the main async loop.

- **Sessions:**  
  BabaDB uses asynchronous sessions (`AsyncSession`) as context managers (`async with`) to batch multiple operations (add, update, delete) before committing them all at once. This ensures atomicity and performance improvements.

- **Logging:**  
  The system supports configurable logging. By default, logs are printed to the terminal in a structured format:  
  `[BABA (LEVEL)] LOG: message`  
  If enabled, logs are saved to timestamped files inside the `baba_logs` directory, automatically created on demand.

- **Type Safety:**  
  The entire codebase is fully typed, utilizing Python's typing system and Pydantic models to ensure data correctness and help catch errors early.

---

## Core Components

- **`BabaDB`**  
  The main database class initialized with a Pydantic model class. It provides the entry point to create asynchronous sessions for interacting with stored data.

- **`AsyncSession`**  
  An asynchronous context manager that manages pending changes and provides CRUD-like methods:  
  - `add(obj, filename=None)` — Queue a model instance for saving.  
  - `get(cls, filename)` — Load a model instance from a file.  
  - `update(obj, filename=None)` — Queue an update (alias for add).  
  - `delete(filename)` — Delete the file associated with a model.  
  - `all(folder, cls)` — Load all model instances from a folder.  
  - `filter(folder, cls, **kwargs)` — Load all instances matching attributes.  
  - `exists(filename)` — Check if a file exists.  
  - `count(folder)` — Count `.baba` files in a folder.  
  - `commit()` — Write all queued changes to disk.

- **Encoding and Decoding Functions (`encrypt.py`)**  
  Custom methods to encode bytes into a ternary + random chars format and decode back, adding a layer of obfuscation to the stored data.

---

## How It Works

1. **Saving Data:**  
   When you add or update a Pydantic model instance via the session, it serializes the object to JSON bytes, encodes it with the custom ternary + random character scheme, and schedules it for writing. Upon committing or exiting the session context, all scheduled objects are written asynchronously to `.baba` files.

2. **Loading Data:**  
   When loading, the session reads the `.baba` file asynchronously, decodes the encoded string back to JSON bytes, deserializes into the original Pydantic model, and returns the object.

3. **Filtering and Querying:**  
   BabaDB allows simple attribute-based filtering of all stored objects in a given directory by loading all matching `.baba` files and returning those with matching fields.

4. **Logging:**  
   All major operations and errors are logged in a unified format, either to the console or log files depending on configuration.

---

## Key Benefits

- **Asynchronous:** Suitable for high-concurrency environments without blocking the main event loop.  
- **Secure and Obfuscated:** Data stored on disk is not plain JSON or plaintext but encoded and obfuscated, making casual inspection or tampering difficult.  
- **Simple to Use:** Minimal setup with an easy, familiar API inspired by SQLModel, but for file-based storage.  
- **Extensible:** Full type annotations and Pydantic models make it easy to extend and integrate with other Python tools.

---

## Requirements

- Python 3.8+  
- `pydantic` library

---

## Installation

```bash
pip install babadb
```

## Examples

```python

import asyncio
from pydantic import BaseModel
from baba import BabaDB

class Hero(BaseModel):
    id: int
    name: str

async def main():
    db = BabaDB(Hero)  # is logged in the terminal by default. you can pass the logging = True parameter to the class and all logs will be saved in the baba_logs folder

    async with db.async_session() as session:
        user = User(id=1, name="Alice")
        await session.add(user)

    async with db.async_session() as session:
        loaded = await session.get(Hero, "1.baba")
        print(f"Loaded: {loaded}")

        await session.delete("1.baba")

asyncio.run(main())


```