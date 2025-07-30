import os
import re
import time
import json
import random
import atexit
import requests
import asyncio
from urllib.parse import urlparse

from readability import Document
from lxml import html as lxml_html
from playwright.async_api import async_playwright
from cneura_ai.logger import logger


class Research:
    DENY_LIST = ["medium.com", "explodingtopics.com", "forbes.com"]

    def __init__(self, google_api_key, search_engine_id, max_workers=4):
        self.google_api_key = google_api_key
        self.search_engine_id = search_engine_id
        self.max_workers = max_workers
        self.playwright = None
        self.browser = None

    async def init(self):
        await self._init_browser()
        atexit.register(lambda: asyncio.run(self.close()))

    async def _init_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)

    def google_search(self, query, num_results=5):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.google_api_key}&cx={self.search_engine_id}&num={num_results}"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            return [(item["title"], item["link"]) for item in data.get("items", [])]
        except requests.RequestException as e:
            logger.error(f"Google Search API error: {e}")
            return []

    def duckduckgo_search(self, query, num_results=5):
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=num_results)
                return [(r["title"], r["href"]) for r in results]
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return []

    async def scrape_page(self, url, retries=2):
        domain = urlparse(url).netloc
        if any(blocked in domain for blocked in self.DENY_LIST):
            logger.info(f"[DenyList] Skipping known bot-protected domain: {domain}")
            return None

        for attempt in range(1, retries + 1):
            try:
                logger.info(f"[Playwright] Attempt {attempt} scraping {url}")

                # Create new stealth context for each attempt
                context = await self.browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                    java_script_enabled=True,
                )
                page = await context.new_page()
                await page.goto(url, timeout=30000, wait_until="domcontentloaded")
                await page.wait_for_selector("body", timeout=5000)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2);")
                await page.wait_for_timeout(random.randint(1000, 3000))  # Human-like delay

                html = await page.content()
                await page.close()
                await context.close()

                if re.search(r"captcha|verify you are human|cloudflare|attention required", html, re.IGNORECASE):
                    logger.warning("CAPTCHA or challenge detected.")
                    continue

                return html

            except Exception as e:
                logger.warning(f"[Playwright] Failed attempt {attempt} on {url}: {e}")
                await asyncio.sleep(1)

        # Fallback: requests
        try:
            logger.info(f"[Fallback] Trying requests for {url}")
            resp = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            })
            if resp.status_code == 200:
                if re.search(r"captcha|verify you are human|cloudflare|attention required", resp.text, re.IGNORECASE):
                    logger.warning("CAPTCHA detected in fallback.")
                    return None
                return resp.text
            else:
                logger.warning(f"[Fallback] Non-200 status: {resp.status_code}")
        except Exception as e:
            logger.warning(f"[Fallback] Request failed: {e}")

        logger.error(f"[Error] Final failure scraping {url}")
        return None

    def extract_main_content(self, html: str) -> str:
        try:
            doc = Document(html)
            summary_html = doc.summary()
            tree = lxml_html.fromstring(summary_html)
            text = tree.text_content()
            return re.sub(r'\s+', ' ', text).strip()
        except Exception as e:
            logger.error(f"Readability extraction failed: {e}")
            return ""

    async def process_results(self, query, engine="google", num_results=5):
        logger.info(f"Searching: '{query}' with {engine}")
        if engine == "google":
            results = self.google_search(query, num_results)
        elif engine == "duckduckgo":
            results = self.duckduckgo_search(query, num_results)
        else:
            raise ValueError("Invalid engine. Use 'google' or 'duckduckgo'.")

        if not results:
            logger.warning("No results found.")
            return {"query": query, "results": []}

        output = []

        async def process(title_link):
            title, link = title_link
            domain = urlparse(link).netloc
            logger.info(f"[Process] Scraping {domain}")
            html = await self.scrape_page(link)
            if not html:
                return None
            text = self.extract_main_content(html)
            if len(re.findall(r'\w+', text)) < 30:
                logger.info(f"Skipping short content from {link}")
                return None
            return {
                "title": title,
                "url": link,
                "content": text,
                "token_count": len(re.findall(r'\w+', text))
            }

        tasks = [process(item) for item in results]
        completed = await asyncio.gather(*tasks)
        output = [r for r in completed if r]

        return {"query": query, "results": output}

    async def close(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None


import asyncio
import json

async def main():
    researcher = Research(
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
        search_engine_id=os.environ.get("SEARCH_ENGINE_ID")
    )
    await researcher.init()
    json_result = await researcher.process_results("latest AI agents", engine="duckduckgo", num_results=3)
    await researcher.close()

    print(json.dumps(json_result, indent=2))

asyncio.run(main())
