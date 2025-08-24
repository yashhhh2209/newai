import streamlit as st
import asyncio
import json
from backend.app.chat_service import HealthcareChatService
from backend.app.models import ChatRequest

# Page configuration
st.set_page_config(
    page_title="🏥 Healthcare AI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #007bff;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .bot-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    
    .emergency-alert {
        background-color: #ffebee;
        border: 2px solid #f44336;
        border-radius: 15px;
        padding: 1rem;
        color: #c62828;
        font-weight: bold;
    }
    
    .quick-actions {
        display: flex;
        gap: 10px;
        margin: 1rem 0;
    }
    
    .quick-action-btn {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        font-size: 14px;
    }
    
    .quick-action-btn:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

# Initialize the chat service
@st.cache_resource
def get_chat_service():
    return HealthcareChatService()

chat_service = get_chat_service()

# Main header
st.markdown("""
<div class="main-header">
    <h1>🏥 Healthcare AI Assistant</h1>
    <p>Your 24/7 healthcare information companion powered by AI</p>
    <p><strong>🚨 FREE • ONLINE • LLM + RAG • NO API KEY NEEDED</strong></p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 Quick Actions")
    
    # Quick action buttons
    if st.button("🕐 OPD Timings", use_container_width=True):
        st.session_state.quick_query = "What are OPD timings on Sunday?"
    
    if st.button("🏥 Insurance Info", use_container_width=True):
        st.session_state.quick_query = "How can I use cashless insurance?"
    
    if st.button("📅 Book Appointment", use_container_width=True):
        st.session_state.quick_query = "How do I book an appointment?"
    
    if st.button("🚨 Emergency Info", use_container_width=True):
        st.session_state.quick_query = "What are the emergency protocols?"
    
    st.markdown("---")
    st.markdown("### 🆘 Emergency Contacts")
    emergency_contacts = chat_service.get_emergency_contacts()
    for service, number in emergency_contacts.items():
        st.markdown(f"**{service.title()}**: {number}")
    
    st.markdown("---")
    st.markdown("### 📚 Available Topics")
    topics = chat_service.get_available_topics()
    for category in topics:
        st.markdown(f"**{category['category']}:**")
        for topic in category['topics']:
            st.markdown(f"- {topic}")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.quick_query = ""

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong> {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        # Check for emergency flags
        if "EMERGENCY" in message.get("safety_flags", []):
            st.markdown(f"""
            <div class="emergency-alert">
                🚨 EMERGENCY ALERT: {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 AI Assistant:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        
        # Display metadata
        if "citations" in message and message["citations"]:
            st.markdown(f"📚 **Sources:** {', '.join(message['citations'])}")
        
        if "confidence" in message:
            confidence_color = {
                "high": "🟢",
                "medium": "🟡", 
                "low": "🔴"
            }.get(message["confidence"], "⚪")
            st.markdown(f"{confidence_color} **Confidence:** {message['confidence']}")
        
        if "follow_up_questions" in message and message["follow_up_questions"]:
            st.markdown("❓ **Follow-up questions:**")
            for question in message["follow_up_questions"][:2]:  # Show first 2
                if st.button(question, key=f"followup_{hash(question)}"):
                    st.session_state.quick_query = question

# Handle quick query
if st.session_state.quick_query:
    st.session_state.messages.append({"role": "user", "content": st.session_state.quick_query})
    st.session_state.quick_query = ""

# Chat input
if prompt := st.chat_input("Ask me about healthcare services..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    st.markdown(f"""
    <div class="chat-message user-message">
        <strong>👤 You:</strong> {prompt}
    </div>
    """, unsafe_allow_html=True)
    
    # Show thinking indicator
    with st.spinner("🤖 AI Assistant is thinking..."):
        try:
            # Process the query using the correct method
            request = ChatRequest(query=prompt)
            response = chat_service.process_chat(request)
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.answer,
                "citations": response.citations,
                "confidence": response.confidence,
                "safety_flags": response.safety_flags,
                "follow_up_questions": response.follow_up_questions
            })
            
            # Rerun to display the new message
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error processing your request: {str(e)}")
            st.info("Please try again or contact support.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>⚠️ Disclaimer:</strong> This is for general healthcare information only, not medical advice.</p>
    <p>Always consult with qualified healthcare professionals for medical concerns.</p>
    <p>🚀 <strong>Powered by FREE AI + RAG Technology</strong></p>
</div>
""", unsafe_allow_html=True)
