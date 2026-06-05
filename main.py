import os
import uuid
import asyncio
import shutil
from typing import Dict
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from services.roteiro_service import gerar_roteiro
from services.voz_service import gerar_audio
from services.video_service import gerar_video

tarefas: Dict[str, dict] = {}

PASTA_STATIC = "static"
os.makedirs(PASTA_STATIC, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mount("/files", StaticFiles(directory=PASTA_STATIC), name="files")
    yield

app = FastAPI(
    title="DirectorIA API",
    description="API para conversão de História em Vídeo",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequisicaoProcessamento(BaseModel):
    historia: str
    modelo: str

class RespostaTarefa(BaseModel):
    tarefa_id: str
    status: str
    mensagem: str

@app.post("/processar", response_model=RespostaTarefa)
async def processar_historia(requisicao: RequisicaoProcessamento):
    if not requisicao.historia.strip():
        raise HTTPException(status_code=400, detail="História não pode ser vazia")

    tarefa_id = str(uuid.uuid4())
    pasta_tarefa = os.path.join(PASTA_STATIC, tarefa_id)
    os.makedirs(pasta_tarefa, exist_ok=True)

    tarefas[tarefa_id] = {
        "status": "iniciando",
        "mensagem": "Tarefa criada, aguardando processamento...",
        "pasta": pasta_tarefa,
        "resultado": {}
    }

    asyncio.create_task(executar_pipeline(tarefa_id, requisicao))

    return RespostaTarefa(
        tarefa_id=tarefa_id,
        status="iniciando",
        mensagem="Processamento iniciado. Consulte /status/{tarefa_id}"
    )

@app.get("/status/{tarefa_id}")
async def consultar_status(tarefa_id: str):
    if tarefa_id not in tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    tarefa = tarefas[tarefa_id]
    resposta = {
        "status": tarefa["status"],
        "mensagem": tarefa["mensagem"],
        "resultado": tarefa["resultado"]
    }

    if tarefa["status"] in ["concluido", "erro"]:
        asyncio.create_task(limpar_tarefa(tarefa_id, delay=300))

    return resposta

async def executar_pipeline(tarefa_id: str, requisicao: RequisicaoProcessamento):
    tarefa = tarefas[tarefa_id]
    pasta = tarefa["pasta"]
    modelo = requisicao.modelo

    try:
        roteiro_texto = ""
        audio_path = None

        if "Roteiro" in modelo or "Completo" in modelo:
            tarefa["status"] = "gerando_roteiro"
            tarefa["mensagem"] = "Gerando roteiro com IA..."
            await asyncio.sleep(0.1)

            roteiro_texto = await gerar_roteiro(requisicao.historia)
            roteiro_path = os.path.join(pasta, "roteiro.txt")
            with open(roteiro_path, "w", encoding="utf-8") as f:
                f.write(roteiro_texto)

            tarefa["resultado"]["roteiro"] = roteiro_texto
            tarefa["resultado"]["roteiro_url"] = f"/files/{tarefa_id}/roteiro.txt"

            if "Apenas Roteiro" in modelo:
                tarefa["status"] = "concluido"
                tarefa["mensagem"] = "Roteiro gerado com sucesso!"
                return

        if "Voz" in modelo or "Completo" in modelo:
            tarefa["status"] = "gerando_voz"
            tarefa["mensagem"] = "Convertendo texto em áudio..."
            await asyncio.sleep(0.1)

            texto_para_narrar = roteiro_texto if roteiro_texto else requisicao.historia
            audio_path = os.path.join(pasta, "narracao.mp3")
            await gerar_audio(texto_para_narrar, audio_path)

            tarefa["resultado"]["audio_url"] = f"/files/{tarefa_id}/narracao.mp3"

            if "Apenas Voz" in modelo:
                tarefa["status"] = "concluido"
                tarefa["mensagem"] = "Áudio gerado com sucesso!"
                return

        tarefa["status"] = "gerando_video"
        tarefa["mensagem"] = "Sincronizando vídeo e áudio..."
        await asyncio.sleep(0.1)

        texto_visual = roteiro_texto if roteiro_texto else requisicao.historia
        video_path = os.path.join(pasta, "video_final.mp4")
        await gerar_video(texto_visual, audio_path, video_path)

        tarefa["resultado"]["video_url"] = f"/files/{tarefa_id}/video_final.mp4"
        tarefa["status"] = "concluido"
        tarefa["mensagem"] = "Vídeo gerado com sucesso!"

    except Exception as e:
        tarefa["status"] = "erro"
        tarefa["mensagem"] = f"Erro no processamento: {str(e)}"

async def limpar_tarefa(tarefa_id: str, delay: int = 300):
    await asyncio.sleep(delay)
    if tarefa_id in tarefas:
        pasta = tarefas[tarefa_id].get("pasta")
        if pasta and os.path.exists(pasta):
            shutil.rmtree(pasta, ignore_errors=True)
        del tarefas[tarefa_id]

@app.get("/health")
async def health_check():
    return {"status": "online", "servico": "DirectorIA API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
