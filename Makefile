.PHONY: help build run test clean demo install-local lint format check-deps test-unit coverage dev-setup

# OpenCraftShop Makefile
# Programmatic Woodworking & 3D Model Designer

.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Default target
help:
	@echo "$(BLUE)OpenCraftShop - Development Commands$(NC)"
	@echo "===================================="
	@echo "$(GREEN)Quick Start:$(NC)"
	@echo "  make dev-setup     - Set up development environment"
	@echo "  make test          - Run all tests"
	@echo "  make run           - Run with default parameters"
	@echo ""
	@echo "$(GREEN)Docker Commands:$(NC)"
	@echo "  make build         - Build the Docker image"
	@echo "  make dev           - Development mode with live reload"
	@echo "  make demo          - Run demo with all furniture types"
	@echo ""
	@echo "$(GREEN)Furniture Types:$(NC)"
	@echo "  make workbench     - Generate workbench design"
	@echo "  make storage-bench - Generate storage bench design"
	@echo "  make bed           - Generate bed frame design"
	@echo "  make bookshelf     - Generate bookshelf design"
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@echo "  make test-unit     - Run unit tests with pytest"
	@echo "  make test-integration - Run integration tests"
	@echo "  make coverage      - Run tests with coverage report"
	@echo "  make test-quick    - Quick smoke test"
	@echo ""
	@echo "$(GREEN)Code Quality:$(NC)"
	@echo "  make lint          - Run linting (ruff)"
	@echo "  make format        - Format code (black)"
	@echo "  make typecheck     - Run type checking (mypy)"
	@echo "  make quality       - Run all quality checks"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make install-hooks - Install git pre-commit hooks"
	@echo "  make clean         - Clean all generated files"
	@echo "  make docs          - Generate documentation"
	@echo ""
	@echo "$(GREEN)Web UI:$(NC)"
	@echo "  make web           - Start web interface (http://localhost:5000)"
	@echo "  make web-stop      - Stop web interface"
	@echo "  make web-logs      - View web interface logs"

# Build Docker image
build:
	docker-compose build

# Run with default parameters
run: build
	docker-compose run --rm opencraftshop

# Run with custom parameters
run-custom: build
	docker-compose run --rm opencraftshop \
		--length $(LENGTH) \
		--width $(WIDTH) \
		--height $(HEIGHT)

# Demo various furniture types
demo: build clean
	@echo "=== WORKBENCH DEMO ==="
	docker-compose run --rm opencraftshop --type workbench --length 72 --width 24 --height 34
	@echo "\n\n=== STORAGE BENCH DEMO ==="
	docker-compose run --rm opencraftshop --type storage_bench
	@echo "\n\n=== BED FRAME DEMO ==="
	docker-compose run --rm opencraftshop --type bed_frame
	@echo "\n\n=== BOOKSHELF DEMO ==="
	docker-compose run --rm opencraftshop --type bookshelf

# Install git hooks
install-hooks:
	@./scripts/install-hooks.sh

# Run all tests
test: build
	@echo "Running OpenCraftShop Test Suite..."
	@./tests/run_all_tests.sh

# Run dimension tests
test-dimensions: build
	@echo "Running dimension tests..."
	@python3 tests/test_dimensions.py

# Test run without Docker (requires local installation)
test-local:
	cd src && python3 main.py --length 60 --width 24 --height 34 --output-dir ../output

# Quick test with minimal output
quick-test: build
	docker-compose run --rm opencraftshop --no-visualize

# Development setup - install everything needed for local development
dev-setup:
	@echo "$(BLUE)Setting up development environment...$(NC)"
	@python3 -m venv venv || (echo "$(RED)Failed to create virtual environment$(NC)" && exit 1)
	@echo "$(GREEN)✓ Virtual environment created$(NC)"
	@. venv/bin/activate && pip install -e . -r requirements-dev.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"
	@./scripts/install-hooks.sh
	@echo "$(GREEN)✓ Git hooks installed$(NC)"
	@echo ""
	@echo "$(YELLOW)To activate the environment:$(NC)"
	@echo "  source venv/bin/activate"
	@echo ""
	@echo "$(GREEN)Development setup complete!$(NC)"

# Install dependencies locally for development
install-local:
	pip3 install -e . -r requirements-dev.txt

# Unit tests with pytest
test-unit:
	@echo "$(BLUE)Running unit tests...$(NC)"
	@if [ -f venv/bin/pytest ]; then \
		venv/bin/pytest tests/unit/ -v; \
	else \
		pytest tests/unit/ -v || echo "$(RED)Install pytest: pip install pytest$(NC)"; \
	fi

# Integration tests
test-integration: build
	@echo "$(BLUE)Running integration tests...$(NC)"
	@./tests/run_tests.sh

# Run tests with coverage
coverage:
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	@if [ -f venv/bin/pytest ]; then \
		venv/bin/pytest --cov=src --cov-report=html --cov-report=term tests/; \
	else \
		pytest --cov=src --cov-report=html --cov-report=term tests/ || echo "$(RED)Install pytest-cov: pip install pytest-cov$(NC)"; \
	fi
	@echo "$(GREEN)Coverage report generated in htmlcov/$(NC)"

# Quick smoke test
test-quick: build
	@echo "$(BLUE)Running quick smoke test...$(NC)"
	docker-compose run --rm opencraftshop --type workbench --no-visualize
	@test -f output/workbench.scad && echo "$(GREEN)✓ OpenSCAD file generated$(NC)" || echo "$(RED)✗ OpenSCAD file missing$(NC)"
	@test -f output/cut_list.txt && echo "$(GREEN)✓ Cut list generated$(NC)" || echo "$(RED)✗ Cut list missing$(NC)"

# Lint Python code
lint:
	@echo "$(BLUE)Running linter...$(NC)"
	@if [ -f venv/bin/ruff ]; then \
		venv/bin/ruff check src/; \
	elif command -v ruff >/dev/null 2>&1; then \
		ruff check src/; \
	else \
		echo "$(YELLOW)ruff not installed, trying flake8...$(NC)"; \
		if command -v flake8 >/dev/null 2>&1; then \
			flake8 src/ --max-line-length=88; \
		else \
			echo "$(RED)No linter found. Install ruff: pip install ruff$(NC)"; \
		fi \
	fi

# Format Python code
format:
	@echo "$(BLUE)Formatting code...$(NC)"
	@if [ -f venv/bin/black ]; then \
		venv/bin/black src/ tests/; \
	elif command -v black >/dev/null 2>&1; then \
		black src/ tests/; \
	else \
		echo "$(RED)black not installed. Run: pip install black$(NC)"; \
	fi

# Type checking
typecheck:
	@echo "$(BLUE)Running type checker...$(NC)"
	@if [ -f venv/bin/mypy ]; then \
		venv/bin/mypy src/; \
	elif command -v mypy >/dev/null 2>&1; then \
		mypy src/; \
	else \
		echo "$(RED)mypy not installed. Run: pip install mypy$(NC)"; \
	fi

# Run all quality checks
quality: lint typecheck
	@echo "$(GREEN)All quality checks complete!$(NC)"

# Check dependencies
check-deps:
	@echo "Checking system dependencies..."
	@command -v docker >/dev/null 2>&1 && echo "✓ Docker installed" || echo "✗ Docker not found"
	@command -v docker-compose >/dev/null 2>&1 && echo "✓ docker-compose installed" || echo "✗ docker-compose not found"
	@command -v python3 >/dev/null 2>&1 && echo "✓ Python 3 installed" || echo "✗ Python 3 not found"
	@command -v openscad >/dev/null 2>&1 && echo "✓ OpenSCAD installed (local)" || echo "✗ OpenSCAD not found (local)"

# Clean output directory
clean:
	@echo "$(BLUE)Cleaning up...$(NC)"
	@rm -rf output/* htmlcov/ .coverage .pytest_cache .mypy_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Cleaned output files and caches$(NC)"

# Generate documentation
docs:
	@echo "$(BLUE)Generating documentation...$(NC)"
	@if [ -f venv/bin/sphinx-build ]; then \
		venv/bin/sphinx-build -b html docs docs/_build; \
		echo "$(GREEN)Documentation generated in docs/_build/$(NC)"; \
	else \
		echo "$(YELLOW)Sphinx not installed. Documentation available in docs/$(NC)"; \
	fi

# Validate outputs exist and are reasonable
validate: run
	@echo "\nValidating outputs..."
	@test -f output/workbench.stl && echo "✓ STL file generated" || echo "✗ STL file missing"
	@test -f output/cut_list.txt && echo "✓ Cut list generated" || echo "✗ Cut list missing"
	@test -f output/shopping_list.txt && echo "✓ Shopping list generated" || echo "✗ Shopping list missing"
	@test -f output/bill_of_materials.txt && echo "✓ BOM generated" || echo "✗ BOM missing"
	@echo "\nOutput summary:"
	@ls -la output/

# Development mode - mount src directory for live changes
dev:
	docker run -it --rm \
		-v $(PWD)/src:/app/src \
		-v $(PWD)/output:/app/output \
		-v $(PWD)/config:/app/config \
		--entrypoint /bin/bash \
		opencraftshop

# Run specific dimensions from command line
# Usage: make custom LENGTH=60 WIDTH=20 HEIGHT=32
custom: build
	docker-compose run --rm opencraftshop \
		--length $(or $(LENGTH),72) \
		--width $(or $(WIDTH),24) \
		--height $(or $(HEIGHT),34)

# Generate cut diagram only
cuts-only: build
	docker-compose run --rm opencraftshop --no-visualize
	@cat output/cut_list.txt

# Show shopping list only
shop-only: build
	docker-compose run --rm opencraftshop --no-visualize
	@cat output/shopping_list.txt

# Furniture-specific targets
workbench: build
	docker-compose run --rm opencraftshop --type workbench

storage-bench: build
	docker-compose run --rm opencraftshop --type storage_bench

bed: build
	docker-compose run --rm opencraftshop --type bed_frame

bookshelf: build
	docker-compose run --rm opencraftshop --type bookshelf

# List available furniture types
list-types:
	@echo "Available furniture types:"
	@echo "  - workbench (default)"
	@echo "  - storage_bench"
	@echo "  - bed_frame"
	@echo "  - bookshelf"
	@echo ""
	@echo "Usage: make <type> or docker-compose run opencraftshop --type <type>"

# Web UI targets
web: build
	@echo "$(BLUE)Starting OpenCraftShop Web UI...$(NC)"
	@docker-compose up -d web
	@echo "$(GREEN)✓ Web UI is running at http://localhost:5000$(NC)"
	@echo "$(YELLOW)To stop: make web-stop$(NC)"

web-stop:
	@echo "$(BLUE)Stopping Web UI...$(NC)"
	@docker-compose stop web
	@echo "$(GREEN)✓ Web UI stopped$(NC)"

web-logs:
	@echo "$(BLUE)Web UI logs (Ctrl+C to exit):$(NC)"
	@docker-compose logs -f web

web-restart: web-stop web
	@echo "$(GREEN)✓ Web UI restarted$(NC)"

# API tests
test-api: web
	@echo "$(BLUE)Running API tests...$(NC)"
	@docker-compose run --rm --entrypoint python3 opencraftshop /app/tests/test_api.py

# 3D model tests
test-models: build
	@echo "$(BLUE)Running 3D model tests...$(NC)"
	@docker-compose run --rm --entrypoint python3 opencraftshop /app/tests/test_3d_models.py

# Run all tests including web UI
test-all: test-api test-models test-unit
	@echo "$(GREEN)All tests complete!$(NC)"