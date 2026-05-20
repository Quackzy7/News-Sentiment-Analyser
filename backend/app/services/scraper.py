import httpx
from bs4 import BeautifulSoup
import re

STATIC_SITES = {
    "onlinekhabar.com": ".ok18-single-post-content-wrap",
    "ratopati.com": ".the-content"
}

DYNAMIC_SITES = {
    # "somesite.com": ".article-content",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_site_name(url: str) -> str:
    for site in {**STATIC_SITES, **DYNAMIC_SITES}.keys():
        if site in url:
            return site
    return "unknown"

def get_static_selector(url: str) -> str | None:
    for site, selector in STATIC_SITES.items():
        if site in url:
            return selector
    return None

def get_dynamic_selector(url: str) -> str | None:
    for site, selector in DYNAMIC_SITES.items():
        if site in url:
            return selector
    return None

async def scrape_article(url: str) -> dict:
    static_selector = get_static_selector(url)
    dynamic_selector = get_dynamic_selector(url)

    if not static_selector and not dynamic_selector:
        raise ValueError(
            f"This site is not supported yet. "
            f"Supported sites: {', '.join({**STATIC_SITES, **DYNAMIC_SITES}.keys())}"
        )
    
    if static_selector:
        return await scrape_static(url, static_selector)

    if dynamic_selector:
        raise ValueError(
            "Dynamic site scraping is not yet implemented. Coming soon."
        )
    
async def scrape_static(url:str,selector :str)->dict:
    async with httpx.AsyncClient(
        headers=HEADERS,
        follow_redirects=True,
        timeout=30
    ) as client:
        response=await client.get(url)
        response.raise_for_status()

    soup=BeautifulSoup(response.text,"html.parser")

    title_tag=soup.find("title")
    title=title_tag.text.strip() if title_tag else "No title found"

    container=soup.select_one(selector)

    if not container:
        raise ValueError(
            "Could not find article content on this page. "
            "The site structure may have changed."
        )
    
    full_text=container.get_text(separator="\n",strip=True)
    full_text = re.sub(r'\n{3,}', '\n\n', full_text).strip()

    return {
        "url":url,
        "title":title,
        "text":full_text,
        "word_count":len(full_text.split()),
        "source":get_site_name(url),
    }