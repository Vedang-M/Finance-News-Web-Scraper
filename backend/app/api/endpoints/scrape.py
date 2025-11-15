from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
import httpx
from bs4 import BeautifulSoup

router = APIRouter(prefix="/scrape", tags=["Scrape"])

class ScrapeRequest(BaseModel):
    url: HttpUrl

class ScrapeResponse(BaseModel):
    title: str
    text: str
    url: str

@router.post("/url", response_model=ScrapeResponse)
async def scrape_url(req: ScrapeRequest):
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(req.url)
            resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch: {e}")

    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    paragraphs = [p.get_text(separator=" ", strip=True) for p in soup.find_all("p")]
    text = " ".join(paragraphs)[:4000]
    return ScrapeResponse(title=title, text=text, url=req.url)