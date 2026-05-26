from kivy.config import Config

Config.set("graphics", "multisamples", "0")
Config.set("graphics", "maxfps", "60")
Config.set("input", "mouse", "mouse,multitouch_on_demand")

import threading
import requests

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class DirectorAI(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=10, padding=10, **kwargs)

        self.api_ip = TextInput(
            text="192.168.0.10",
            hint_text="IP do servidor Flask",
            multiline=False,
            size_hint=(1, None),
            height=60
        )

        self.tema_input = TextInput(
            hint_text="Digite o tema do vídeo...",
            multiline=True,
            size_hint=(1, None),
            height=150
        )

        self.botao = Button(
            text="Gerar Direção Cinematográfica",
            size_hint=(1, None),
            height=70
        )

        self.botao.bind(on_press=self.iniciar_geracao)

        self.resultado = Label(
            text="DirectorAI Online",
            markup=True,
            size_hint_y=None,
            valign="top",
            halign="left"
        )

        self.resultado.bind(
            width=self.atualizar_text_size
        )

        self.resultado.bind(
            texture_size=self.atualizar_altura
        )

        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True
        )

        scroll.add_widget(self.resultado)

        self.add_widget(Label(
            text="IP do Servidor Flask",
            size_hint=(1, None),
            height=40
        ))

        self.add_widget(self.api_ip)

        self.add_widget(Label(
            text="Tema do Vídeo",
            size_hint=(1, None),
            height=40
        ))

        self.add_widget(self.tema_input)

        self.add_widget(self.botao)

        self.add_widget(scroll)

    def atualizar_text_size(self, *args):
        self.resultado.text_size = (self.resultado.width - 20, None)

    def atualizar_altura(self, *args):
        self.resultado.height = self.resultado.texture_size[1] + 30

    def iniciar_geracao(self, instance):

        tema = self.tema_input.text.strip()

        if not tema:
            self.resultado.text = "[color=ff0000]Digite um tema.[/color]"
            return

        self.botao.disabled = True

        self.resultado.text = "[color=00ff00]Conectando ao DirectorAI...[/color]"

        thread = threading.Thread(
            target=self.gerar_direcao,
            args=(tema,),
            daemon=True
        )

        thread.start()

    def gerar_direcao(self, tema):

        try:

            ip = self.api_ip.text.strip()

            url = f"http://{ip}:5001/api/v1/generate"

            prompt = f"""
            Atue como um Diretor Cinematográfico Profissional.

            Crie diretrizes avançadas para um vídeo sobre:

            {tema}

            Para cada cena forneça:

            1. ENQUADRAMENTO
            2. ILUMINAÇÃO
            3. MOVIMENTO DE CÂMERA
            4. NARRATIVA
            5. CLIMA CINEMATOGRÁFICO
            6. ESTILO VISUAL
            7. TRANSIÇÕES
            8. DETALHES TÉCNICOS

            Estruture tudo profissionalmente.
            """

            payload = {
                "prompt": prompt,
                "max_length": 1000
            }

            response = requests.post(
                url,
                json=payload,
                timeout=120
            )

            data = response.json()

            texto = data["results"][0]["text"]

            Clock.schedule_once(
                lambda dt: self.finalizar_resultado(texto)
            )

        except Exception as e:

            Clock.schedule_once(
                lambda dt: self.finalizar_resultado(
                    f"[color=ff0000]ERRO:[/color]\n\n{str(e)}"
                )
            )

    def finalizar_resultado(self, texto):

        self.resultado.text = texto

        self.botao.disabled = False


class DirectorAIApp(App):

    def build(self):
        return DirectorAI()


if __name__ == "__main__":
    DirectorAIApp().run()

