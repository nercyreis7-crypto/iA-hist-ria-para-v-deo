limport requests
import json
import subprocess

class CerebroSupremo:
    def __init__(self, api_url="http://localhost:5001/api/v1/generate"):
        self.api_url = api_url

    def pensar(self, prompt):
        print("[Status] O cérebro está processando...")
        payload = {
            "prompt": f"Atue como um diretor de anime. {prompt}",
            "max_length": 500
        }
        try:
            response = requests.post(self.api_url, json=payload)
            return response.json()["results"][0]["text"]
        except Exception as e:
            return f"Erro ao conectar no KoboldCPP: {e}"

if __name__ == "__main__":
    cerebro = CerebroSupremo()
    tema = "Samurai Cyberpunk em Neo-Tokyo"
    roteiro = cerebro.pensar(f"Crie um roteiro de 3 cenas para: {tema}")
    print("\n--- ROTEIRO GERADO ---")
    print(roteiro)
    with open("roteiro_final.json", "w", encoding="utf-8") as f:
        f.write(roteiro)

