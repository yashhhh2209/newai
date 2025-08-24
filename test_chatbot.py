#!/usr/bin/env python3
"""
Simple test script for the Healthcare Chatbot
Tests the core functionality without starting the full server
"""

import asyncio
import os
from dotenv import load_dotenv
from backend.app.chat_service import HealthcareChatService

# Load environment variables
load_dotenv()

async def test_chatbot():
    """Test the chatbot with various queries"""
    
    print("🏥 Testing Healthcare Chatbot...")
    print("=" * 50)
    
    # Initialize the chat service
    chat_service = HealthcareChatService()
    
    # Test queries
    test_queries = [
        "What are OPD timings on Sunday?",
        "How can I use cashless insurance?",
        "I have chest pain and sweating",
        "Show me my medical records",
        "What should I do for a fever?",
        "What are the visiting hours?",
        "How do I book an appointment?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 40)
        
        try:
            # Process the query
            response = await chat_service.process_query(query)
            
            # Display response
            print(f"🤖 Answer: {response.answer}")
            print(f"📊 Confidence: {response.confidence}")
            print(f"🚨 Safety Flags: {response.safety_flags}")
            print(f"📚 Citations: {response.citations}")
            print(f"❓ Follow-up: {response.follow_up_questions[:2]}")  # Show first 2
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 40)
    
    print("\n✅ Testing completed!")
    print("\n📋 Available topics:")
    topics = chat_service.get_available_topics()
    for category in topics:
        print(f"  {category['category']}: {', '.join(category['topics'])}")
    
    print("\n🚨 Emergency contacts:")
    contacts = chat_service.get_emergency_contacts()
    for service, number in contacts.items():
        print(f"  {service.title()}: {number}")

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
        print("Example: cp env.example .env")
        exit(1)
    
    # Run the test
    asyncio.run(test_chatbot())
