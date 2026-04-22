from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, HttpUrl
from contextlib import asynccontextmanager
from screenshot_service import init_browser, close_browser, take_screenshot
from cache_manager import screenshot_cache

# Lifespan manager to handle startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Launch the browser once
    await init_browser()
    yield
    # Shutdown: Clean up resources gracefully
    await close_browser()

app = FastAPI(
    title="AWS Scalable Screenshot API",
    description="A high-speed, scalable screenshot API with warm-boot capabilities.",
    version="2.0.0",
    lifespan=lifespan
)

class ScreenshotRequest(BaseModel):
    url: HttpUrl
    width: int = 1280
    height: int = 800
    dark_mode: bool = False
    is_thumbnail: bool = False
    use_cache: bool = True
    optimize_speed: bool = True

@app.get("/")
def health_check():
    return {"status": "active", "message": "API is running at warp speed on AWS"}

@app.post("/api/screenshot")
async def generate_screenshot(req: ScreenshotRequest):
    target_url = str(req.url)
    
    # Create a unique cache key including size parameters
    cache_key = f"{target_url}_{req.width}x{req.height}_{req.dark_mode}_{req.is_thumbnail}"
    
    if req.use_cache:
        cached_image = screenshot_cache.get(cache_key)
        if cached_image:
            return Response(content=cached_image, media_type="image/png")
            
    try:
        image_bytes = await take_screenshot(
            url=target_url,
            width=req.width,
            height=req.height,
            dark_mode=req.dark_mode,
            is_thumbnail=req.is_thumbnail,
            optimize_speed=req.optimize_speed
        )
        
        if req.use_cache:
            screenshot_cache.set(cache_key, image_bytes)
            
        return Response(content=image_bytes, media_type="image/png")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to capture screenshot: {str(e)}")
