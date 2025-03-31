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

    engine = pyttsx3.init()

    # Configura a voz jovem feminina
    voices = engine.getProperty('voices')
    young_female_voice = None
    for voice in voices:
        if "young" in voice.name.lower() or "jovem" in voice.name.lower():
            young_female_voice = voice
            break

    if young_female_voice:
        engine.setProperty('voice', young_female_voice.id)
    else:
        print("Voz jovem feminina não encontrada. Tentando outra voz feminina.")
        # Fallback para qualquer voz feminina
        for voice in voices:
            if "female" in voice.name.lower() or "feminina" in voice.name.lower():
                young_female_voice = voice
                break

    if young_female_voice:
        engine.setProperty('voice', young_female_voice.id)
    else:
        print("Nenhuma voz feminina encontrada. Usando a voz padrão.")

    # Configura a velocidade da fala
    engine.setProperty('rate', 200)  # Velocidade ajustada para leitura mais natural

    # Salva o áudio em um arquivo
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    print(f"Áudio salvo em {output_file}")
