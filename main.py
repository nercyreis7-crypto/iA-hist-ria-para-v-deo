    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.input_modelo = TextInput(hint_text="Nome do Modelo (ex: gemini-1.5-flash)", multiline=False)
        self.input_key = TextInput(hint_text="Sua API Key", multiline=False)
        self.input_historia = TextInput(hint_text="História ou comando...", multiline=True)
        
        self.btn_executar = Button(text="Executar Ação", on_press=self.roteador_de_modelos)
        
        self.layout.add_widget(self.input_modelo)
        self.layout.add_widget(self.input_key)
        self.layout.add_widget(self.input_historia)
        self.layout.add_widget(self.btn_executar)
        return self.layout

    def roteador_de_modelos(self, instance):
        modelo = self.input_modelo.text.strip()
        
        if "gemini" in modelo:
            self.processar_roteiro()
        elif "video" in modelo:
            self.processar_video()
        else:
            self.label_status.text = "Modelo não reconhecido. Adicione um modelo válido."
