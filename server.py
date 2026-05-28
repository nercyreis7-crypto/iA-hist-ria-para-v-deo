

import os
import asyncio
from fastapi import FastAPI, Header
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai

app = FastAPI()

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/gerar_video_final")
async def gerar_video_final(tema: str, fala: str, x_api_key: str = Header(...)):
    # Limpeza de caracteres (#)
    tema_limpo = tema.replace("#", "")
    fala_limpa = fala.replace("#", "")
    
    try:
        genai.configure(api_key=x_api_key)
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        return {"status": "erro", "mensagem": "Chave de API inválida."}

    audio_path = "audio.mp3"
    video_path = "video_base.mp4"
    output_path = "static/final.mp4"
    
    if not os.path.exists(audio_path) or not os.path.exists(video_path):
        return {"status": "erro", "mensagem": "Arquivos de mídia ausentes."}

    try:
        prompt_ia = f"Crie um roteiro de 30s sobre {tema_limpo}. O personagem deve dizer: '{fala_limpa}'"
        response = model.generate_content(prompt_ia)
        roteiro = response.text
    except Exception as e:
        return {"status": "erro", "mensagem": f"Erro na IA: {str(e)}"}

    cmd = [
        "ffmpeg", "-y", "-i", audio_path, "-i", video_path, 
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30", 
        "-s", "640x360", "-pix_fmt", "yuv420p", "-shortest", output_path
    ]
    
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            return {"status": "erro", "mensagem": f"FFmpeg falhou: {stderr.decode()}"}
            
    except Exception as e:
        return {"status": "erro", "mensagem": f"Erro no FFmpeg: {str(e)}"}
    
    return {"status": "pronto", "url": "/static/final.mp4", "roteiro": roteiro}
