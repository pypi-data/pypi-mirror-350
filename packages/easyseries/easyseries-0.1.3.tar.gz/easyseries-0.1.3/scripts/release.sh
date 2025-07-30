#!/bin/bash

# Release script for EasySeries

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're on main branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    print_error "Must be on main branch to release. Current branch: $current_branch"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    print_error "There are uncommitted changes. Please commit or stash them."
    exit 1
fi

# Get version from user
echo "Current version: $(grep '__version__' src/easyseries/__init__.py | cut -d'"' -f2)"
read -p "Enter new version (e.g., 1.0.0): " new_version

if [ -z "$new_version" ]; then
    print_error "Version cannot be empty"
    exit 1
fi

# Validate version format (basic check)
if ! [[ $new_version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    print_error "Version must be in format X.Y.Z"
    exit 1
fi

print_status "Preparing release v$new_version"

# Update version in __init__.py
sed -i.bak "s/__version__ = \".*\"/__version__ = \"$new_version\"/" src/easyseries/__init__.py
rm src/easyseries/__init__.py.bak

# Run tests
print_status "Running tests..."
uv run pytest

# Run quality checks
print_status "Running quality checks..."
uv run pre-commit run --all-files

# Build package
print_status "Building package..."
uv build

# Check package
print_status "Checking package..."
uv run twine check dist/*

# Commit version change
git add src/easyseries/__init__.py
git commit -m "Bump version to $new_version"

# Create and push tag
git tag "v$new_version"
git push origin main
git push origin "v$new_version"

print_status "Release v$new_version completed!"
print_status "GitHub Actions will automatically publish to PyPI"
print_status "Monitor the release at: https://github.com/ScienisTmiaoT/easyseries/actions"
