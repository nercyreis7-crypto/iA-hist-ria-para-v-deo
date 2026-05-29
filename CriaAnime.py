import sys
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class MotorIsekai:
    def gerar_historia(self, tema, fala, api_key, callback):
        def tarefa():
            if not genai:
                Clock.schedule_once(lambda dt: callback("Erro: Biblioteca da IA nao instalada!"))
                return
            
            try:
                historia_limpa = tema.replace("#", "")
                fala_limpa = fala.replace("#", "")
                
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"Historia Isekai: {historia_limpa}. Com a fala: {fala_limpa}."
                response = model.generate_content(prompt)
                resultado = response.text
            except Exception as e:
                resultado = f"Erro de conexao: {str(e)}"
            
            Clock.schedule_once(lambda dt: callback(resultado))
            
        threading.Thread(target=tarefa, daemon=True).start()

class AppIsekai(App):
    def build(self):
        self.motor = MotorIsekai()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.input_chave = TextInput(hint_text="Sua API Key (obrigatorio)", multiline=False)
        self.input_tema = TextInput(hint_text="Tema da historia")
        self.input_fala = TextInput(hint_text="O que o pessoal deve falar?")
        
        self.lbl = Label(text="Pressione para comecar", halign='center')
        btn = Button(text="Gerar Historia", on_press=self.iniciar)
        
        layout.add_widget(self.input_chave)
        layout.add_widget(self.input_tema)
        layout.add_widget(self.input_fala)
        layout.add_widget(self.lbl)
        layout.add_widget(btn)
        return layout

    def iniciar(self, instance):
        if not self.input_chave.text:
            self.lbl.text = "Erro: Coloque sua chave de acesso!"
            return
        self.lbl.text = "Gerando..."
        self.motor.gerar_historia(self.input_tema.text, self.input_fala.text, self.input_chave.text, self.atualizar)

    def atualizar(self, texto):
        self.lbl.text = texto

if __name__ == "__main__":
    sys.setrecursionlimit(2000)
    AppIsekai().run()
