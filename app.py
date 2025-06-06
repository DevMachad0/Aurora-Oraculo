from flask import Flask, render_template, request, send_file, send_from_directory
from flask_compress import Compress
from modulo.api_connector import search_topic
from modulo.text_to_speech import synthesize_speech
import markdown  # Reintroduzindo a biblioteca markdown
import os

app = Flask(__name__)
Compress(app)  # Ativa compactação para respostas HTTP

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

@app.route('/ads.txt')
def ads_txt():
    """Serve o arquivo ads.txt para o Google AdSense."""
    return send_from_directory(directory='.', path='ads.txt', mimetype='text/plain')

if __name__ == '__main__':
    # Obtém a porta da variável de ambiente ou usa 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    # Configura o Flask para rodar no host 0.0.0.0 e na porta especificada
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
