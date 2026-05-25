import requests
import json

class MotorOrquestracaoVideo:
    def __init__(self, estilo_visual="Cinematico"):
        self.estilo = estilo_visual
        self.url = "http://localhost:5001/api/v1/generate"

    def gerar_diretrizes_superiores(self, tema):
        prompt = (
            "Atue como um Diretor de Cinema. Crie diretrizes para um vídeo impactante sobre: " + tema + ". "
            "Para cada cena, forneça: "
            "1. ENQUADRAMENTO. "
            "2. ILUMINAÇÃO. "
            "3. NARRATIVA. "
            "Estruture de forma técnica e profissional."
        )
        payload = {"prompt": prompt, "max_length": 1000}
        response = requests.post(self.url, json=payload)
        return response.json()["results"][0]["text"]

if __name__ == "__main__":
    motor = MotorOrquestracaoVideo()
    tema = input("Qual a história para o vídeo hoje? ")
    roteiro_superior = motor.gerar_diretrizes_superiores(tema)
    print(roteiro_superior)
    with open("orquestracao_video.txt", "w", encoding="utf-8") as f:
        f.write(roteiro_superior)

