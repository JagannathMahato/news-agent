import asyncio
import sys
from crawler import main as run_crawler

def main():
    """
    Main entry point for the new-feed-ai crawler.
    Usage: python main.py <url1> <url2> ...
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <url1> <url2> ...")
        print("Example: python main.py https://example.com https://wikipedia.org")
        return

    urls = sys.argv[1:]
    print(f"Starting crawler for {len(urls)} websites...")
    
    try:
        asyncio.run(run_crawler(urls))
    except KeyboardInterrupt:
        print("\nCrawler stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
