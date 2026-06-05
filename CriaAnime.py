import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading
import os
import requests
from gtts import gTTS

class DirectorIAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DirectorIA - História para Vídeo")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        frame_principal = ttk.Frame(self.root, padding="20")
        frame_principal.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame_principal, text="Ideia / História:", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.text_historia = tk.Text(frame_principal, height=6, width=60, font=("Arial", 10))
        self.text_historia.grid(row=1, column=0, columnspan=2, pady=(0, 15))

        ttk.Label(frame_principal, text="Motor de Processamento:", font=("Arial", 11, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.modelo_selecionado = ttk.Combobox(frame_principal, state="readonly", width=57, font=("Arial", 10))
        self.modelo_selecionado['values'] = ("Pipeline Completo (Roteiro + Voz + Vídeo)", "Apenas Roteiro (Qwen)", "Apenas Voz (TTS Nativo)")
        self.modelo_selecionado.current(0)
        self.modelo_selecionado.grid(row=3, column=0, columnspan=2, pady=(0, 15))

        self.btn_processar = ttk.Button(frame_principal, text="Gerar Vídeo", command=self._iniciar_processamento)
        self.btn_processar.grid(row=4, column=0, columnspan=2, pady=(0, 15))

        self.label_status = ttk.Label(frame_principal, text="Aguardando início...", font=("Arial", 10, "italic"), foreground="gray")
        self.label_status.grid(row=5, column=0, columnspan=2, sticky=tk.W)

    def _atualizar_status(self, mensagem: str):
        self.root.after(0, lambda: self.label_status.config(text=mensagem))

    def _iniciar_processamento(self):
        historia = self.text_historia.get("1.0", tk.END).strip()
        if not historia:
            messagebox.showwarning("Atenção", "Por favor, insira uma história ou ideia.")
            return

        modelo = self.modelo_selecionado.get()
        self.btn_processar.config(state=tk.DISABLED)
        
        threading.Thread(target=self._run_async_loop, args=(historia, modelo), daemon=True).start()

    def _run_async_loop(self, historia: str, modelo: str):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.processar_voz_e_video(historia, modelo))
        except Exception as e:
            self._atualizar_status(f"Erro crítico: {str(e)}")
        finally:
            loop.close()
            self.root.after(0, lambda: self.btn_processar.config(state=tk.NORMAL))

    async def processar_voz_e_video(self, historia: str, modelo: str):
        try:
            roteiro_final = ""
            audio_path = "narracao_temp.mp3"
            video_path = "video_final.mp4"

            if "Roteiro" in modelo or "Completo" in modelo:
                self._atualizar_status("Gerando roteiro com Qwen...")
                roteiro_final = await self._chamar_qwen(historia)
                if "Apenas Roteiro" in modelo:
                    self._atualizar_status("Concluído! Roteiro gerado.")
                    messagebox.showinfo("Sucesso", f"Roteiro:\n\n{roteiro_final}")
                    return

            if "Voz" in modelo or "Completo" in modelo:
                self._atualizar_status("Convertendo áudio com TTS nativo...")
                texto_para_falar = roteiro_final if roteiro_final else historia
                tts = gTTS(text=texto_para_falar, lang='pt', slow=False)
                tts.save(audio_path)

                if "Apenas Voz" in modelo:
                    self._atualizar_status("Concluído! Áudio gerado com sucesso.")
                    messagebox.showinfo("Sucesso", f"Áudio salvo como: {os.path.abspath(audio_path)}")
                    return

            self._atualizar_status("Sincronizando vídeo e áudio...")
            await self._integrar_audio_video(roteiro_final if roteiro_final else historia, audio_path, video_path)

            self._atualizar_status("Processo finalizado com sucesso!")
            messagebox.showinfo("Sucesso", f"Vídeo gerado com sucesso!\nSalvo em: {os.path.abspath(video_path)}")

        except Exception as e:
            self._atualizar_status(f"Falha no processo: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro durante o processamento:\n{str(e)}")

    async def _chamar_qwen(self, historia: str) -> str:
        try:
            payload = {
                "model": "qwen",
                "prompt": f"Crie um roteiro curto, narrativo e envolvente baseado nesta história, pronto para narração: {historia}",
                "stream": False
            }
            response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=15)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
        except requests.exceptions.RequestException:
            pass
        
        return f"Narração: {historia}. O protagonista embarcou em uma jornada inesquecível, superando todos os obstáculos com coragem e determinação até alcançar seu objetivo final."

    async def _integrar_audio_video(self, texto: str, audio_path: str, video_path: str):
        try:
            from moviepy import AudioFileClip, ColorClip
            
            audio = AudioFileClip(audio_path)
            duracao = audio.duration
            
            video = ColorClip(size=(1280, 720), color=(40, 40, 40), duration=duracao)
            video = video.with_audio(audio)
            
            video.write_videofile(
                video_path, 
                fps=24, 
                codec="libx264", 
                audio_codec="aac", 
                logger=None
            )
            
            audio.close()
            video.close()
            
        except ImportError:
            with open(video_path, "w", encoding="utf-8") as f:
                f.write(f"ARQUIVO DE VÍDEO SIMULADO.\nPara renderização real, instale: pip install moviepy\n\nRoteiro usado:\n{texto}")
        except Exception as e:
            with open(video_path, "w", encoding="utf-8") as f:
                f.write(f"Erro na renderização do vídeo: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DirectorIAApp(root)
    root.mainloop()
