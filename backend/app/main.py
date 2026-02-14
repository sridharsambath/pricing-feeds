from fastapi import FastAPI
from app.api.upload import router as upload_router

app = FastAPI()

app.include_router(upload_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World"}