from fastapi import APIRouter ,HTTPException,Depends
from pydantic import BaseModel, HttpUrl
from app.services.scraper import scrape_article, STATIC_SITES
from app.services.analyzer import analyze_article
from app.api.dependencies import get_current_user

from sqlalchemy.ext.asyncio import AsyncSession
from app.services.history_service import save_analysis, get_user_history
from app.db.database import get_db

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
    
@router.post("/analyze")
async def analyze(request: ArticleRequest,current_user:dict=Depends(get_current_user),db: AsyncSession=Depends(get_db)):
    if request.source not in SUPPORTED_SOURCES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source. Choose from: {', '.join(SUPPORTED_SOURCES)}"
        )

    if request.source not in str(request.url):
        raise HTTPException(
            status_code=400,
            detail=f"URL does not match selected source '{request.source}'"
        )

    try:
        scraped = await scrape_article(str(request.url))
        analysis = await analyze_article(scraped["text"])
        await save_analysis(db, current_user, scraped, analysis)
        return {
            "url": scraped["url"],
            "title": scraped["title"],
            "source": scraped["source"],
            "word_count": scraped["word_count"],
            "analyzed_by": current_user["email"],
            "analysis": analysis
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong: {type(e).__name__}: {str(e)}"
        )

@router.get("/history")
async def get_history(
    current_user:dict=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    records= await get_user_history(db,current_user["email"])

    return {
        "email": current_user["email"],
        "total": len(records),
        "history": [
            {
                "id": r.id,
                "title": r.title,
                "source": r.source,
                "url": r.url,
                "language": r.language,
                "sentiment": r.sentiment_overall,
                "bias_detected": r.bias_detected,
                "bias_lean": r.bias_lean,
                "credibility_score": r.credibility_score,
                "summary": r.summary,
                "analyzed_at": r.created_at,
            }
            for r in records
        ]
    }