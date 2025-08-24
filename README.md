# 🏥 Healthcare Chatbot with LLM + RAG

A production-ready healthcare information chatbot that uses Retrieval-Augmented Generation (RAG) to provide accurate, grounded responses from hospital documents and policies.

## ✨ Features

- **🤖 AI-Powered Responses**: Uses OpenAI GPT models for natural language understanding
- **📚 RAG Integration**: Retrieves relevant information from hospital knowledge base
- **🚨 Emergency Detection**: Automatically detects and responds to emergency situations
- **🔒 Privacy Protection**: Handles PHI requests securely with proper authentication
- **📱 Modern UI**: Beautiful, responsive chat interface with quick actions
- **⚡ Fast Performance**: Built with FastAPI for high-performance backend
- **🔍 Document Search**: FAISS vector database for semantic document retrieval

## 🏗️ Architecture

```
User Query → RAG Service → Document Retrieval → LLM Service → Structured Response → UI
```

- **Frontend**: HTML/JS chat interface with modern design
- **Backend**: FastAPI with async processing
- **RAG**: FAISS + Sentence Transformers for document search
- **LLM**: OpenAI GPT for response generation
- **Safety**: Emergency detection, PHI protection, medical disclaimers

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- 4GB+ RAM (for FAISS and embeddings)

### Installation

1. **Clone and setup**:
```bash
git clone <your-repo>
cd aichatbot
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp env.example .env
# Edit .env and add your OpenAI API key
```

4. **Run the application**:
```bash
python run.py
```

5. **Access the chatbot**:
   - Open your browser to `http://localhost:8000`
   - Start chatting with the healthcare assistant!

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_api_key_here
HOST=0.0.0.0
PORT=8000
```

### API Endpoints

- `GET /` - Chat interface
- `POST /chat` - Main chat endpoint
- `GET /health` - Health check

## 📊 Sample Queries to Test

### General Information
- "What are OPD timings on Sunday?"
- "How can I use cashless insurance?"
- "What are the visiting hours?"
- "How do I book an appointment?"

### Emergency Detection
- "I have chest pain and sweating"
- "I'm feeling suicidal"
- "I'm bleeding heavily"

### Privacy Protection
- "Show me my medical records"
- "What's my diagnosis?"
- "Show me my next appointment"

## 🛡️ Safety Features

### Emergency Detection
- Automatically detects emergency keywords
- Provides immediate emergency response
- Sets `EMERGENCY` safety flag
- Suggests calling 911

### Privacy Protection
- Detects PHI requests
- Requires patient authentication
- Sets `PHI_REQUEST` safety flag
- Redirects to proper channels

### Medical Disclaimer
- Never provides medical advice
- Always includes disclaimers
- Sets `MED_ADVICE` safety flag
- Recommends consulting healthcare providers

## 📁 Project Structure

```
aichatbot/
├── backend/
│   └── app/
│       ├── __init__.py
│       ├── main.py          # FastAPI application
│       ├── models.py        # Pydantic models
│       ├── chat_service.py  # Main orchestration
│       ├── rag_service.py   # Document retrieval
│       └── llm_service.py   # OpenAI integration
├── frontend/
│   └── index.html          # Chat interface
├── requirements.txt         # Python dependencies
├── run.py                  # Startup script
├── env.example             # Environment template
└── README.md               # This file
```

## 🔍 How It Works

### 1. Query Processing
- User sends query through chat interface
- Query is processed for safety flags (emergency, PHI, medical advice)

### 2. Document Retrieval (RAG)
- Query is embedded using Sentence Transformers
- FAISS vector database searches for relevant documents
- Top 3 most relevant document chunks are retrieved

### 3. Response Generation
- Retrieved documents + query sent to OpenAI GPT
- LLM generates contextual response
- Response is structured according to JSON schema

### 4. Safety & Output
- Safety flags are set based on query analysis
- Confidence level determined by document relevance
- Citations and follow-up questions included
- JSON response sent back to frontend

## 📋 JSON Response Schema

```json
{
  "answer": "string",
  "citations": ["doc_id or title"],
  "follow_up_questions": ["string"],
  "confidence": "low|medium|high",
  "safety_flags": ["EMERGENCY" | "PHI_REQUEST" | "MED_ADVICE" | "NONE"],
  "actions": [
    {
      "type": "TOOL_CALL" | "NONE",
      "tool": "rag_search" | "ehr_read" | "appt_schedule" | "ticket_create" | null,
      "args": { "key": "value" }
    }
  ]
}
```

## 🧪 Testing

### Manual Testing
1. Start the application
2. Open browser to `http://localhost:8000`
3. Try the sample queries above
4. Test emergency detection with "chest pain"
5. Test PHI protection with "my medical records"

### API Testing
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are OPD timings?"}'
```

## 🚀 Production Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

### Environment Variables
- Set `OPENAI_API_KEY` in production
- Configure `HOST` and `PORT` for your deployment
- Add logging and monitoring
- Set up proper CORS origins

### Security Considerations
- Restrict CORS origins to your frontend domain
- Implement rate limiting
- Add authentication for patient data access
- Log all interactions for compliance
- Use HTTPS in production

## 🔧 Customization

### Adding New Documents
Edit `backend/app/rag_service.py` and add to the `documents` list:

```python
{
    "id": "new_doc_id",
    "title": "Document Title",
    "content": "Document content here...",
    "category": "category_name"
}
```

### Modifying Safety Rules
Edit `backend/app/llm_service.py` to customize:
- Emergency keywords
- PHI detection patterns
- Medical advice detection

### Changing LLM Model
Modify the model in `backend/app/llm_service.py`:
```python
self.model = "gpt-4"  # or any other OpenAI model
```

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're in the correct directory
2. **OpenAI API errors**: Check your API key and billing
3. **Memory issues**: FAISS requires significant RAM
4. **Port conflicts**: Change PORT in .env file

### Debug Mode
```bash
export LOG_LEVEL=DEBUG
python run.py
```

## 📈 Performance

- **Response Time**: ~2-5 seconds (depends on OpenAI API)
- **Memory Usage**: ~2-4GB (mainly FAISS and embeddings)
- **Concurrent Users**: 10-50 (depends on OpenAI rate limits)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This chatbot is for **INFORMATIONAL PURPOSES ONLY**. It does not provide medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.

## 🆘 Support

- **Issues**: Create a GitHub issue
- **Questions**: Check the documentation above
- **Emergency**: Call 911 or visit nearest emergency room

---

**Built with ❤️ for better healthcare information access**
