from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.auth import router as auth_router
import os 

load_dotenv()

app=FastAPI(
    title="News Bias Detector",
    description="Detects bias and propaganda in news articles",
    version="1.0.0"
)
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router,prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth")

@app.get("/")
def root():
    return {"message":"News Bias Detector API is running"}

@app.get("/health")
def health_check():
    return {"status":"healthy"}