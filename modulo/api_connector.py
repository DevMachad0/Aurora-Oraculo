import os
from dotenv import load_dotenv
from google import genai
import requests

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")  # ID do mecanismo de busca personalizado do Google

# Configure o cliente da API Gemini
client = genai.Client(api_key=API_KEY)

def search_topic(query):
    try:
        # Contexto para a IA gerar um texto detalhado e formatado
        context = (
            f"Você é um especialista em criar textos informativos e detalhados. "
            f"Escreva um seminário completo sobre o tema '{query}'. "
            f"O texto deve incluir uma introdução clara e objetiva, tópicos principais bem organizados, "
            f"subtópicos detalhados, exemplos práticos e uma conclusão. "
            f"Certifique-se de que o texto seja consistente e bem estruturado, sem interrupções ou erros. "
            f"Use Markdown para formatar títulos, subtítulos, listas e parágrafos. "
            f"Inclua tabelas diretamente em HTML para apresentar dados de forma clara e organizada. "
            f"Não tente gerar gráficos, apenas tabelas. "
            f"Use uma linguagem envolvente e educativa, e formate o texto com títulos, subtítulos, listas, "
            f"tabelas e parágrafos bem estruturados."
        )
        
        # Use o método generate_content para enviar a solicitação
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=context
        )
        ai_content = response.text

        # Buscar informações de múltiplos sites usando o Google Custom Search API
        google_results = search_google(query)

        return {"response": ai_content, "sources": google_results}
    except genai.exceptions.GenAIException as e:
        return {"error": f"API error: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

def search_google(query):
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CX,
            "q": query,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            sources = [
                {"title": item["title"], "link": item["link"]}
                for item in data.get("items", [])
            ]
            return sources
        else:
            return [{"title": "Erro ao buscar no Google", "link": ""}]
    except Exception as e:
        return [{"title": f"Erro: {str(e)}", "link": ""}]
