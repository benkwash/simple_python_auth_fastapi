from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .config.db import connect_to_db, close_db
from .config.create_indexes import create_indexes
from .routes import routes, public_routes

origins = ["*"]

async def lifespan(app:FastAPI):
    await connect_to_db()
    await create_indexes()

    yield
    await close_db()

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def root():
    return {"message": "app works"}

app.include_router(public_routes)

# auth middleware comes here
app.include_router(routes)


