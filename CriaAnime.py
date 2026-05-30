from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import google.generativeai as genai

class DirectorIA(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.input_chave = TextInput(hint_text="Cole sua API Key aqui", multiline=False)
        self.input_tema = TextInput(hint_text="Sobre o que é a história?", multiline=True, size_hint_y=0.2)
        self.input_fala = TextInput(hint_text="Estilo da fala (Ex: Ameaçador)", multiline=False, size_hint_y=0.1)
        
        self.btn_gerar = Button(text="Gerar História com Falas", on_press=self.gerar)
        
        self.scroll = ScrollView()
        self.label_resposta = Label(text="Resultado aparecerá aqui...", size_hint_y=None)
        self.label_resposta.bind(texture_size=self.label_resposta.setter('size'))
        self.scroll.add_widget(self.label_resposta)
        
        self.layout.add_widget(self.input_chave)
        self.layout.add_widget(self.input_tema)
        self.layout.add_widget(self.input_fala)
        self.layout.add_widget(self.btn_gerar)
        self.layout.add_widget(self.scroll)
        
        return self.layout

    def gerar(self, instance):
        chave = self.input_chave.text.strip()
        tema = self.input_tema.text.strip()
        fala = self.input_fala.text.strip()
        
        if not chave or not tema:
            self.label_resposta.text = "Erro: Preencha a Chave e o Tema!"
            return
            
        try:
            self.label_resposta.text = "Conectando..."
            genai.configure(api_key=chave)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Escreva um roteiro épico sobre: {tema}. O estilo da fala dos personagens deve ser: {fala}. Inclua diálogos alternados."
            
            resposta = model.generate_content(prompt)
            self.label_resposta.text = resposta.text
        except Exception as e:
            self.label_resposta.text = f"Erro: {str(e)}"

if __name__ == '__main__':
    DirectorIA().run()
