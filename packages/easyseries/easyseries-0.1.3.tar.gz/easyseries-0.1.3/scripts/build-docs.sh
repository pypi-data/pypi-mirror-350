#!/bin/bash

# Documentation build script

set -e

echo "📚 Building EasySeries documentation..."

# Install documentation dependencies
echo "📦 Installing documentation dependencies..."
uv sync --extra docs

# Build documentation
echo "🔨 Building HTML documentation..."
cd docs
uv run sphinx-build -b html source _build/html

# Open documentation if on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    open _build/html/index.html
else
    echo "✅ Documentation built successfully!"
    echo "📖 Open docs/_build/html/index.html in your browser"
fi

cd ..
