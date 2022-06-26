from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import auth, cursos
from app.db import init_db, create_user_staff
from app.db.broadcast import broadcast
from app.containers import Container


app = FastAPI(on_startup=[broadcast.connect], on_shutdown=[broadcast.disconnect])
container = Container()


@app.on_event("startup")
async def start_db():
     await init_db()
     await create_user_staff()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cursos.router)
app.include_router(auth.router, prefix="/auth")
