# AWS Scalable Screenshot API 🚀

A high-speed, production-ready, and highly scalable Screenshot API built with **FastAPI** and **Playwright**. This service is optimized for containerized environments (like AWS ECS/Fargate) and features intelligent performance optimizations such as browser warm-boot, concurrency management, automated cache expiration, and resource-blocking mechanisms.

---

## ✨ Features

- **⚡ Fast Execution (Warm-Boot Architecture):** Launches a global browser instance once during API startup and reuses it across incoming requests via lightweight browser contexts (tabs).
- **🔒 Concurrency Management:** Built-in semaphore control limiting simultaneous page captures (`MAX_CONCURRENT_REQUESTS = 5`) to prevent CPU bottlenecks.
- **🚀 Speed Optimization Mode:** Option to intercept and block heavy, non-essential web resources (such as videos, audio, and custom fonts) to save bandwidth and drastically reduce loading time.
- **💾 Lightweight Memory Caching:** Automated key-based cache system with a default 5-minute expiration window to bypass repetitive processing for identical requests.
- **🌓 Dark Mode Support:** Allows capturing websites in dark mode layouts dynamically.
- **🖼️ Thumbnail Generation:** Automatically downscales screenshots to standard thumbnail sizes (320x200) using the Pillow library.
- **🐳 Dockerized:** Fully containerized structure using a lightweight Python image tailored with all system-level Chromium dependencies.

---

## 🏗️ Project Structure

```text
├── Dockerfile              # Docker container configurations & system dependencies
├── requirements.txt        # Python dependency manifest
├── main.py                 # FastAPI application and endpoint logic
├── screenshot_service.py   # Playwright browser automation & page captures
└── cache_manager.py       # In-memory caching logic with TTL expiration


```
## 🛠️ Installation & Setup
Local Setup (Using Virtual Environment)

#### 1:Clone the repository:
```bash
git clone https://github.com/Ahmad-beast/screenshort_api
cd screenshort_api
```
### 2:Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
### 3: Install dependencies:
```bash
pip install -r requirements.txt
```
### 4: Install Playwright Chromium Browser:
```bash
playwright install chromium
```
### 5: Run the API:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
## 🐳 Docker Setup
The service includes a pre-configured multi-step Dockerfile that installs all necessary Linux system libraries for running headless Chromium.
### 1: Build the Docker Image:
```bash
docker build -t screenshot-api 
```
### 2: Run the Container:
```bash
docker run -d -p 8000:8000 --name screenshot-api-container screenshot-api
```

🔌 API Documentation
Once the server is up and running, you can access the interactive Swagger UI documentation at: http://localhost:8000/docs

### 1. Health Check
Endpoint: GET /

Response:
```bash
{
  "status": "active",
  "message": "API is running at warp speed on AWS"
}
```

### 2. Generate Screenshot
Endpoint: POST /api/screenshot

Content-Type: application/json

Request Body Parameters:

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `url` | string (Required) | - | The target website URL to capture. |
| `width` | int | 1280 | Viewport width in pixels. |
| `height` | int | 800 | Viewport height in pixels. |
| `dark_mode` | boolean | false | Sets preferred color scheme to dark mode. |
| `is_thumbnail` | boolean | false | If true, returns a resized 320x200 thumbnail. |
| `use_cache` | boolean | true | Enables/disables reading/writing to memory cache. |
| `optimize_speed` | boolean | true | Blocks video, audio, and fonts for faster speed. |

### Example Request Body:
```bash
{
  "url": "[https://github.com](https://github.com)",
  "width": 1920,
  "height": 1080,
  "dark_mode": true,
  "is_thumbnail": false,
  "use_cache": true,
  "optimize_speed": true
}
```

Response: Returns binary stream content with media_type="image/png".

### 🛠️ Core Stack Details
FastAPI (v0.110.0): High-performance framework used to orchestrate async operations.

Playwright (v1.42.0): Used for robust and modern headless browser manipulation.

Pillow (v10.2.0): Handles image processing for generating thumbnails asynchronously.

