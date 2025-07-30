## scripts/setup-dev.sh

#!/bin/bash

# Development environment setup script

set -e

echo "🚀 Setting up EasySeries development environment..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install all dependencies
echo "📦 Installing dependencies..."
uv sync --all-extras --dev

# Install pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
uv run pre-commit install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "   Please edit .env file with your configuration"
fi

# Run initial tests
echo "🧪 Running initial tests..."
uv run pytest --tb=short

echo "✅ Development environment setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env file with your configuration"
echo "  2. Run 'uv run pytest' to run tests"
echo "  3. Run 'easyseries --help' to see CLI options"
echo "  4. Check 'uv run pre-commit run --all-files' before committing"
