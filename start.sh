#!/bin/bash

# Healthcare Chatbot Startup Script

echo "🏥 Starting Healthcare Chatbot..."
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env file from template..."
    cp env.example .env
    echo "📝 Please edit .env file and add your OpenAI API key"
    echo "Then run this script again"
    exit 1
fi

# Check if OpenAI API key is set
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "❌ Error: OpenAI API key not found in .env file"
    echo "Please edit .env file and add your OpenAI API key"
    echo "Example: OPENAI_API_KEY=sk-your-key-here"
    exit 1
fi

# Check if requirements are installed
if [ ! -d "backend" ]; then
    echo "❌ Error: Backend directory not found"
    echo "Please make sure you're in the correct directory"
    exit 1
fi

# Install requirements if needed
echo "📦 Checking dependencies..."
if ! python3 -c "import fastapi, openai, faiss" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "🚀 Starting the chatbot..."
echo "📡 Server will be available at: http://localhost:8000"
echo "🔄 Press Ctrl+C to stop the server"
echo ""

# Start the chatbot
python3 run.py
