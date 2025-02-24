from fastapi import FastAPI
from app.api.v1.endpoints import user

app = FastAPI(title="FastAPI Project", version="1.0.0")

# Include routers
app.include_router(user.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}