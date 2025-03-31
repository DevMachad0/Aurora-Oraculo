from gtts import gTTS
from markdown import markdown
from bs4 import BeautifulSoup

def markdown_to_plain_text(markdown_text):
    """Converte texto em Markdown para texto simples."""
    html = markdown(markdown_text)  # Converte Markdown para HTML
    soup = BeautifulSoup(html, "html.parser")  # Usa BeautifulSoup para extrair texto
    return soup.get_text()

def synthesize_speech(markdown_text, output_file="static/output.mp3"):
    """Gera áudio a partir de texto usando gTTS."""
    # Converte Markdown para texto simples
    text = markdown_to_plain_text(markdown_text)

    # Gera o áudio usando gTTS
    tts = gTTS(text, lang="pt")
    tts.save(output_file)
    print(f"Áudio salvo em {output_file}")
