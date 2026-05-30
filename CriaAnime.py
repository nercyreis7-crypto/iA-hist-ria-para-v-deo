import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests
import json

class DirectorIA(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.input_key = TextInput(hint_text="Sua API Key", multiline=False)
        self.input_historia = TextInput(hint_text="História para vídeo...", multiline=True)
        
        self.btn_gerar = Button(text="Gerar e Salvar", on_press=self.processar)
        self.btn_listar = Button(text="Ver Arquivos Salvos", on_press=self.listar_arquivos)
        
        self.label_status = Label(text="Aguardando...", size_hint_y=None)
        self.label_status.bind(texture_size=self.label_status.setter('size'))
        
        self.scroll = ScrollView()
        self.scroll.add_widget(self.label_status)
        
        self.layout.add_widget(self.input_key)
        self.layout.add_widget(self.input_historia)
        self.layout.add_widget(self.btn_gerar)
        self.layout.add_widget(self.btn_listar)
        self.layout.add_widget(self.scroll)
        return self.layout

    def salvar_roteiro(self, conteudo):
        caminho = "/sdcard/Download/"
        nome = "roteiro_video.json"
        with open(os.path.join(caminho, nome), "w") as f:
            f.write(conteudo)
        return f"Salvo com sucesso em {caminho}{nome}"

    def processar(self, instance):
        api_key = self.input_key.text.strip()
        historia = self.input_historia.text.strip()
        
        if not api_key or not historia:
            self.label_status.text = "Erro: API Key e História são obrigatórias."
            return

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        prompt = f"""
        Transforme esta história em um roteiro de vídeo técnico em formato JSON.
        História: {historia}
        Responda APENAS com este formato JSON:
        {{"title": "Título", "scenes": [{{"scene": 1, "dialog": "...", "action": "...", "broll": "...", "transition": "..."}}]}}
        """
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            self.label_status.text = "Gerando... aguarde."
            resp = requests.post(url, json=payload, timeout=20)
            data = resp.json()
            
            # Extrai o texto limpo da resposta
            conteudo_json = data['candidates'][0]['content']['parts'][0]['text']
            conteudo_limpo = conteudo_json.replace("```json", "").replace("```", "").strip()
            
            # Salva na pasta Download
            msg = self.salvar_roteiro(conteudo_limpo)
            self.label_status.text = msg
        except Exception as e:
            self.label_status.text = f"Erro na conexão: {str(e)}"

    def listar_arquivos(self, instance):
        try:
            arquivos = os.listdir("/sdcard/Download/")
            roteiros = [f for f in arquivos if f.endswith(".json")]
            self.label_status.text = "Arquivos encontrados:\n" + "\n".join(roteiros)
        except Exception as e:
            self.label_status.text = "Erro ao acessar pasta: verifique permissões."

if __name__ == '__main__':
    DirectorIA().run()
