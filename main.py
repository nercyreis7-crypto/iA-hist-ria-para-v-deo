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
        
        # Campo da Chave API
        self.input_chave = TextInput(hint_text="Cole sua chave API Gemini aqui", multiline=False)
        # Campo do Tema
        self.input_tema = TextInput(hint_text="Sobre o que é o vídeo?", multiline=True, size_hint_y=0.3)
        # Botão de Gerar
        self.btn_gerar = Button(text="Gerar História com Falas", on_press=self.gerar)
        
        # Área de Scroll para a história (para não cortar o texto)
        self.scroll = ScrollView()
        self.label_resposta = Label(text="O roteiro aparecerá aqui...", size_hint_y=None)
        self.label_resposta.bind(texture_size=self.label_resposta.setter('size'))
        self.scroll.add_widget(self.label_resposta)
        
        self.layout.add_widget(self.input_chave)
        self.layout.add_widget(self.input_tema)
        self.layout.add_widget(self.btn_gerar)
        self.layout.add_widget(self.scroll)
        
        return self.layout

    def gerar(self, instance):
        api_key = self.input_chave.text.strip()
        tema = self.input_tema.text.strip()
        
        if not api_key:
            self.label_resposta.text = "Erro: Coloque sua chave de acesso!"
            return
            
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Comando melhorado para incluir diálogos
            prompt = f"Escreva um roteiro épico sobre: {tema}. Inclua diálogos alternados entre os personagens para dar emoção à cena."
            
            resposta = model.generate_content(prompt)
            self.label_resposta.text = resposta.text
        except Exception as e:
            self.label_resposta.text = f"Erro na conexão: {str(e)}"

if __name__ == '__main__':
    DirectorIA().run()
