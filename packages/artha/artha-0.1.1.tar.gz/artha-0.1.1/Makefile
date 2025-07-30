.PHONY: setup

setup:
	@if ! command -v uv > /dev/null 2>&1; then \
		echo "Installing uv package manager..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@echo "Setting up virtual environment..."
	uv venv
	uv sync

upload_to_pypi:
	@echo "Building package..."
	uv sync
	uv build
	
	@echo "Uploading package to PyPI... "
	uv run -- twine upload dist/*

	@echo "Cleaning up..."
	rm -rf dist
	rm -rf build
	rm -rf artha.egg-info
