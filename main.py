import threading
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import google.generativeai as genai

class MotorIsekai:
    def gerar_historia(self, tema, fala, api_key, callback):
        def tarefa():
            try:
                # 1. Função de Limpeza (Validação de Segurança)
                historia_limpa = tema.replace("#", "")
                fala_limpa = fala.replace("#", "")
                
                # 2. Configuração Dinâmica da Chave do Usuário
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"História Isekai: {historia_limpa}. Com a fala: {fala_limpa}. Tom emocionante e épico."
                response = model.generate_content(prompt)
                resultado = response.text
            except Exception as e:
                resultado = f"Erro ao conectar com a IA: {str(e)}"
            Clock.schedule_once(lambda dt: callback(resultado))
        threading.Thread(target=tarefa).start()

class AppIsekai(App):
    def build(self):
        self.motor = MotorIsekai()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Campos de Entrada
        self.input_chave = TextInput(hint_text="Cole sua Chave de Acesso (API Key)", multiline=False)
        self.input_tema = TextInput(hint_text="Tema da história")
        self.input_fala = TextInput(hint_text="Opção de Fala")
        
        self.lbl = Label(text="Bem-vindo, Viajante!")
        btn = Button(text="Gerar História com Fala", on_press=self.iniciar)
        
        layout.add_widget(self.input_chave)
        layout.add_widget(self.input_tema)
        layout.add_widget(self.input_fala)
        layout.add_widget(self.lbl)
        layout.add_widget(btn)
        return layout

    def iniciar(self, instance):
        if not self.input_chave.text:
            self.lbl.text = "Erro: Chave obrigatória!"
            return
        
        self.lbl.text = "Gerando seu Isekai..."
        self.motor.gerar_historia(self.input_tema.text, self.input_fala.text, self.input_chave.text, self.atualizar)

    def atualizar(self, texto):
        self.lbl.text = texto

if __name__ == "__main__":
    AppIsekai().run()
