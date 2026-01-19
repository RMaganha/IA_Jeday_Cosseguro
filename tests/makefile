.PHONY: help test test-unit test-integration test-cov lint format clean install run

help:  ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Instala as dependências
	pip install -r requirements.txt
	pip install pytest pytest-cov pytest-mock black flake8 mypy

test:  ## Executa todos os testes
	pytest tests/ -v

test-unit:  ## Executa apenas testes unitários
	pytest tests/ -v -m unit

test-integration:  ## Executa testes de integração (requer API configurada)
	RUN_INTEGRATION_TESTS=true pytest tests/ -v -m integration

test-cov:  ## Executa testes com cobertura de código
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing

test-watch:  ## Executa testes em modo watch (re-executa ao salvar)
	pytest-watch tests/ -v

lint:  ## Verifica qualidade do código
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics

format:  ## Formata o código com black
	black . --line-length=100

type-check:  ## Verifica tipos com mypy
	mypy . --ignore-missing-imports

clean:  ## Remove arquivos temporários
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache

run:  ## Executa a aplicação
	streamlit run app.py

run-dev:  ## Executa em modo desenvolvimento (com reload automático)
	streamlit run app.py --server.runOnSave true

check:  ## Executa todas as verificações (lint + type-check + test)
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) test

setup:  ## Configuração inicial do projeto
	@echo "Configurando projeto..."
	cp .env.example .env
	@echo "Edite o arquivo .env com suas credenciais"
	$(MAKE) install
	@echo "Setup completo! Execute 'make run' para iniciar"