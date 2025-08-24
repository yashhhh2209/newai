#!/usr/bin/env python3
"""
Healthcare Chatbot Startup Script
Run this to start the FastAPI server
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print("🏥 Starting Healthcare Chatbot...")
    print(f"📡 Server will be available at: http://{host}:{port}")
    print("🔑 Make sure to set your OPENAI_API_KEY in the .env file")
    print("🚀 Starting FastAPI server...")
    
    # Start the server
    uvicorn.run(
        "backend.app.main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
