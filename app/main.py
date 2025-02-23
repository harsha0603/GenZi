from fastapi import FastAPI
from app.api.routes import router as webhook_router

app = FastAPI()
app.include_router(webhook_router)


@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}
