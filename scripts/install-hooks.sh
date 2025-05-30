#!/bin/bash
# Install OpenCraftShop Git Hooks

echo "Installing OpenCraftShop Git Hooks..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository"
    echo "Please run this from the OpenCraftShop root directory"
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy pre-commit hook
if [ -f ".githooks/pre-commit" ]; then
    cp .githooks/pre-commit .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    echo "✓ Pre-commit hook installed"
else
    echo "Error: .githooks/pre-commit not found"
    exit 1
fi

# Copy prepare-commit-msg hook
if [ -f ".githooks/prepare-commit-msg" ]; then
    cp .githooks/prepare-commit-msg .git/hooks/prepare-commit-msg
    chmod +x .git/hooks/prepare-commit-msg
    echo "✓ Prepare-commit-msg hook installed"
else
    echo "Error: .githooks/prepare-commit-msg not found"
    exit 1
fi

echo ""
echo "Git hooks installed successfully!"
echo ""
echo "The hooks will:"
echo "  - Validate Python syntax before commit"
echo "  - Validate JSON configuration files"
echo "  - Add validation results to your commit message"
echo "  - Include code statistics in the commit"
echo ""
echo "To skip hooks temporarily, use: git commit --no-verify"