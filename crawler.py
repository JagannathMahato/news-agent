import asyncio
import json
import random
from typing import List, Dict
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def crawl_website(url: str, browser_context) -> Dict[str, List[str]]:
    """
    Crawls a single website and gathers data topic-wise.
    """
    page = await browser_context.new_page()
    
    # Apply stealth to bypass bot protection
    stealth = Stealth()
    await stealth.apply_stealth_async(page)
    
    # Set a random user agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    ]
    await page.set_extra_http_headers({"User-Agent": random.choice(user_agents)})

    print(f"Crawling: {url}...")
    try:
        # Navigate to the URL
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # Wait a bit to simulate human behavior
        await asyncio.sleep(random.uniform(2, 5))
        
        # Get the page content
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract data topic-wise (using headings as topics)
        data = {}
        current_topic = "General"
        data[current_topic] = []
        
        # Simple heuristic: Group content by headings
        for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
            if element.name in ['h1', 'h2', 'h3']:
                current_topic = element.get_text(strip=True)
                if current_topic not in data:
                    data[current_topic] = []
            elif element.name == 'p':
                text = element.get_text(strip=True)
                if text:
                    data[current_topic].append(text)
                    
        # Remove empty topics
        data = {k: v for k, v in data.items() if v}
        
        return data
    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return {"error": str(e)}
    finally:
        await page.close()

import os

async def main(urls: List[str], output_file: str = "crawled_data.json"):
    # Set playwright browser path to local directory if it exists
    local_pw_path = os.path.join(os.getcwd(), "pw-browsers")
    if os.path.exists(local_pw_path):
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = local_pw_path

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        results = {}
        for url in urls:
            website_data = await crawl_website(url, context)
            results[url] = website_data
            
        # Store data in JSON format
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
            
        print(f"Data saved to {output_file}")
        await browser.close()

if __name__ == "__main__":
    # Example usage: Replace with your list of websites
    target_websites = [
        "https://example.com",
        "https://www.wikipedia.org"
    ]
    
    import sys
    if len(sys.argv) > 1:
        target_websites = sys.argv[1:]
        
    asyncio.run(main(target_websites))
