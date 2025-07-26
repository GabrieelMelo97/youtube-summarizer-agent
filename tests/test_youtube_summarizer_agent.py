import pytest
from unittest.mock import patch, MagicMock
from youtube_summarizer_agent import YouTubeSummarizerAgent, VideoState

# Exemplo de URL válida e inválida
youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
invalid_url = "not_a_url"

@pytest.fixture
def agent():
    return YouTubeSummarizerAgent()

def test_extrair_video_id_valido(agent):
    state = VideoState(url=youtube_url, video_id="", transcript="", resumo="", erro=None, status="inicial")
    result = agent._extrair_video_id(state)
    assert result["video_id"] == "dQw4w9WgXcQ"
    assert result["status"] == "id_extraido"
    assert result["erro"] is None

def test_extrair_video_id_invalido(agent):
    state = VideoState(url=invalid_url, video_id="", transcript="", resumo="", erro=None, status="inicial")
    result = agent._extrair_video_id(state)
    assert result["status"] == "erro"
    assert "URL inválida" in result["erro"]

@patch("youtube_summarizer_agent.YouTubeTranscriptApi.get_transcript")
def test_obter_transcricao_sucesso(mock_get_transcript, agent):
    mock_get_transcript.return_value = [{"text": "Olá mundo"}]
    state = VideoState(url=youtube_url, video_id="dQw4w9WgXcQ", transcript="", resumo="", erro=None, status="id_extraido")
    result = agent._obter_transcricao(state)
    assert result["transcript"] == "Olá mundo"
    assert result["status"] == "transcricao_obtida"
    assert result["erro"] is None

@patch("youtube_summarizer_agent.YouTubeTranscriptApi.get_transcript", side_effect=Exception("Sem legenda"))
def test_obter_transcricao_erro(mock_get_transcript, agent):
    state = VideoState(url=youtube_url, video_id="dQw4w9WgXcQ", transcript="", resumo="", erro=None, status="id_extraido")
    result = agent._obter_transcricao(state)
    assert result["status"] == "erro"
    assert "Erro ao obter transcrição" in result["erro"]

@patch("youtube_summarizer_agent.genai.GenerativeModel")
def test_gerar_resumo_sucesso(mock_model, agent):
    mock_instance = MagicMock()
    mock_instance.generate_content.return_value.text = "Resumo gerado"
    mock_model.return_value = mock_instance
    state = VideoState(url=youtube_url, video_id="dQw4w9WgXcQ", transcript="Texto da transcrição", resumo="", erro=None, status="transcricao_obtida")
    result = agent._gerar_resumo(state)
    assert result["resumo"] == "Resumo gerado"
    assert result["status"] == "resumo_gerado"
    assert result["erro"] is None

@patch("youtube_summarizer_agent.genai.GenerativeModel", side_effect=Exception("Erro Gemini"))
def test_gerar_resumo_erro(mock_model, agent):
    state = VideoState(url=youtube_url, video_id="dQw4w9WgXcQ", transcript="Texto da transcrição", resumo="", erro=None, status="transcricao_obtida")
    result = agent._gerar_resumo(state)
    assert result["status"] == "erro"
    assert "Erro ao gerar resumo" in result["erro"]

def test_lidar_com_erro(agent):
    state = VideoState(url=youtube_url, video_id="", transcript="", resumo="", erro="algum erro", status="erro")
    result = agent._lidar_com_erro(state)
    assert result["status"] == "erro_processado"

def test_decidir_proximo_passo(agent):
    state = VideoState(url=youtube_url, video_id="", transcript="", resumo="", erro=None, status="erro")
    assert agent._decidir_proximo_passo(state) == "erro"
    state["status"] = "id_extraido"
    assert agent._decidir_proximo_passo(state) == "transcricao"
    state["status"] = "transcricao_obtida"
    assert agent._decidir_proximo_passo(state) == "resumo"
    state["status"] = "outro"
    assert agent._decidir_proximo_passo(state) == "erro" 