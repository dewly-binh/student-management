from contextlib import asynccontextmanager

from fastapi import FastAPI

from student_management.db.mongo import close_db, open_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Khởi động Server")
    await open_db()
    yield
    print("Tắt Server")
    await close_db()


app = FastAPI(lifespan=life_span)
