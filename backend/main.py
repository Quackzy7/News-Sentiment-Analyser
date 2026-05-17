from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app=FastAPI(
    title="News Bias Detector",
    description="Detects bias and propaganda in news articles",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message":"News Bias Detector API is running"}

@app.get("/health")
def health_check():
    return {"status":"healthy"}