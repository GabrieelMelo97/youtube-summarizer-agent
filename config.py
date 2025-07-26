import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da API do Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash-lite")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY não encontrada. Adicione sua chave da API do Gemini no arquivo .env")

# Configurações do agente
RESUMO_PROMPT = """
Você é um especialista em resumir vídeos do YouTube. Sua tarefa é analisar a transcrição fornecida e criar um resumo estruturado com os principais pontos.

Transcrição do vídeo:
{transcript}

Por favor, forneça um resumo seguindo esta estrutura:

## 📝 RESUMO EXECUTIVO
(Um parágrafo conciso com a essência do vídeo)

## 🎯 PRINCIPAIS PONTOS
(Lista dos 5-7 pontos mais importantes, numerados)

## 💡 INSIGHTS CHAVE
(Ideias e conceitos mais relevantes)

## 📊 DADOS E ESTATÍSTICAS
(Números, percentuais ou dados mencionados, se houver)

## 🎬 CONCLUSÃO
(Síntese final e principais takeaways)

Mantenha o resumo informativo, bem estruturado e fácil de ler.
""" 