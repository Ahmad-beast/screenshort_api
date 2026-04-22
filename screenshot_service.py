import asyncio
from playwright.async_api import async_playwright
from io import BytesIO
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_CONCURRENT_REQUESTS = 5
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

# Global variables for Warm Boot
_playwright = None
_browser = None

async def init_browser():
    """Initializes the browser once when the API starts."""
    global _playwright, _browser
    _playwright = await async_playwright().start()
    # Launch browser once and keep it running
    _browser = await _playwright.chromium.launch(headless=True)
    logger.info("Global Playwright Browser initialized successfully.")

async def close_browser():
    """Closes the browser when the API shuts down."""
    global _playwright, _browser
    if _browser:
        await _browser.close()
    if _playwright:
        await _playwright.stop()
    logger.info("Global Playwright Browser shut down securely.")

async def take_screenshot(
    url: str, 
    width: int = 1280, 
    height: int = 800, 
    dark_mode: bool = False, 
    is_thumbnail: bool = False,
    optimize_speed: bool = True
) -> bytes:
    
    async with semaphore:
        context = None
        try:
            # Apply Dark Mode
            color_scheme = 'dark' if dark_mode else 'light'
            
            # Create a new context (tab) from the warm browser instead of launching a new browser
            context = await _browser.new_context(
                color_scheme=color_scheme,
                viewport={"width": width, "height": height}
            )
            
            page = await context.new_page()
            
            # Speed Optimization: Intercept and block heavy, unnecessary resources
            if optimize_speed:
                async def route_intercept(route):
                    # Block media (video/audio) and fonts to speed up rendering
                    if route.request.resource_type in ["media", "font"]:
                        await route.abort()
                    else:
                        await route.continue_()
                
                await page.route("**/*", route_intercept)
            
            logger.info(f"Navigating to {url} with size {width}x{height}")
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            screenshot_bytes = await page.screenshot(full_page=False)
            
            # Generate Thumbnail
            if is_thumbnail:
                img = Image.open(BytesIO(screenshot_bytes))
                img.thumbnail((320, 200))
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='PNG')
                screenshot_bytes = img_byte_arr.getvalue()
                
            return screenshot_bytes

        except Exception as e:
            logger.error(f"Error capturing screenshot for {url}: {str(e)}")
            raise e
        
        finally:
            # Only close the context (tab), keep the main browser running
            if context:
                await context.close()
