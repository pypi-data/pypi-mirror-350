import asyncio
from playwright.async_api import async_playwright

async def render_html_to_image(html, output_path, width, height):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": width, "height": height})
        await page.set_content(html, wait_until="networkidle")

        # Esperar todos os gráficos renderizarem (canvas com altura visível)
        await page.evaluate("""
          () => {
            return new Promise((resolve) => {
              const wait = (ms) => new Promise(r => setTimeout(r, ms));

              async function checkCanvases() {
                for (let i = 0; i < 30; i++) {
                  const allReady = Array.from(document.querySelectorAll('canvas')).every(c => c.offsetHeight > 0);
                  if (allReady) return resolve();
                  await wait(100);
                }
                resolve();  // força o fim após 3s mesmo que incompleto
              }

              checkCanvases();
            });
          }
        """)

        await page.screenshot(path=output_path, full_page=False)
        await browser.close()
