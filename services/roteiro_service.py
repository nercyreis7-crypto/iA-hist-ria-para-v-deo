import os
import asyncio
import requests
from dotenv import load_dotenv
import time

load_dotenv()

QWEN_API_URL = os.getenv("QWEN_API_URL", "https://openrouter.ai/api/v1/chat/completions")
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen/qwen-2.5-7b-instruct")

# Configurações de retry
MAX_RETRIES = 3
RETRY_DELAY = 2  # segundos

if not QWEN_API_KEY:
    print("[AVISO] QWEN_API_KEY não configurada. Usando fallback para todos os roteiros.")


async def gerar_roteiro(historia: str) -> str:
    """
    Chama o modelo Qwen para transformar uma ideia em roteiro narrativo.
    Executado em thread separada para não bloquear o event loop.
    """
    if not QWEN_API_KEY:
        return _fallback_roteiro(historia)
    
    prompt = (
        "Você é um roteirista profissional. Transforme a ideia abaixo em um roteiro "
        "curto, envolvente e pronto para narração em vídeo. Use linguagem clara e "
        f"emocionante. Máximo de 150 palavras.\n\nIdeia/História: {historia}"
    )

    try:
        roteiro = await asyncio.to_thread(_chamar_api_com_retry, prompt)
        return roteiro

    except Exception as e:
        print(f"[AVISO] Falha na API Qwen após {MAX_RETRIES} tentativas: {e}. Usando fallback.")
        return _fallback_roteiro(historia)


def _chamar_api_com_retry(prompt: str) -> str:
    """Chamada à API com sistema de retry automático."""
    last_exception = None
    
    for tentativa in range(MAX_RETRIES):
        try:
            return _chamar_api_sync(prompt)
        except requests.exceptions.Timeout as e:
            last_exception = e
            print(f"[TENTATIVA {tentativa + 1}/{MAX_RETRIES}] Timeout da API. Aguardando...")
        except requests.exceptions.ConnectionError as e:
            last_exception = e
            print(f"[TENTATIVA {tentativa + 1}/{MAX_RETRIES}] Erro de conexão. Aguardando...")
        except requests.exceptions.HTTPError as e:
            # ✅ CORREÇÃO COMPLETA: Tratamento inteligente de erros HTTP
            if e.response is not None:
                status_code = e.response.status_code
                
                # Erros 4xx (exceto 429) - Erro do cliente, não retentar
                if 400 <= status_code < 500 and status_code != 429:
                    print(f"[ERRO] Erro do cliente ({status_code}). Não será retentado.")
                    raise
                
                # Erros 429 (Rate Limit) - Retentar com delay maior
                elif status_code == 429:
                    last_exception = e
                    print(f"[TENTATIVA {tentativa + 1}/{MAX_RETRIES}] Rate limit. Aguardando...")
                    time.sleep(RETRY_DELAY * 2)
                    continue
                
                # Erros 5xx - Erro do servidor, retentar
                elif 500 <= status_code < 600:
                    last_exception = e
                    print(f"[TENTATIVA {tentativa + 1}/{MAX_RETRIES}] Erro do servidor ({status_code}). Aguardando...")
                
                # Outros códigos HTTP
                else:
                    last_exception = e
                    print(f"[TENTATIVA {tentativa + 1}/{MAX_RETRIES}] Erro HTTP {status_code}. Aguardando...")
            else:
                # e.response é None (caso raro)
                last_exception = e
                print(f"[TENTATIVA {tentativa + 1}/{MAX_RETRIES}] Erro HTTP sem resposta. Aguardando...")
        
        except Exception as e:
            last_exception = e
            print(f"[TENTATIVA {tentativa + 1}/{MAX_RETRIES}] Erro inesperado: {e}")
        
        # Espera antes de tentar novamente (backoff exponencial)
        if tentativa < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY * (2 ** tentativa))
    
    raise last_exception


def _chamar_api_sync(prompt: str) -> str:
    """Chamada síncrona à API (executada em thread)."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {QWEN_API_KEY}"
    }
    
    payload = {
        "model": QWEN_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.8
    }

    response = requests.post(
        QWEN_API_URL, 
        json=payload, 
        headers=headers, 
        timeout=30
    )
    response.raise_for_status()

    data = response.json()
    
    # Validação robusta
    if not isinstance(data, dict):
        raise ValueError("Resposta inválida da API")
    
    choices = data.get("choices", [])
    if not choices:
        raise ValueError("Nenhuma escolha retornada pela API")
    
    content = choices[0].get("message", {}).get("content", "")
    if not content:
        raise ValueError("Conteúdo vazio na resposta")
    
    return content.strip()


def _fallback_roteiro(historia: str) -> str:
    """Roteiro de emergência caso a IA esteja offline."""
    return (
        f"{historia}. "
        "Esta é uma jornada que toca o coração de todos que a conhecem. "
        "Cada passo revela uma nova descoberta, cada desafio fortalece o espírito. "
        "No fim, a verdadeira vitória não está no destino, mas na transformação "
        "que aconteceu ao longo do caminho."
  )
