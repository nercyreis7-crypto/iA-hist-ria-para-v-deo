import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import google.generativeai as genai

genai.configure(api_key="AIzaSyAebI0PJGy35buoyYgooiiuZzmOwHb27Ao")
model = genai.GenerativeModel('gemini-pro')

class MotorIsekai:
    def gerar_historia(self, tema, callback):
        def tarefa():
            try:
                
                prompt = f"Escreva uma história curta de Isekai épico sobre: {tema}. Use um tom emocionante, descreva o mundo fantástico e o poder especial do protagonista. Divida em 3 cenas curtas."
                response = model.generate_content(prompt)
                resultado = response.text
            except Exception as e:
                resultado = f"Erro de conexão com o cérebro: {str(e)}"
            Clock.schedule_once(lambda dt: callback(resultado))
        threading.Thread(target=tarefa).start()

class AppIsekai(App):
    def build(self):
        self.motor = MotorIsekai()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.lbl = Label(text="Pressione para iniciar sua jornada Isekai", text_size=(300, None))
        btn = Button(text="Gerar História", size_hint=(1, 0.2), on_press=self.iniciar)
        layout.add_widget(self.lbl)
        layout.add_widget(btn)
        return layout

    def iniciar(self, instance):
        self.lbl.text = "Viajando para outro mundo..."
        self.motor.gerar_historia("Um estudante comum que renasce como um mago das sombras", self.atualizar)

    def atualizar(self, texto):
        self.lbl.text = texto

if __name__ == "__main__":
    AppIsekai().run()



    
