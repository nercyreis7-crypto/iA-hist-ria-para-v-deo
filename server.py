import os
import subprocess
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai

app = FastAPI()

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

@app.get("/gerar_video_final")
async def gerar_video_final(tema: str):
    roteiro = model.generate_content(f"Crie um roteiro técnico de 30s sobre {tema}")
    
    cmd = [
        "ffmpeg", "-y", "-i", "audio.mp3", "-i", "video_base.mp4", 
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-shortest", "static/final.mp4"
    ]
    subprocess.run(cmd)
    
    return {"status": "pronto", "url": "/static/final.mp4"}
