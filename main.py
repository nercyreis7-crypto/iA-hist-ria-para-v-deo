from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import requests

class MeuApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.btn = Button(text="Gerar História")
        self.btn.bind(on_press=self.gerar)
        self.label = Label(text="Pressione para começar")
        self.layout.add_widget(self.btn)
        self.layout.add_widget(self.label)
        return self.layout

    def gerar(self, instance):
        try:
            resposta = requests.post("http://localhost:5001/api/v1/generate", json={"prompt": "Crie uma história curta"})
            texto = resposta.json()["results"][0]["text"]
            self.label.text = texto
        except:
            self.label.text = "Erro ao conectar"

if __name__ == '__main__':
    MeuApp().run()

