import asyncio
from playwright.async_api import async_playwright

async def render_html_to_image(html_content, output_path, width, height):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": width, "height": height})
        await page.set_content(html_content, wait_until="load")
        await page.wait_for_function("window.chartsDone === true", timeout=5000)
        await page.screenshot(path=output_path)
        await browser.close()
