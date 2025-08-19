from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .api import streams, detections, recordings, analytics
from .core.db import get_pool  # ensure schema at startup

app = FastAPI(title="StreamVision Oracle", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount /static
STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(streams.router,     prefix="/streams",    tags=["streams"])
app.include_router(detections.router,  prefix="/detections", tags=["detections"])
app.include_router(recordings.router,  prefix="/recordings", tags=["recordings"])
app.include_router(analytics.router,   prefix="/analytics",  tags=["analytics"])

@app.on_event("startup")
def _startup():
    # initialize Oracle pool + schema
    try:
        get_pool()
    except Exception as e:
        # still allow app to run without DB (for demo)
        print("DB init warning:", e)

@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <html><body style="font-family:system-ui;margin:24px;line-height:1.6">
      <h1>StreamVision Oracle</h1>
      <p><a href="/docs">Swagger</a> • <a href="/static/index.html">Live Detection Page</a></p>
      <ol>
        <li>POST <code>/streams</code> → {"name":"Webcam","source":"0"}</li>
        <li>Open <code>/static/index.html</code> and enter Stream ID</li>
        <li>(Optional) Start recording in <code>/recordings/start</code> to persist counts per frame</li>
      </ol>
    </body></html>
    """
