import threading
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

class MotorOrquestracaoVideo:
    def __init__(self):
        self.url = "http://192.168.0.XX:5001/api/v1/generate"

    def gerar_roteiro(self, tema, callback):
        def tarefa_em_segundo_plano():
            try:
                payload = {"prompt": f"Diretor de Cinema: {tema}", "max_length": 500}
                response = requests.post(self.url, json=payload, timeout=10)
                resultado = response.json()["results"][0]["text"]
            except Exception as e:
                resultado = f"Erro: {str(e)}"
            Clock.schedule_once(lambda dt: callback(resultado))
        threading.Thread(target=tarefa_em_segundo_plano).start()

class AppDiretor(App):
    def build(self):
        self.motor = MotorOrquestracaoVideo()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.lbl = Label(text="Pressione para começar", text_size=(300, None))
        btn = Button(text="Gerar História", size_hint=(1, 0.2), on_press=self.iniciar_geracao)
        layout.add_widget(self.lbl)
        layout.add_widget(btn)
        return layout

    def iniciar_geracao(self, instance):
        self.lbl.text = "Pensando..."
        self.motor.gerar_roteiro("História de um herói", self.atualizar_label)

    def atualizar_label(self, texto):
        self.lbl.text = texto

if __name__ == "__main__":
    AppDiretor().run()

