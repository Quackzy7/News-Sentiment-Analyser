from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.analysis import Analysis

async def save_analysis(db: AsyncSession, user: dict, scraped: dict, analysis: dict) -> Analysis:
    record = Analysis(
        user_email=user["email"],
        user_name=user["name"],
        url=scraped["url"],
        title=scraped["title"],
        source=scraped["source"],
        word_count=scraped["word_count"],
        language=analysis.get("language"),
        sentiment_overall=analysis.get("sentiment", {}).get("overall"),
        sentiment_score=analysis.get("sentiment", {}).get("score"),
        bias_detected=analysis.get("bias", {}).get("detected"),
        bias_lean=analysis.get("bias", {}).get("lean"),
        bias_score=analysis.get("bias", {}).get("score"),
        bias_explanation=analysis.get("bias", {}).get("explanation"),
        credibility_score=analysis.get("credibility_indicators", {}).get("credibility_score"),
        propaganda_techniques=analysis.get("propaganda_techniques"),
        loaded_language=analysis.get("loaded_language"),
        summary=analysis.get("summary"),
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

async def get_user_history(db: AsyncSession, user_email: str) -> list:
    result = await db.execute(
        select(Analysis)
        .where(Analysis.user_email == user_email)
        .order_by(Analysis.created_at.desc())
    )
    return result.scalars().all()