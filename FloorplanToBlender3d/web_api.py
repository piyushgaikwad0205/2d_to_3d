from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
import subprocess
import uuid
from pathlib import Path

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent.resolve()
UPLOAD_DIR = BASE_DIR / "uploads"
TARGET_DIR = BASE_DIR / "Target"
BLENDER_PATH = r"P:\blender\blender.exe" # Based on run_auto.py discovery

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TARGET_DIR, exist_ok=True)

@app.post("/convert")
async def convert_floorplan(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1]
    input_path = UPLOAD_DIR / f"{job_id}.{ext}"
    
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Run conversion logic
    background_tasks.add_task(run_conversion, job_id, input_path)
    
    return {"job_id": job_id, "status": "processing"}

def run_conversion(job_id: str, input_path: Path):
    try:
        # We leverage main.py or run_auto.py logic here
        # For a clean product, we'll invoke the blender script directly with arguments
        # Using export_glb.py logic for web viewing
        subprocess.run([
            BLENDER_PATH,
            "--background",
            "--python", "main.py", # Simplified for now, we'll refine this
            "--",
            str(input_path),
            str(TARGET_DIR / f"{job_id}.glb")
        ], check=True)
        print(f"Job {job_id} completed successfully.")
    except Exception as e:
        print(f"Error in job {job_id}: {e}")

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    output_file = TARGET_DIR / f"{job_id}.glb"
    if output_file.exists():
        return {"status": "completed", "download_url": f"/download/{job_id}"}
    return {"status": "processing"}

@app.get("/download/{job_id}")
async def download_file(job_id: str):
    file_path = TARGET_DIR / f"{job_id}.glb"
    return FileResponse(file_path, filename="floorplan_3d.glb")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
