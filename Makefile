.PHONY: setup test clean

VENV ?= .venv
PYTHON ?= $(shell which $(VENV)/bin/python3 2>/dev/null || which python3 2>/dev/null)

# Prepara o clone: ativa o hook que impede assinatura de coautoria de IA nos commits
setup:
	@git config core.hooksPath .githooks
	@echo "core.hooksPath = $$(git config --get core.hooksPath)"
	@echo "Hook de autoria ativo. Regras do repositorio: AGENTS.md"

# Executa testes de regressao e suite automatizada
test:
	$(PYTHON) -m unittest discover -s tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
