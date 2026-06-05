from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
import json


class DirectorIAApp(App):
    def build(self):
        self.title = "DirectorIA"
        self.tarefa_id = None
        self.polling_event = None
        self.processando = False
        self.base_url = "https://seu-projeto.railway.app"
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        titulo = Label(
            text="DirectorIA - História para Vídeo",
            font_size='20sp',
            bold=True,
            size_hint_y=0.1
        )
        layout.add_widget(titulo)
        
        label_historia = Label(text="Sua História:", size_hint_y=0.05, halign='left')
        layout.add_widget(label_historia)
        
        self.input_historia = TextInput(
            hint_text="Digite sua ideia ou história aqui...",
            multiline=True,
            size_hint_y=0.3
        )
        layout.add_widget(self.input_historia)
        
        label_modelo = Label(text="Motor de Processamento:", size_hint_y=0.05, halign='left')
        layout.add_widget(label_modelo)
        
        self.spinner_modelo = Spinner(
            text="Pipeline Completo",
            values=("Pipeline Completo", "Apenas Roteiro", "Apenas Voz"),
            size_hint_y=0.1,
            font_size='16sp'
        )
        layout.add_widget(self.spinner_modelo)
        
        self.btn_processar = Button(
            text="Gerar Vídeo",
            size_hint_y=0.1,
            font_size='18sp',
            bold=True
        )
        self.btn_processar.bind(on_press=self.iniciar_processamento)
        layout.add_widget(self.btn_processar)
        
        self.label_status = Label(
            text="Aguardando início...",
            size_hint_y=0.05,
            color=(0.5, 0.5, 0.5, 1)
        )
        layout.add_widget(self.label_status)
        
        scroll = ScrollView(size_hint_y=0.3)
        self.label_resultado = Label(
            text="",
            size_hint_y=None,
            height=0,
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        self.label_resultado.bind(texture_size=self.label_resultado.setter('size'))
        scroll.add_widget(self.label_resultado)
        layout.add_widget(scroll)
        
        return layout
    
    def on_start(self):
        Clock.schedule_once(self._update_text_size, 0.1)
    
    def _update_text_size(self, dt):
        if hasattr(self, 'label_resultado') and self.root:
            self.label_resultado.text_size = (self.root.width - 40, None)
    
    def on_stop(self):
        self._cancelar_polling()
    
    def on_pause(self):
        self._cancelar_polling()
        return True
    
    def on_resume(self):
        if self.processando and self.tarefa_id:
            self.label_status.text = "Verificando status..."
            self.consultar_status_uma_vez()
    
    def consultar_status_uma_vez(self):
        """Consulta status uma única vez ao voltar do background"""
        if not self.tarefa_id:
            return
        
        url = f"{self.base_url}/status/{self.tarefa_id}"
        
        UrlRequest(
            url,
            on_success=self.on_status_recebido_resume,
            on_failure=self.on_api_failure,
            on_error=self.on_api_error,
            timeout=15
        )
    
    def on_status_recebido_resume(self, request, result):
        """Handler específico para quando volta do background"""
        if not isinstance(result, dict):
            self._finalizar_processamento()
            return
        
        status = result.get("status", "")
        
        if status in ["concluido", "erro"]:
            self.on_status_recebido(request, result)
        else:
            self.label_status.text = result.get("mensagem", "Processando...")
            self.polling_event = Clock.schedule_interval(self.consultar_status, 2)
    
    def _cancelar_polling(self):
        """Cancela polling de forma segura"""
        if self.polling_event:
            self.polling_event.cancel()
            self.polling_event = None
    
    def iniciar_processamento(self, instance):
        if self.processando:
            return
        
        historia = self.input_historia.text.strip()
        if not historia:
            self.label_status.text = "Por favor, insira uma história!"
            return
        
        modelo = self.spinner_modelo.text
        self.processando = True
        self.btn_processar.disabled = True
        self.label_status.text = "Enviando para API..."
        self.label_resultado.text = ""
        
        self.chamar_api(historia, modelo)
    
    def chamar_api(self, historia, modelo):
        url = f"{self.base_url}/processar"
        
        data = {
            "historia": historia,
            "modelo": modelo
        }
        
        self.request = UrlRequest(
            url,
            req_body=json.dumps(data),
            req_headers={"Content-Type": "application/json"},
            on_success=self.on_tarefa_criada,
            on_failure=self.on_api_failure,
            on_error=self.on_api_error,
            timeout=30
        )
    
    def on_tarefa_criada(self, request, result):
        if isinstance(result, dict) and "tarefa_id" in result:
            self.tarefa_id = result["tarefa_id"]
            self.label_status.text = "Processando..."
            self.polling_event = Clock.schedule_interval(self.consultar_status, 2)
        else:
            self.label_status.text = "Erro: resposta inválida da API"
            self._finalizar_processamento()
    
    def consultar_status(self, dt):
        if not self.tarefa_id or not self.processando:
            return
        
        url = f"{self.base_url}/status/{self.tarefa_id}"
        
        UrlRequest(
            url,
            on_success=self.on_status_recebido,
            on_failure=self.on_api_failure,
            on_error=self.on_api_error,
            timeout=15
        )
    
    def on_status_recebido(self, request, result):
        if not isinstance(result, dict):
            self.label_status.text = "Erro: resposta inválida do servidor"
            self._finalizar_processamento()
            return
        
        status = result.get("status", "")
        mensagem = result.get("mensagem", "Processando...")
        
        self.label_status.text = mensagem
        
        if status == "concluido":
            self._cancelar_polling()
            self.exibir_resultado(result.get("resultado", {}))
            self._finalizar_processamento()
        
        elif status == "erro":
            self._cancelar_polling()
            self.label_status.text = f"Erro: {mensagem}"
            self._finalizar_processamento()
    
    def exibir_resultado(self, resultado):
        texto = "✅ Concluído!\n\n"
        
        if "roteiro" in resultado:
            texto += f"📝 ROTEIRO:\n{resultado['roteiro']}\n\n"
        
        if "roteiro_url" in resultado:
            texto += f"📄 Download roteiro: {resultado['roteiro_url']}\n\n"
        
        if "audio_url" in resultado:
            texto += f"🎵 Áudio: {resultado['audio_url']}\n\n"
        
        if "video_url" in resultado:
            texto += f"🎥 Vídeo: {resultado['video_url']}\n\n"
        
        self.label_resultado.text = texto
    
    def _finalizar_processamento(self):
        """Limpa estado após processamento"""
        self._cancelar_polling()
        self.processando = False
        self.tarefa_id = None
        self.btn_processar.disabled = False
    
    def on_api_error(self, request, error):
        self.label_status.text = f"Erro na API: {error}"
        self._finalizar_processamento()
    
    def on_api_failure(self, request, result):
        self.label_status.text = "Falha na conexão com o servidor!"
        self._finalizar_processamento()


if __name__ == "__main__":
    DirectorIAApp().run()
