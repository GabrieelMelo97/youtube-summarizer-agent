# YouTube Summarizer Agent - Makefile
# Comandos para facilitar o desenvolvimento e uso

.PHONY: help install run-web run-cli run-example test clean dev-install lint format check

# Comando padrão
help:
	@echo "🎬 YouTube Summarizer Agent - Comandos Disponíveis"
	@echo "=================================================="
	@echo ""
	@echo "📦 Instalação:"
	@echo "  make install     - Instalar dependências com uv"
	@echo "  make dev-install - Instalar dependências de desenvolvimento"
	@echo ""
	@echo "🚀 Execução:"
	@echo "  make run-web     - Executar interface web"
	@echo "  make run-cli     - Executar linha de comando"
	@echo "  make run-example - Executar exemplos"
	@echo "  make test        - Executar testes de configuração"
	@echo ""
	@echo "🔧 Desenvolvimento:"
	@echo "  make lint        - Executar linting"
	@echo "  make format      - Formatar código"
	@echo "  make check       - Verificar código"
	@echo "  make clean       - Limpar arquivos temporários"
	@echo ""
	@echo "📚 Documentação:"
	@echo "  make docs        - Gerar documentação"
	@echo ""

# Instalação
install:
	@echo "📦 Instalando dependências com uv..."
	uv sync

dev-install:
	@echo "📦 Instalando dependências de desenvolvimento..."
	uv sync --dev

# Execução
run-web:
	@echo "🌐 Iniciando interface web..."
	uv run streamlit run streamlit_app.py

run-cli:
	@echo "💻 Iniciando linha de comando..."
	uv run python youtube_summarizer_agent.py

run-example:
	@echo "📚 Executando exemplos..."
	uv run python exemplo_uso.py

test:
	@echo "🧪 Executando teste de configuração..."
	uv run python teste_configuracao.py

# Desenvolvimento
lint:
	@echo "🔍 Executando linting..."
	uv run flake8 .
	uv run mypy .

format:
	@echo "🎨 Formatando código..."
	uv run black .
	uv run isort .

check: format lint
	@echo "✅ Verificação completa do código"

# Limpeza
clean:
	@echo "🧹 Limpando arquivos temporários..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".mypy_cache" -delete
	find . -type f -name "*.egg-info" -delete
	rm -rf dist/
	rm -rf build/
	@echo "✅ Limpeza concluída"

# Documentação
docs:
	@echo "📚 Gerando documentação..."
	@echo "Documentação disponível em README.md"

# Instalação rápida
quick-install:
	@echo "⚡ Instalação rápida..."
	python scripts/install.py

# Verificação de dependências
check-deps:
	@echo "🔍 Verificando dependências..."
	uv run python -c "import google.generativeai, youtube_transcript_api, langgraph, streamlit, validators; print('✅ Todas as dependências OK!')"

# Atualizar dependências
update:
	@echo "🔄 Atualizando dependências..."
	uv sync --upgrade

# Informações do projeto
info:
	@echo "ℹ️ Informações do projeto:"
	@echo "  Nome: YouTube Summarizer Agent"
	@echo "  Versão: 2.0.0"
	@echo "  Python: $(shell python --version)"
	@echo "  uv: $(shell uv --version 2>/dev/null || echo 'não instalado')"
	@echo "  Diretório: $(shell pwd)"

# Backup do projeto
backup:
	@echo "💾 Criando backup do projeto..."
	tar -czf youtube-summarizer-backup-$(shell date +%Y%m%d-%H%M%S).tar.gz \
		--exclude='.git' \
		--exclude='__pycache__' \
		--exclude='*.pyc' \
		--exclude='.uv' \
		--exclude='dist' \
		--exclude='build' \
		.
	@echo "✅ Backup criado"

# Comandos para usuários iniciantes
start: install run-web
	@echo "🎉 Projeto iniciado!"

setup:
	@echo "🔧 Configurando projeto..."
	python scripts/install.py 