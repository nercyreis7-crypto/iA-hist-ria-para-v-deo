import asyncio
from gtts import gTTS
import os

async def gerar_audio(texto: str, caminho_saida: str) -> str:
    """
    Gera áudio usando gTTS (Text-to-Speech nativo).
    Executado em thread separada para não bloquear o servidor FastAPI.
    """
    # asyncio.to_thread executa a função pesada em background
    await asyncio.to_thread(_gerar_audio_sync, texto, caminho_saida)
    return caminho_saida

def _gerar_audio_sync(texto: str, caminho_saida: str):
    """Versão síncrona que roda em outra thread."""
    # Limpa o texto de caracteres que podem dar erro no gTTS
    texto_limpo = texto.replace('\n', ' ').strip()
    
    # Limita o texto para evitar travamentos (gTTS tem limite de tamanho)
    if len(texto_limpo) > 4500:
        texto_limpo = texto_limpo[:4500]

    # Gera o áudio em Português do Brasil
    tts = gTTS(text=texto_limpo, lang='pt', slow=False, tld='com.br')
    
    # Salva o arquivo no servidor
    tts.save(caminho_saida)
    
    # Verifica se o arquivo foi criado com sucesso
    if not os.path.exists(caminho_saida) or os.path.getsize(caminho_saida) == 0:
        raise ValueError("Falha ao gerar o arquivo de áudio.")
