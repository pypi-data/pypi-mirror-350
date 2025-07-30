.PHONY: setup

setup:
	@if ! command -v uv > /dev/null 2>&1; then \
		echo "Installing uv package manager..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@echo "Setting up virtual environment..."
	uv venv
	uv sync
