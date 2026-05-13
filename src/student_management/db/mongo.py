from beanie import init_beanie
from pymongo import AsyncMongoClient

from student_management.core.config import settings
from student_management.models import ALL

_client: AsyncMongoClient | None = None


async def open_db() -> None:
    global _client
    _client = AsyncMongoClient(settings.MONGO_URL)
    await init_beanie(database=_client[settings.DB_NAME], document_models=[*ALL])
    print(f"Beanie initialized → {settings.DB_NAME}")


async def close_db() -> None:
    global _client
    if _client is not None:
        await _client.close()
        _client = None
        print("MongoDB disconnected")
