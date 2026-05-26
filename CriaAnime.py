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
            size_hint_y=None,
            height=100
        )

        self.tema_input = TextInput(
            hint_text="Digite o tema do vídeo...",
            multiline=True,
            size_hint_y=None,
            height=200
        )

        self.botao = Button(
            text="Gerar Direção Cinematográfica",
            size_hint_y=None,
            height=100
        )

        self.botao.bind(on_press=self.iniciar_geracao)

        self.resultado = Label(
            text="DirectorAI Online",
            size_hint_y=None,
            markup=True,
            valign="top"
        )

        self.resultado.bind(
            width=lambda *x: self.resultado.setter("text_size")(self.resultado, (self.resultado.width, None))
        )

        self.resultado.bind(
            texture_size=lambda *x: setattr(self.resultado, "height", self.resultado.texture_size[1])
        )

        scroll = ScrollView()
        scroll.add_widget(self.resultado)

        self.add_widget(Label(
            text="IP do Servidor Flask",
            size_hint_y=None,
            height=50
        ))

        self.add_widget(self.api_ip)

        self.add_widget(Label(
            text="Tema do Vídeo",
            size_hint_y=None,
            height=50
        ))

        self.add_widget(self.tema_input)

        self.add_widget(self.botao)

        self.add_widget(scroll)

    def iniciar_geracao(self, instance):
        tema = self.tema_input.text.strip()

        if not tema:
            self.resultado.text = "[color=ff0000]Digite um tema.[/color]"
            return

        self.resultado.text = "[color=00ff00]Conectando ao DirectorAI...[/color]"

        threading.Thread(
            target=self.gerar_direcao,
            args=(tema,),
            daemon=True
        ).start()

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
                lambda dt: self.atualizar_resultado(texto)
            )

        except Exception as e:

            Clock.schedule_once(
                lambda dt: self.atualizar_resultado(
                    f"[color=ff0000]ERRO:[/color]\n\n{str(e)}"
                )
            )

    def atualizar_resultado(self, texto):
        self.resultado.text = texto


class DirectorAIApp(App):

    def build(self):
        return DirectorAI()


if __name__ == "__main__":
    DirectorAIApp().run()

