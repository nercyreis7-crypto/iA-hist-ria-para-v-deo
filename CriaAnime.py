 
import requests
import json

class MotorOrquestracaoVideo:
    def __init__(self, estilo_visual="Cinematico"):
        self.estilo = estilo_visual
        # Mude o IP abaixo para o IP do seu computador na rede Wi-Fi
        self.url = "http://192.168.0.XX:5001/api/v1/generate" 

    def gerar_diretrizes_superiores(self, tema):
        try:
            prompt = f"Atue como um Diretor de Cinema. Tema: {tema}."
            payload = {"prompt": prompt, "max_length": 1000}
            # Adicionamos um timeout para o app não travar se o PC estiver desligado
            response = requests.post(self.url, json=payload, timeout=10)
            return response.json()["results"][0]["text"]
        except Exception as e:
            return f"Erro de conexão: {str(e)}"
