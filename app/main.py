from fastapi import FastAPI
from app.api.customfield import customfield

app = FastAPI(title="FastAPI Project", version="1.0.0")

# Include routers
app.include_router(customfield.router, prefix="/customfield", tags=["customfield"])

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}