from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.products import router as products_router

app = FastAPI()

app.include_router(upload_router, prefix="/api")
app.include_router(products_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World"}