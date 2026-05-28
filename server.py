import os
import asyncio
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
    # 1. Verifica se os arquivos base existem
    if not os.path.exists("audio.mp3") or not os.path.exists("video_base.mp4"):
        return {"status": "erro", "mensagem": "Arquivos de base (audio/video) não encontrados"}

    # 2. Roteiro (IA)
    roteiro = model.generate_content(f"Crie um roteiro técnico de 30s sobre {tema}")
    
    # 3. Execução assíncrona para não travar o servidor
    cmd = [
        "ffmpeg", "-y", "-i", "audio.mp3", "-i", "video_base.mp4", 
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-shortest", "static/final.mp4"
    ]
    
    # Criamos um processo separado para o FFmpeg
    process = await asyncio.create_subprocess_exec(*cmd)
    await process.wait() # Espera terminar sem congelar o servidor
    
    return {"status": "pronto", "url": "/static/final.mp4"}
