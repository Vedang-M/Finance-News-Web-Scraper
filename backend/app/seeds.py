import asyncio
from app.db.session import AsyncSessionLocal
from app.db.models import Source
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

DEFAULT_SOURCES = [
    {
        "name": "Reuters",
        "base_url": "https://www.reuters.com",
        "rss_url": "https://www.reuters.com/rssFeed/businessNews",
        "type": "news"
    },
    {
        "name": "CNBC",
        "base_url": "https://www.cnbc.com",
        "rss_url": "https://www.cnbc.com/id/19854910/device/rss/rss.html",
        "type": "news"
    },
    {
        "name": "Yahoo Finance",
        "base_url": "https://finance.yahoo.com",
        "rss_url": "https://finance.yahoo.com/news/rssindex",
        "type": "news"
    },
]

def seed_sources(session: AsyncSession):
    for src in DEFAULT_SOURCES:
        result = await session.execute(select(Source).where(Source.name == src["name"]))
        existing = result.scalar()
        if not existing:
            session.add(Source(**src))
    await session.commit()

async def run_seed():
    async with AsyncSessionLocal() as session:
        await seed_sources(session)

if __name__ == "__main__":
    asyncio.run(run_seed())
