#!/bin/bash

# SaasToMCP Setup Script
# This script sets up a Python virtual environment and installs dependencies

set -e

echo "🚀 Setting up SaasToMCP..."

# Check if Python 3.10+ is available
python_cmd=""
for cmd in python3.12 python3.11 python3.10 python3; do
    if command -v "$cmd" &> /dev/null; then
        version=$($cmd -V 2>&1 | grep -Po '(?<=Python )\d+\.\d+' || echo "0.0")
        if [ "$(echo "$version >= 3.10" | bc 2>/dev/null || echo 0)" -eq 1 ] 2>/dev/null; then
            python_cmd="$cmd"
            break
        fi
    fi
done

if [ -z "$python_cmd" ]; then
    echo "❌ Python 3.10 or higher is required"
    echo "Please install Python 3.10+ and try again"
    exit 1
fi

echo "✅ Found Python: $python_cmd"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $python_cmd -m venv venv
else
    echo "📦 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install package in development mode
echo "📦 Installing SaasToMCP in development mode..."
pip install -e .

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use SaasToMCP:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the server: python main.py"
echo "  3. Or use the CLI: saas-to-mcp run"
echo "  4. Or test it: python test_saas_to_mcp.py"
echo ""
echo "For more options: saas-to-mcp --help"
