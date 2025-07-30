# https://stackoverflow.com/a/2145605
.PHONY: setup upload_to_pypi build_frontend

# This takes care of setting up the project for the first time
setup:
	@if ! command -v uv > /dev/null 2>&1; then \
		echo "Installing uv package manager..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi

	@echo "Setting up virtual environment..."
	uv venv
	uv sync

# This upload the package to PyPI. This can only be run by me.
upload_to_pypi:
	@echo "Building package..."
	uv sync
	uv build
	
	@echo "Uploading package to PyPI... "
	uv run -- twine upload dist/*

	@echo "Cleaning up..."
	rm -rf dist

# This commands builds the frontend and move it to the static folder in the backend
build_frontend:
	cd frontend && npm run build
	rm -rf artha/ui
	mkdir artha/ui
	cp -r frontend/dist/* artha/ui/
