import re
from typing import TypedDict, List, Optional
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import validators
from config import GOOGLE_API_KEY, GEMINI_MODEL_NAME, RESUMO_PROMPT


class VideoState(TypedDict):
    url: str
    video_id: str
    transcript: str
    resumo: str
    erro: Optional[str]
    status: str


class YouTubeSummarizerAgent:
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        self.memory = MemorySaver()
        self.graph = self._create_graph()
    
    def _create_graph(self) -> StateGraph:
        """Cria o grafo do agente LangGraph"""
        workflow = StateGraph(VideoState)
        
        # Adicionar nós
        workflow.add_node("extrair_video_id", self._extrair_video_id)
        workflow.add_node("obter_transcricao", self._obter_transcricao)
        workflow.add_node("gerar_resumo", self._gerar_resumo)
        workflow.add_node("erro", self._lidar_com_erro)
        
        # Definir fluxo
        workflow.set_entry_point("extrair_video_id")
        
        # Condicionais
        workflow.add_conditional_edges(
            "extrair_video_id",
            self._decidir_proximo_passo,
            {
                "transcricao": "obter_transcricao",
                "erro": "erro"
            }
        )
        
        workflow.add_conditional_edges(
            "obter_transcricao",
            self._decidir_proximo_passo,
            {
                "resumo": "gerar_resumo",
                "erro": "erro"
            }
        )
        
        workflow.add_edge("gerar_resumo", END)
        workflow.add_edge("erro", END)
        
        return workflow.compile(checkpointer=self.memory)
    
    def _extrair_video_id(self, state: VideoState) -> VideoState:
        """Extrai o ID do vídeo da URL do YouTube"""
        try:
            url = state["url"]
            
            # Validar se é uma URL válida
            if not validators.url(url):
                return {
                    **state,
                    "erro": "URL inválida fornecida",
                    "status": "erro"
                }
            
            # Extrair ID do vídeo
            video_id = self._extrair_id_youtube(url)
            
            if not video_id:
                return {
                    **state,
                    "erro": "Não foi possível extrair o ID do vídeo. Verifique se é uma URL válida do YouTube.",
                    "status": "erro"
                }
            
            return {
                **state,
                "video_id": video_id,
                "status": "id_extraido"
            }
        
        except Exception as e:
            return {
                **state,
                "erro": f"Erro ao extrair ID do vídeo: {str(e)}",
                "status": "erro"
            }
    
    def _extrair_id_youtube(self, url: str) -> Optional[str]:
        """Extrai ID do vídeo de diferentes formatos de URL do YouTube"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _obter_transcricao(self, state: VideoState) -> VideoState:
        """Obtém a transcrição do vídeo do YouTube"""
        try:
            video_id = state["video_id"]
            
            # Tentar obter transcrição
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
            
            # Combinar todas as partes da transcrição
            transcript_text = " ".join([entry['text'] for entry in transcript_list])
            
            return {
                **state,
                "transcript": transcript_text,
                "status": "transcricao_obtida"
            }
        
        except Exception as e:
            return {
                **state,
                "erro": f"Erro ao obter transcrição: {str(e)}. O vídeo pode não ter legendas disponíveis.",
                "status": "erro"
            }
    
    def _gerar_resumo(self, state: VideoState) -> VideoState:
        """Gera resumo usando o Gemini"""
        try:
            transcript = state["transcript"]
            
            # Limitar tamanho da transcrição se muito longa
            if len(transcript) > 50000:
                transcript = transcript[:50000] + "..."
            
            # Criar prompt personalizado
            prompt = RESUMO_PROMPT.format(transcript=transcript)
            
            # Gerar resumo
            response = self.model.generate_content(prompt)
            
            return {
                **state,
                "resumo": response.text,
                "status": "resumo_gerado"
            }
        
        except Exception as e:
            return {
                **state,
                "erro": f"Erro ao gerar resumo: {str(e)}",
                "status": "erro"
            }
    
    def _lidar_com_erro(self, state: VideoState) -> VideoState:
        """Lida com erros no processo"""
        return {
            **state,
            "status": "erro_processado"
        }
    
    def _decidir_proximo_passo(self, state: VideoState) -> str:
        """Decide qual o próximo passo baseado no status atual"""
        status = state.get("status", "")
        
        if status == "erro":
            return "erro"
        elif status == "id_extraido":
            return "transcricao"
        elif status == "transcricao_obtida":
            return "resumo"
        else:
            return "erro"
    
    def processar_video(self, url: str) -> VideoState:
        """Processa um vídeo do YouTube e retorna o resumo"""
        initial_state = VideoState(
            url=url,
            video_id="",
            transcript="",
            resumo="",
            erro=None,
            status="inicial"
        )
        
        # Configuração para o checkpointer
        config = {"configurable": {"thread_id": f"video_{hash(url)}"}}
        
        # Executar o grafo
        result = self.graph.invoke(initial_state, config=config)
        return result


def main():
    """Função principal para teste"""
    agent = YouTubeSummarizerAgent()
    
    # Exemplo de uso
    url = input("Digite a URL do vídeo do YouTube: ")
    
    print("🔄 Processando vídeo...")
    resultado = agent.processar_video(url)
    
    if resultado["status"] == "resumo_gerado":
        print("✅ Resumo gerado com sucesso!")
        print("\n" + "="*50)
        print(resultado["resumo"])
        print("="*50)
    else:
        print("❌ Erro ao processar vídeo:")
        print(resultado["erro"])


if __name__ == "__main__":
    main() 