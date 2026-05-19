from fastapi import APIRouter ,HTTPException
from pydantic import BaseModel, HttpUrl
from app.services.scraper import scrape_article, STATIC_SITES

router = APIRouter()

SUPPORTED_SOURCES = list(STATIC_SITES.keys())


class ArticleRequest(BaseModel):
    url:HttpUrl
    source: str


@router.get("/sources")
def get_sources():
    return {
        "supported_sources": SUPPORTED_SOURCES
    }

@router.post("/scrape")
async def scrape(request:ArticleRequest):
    if request.source not in SUPPORTED_SOURCES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source. Choose from: {', '.join(SUPPORTED_SOURCES)}"
        )

    if request.source not in str(request.url):
        raise HTTPException(
            status_code=400,
            detail=f"The URL does not match the selected source '{request.source}'. Please paste a URL from {request.source}"
        )
    
    try:
        result=await scrape_article(str(request.url))
        return result
    except ValueError as e :
        raise HTTPException(status_code=400,detail=str(e))
    except Exception as e:
        raise HTTPException(
        status_code=500, 
        detail=f"Something went wrong: {type(e).__name__}: {str(e)}"
        )