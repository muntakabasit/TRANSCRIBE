"""
Design Scraper API - FastAPI application
Maximum extraction tool for UI/UX designs
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel, HttpUrl
import asyncio
from pathlib import Path
import json
from datetime import datetime
import os

from scraper_engine import DesignScraper

app = FastAPI(title="Design Scraper", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

# In-memory job storage
jobs = {}

class ScrapeRequest(BaseModel):
    url: HttpUrl

class JobStatus(BaseModel):
    job_id: str
    url: str
    status: str
    progress: str
    started_at: str
    completed_at: str | None = None
    result_path: str | None = None
    error: str | None = None

async def run_scraper(job_id: str, url: str):
    """Background task to run the scraper"""
    try:
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['progress'] = 'Initializing scraper...'
        
        scraper = DesignScraper(url, output_dir="downloads")
        
        jobs[job_id]['progress'] = 'Extracting design elements...'
        result = await scraper.scrape_everything()
        
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['completed_at'] = datetime.now().isoformat()
        jobs[job_id]['result_path'] = str(scraper.job_dir)
        jobs[job_id]['result_data'] = result
        jobs[job_id]['progress'] = 'Complete!'
        
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)
        jobs[job_id]['completed_at'] = datetime.now().isoformat()

@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the main UI"""
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/scrape")
async def create_scrape_job(request: ScrapeRequest, background_tasks: BackgroundTasks):
    """Create a new design scraping job"""
    import hashlib
    
    job_id = hashlib.md5(str(request.url).encode()).hexdigest()[:8]
    
    if job_id in jobs and jobs[job_id]['status'] == 'processing':
        return {"job_id": job_id, "message": "Job already in progress"}
    
    jobs[job_id] = {
        'job_id': job_id,
        'url': str(request.url),
        'status': 'queued',
        'progress': 'Job queued...',
        'started_at': datetime.now().isoformat(),
        'completed_at': None,
        'result_path': None,
        'error': None
    }
    
    background_tasks.add_task(run_scraper, job_id, str(request.url))
    
    return {"job_id": job_id, "status": "queued"}

@app.get("/status/{job_id}")
async def get_job_status(job_id: str):
    """Get the status of a scraping job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]

@app.get("/result/{job_id}")
async def get_job_result(job_id: str):
    """Get the full result of a completed job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job['status'] != 'completed':
        raise HTTPException(status_code=400, detail="Job not completed yet")
    
    return job.get('result_data', {})

@app.get("/download/{job_id}")
async def download_job_result(job_id: str):
    """Download the job result as a ZIP file"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job['status'] != 'completed':
        raise HTTPException(status_code=400, detail="Job not completed yet")
    
    # Create ZIP of the job directory
    import shutil
    result_dir = Path(job['result_path'])
    zip_path = result_dir.parent / f"{result_dir.name}.zip"
    
    if not zip_path.exists():
        shutil.make_archive(str(result_dir), 'zip', result_dir)
    
    return FileResponse(
        path=str(zip_path),
        media_type="application/zip",
        filename=f"design_{job_id}.zip"
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Design Scraper",
        "version": "1.0.0",
        "active_jobs": len([j for j in jobs.values() if j['status'] == 'processing'])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6000)
