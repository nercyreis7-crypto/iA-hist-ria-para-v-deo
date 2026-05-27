import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel

# Configuração de segurança: A chave vem do Render
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI()

class Pedido(BaseModel):
    tema: str

@app.post("/gerar")
async def gerar(pedido: Pedido):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Escreva uma história curta de Isekai épico sobre: {pedido.tema}")
    return {"historia": response.text}

