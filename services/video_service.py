import asyncio
from moviepy.editor import AudioFileClip, ColorClip, TextClip, CompositeVideoClip


async def gerar_video(texto: str, audio_path: str, video_path: str) -> str:
    """
    Integra o áudio gerado com uma cena visual.
    Executado em thread separada (moviepy é síncrono).
    """
    await asyncio.to_thread(_gerar_video_sync, texto, audio_path, video_path)
    return video_path


def _gerar_video_sync(texto: str, audio_path: str, video_path: str):
    """Versão síncrona executada em thread."""
    audio = AudioFileClip(audio_path)
    duracao = audio.duration

    # Fundo gradiente escuro
    fundo = ColorClip(size=(1280, 720), color=(25, 25, 35), duration=duracao)

    # Tenta adicionar legenda (pode falhar se ImageMagick não estiver instalado)
    try:
        # Pega os primeiros 80 caracteres para legenda
        legenda_texto = texto[:80].replace('\n', ' ') + ("..." if len(texto) > 80 else "")
        
        legenda = TextClip(
            legenda_texto,
            fontsize=36,
            color='white',
            font='DejaVu-Sans',  # Mais compatível com Linux
            size=(1100, None),
            method='caption'
        )
        legenda = legenda.set_duration(duracao).set_position(('center', 'center'))
        video_final = CompositeVideoClip([fundo, legenda])
        
    except Exception as e:
        print(f"[AVISO] Falha ao criar legenda: {e}. Usando apenas fundo.")
        video_final = fundo

    video_final = video_final.set_audio(audio)

    video_final.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        logger=None  # Silencia logs
    )

    audio.close()
    video_final.close()
