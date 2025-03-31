from flask import Flask, render_template, request, send_file
from modulo.api_connector import search_topic
from modulo.text_to_speech import synthesize_speech
import markdown  # Reintroduzindo a biblioteca markdown
import os

app = Flask(__name__)

# Lista de palavras-chave proibidas
PROHIBITED_TOPICS = ["pornografia", "crime", "violência", "terrorismo", "drogas"]

def clean_prefixes(text):
    """Remove prefixos indesejados do texto gerado."""
    return text.replace("```html", "").replace("```", "").strip()

def validate_and_clean_text(text):
    """Valida e corrige problemas de formatação no texto gerado."""
    # Remove prefixos indesejados
    text = clean_prefixes(text)
    # Garante que o texto termine com uma conclusão
    if "Conclusão" not in text:
        text += "\n\n### Conclusão\nEste é o fim do seminário. Obrigado por ler!"
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        # Verifica se o tema contém palavras proibidas
        if any(prohibited in query.lower() for prohibited in PROHIBITED_TOPICS):
            return render_template('index.html', error="O tema solicitado não é permitido.")
        
        results = search_topic(query)
        if "error" in results:
            return render_template('index.html', query=query, error=results["error"])
        
        # Processa o texto como Markdown
        if "response" in results:
            response_text = validate_and_clean_text(results["response"])  # Valida e limpa o texto
            results["markdown_content"] = markdown.markdown(response_text)

            # Gera o áudio do texto
            audio_file = "static/output.mp3"
            synthesize_speech(results["markdown_content"], output_file=audio_file)
            results["audio_file"] = audio_file
        
        # Formata as fontes de busca como HTML
        if "sources" in results:
            sources_html = "".join(
                [f"<li><a href='{source['link']}' target='_blank'>{source['title']}</a></li>" for source in results["sources"]]
            )
            results["sources_html"] = f"<ul>{sources_html}</ul>"
        
        return render_template('index.html', query=query, results=results)
    return render_template('index.html', error="Nenhuma pesquisa foi realizada.")

@app.route('/audio')
def audio():
    """Endpoint para baixar o áudio gerado."""
    audio_path = "static/output.mp3"
    if os.path.exists(audio_path):
        return send_file(audio_path, as_attachment=True)
    return "Áudio não encontrado.", 404

if __name__ == '__main__':
    app.run(debug=True)
