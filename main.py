        
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
        self.servidor_testando = False
        self.aguardando_resposta = False  # FIX: evita requisições de polling simultâneas

        # Lista de servidores pré-configurados
        self.servidores = {
            "🌟 Servidor Oficial (Recomendado)": "https://seu-projeto.railway.app",
            "⚡ Servidor Alternativo": "https://seu-projeto-backup.railway.app",
            "✏️ Personalizado (Digitar URL)": ""
        }

        # Carrega configurações salvas
        self.servidor_selecionado = self.get_servidor_salvo()
        self.base_url = self.servidores.get(self.servidor_selecionado, "")

        if self.servidor_selecionado == "✏️ Personalizado (Digitar URL)":
            self.base_url = self.get_url_personalizada_salva()

        layout = BoxLayout(orientation='vertical', padding=20, spacing=8)

        # Título
        titulo = Label(
            text="🎬 DirectorIA",
            font_size='22sp',
            bold=True,
            size_hint_y=0.06,
            color=(0.3, 0.6, 1, 1)
        )
        layout.add_widget(titulo)

        # ============================================
        # SEÇÃO DE SERVIDOR
        # ============================================
        label_servidor = Label(
            text="🖥️ Escolha o Servidor:",
            size_hint_y=0.03,
            halign='left',
            bold=True
        )
        layout.add_widget(label_servidor)

        self.spinner_servidor = Spinner(
            text=self.servidor_selecionado,
            values=list(self.servidores.keys()),
            size_hint_y=0.07,
            font_size='14sp'
        )
        self.spinner_servidor.bind(text=self.mudar_servidor)
        layout.add_widget(self.spinner_servidor)

        # Campo de URL personalizada (aparece só quando "Personalizado" está selecionado)
        self.box_url_personalizada = BoxLayout(orientation='vertical', size_hint_y=0.08, spacing=5)

        self.input_url = TextInput(
            text=self.base_url if self.servidor_selecionado == "✏️ Personalizado (Digitar URL)" else "",
            hint_text="https://seu-servidor-personalizado.com",
            multiline=False,
            size_hint_y=1,
            font_size='13sp'
        )
        self.input_url.bind(text=self.salvar_url_personalizada)
        self.box_url_personalizada.add_widget(self.input_url)

        if self.servidor_selecionado != "✏️ Personalizado (Digitar URL)":
            self.box_url_personalizada.opacity = 0
            self.box_url_personalizada.size_hint_y = 0

        layout.add_widget(self.box_url_personalizada)

        # Botão de Testar Conexão + Status
        box_teste = BoxLayout(size_hint_y=0.06, spacing=10)

        self.btn_testar = Button(
            text="🔍 Testar Conexão",
            size_hint_x=0.6,
            font_size='14sp',
            bold=True
        )
        self.btn_testar.bind(on_press=self.testar_conexao)
        box_teste.add_widget(self.btn_testar)

        self.label_status_servidor = Label(
            text="⚪ Não testado",
            size_hint_x=0.4,
            font_size='13sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        box_teste.add_widget(self.label_status_servidor)

        layout.add_widget(box_teste)

        # Linha divisória visual
        divisoria = Label(text="", size_hint_y=0.01, color=(0.3, 0.3, 0.3, 1))
        layout.add_widget(divisoria)

        # ============================================
        # SEÇÃO DE CONTEÚDO
        # ============================================
        label_modo = Label(text="🎯 Modo de Entrada:", size_hint_y=0.03, halign='left')
        layout.add_widget(label_modo)

        self.spinner_modo = Spinner(
            text="📝 Digitar Texto",
            values=("📝 Digitar Texto", "🔗 Colar Link"),
            size_hint_y=0.06,
            font_size='14sp'
        )
        self.spinner_modo.bind(text=self.mudar_modo)
        layout.add_widget(self.spinner_modo)

        self.label_entrada = Label(text="📝 Sua História:", size_hint_y=0.03, halign='left')
        layout.add_widget(self.label_entrada)

        self.input_entrada = TextInput(
            hint_text="Digite sua ideia ou história aqui...",
            multiline=True,
            size_hint_y=0.18
        )
        layout.add_widget(self.input_entrada)

        label_modelo = Label(text="⚙️ Motor de Processamento:", size_hint_y=0.03, halign='left')
        layout.add_widget(label_modelo)

        self.spinner_modelo = Spinner(
            text="Pipeline Completo",
            values=("Pipeline Completo", "Apenas Roteiro", "Apenas Voz"),
            size_hint_y=0.06,
            font_size='14sp'
        )
        layout.add_widget(self.spinner_modelo)

        self.btn_processar = Button(
            text="🎬 Gerar Vídeo",
            size_hint_y=0.07,
            font_size='16sp',
            bold=True,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.btn_processar.bind(on_press=self.iniciar_processamento)
        layout.add_widget(self.btn_processar)

        self.label_status = Label(
            text="Aguardando início...",
            size_hint_y=0.03,
            color=(0.5, 0.5, 0.5, 1)
        )
        layout.add_widget(self.label_status)

        scroll = ScrollView(size_hint_y=0.25)
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

    # ============================================
    # MÉTODOS DE SERVIDOR
    # ============================================

    def mudar_servidor(self, spinner, texto):
        self.servidor_selecionado = texto
        self.salvar_servidor(texto)

        if texto == "✏️ Personalizado (Digitar URL)":
            self.box_url_personalizada.opacity = 1
            self.box_url_personalizada.size_hint_y = 0.08
            self.base_url = self.get_url_personalizada_salva()
            self.input_url.text = self.base_url
        else:
            self.box_url_personalizada.opacity = 0
            self.box_url_personalizada.size_hint_y = 0
            self.base_url = self.servidores.get(texto, "")

        self.label_status_servidor.text = "⚪ Não testado"
        self.label_status_servidor.color = (0.7, 0.7, 0.7, 1)

    def testar_conexao(self, instance):
        if self.servidor_testando:
            return

        if self.servidor_selecionado == "✏️ Personalizado (Digitar URL)":
            self.base_url = self.input_url.text.strip().rstrip('/')

        if not self.base_url:
            self.label_status_servidor.text = "❌ Sem URL"
            self.label_status_servidor.color = (1, 0.3, 0.3, 1)
            return

        self.servidor_testando = True
        self.btn_testar.disabled = True
        self.label_status_servidor.text = "🔄 Testando..."
        self.label_status_servidor.color = (1, 1, 0.3, 1)

        url_teste = self.base_url.rstrip('/')

        UrlRequest(
            f"{url_teste}/health",
            on_success=self._teste_sucesso,
            on_failure=self._teste_falha,
            on_error=self._teste_erro,
            timeout=10
        )

    def _teste_sucesso(self, request, result):
        """Servidor respondeu 200 — está online"""
        self.servidor_testando = False
        self.btn_testar.disabled = False

        if isinstance(result, dict) and result.get("status") in ("online", "ok"):
            self.label_status_servidor.text = "🟢 Online"
            self.label_status_servidor.color = (0.3, 1, 0.3, 1)
        else:
            self.label_status_servidor.text = "🟡 Respondeu"
            self.label_status_servidor.color = (1, 1, 0.3, 1)

    def _teste_falha(self, request, result):
        # FIX: servidor respondeu com erro HTTP (4xx/5xx), mas está ONLINE
        # Mostrar "Offline" aqui estava errado — sem rede é o _teste_erro
        self.servidor_testando = False
        self.btn_testar.disabled = False
        self.label_status_servidor.text = "🟡 Online (com erro)"
        self.label_status_servidor.color = (1, 1, 0.3, 1)

    def _teste_erro(self, request, error):
        """Erro de rede — servidor realmente inacessível"""
        self.servidor_testando = False
        self.btn_testar.disabled = False
        self.label_status_servidor.text = "🔴 Sem conexão"
        self.label_status_servidor.color = (1, 0.3, 0.3, 1)

    def salvar_servidor(self, nome_servidor):
        from kivy.config import Config
        try:
            if not Config.has_section('directorIA'):
                Config.add_section('directorIA')
            Config.set('directorIA', 'servidor_selecionado', nome_servidor)
            Config.write()
        except Exception as e:
            print(f"[AVISO] Falha ao salvar servidor: {e}")

    def get_servidor_salvo(self):
        from kivy.config import Config
        try:
            servidor = Config.get('directorIA', 'servidor_selecionado')
            if servidor and servidor in self.servidores:
                return servidor
        except:
            pass
        return "🌟 Servidor Oficial (Recomendado)"

    def salvar_url_personalizada(self, instance, value):
        if value and value.strip():
            from kivy.config import Config
            try:
                if not Config.has_section('directorIA'):
                    Config.add_section('directorIA')
                Config.set('directorIA', 'url_personalizada', value.strip())
                Config.write()
                self.base_url = value.strip()
            except Exception as e:
                print(f"[AVISO] Falha ao salvar URL: {e}")

    def get_url_personalizada_salva(self):
        from kivy.config import Config
        try:
            url = Config.get('directorIA', 'url_personalizada')
            if url and url != '':
                return url
        except:
            pass
        return ""

    # ============================================
    # MÉTODOS DE MODO DE ENTRADA
    # ============================================

    def mudar_modo(self, spinner, texto):
        if "Link" in texto:
            self.label_entrada.text = "🔗 Cole o Link do Site:"
            self.input_entrada.hint_text = "https://exemplo.com/artigo-ou-noticia"
            self.input_entrada.text = ""
            self.input_entrada.multiline = False
        else:
            self.label_entrada.text = "📝 Sua História:"
            self.input_entrada.hint_text = "Digite sua ideia ou história aqui..."
            self.input_entrada.text = ""
            self.input_entrada.multiline = True

    # ============================================
    # MÉTODOS DE LIFECYCLE
    # ============================================

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
        if not isinstance(result, dict):
            self._finalizar_processamento()
            return

        status = result.get("status", "")

        if status in ("concluido", "erro"):
            self.on_status_recebido(request, result)
        else:
            self.label_status.text = result.get("mensagem", "Processando...")
            self.aguardando_resposta = False
            self.polling_event = Clock.schedule_interval(self.consultar_status, 2)

    def _cancelar_polling(self):
        if self.polling_event:
            self.polling_event.cancel()
            self.polling_event = None
        self.aguardando_resposta = False  # FIX: reseta a trava de requisição simultânea

    # ============================================
    # MÉTODOS DE PROCESSAMENTO
    # ============================================

    def iniciar_processamento(self, instance):
        if self.processando:
            return

        if self.servidor_selecionado == "✏️ Personalizado (Digitar URL)":
            self.base_url = self.input_url.text.strip().rstrip('/')
        else:
            self.base_url = self.servidores.get(self.servidor_selecionado, "").rstrip('/')

        if not self.base_url:
            self.label_status.text = "Por favor, configure a URL do servidor!"
            return

        entrada = self.input_entrada.text.strip()
        if not entrada:
            if "Link" in self.spinner_modo.text:
                self.label_status.text = "Por favor, cole um link!"
            else:
                self.label_status.text = "Por favor, insira uma história!"
            return

        modelo = self.spinner_modelo.text
        modo = self.spinner_modo.text

        if "Link" in modo:
            if not entrada.startswith(('http://', 'https://')):
                self.label_status.text = "Link inválido! Deve começar com http:// ou https://"
                return
            tipo_conteudo = "link"
            self.label_status.text = "Enviando link para API..."
        else:
            tipo_conteudo = "texto"
            self.label_status.text = "Enviando texto para API..."

        self.processando = True
        self.aguardando_resposta = False
        self.btn_processar.disabled = True
        self.label_resultado.text = ""

        self.chamar_api(entrada, modelo, tipo_conteudo)

    def chamar_api(self, conteudo, modelo, tipo_conteudo):
        url = f"{self.base_url}/processar"

        data = {
            "conteudo": conteudo,
            "tipo": tipo_conteudo,
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
        # FIX: não dispara nova requisição se ainda está aguardando resposta da anterior
        if not self.tarefa_id or not self.processando or self.aguardando_resposta:
            return

        self.aguardando_resposta = True
        url = f"{self.base_url}/status/{self.tarefa_id}"

        UrlRequest(
            url,
            on_success=self.on_status_recebido,
            on_failure=self.on_api_failure,
            on_error=self.on_api_error,
            timeout=15
        )

    def on_status_recebido(self, request, result):
        self.aguardando_resposta = False  # FIX: libera para próxima requisição

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
        self._cancelar_polling()
        self.processando = False
        self.tarefa_id = None
        self.btn_processar.disabled = False

    def on_api_error(self, request, error):
        self.aguardando_resposta = False  # FIX: reseta trava em caso de erro de rede
        self.label_status.text = f"Erro na API: {error}"
        self._finalizar_processamento()

    def on_api_failure(self, request, result):
        self.aguardando_resposta = False  # FIX: reseta trava em caso de falha HTTP
        self.label_status.text = "Falha na conexão com o servidor!"
        self._finalizar_processamento()


if __name__ == "__main__":
    DirectorIAApp().run()
