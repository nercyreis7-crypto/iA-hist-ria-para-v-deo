import os
import requests

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

API_URL = "https://seu-servidor.com/generate-video"

class DirectorIA(App):

def build(self):

    layout = BoxLayout(
        orientation="vertical",
        padding=10,
        spacing=10
    )

    self.api_key = TextInput(
        hint_text="Chave de acesso",
        multiline=False
    )

    self.story = TextInput(
        hint_text="Digite sua história...",
        multiline=True
    )

    self.status = Label(
        text="Pronto"
    )

    btn = Button(
        text="Gerar Vídeo"
    )

    btn.bind(on_press=self.generate_video)

    layout.add_widget(self.api_key)
    layout.add_widget(self.story)
    layout.add_widget(btn)
    layout.add_widget(self.status)

    return layout

def save_video(self, content):

    path = "/sdcard/Download"

    if not os.path.exists(path):
        os.makedirs(path)

    video_file = os.path.join(
        path,
        "video_final.mp4"
    )

    with open(video_file, "wb") as f:
        f.write(content)

    return video_file

def generate_video(self, instance):

    key = self.api_key.text.strip()
    story = self.story.text.strip()

    if not key:
        self.status.text = "Informe a chave."
        return

    if not story:
        self.status.text = "Digite uma história."
        return

    self.status.text = "Enviando para a nuvem..."

    payload = {
        "api_key": key,
        "story": story
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=300
        )

        if response.status_code != 200:
            self.status.text = (
                f"Erro {response.status_code}"
            )
            return

        video_path = self.save_video(
            response.content
        )

        self.status.text = (
            f"Vídeo salvo:\n{video_path}"
        )

    except Exception as e:
        self.status.text = str(e)

if name == "main":
DirectorIA().run()
