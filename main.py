from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label


class MeuApp(App):

    def build(self):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.input_modelo = TextInput(
            hint_text="Nome do modelo",
            multiline=False
        )

        self.input_key = TextInput(
            hint_text="Sua API Key",
            multiline=False
        )

        self.input_historia = TextInput(
            hint_text="Digite a história",
            multiline=True
        )

        self.label_status = Label(text="Pronto")

        btn = Button(
            text="Executar",
            on_press=self.roteador_de_modelos
        )

        layout.add_widget(self.input_modelo)
        layout.add_widget(self.input_key)
        layout.add_widget(self.input_historia)
        layout.add_widget(btn)
        layout.add_widget(self.label_status)

        return layout

    def roteador_de_modelos(self, instance):
        modelo = self.input_modelo.text.strip().lower()

        if "gemini" in modelo:
            self.label_status.text = "Modelo Gemini selecionado"
        elif "video" in modelo:
            self.label_status.text = "Modelo de vídeo selecionado"
        else:
            self.label_status.text = "Modelo não reconhecido"


MeuApp().run()
