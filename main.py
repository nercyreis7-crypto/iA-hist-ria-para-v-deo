import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests

class DirectorIA(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.input_key = TextInput(hint_text="Sua API Key", multiline=False)
        self.input_historia = TextInput(hint_text="História para vídeo...", multiline=True)
        
        self.btn_gerar = Button(text="Gerar e Salvar", on_press=self.processar)
        self.btn_listar = Button(text="Ver Arquivos Salvos", on_press=self.listar_arquivos)
        
        self.label_status = Label(text="Aguardando...", size_hint_y=None)
        self.label_status.bind(texture_size=self.label_status.setter('size'))
        
        self.scroll = ScrollView()
        self.scroll.add_widget(self.label_status)
        
        self.layout.add_widget(self.input_key)
        self.layout.add_widget(self.input_historia)
        self.layout.add_widget(self.btn_gerar)
        self.layout.add_widget(self.btn_listar)
        self.layout.add_widget(self.scroll)
        return self.layout

    def salvar_roteiro(self, conteudo):
        caminho = "/sdcard/Download/"
        nome = "roteiro_video.json"
        with open(os.path.join(caminho, nome), "w") as f:
            f.write(conteudo)
        return f"Salvo com sucesso em {caminho}"

    def processar(self, instance):
        # ... (seu código de requests aqui) ...
        # Exemplo de conteúdo recebido da IA:
        exemplo_json = '{"title": "Dragão", "scenes": [{"id": 1, "action": "Voar"}]}'
        msg = self.salvar_roteiro(exemplo_json)
        self.label_status.text = msg

    def listar_arquivos(self, instance):
        arquivos = os.listdir("/sdcard/Download/")
        roteiros = [f for f in arquivos if f.endswith(".json")]
        self.label_status.text = "Arquivos encontrados:\n" + "\n".join(roteiros)

if __name__ == '__main__':
    DirectorIA().run()
