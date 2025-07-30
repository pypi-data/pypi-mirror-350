#!/bin/bash
# Installation script for the DevOps MCP Server

echo "DevOps MCP Server Installation"
echo "============================="
echo

# Check if Python 3.12+ is installed
python_version=$(python --version 2>&1 | awk '{print $2}')
python_major=$(echo $python_version | cut -d. -f1)
python_minor=$(echo $python_version | cut -d. -f2)

if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 12 ]); then
    echo "Error: Python 3.12 or higher is required."
    echo "Current version: $python_version"
    echo "Please install Python 3.12+ and try again."
    exit 1
fi

echo "Python version $python_version detected."
echo

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed."
    echo "Please install uv and try again."
    echo "You can install uv with: pip install uv"
    exit 1
fi

echo "uv detected."
echo

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "Virtual environment activated."
echo

# Install dependencies
echo "Installing dependencies..."
uv pip install -e .
echo "Dependencies installed."
echo

# Make scripts executable
echo "Making scripts executable..."
chmod +x main.py
echo "Scripts are now executable."
echo

echo "Installation complete!"
echo
echo "To use the DevOps MCP Server:"
echo "1. Activate the virtual environment: source .venv/bin/activate"
echo "2. Set up your Kubernetes configuration: export KUBECONFIG='path/to/your/kubeconfig'"
echo "3. Start the server: ./main.py"
echo
echo "For more information, see the README.md file."
