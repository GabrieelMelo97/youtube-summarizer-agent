import streamlit as st
import os
from youtube_summarizer_agent import YouTubeSummarizerAgent
import validators
import time

# Configuração da página
st.set_page_config(
    page_title="YouTube Video Summarizer",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF0000;
        font-size: 2.5em;
        margin-bottom: 30px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #e2f3ff;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Cabeçalho principal
    st.markdown('<h1 class="main-header">📺 YouTube Video Summarizer</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar com informações
    with st.sidebar:
        st.header("📋 Como usar")
        st.markdown("""
        1. **Configure sua API Key** do Google Gemini
        2. **Cole a URL** do vídeo do YouTube
        3. **Clique em 'Gerar Resumo'**
        4. **Aguarde** o processamento
        
        ### 🔑 Configuração da API
        Certifique-se de ter configurado a variável de ambiente `GOOGLE_API_KEY` ou crie um arquivo `.env` com sua chave.
        """)
        
        st.markdown("---")
        st.header("🎯 Funcionalidades")
        st.markdown("""
        - ✅ Extração automática de transcrições
        - ✅ Resumo estruturado com pontos principais
        - ✅ Insights e conclusões
        - ✅ Suporte a vídeos em PT e EN
        - ✅ Interface amigável
        """)
        
        st.markdown("---")
        st.header("⚙️ Status da API")
        
        # Verificar se a API key está configurada
        try:
            from config import GOOGLE_API_KEY, GEMINI_MODEL_NAME
            if GOOGLE_API_KEY:
                st.success("✅ API Key configurada")
                st.info(f"🤖 Modelo: {GEMINI_MODEL_NAME}")
            else:
                st.error("❌ API Key não configurada")
        except Exception as e:
            st.error(f"❌ Erro na configuração: {str(e)}")
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎬 Inserir URL do Vídeo")
        
        # Input para URL do vídeo
        video_url = st.text_input(
            "URL do YouTube:",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Cole aqui a URL completa do vídeo do YouTube"
        )
        
        # Botão para gerar resumo
        if st.button("🚀 Gerar Resumo", type="primary", use_container_width=True):
            if not video_url:
                st.error("❌ Por favor, insira uma URL válida do YouTube")
            elif not validators.url(video_url):
                st.error("❌ URL inválida. Verifique se é uma URL válida do YouTube")
            else:
                processar_video(video_url)
    
    with col2:
        st.header("📊 Estatísticas")
        
        # Placeholder para estatísticas
        if 'total_videos' not in st.session_state:
            st.session_state.total_videos = 0
        
        if 'videos_sucesso' not in st.session_state:
            st.session_state.videos_sucesso = 0
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Total de Vídeos", st.session_state.total_videos)
        with col_stat2:
            st.metric("Sucessos", st.session_state.videos_sucesso)
    
    # Área de exemplos
    st.markdown("---")
    st.header("💡 Exemplos de URLs")
    
    exemplos = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ"
    ]
    
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    with col_ex1:
        if st.button("📺 Exemplo 1", key="ex1"):
            st.session_state.example_url = exemplos[0]
    with col_ex2:
        if st.button("📺 Exemplo 2", key="ex2"):
            st.session_state.example_url = exemplos[1]
    with col_ex3:
        if st.button("📺 Exemplo 3", key="ex3"):
            st.session_state.example_url = exemplos[2]
    
    # Mostrar URL do exemplo selecionado
    if 'example_url' in st.session_state:
        st.info(f"URL do exemplo: {st.session_state.example_url}")

def processar_video(url: str):
    """Processa o vídeo e exibe o resultado"""
    try:
        # Inicializar o agente
        with st.spinner("🔄 Inicializando agente..."):
            agent = YouTubeSummarizerAgent()
        
        # Atualizar contador
        st.session_state.total_videos += 1
        
        # Processar vídeo
        with st.spinner("🔄 Processando vídeo... Isso pode levar alguns minutos."):
            resultado = agent.processar_video(url)
        
        # Mostrar resultado
        if resultado["status"] == "resumo_gerado":
            st.session_state.videos_sucesso += 1
            
            st.success("✅ Resumo gerado com sucesso!")
            
            # Mostrar informações do vídeo
            st.subheader("📹 Informações do Vídeo")
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.write(f"**URL:** {resultado['url']}")
                st.write(f"**ID do Vídeo:** {resultado['video_id']}")
            with col_info2:
                st.write(f"**Status:** {resultado['status']}")
                st.write(f"**Tamanho da Transcrição:** {len(resultado['transcript'])} caracteres")
            
            # Mostrar resumo
            st.subheader("📝 Resumo do Vídeo")
            st.markdown(resultado["resumo"])
            
            # Opções adicionais
            st.subheader("📎 Opções")
            
            col_opt1, col_opt2, col_opt3 = st.columns(3)
            with col_opt1:
                if st.button("💾 Salvar Resumo"):
                    salvar_resumo(resultado)
            with col_opt2:
                if st.button("📋 Copiar Resumo"):
                    st.code(resultado["resumo"], language="markdown")
            with col_opt3:
                if st.button("🔗 Ver Transcrição"):
                    mostrar_transcricao(resultado["transcript"])
        
        else:
            st.error(f"❌ Erro ao processar vídeo: {resultado['erro']}")
            
            # Mostrar detalhes do erro
            with st.expander("Ver detalhes do erro"):
                st.json(resultado)
    
    except Exception as e:
        st.error(f"❌ Erro inesperado: {str(e)}")
        st.exception(e)

def salvar_resumo(resultado):
    """Salva o resumo em um arquivo"""
    try:
        filename = f"resumo_{resultado['video_id']}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Resumo do Vídeo\n\n")
            f.write(f"**URL:** {resultado['url']}\n")
            f.write(f"**ID:** {resultado['video_id']}\n\n")
            f.write(resultado['resumo'])
        
        st.success(f"✅ Resumo salvo em: {filename}")
    except Exception as e:
        st.error(f"❌ Erro ao salvar: {str(e)}")

def mostrar_transcricao(transcript):
    """Mostra a transcrição completa"""
    st.subheader("📜 Transcrição Completa")
    
    # Limitar o tamanho da transcrição exibida
    if len(transcript) > 10000:
        st.warning("⚠️ Transcrição muito longa. Mostrando apenas os primeiros 10.000 caracteres.")
        transcript = transcript[:10000] + "..."
    
    st.text_area("Transcrição:", transcript, height=300)

if __name__ == "__main__":
    main() 