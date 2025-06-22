# twitch_stream_auto_switcher.py

import asyncio
from playwright.async_api import Playwright, async_playwright
import random
import time
import sys

TWITCH_COLLECTION_URL = "https://www.twitch.tv/directory/collection/science-and-technology-streams"
INTERVAL_MINUTES = 30 # how often to select a new stream (in minutes)
HEADLESS_MODE = False # set to True to run the browser in the background (no UI)
                      # set to False to see the browser window

async def scrape_and_navigate(playwright: Playwright):
    """
    Launches a browser, scrapes Twitch stream links, selects a random one,
    and navigates the browser to that stream.
    """
    print("Launching browser...")
    # Launch Chromium browser. You can change to .firefox or .webkit if preferred.

    browser = await playwright.chromium.launch(headless=HEADLESS_MODE)
    page = await browser.new_page()

    while True:
        try:
            print(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
            print(f"Navigating to Twitch collection: {TWITCH_COLLECTION_URL}")
            await page.goto(TWITCH_COLLECTION_URL, wait_until="domcontentloaded")

            print("Waiting for stream links to load...")
            await page.wait_for_selector('a[data-test-selector="ChannelLink"]', timeout=30000)

            stream_links = await page.evaluate('''() => {
                const links = Array.from(document.querySelectorAll('a[data-test-selector="ChannelLink"]'));
                // Filter out any links that might not be direct stream URLs if necessary
                return links.map(link => link.href).filter(href => href.startsWith('https://www.twitch.tv/'));
            }''')

            if not stream_links:
                print("No stream links found on the page. This might be a temporary issue or page structure change.")
                print("Retrying after the interval...")
            else:
                random_stream_url = random.choice(stream_links)
                print(f"Selected random stream: {random_stream_url}")

                print(f"Navigating to stream: {random_stream_url}")
                await page.goto(random_stream_url, wait_until="domcontentloaded")
                print("Successfully navigated to stream.")

        except Exception as e:
            print(f"An error occurred during stream selection: {e}", file=sys.stderr)
            print("Attempting to close browser context and retry.", file=sys.stderr)

            try:
                await page.close()
                await browser.close()
                browser = await playwright.chromium.launch(headless=HEADLESS_MODE)
                page = await browser.new_page()
            except Exception as restart_e:
                print(f"Failed to restart browser after error: {restart_e}", file=sys.stderr)
                print("Exiting script due to persistent browser issues.", file=sys.stderr)
                return

        print(f"Waiting for {INTERVAL_MINUTES} minutes before selecting the next stream...")
        await asyncio.sleep(INTERVAL_MINUTES * 60)

async def main():
    """
    Initializes Playwright and calls the main automation function.
    """
    async with async_playwright() as playwright:
        await scrape_and_navigate(playwright)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript terminated by user (Ctrl+C). Exiting.")
    except Exception as final_e:
        print(f"An unhandled error occurred: {final_e}", file=sys.stderr)
