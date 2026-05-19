from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.routes import router

load_dotenv()

app=FastAPI(
    title="News Bias Detector",
    description="Detects bias and propaganda in news articles",
    version="1.0.0"
)

app.include_router(router,prefix="/api/v1")

@app.get("/")
def root():
    return {"message":"News Bias Detector API is running"}

@app.get("/health")
def health_check():
    return {"status":"healthy"}