# 📺 YouTube Video Summarizer - Agente LangGraph

Um agente inteligente construído com **LangGraph** e **Google Gemini** para resumir vídeos do YouTube automaticamente, extraindo os principais pontos e insights.

## 🚀 Funcionalidades

- ✅ **Extração automática de transcrições** do YouTube
- ✅ **Resumo estruturado** com pontos principais
- ✅ **Insights e conclusões** utilizando IA
- ✅ **Suporte a vídeos em PT e EN**
- ✅ **Interface web amigável** com Streamlit
- ✅ **Arquitetura baseada em grafos** com LangGraph
- ✅ **Tratamento de erros robusto**
- ✅ **Salvamento de resumos em arquivos**
- ✅ **Google Generative AI** integrado diretamente
- ✅ **Modelo Gemini 2.0 Flash Lite** para melhor performance
- ✅ **uv** para gerenciamento rápido de dependências
- ✅ **Makefile** com comandos facilitados

## 🏗️ Arquitetura do Agente

O agente é construído usando **LangGraph** e segue um fluxo de processamento estruturado:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Extrair ID     │───▶│  Obter          │───▶│  Gerar Resumo   │
│  do Vídeo      │    │  Transcrição    │    │  com Gemini     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Tratamento     │    │  Tratamento     │    │    Sucesso      │
│  de Erros      │    │  de Erros      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd Youtube_transcribe
```

### 2. Instale as dependências

#### Opção 1: Usando uv (Recomendado) ⚡
```bash
# Instalação automática
python scripts/install.py

# Ou manualmente
uv sync
```

#### Opção 2: Usando pip
```bash
pip install -r requirements.txt
```

#### Opção 3: Usando Make
```bash
make install
```

### 3. Configure a API Key do Google Gemini

#### Opção 1: Arquivo .env
Crie um arquivo `.env` na raiz do projeto:
```env
GOOGLE_API_KEY=sua_chave_da_api_do_gemini_aqui
GEMINI_MODEL_NAME=gemini-2.0-flash-lite
```

#### Opção 2: Variável de ambiente
```bash
# Windows
set GOOGLE_API_KEY=sua_chave_da_api_do_gemini_aqui

# Linux/Mac
export GOOGLE_API_KEY=sua_chave_da_api_do_gemini_aqui
```

### 4. Obter API Key do Google Gemini

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Clique em "Create API Key"
3. Copie a chave gerada
4. Configure conforme instruções acima

### Instalação do uv

```bash
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ou usar o script automático
python scripts/install.py
```
## 🏃‍♂️ Como Usar

### Interface Web (Recomendado)
```bash
# Com uv
uv run streamlit run streamlit_app.py

# Com make
make run-web

# Com pip
streamlit run streamlit_app.py
```

### Linha de Comando
```bash
# Com uv
uv run python youtube_summarizer_agent.py

# Com make
make run-cli

# Com pip
python youtube_summarizer_agent.py
```

### Comandos Rápidos com Make
```bash
make help        # Ver todos os comandos
make install     # Instalar dependências
make run-web     # Interface web
make run-cli     # Linha de comando
make test        # Teste de configuração
make run-example # Executar exemplos
make clean       # Limpar arquivos temporários
make format      # Formatar código
make lint        # Verificar código
make update      # Atualizar dependências
```
### Troubleshooting - Execução

Se houver problemas com comandos uv/make, use alternativas:

```bash
# Se "make run-web" não funcionar:
python run_streamlit.py

# Se "uv run" não funcionar:
pip install -r requirements.txt
streamlit run streamlit_app.py

# Se houver erro de thread_id (já corrigido):
# O erro foi corrigido automaticamente na v2.1
```

## 🚀 Instalação Rápida

Para começar imediatamente:

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd Youtube_transcribe

# 2. Instalação automática (recomendado)
python scripts/install.py

# 3. Executar interface web
make run-web
```

## 📋 Exemplo de Uso

1. **Acesse a interface web**:
   ```bash
   # Com uv/make (recomendado)
   make run-web
   
   # Com pip
   streamlit run streamlit_app.py
   ```

2. **Cole a URL do vídeo do YouTube**:
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

3. **Clique em "Gerar Resumo"**

4. **Aguarde o processamento** (pode levar alguns minutos)

5. **Veja o resumo estruturado**:
   - 📝 Resumo Executivo
   - 🎯 Principais Pontos
   - 💡 Insights Chave
   - 📊 Dados e Estatísticas
   - 🎬 Conclusão

## 🔧 Estrutura do Projeto

```
Youtube_transcribe/
├── 📄 pyproject.toml           # Configuração do projeto (uv)
├── 📄 Makefile                 # Comandos facilitados
├── 📄 .python-version          # Versão do Python
├── 📄 requirements.txt         # Dependências (pip)
├── 📄 config.py                # Configurações e prompts
├── 📄 youtube_summarizer_agent.py # Agente principal LangGraph
├── 📄 streamlit_app.py         # Interface web
├── 📄 exemplo_uso.py           # Exemplos de uso
├── 📄 teste_configuracao.py    # Teste da configuração
├── 📄 env_example.txt          # Exemplo de configuração
├── 📄 README.md               # Documentação
└── 📄 .env                    # Variáveis de ambiente (criar)
```

## 🤖 Como Funciona o Agente

### 1. **Extração do ID do Vídeo**
- Valida a URL fornecida
- Extrai o ID do vídeo usando regex
- Suporta diferentes formatos de URL do YouTube

### 2. **Obtenção da Transcrição**
- Usa `youtube-transcript-api` para extrair legendas
- Suporta vídeos em português e inglês
- Combina todas as partes da transcrição

### 3. **Geração do Resumo**
- Utiliza o Google Gemini (2.0-flash-lite) para análise
- Aplica prompt estruturado para resumos consistentes
- Limita tamanho da transcrição para otimizar processamento

### 4. **Tratamento de Erros**
- Gerencia erros em cada etapa do processo
- Fornece mensagens de erro claras
- Permite debugging com informações detalhadas

## 📊 Exemplo de Resumo Gerado

```markdown
## 📝 RESUMO EXECUTIVO
O vídeo apresenta uma análise abrangente sobre...

## 🎯 PRINCIPAIS PONTOS
1. Primeiro ponto importante identificado
2. Segunda observação relevante
3. Terceiro insight significativo
...

## 💡 INSIGHTS CHAVE
- Conceito fundamental explicado
- Estratégia recomendada
- Implicações futuras

## 📊 DADOS E ESTATÍSTICAS
- 85% de melhoria em performance
- 3x aumento na eficiência
- Redução de 40% nos custos

## 🎬 CONCLUSÃO
A principal conclusão é que...
```

## 🔧 Troubleshooting

### Erro: "API Key não encontrada"
```bash
# Verifique se a variável está definida
echo $GOOGLE_API_KEY  # Linux/Mac
echo %GOOGLE_API_KEY%  # Windows

# Ou execute o teste de configuração
python teste_configuracao.py
```

### Erro: "Transcrição não disponível"
- Vídeo pode não ter legendas automáticas
- Tente com vídeos que possuem legendas em PT/EN

### Erro: "URL inválida"
- Verifique se a URL está completa
- Formatos suportados:
  - `https://www.youtube.com/watch?v=ID`
  - `https://youtu.be/ID`
  - `https://www.youtube.com/embed/ID`

### Erro: "Modelo não encontrado"
- Verifique se o modelo `gemini-2.0-flash-lite` está disponível
- Ou ajuste o `GEMINI_MODEL_NAME` no arquivo `.env`

## 👨‍💻 Desenvolvimento

### Configuração do Ambiente de Desenvolvimento
```bash
# Instalar dependências de desenvolvimento
make dev-install

# Ou com uv
uv sync --dev
```

### Ferramentas de Desenvolvimento
- **Black**: Formatação automática de código
- **isort**: Organização de imports
- **flake8**: Análise de código
- **mypy**: Verificação de tipos
- **pytest**: Testes automatizados

### Comandos de Desenvolvimento
```bash
make format      # Formatar código
make lint        # Verificar código
make check       # Formatação + verificação
make test        # Executar testes
make clean       # Limpar arquivos temporários
```

### Estrutura de Comandos
```bash
# Instalação e configuração
make install     # Instalar dependências
make setup       # Configuração completa

# Execução
make run-web     # Interface web
make run-cli     # Linha de comando
make run-example # Exemplos

# Desenvolvimento
make dev-install # Dependências de desenvolvimento
make format      # Formatar código
make lint        # Verificar código
make test        # Executar testes

# Utilitários
make info        # Informações do projeto
make backup      # Backup do projeto
make update      # Atualizar dependências
```

## 📈 Melhorias Futuras

- [ ] Suporte a mais idiomas
- [ ] Integração com outras plataformas de vídeo
- [ ] Análise de sentimentos
- [ ] Geração de tags automáticas
- [ ] Exportação em PDF/Word
- [ ] API REST para integração
- [ ] Testes automatizados
- [ ] CI/CD pipeline

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

**Desenvolvido com ❤️ usando LangGraph e Google Gemini** 