import pyttsx3
from markdown import markdown
from bs4 import BeautifulSoup

def markdown_to_plain_text(markdown_text):
    """Converte texto em Markdown para texto simples."""
    html = markdown(markdown_text)  # Converte Markdown para HTML
    soup = BeautifulSoup(html, "html.parser")  # Usa BeautifulSoup para extrair texto
    return soup.get_text()

def synthesize_speech(markdown_text, output_file="static/output.mp3"):
    """Gera áudio a partir de texto usando pyttsx3."""
    # Converte Markdown para texto simples
    text = markdown_to_plain_text(markdown_text)

    # Inicializa o pyttsx3 com o driver especificado
    engine = pyttsx3.init(driverName='dummy')  # Substitua 'dummy' por 'sapi5' (Windows) ou 'nsss' (macOS)

    # Configura a voz feminina
    voices = engine.getProperty('voices')
    female_voice = None
    for voice in voices:
        if "female" in voice.name.lower() or "feminina" in voice.name.lower():
            female_voice = voice
            break

    if female_voice:
        engine.setProperty('voice', female_voice.id)
    else:
        print("Voz feminina não encontrada. Usando a voz padrão.")

    # Configura a velocidade da fala
    engine.setProperty('rate', 200)  # Velocidade ajustada para leitura mais natural

    # Salva o áudio em um arquivo
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    print(f"Áudio salvo em {output_file}")
