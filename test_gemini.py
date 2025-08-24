#!/usr/bin/env python3
"""
Test script to verify Gemini AI integration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'app'))

# Import the models first
from models import ChatResponse, Action
from llm_service import LLMService
from rag_service import RAGService

def test_gemini():
    print("🧪 Testing Gemini AI Integration...")
    
    try:
        # Test LLM Service
        print("1. Testing LLM Service...")
        llm_service = LLMService()
        print("✅ LLM Service initialized successfully!")
        
        # Test RAG Service
        print("2. Testing RAG Service...")
        rag_service = RAGService()
        print("✅ RAG Service initialized successfully!")
        
        # Test general conversation
        print("3. Testing general conversation...")
        response = llm_service._generate_general_response("Tell me about movies")
        print(f"✅ General response: {response.answer[:100]}...")
        
        # Test hospital query
        print("4. Testing hospital query...")
        docs = rag_service.search_documents("OPD timing")
        print(f"✅ Found {len(docs)} relevant documents")
        
        if docs:
            response = llm_service._generate_rag_response("OPD timing", docs)
            print(f"✅ Hospital response: {response.answer[:100]}...")
        
        print("\n🎉 All tests passed! Gemini AI is fully integrated!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_gemini()
