from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(project_root)

from research_and_analyst.api.routes import report_routes
from fastapi.responses import FileResponse

app = FastAPI(title="Autonomous Report Generator UI")

FAVICON_PATH = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")

@app.get("/favicon.ico")
async def favicon():
    if os.path.exists(FAVICON_PATH):
        return FileResponse(FAVICON_PATH)
    return {"message": "Favicon not found"}

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="research_and_analyst/api/templates")
app.templates = templates  # so templates accessible inside router

# 🔹 ADD THIS FUNCTION
def basename_filter(path: str):
    return os.path.basename(path)

# 🔹 REGISTER FILTER
templates.env.filters["basename"] = basename_filter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(report_routes.router)