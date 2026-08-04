Memory

An intelligent AI-powered chatbot built using LangChain,Langgraph, Mistral AI, Retrieval-Augmented Generation (RAG), and Streamlit. The chatbot is capable of answering general queries, retrieving information from uploaded PDF documents, performing web searches for real-time information, and maintaining persistent conversation history using SQLite.

🚀 Features
🧠 AI-Powered Conversation
Natural language conversations using a Large Language Model (LLM)
Context-aware responses
General question answering
Intelligent response generation


📚 Retrieval-Augmented Generation (RAG)
Upload PDF documents
Extracts and processes document text
Recursive text chunking
Embedding generation
Semantic similarity search
Context-aware document question answering
Reduces LLM hallucinations by grounding responses in document content


🌐 Web Search Tool
Retrieves the latest information from the internet
Useful for:
Current Affairs
Latest News
Weather
Stock Prices
Sports Scores
Technology Updates


💬 Persistent Chat History
Stores conversations permanently
Resume previous conversations
Session management
SQLite-based storage

🎨 Interactive User Interface

Developed using Streamlit

Features include:

Clean chat interface
Responsive layout
PDF upload support
Real-time AI responses
Easy-to-use interface


# 🛠️ Tech Stack

## Programming Language
- Python

## AI Frameworks
- LangGraph
- LangChain

## Large Language Model
- Mistral AI

## Embedding Model
- Mistral Embeddings

## Vector Database
- ChromaDB

## Database
- SQLite

## User Interface
- Streamlit

## Document Processing
- PyPDFLoader
- RecursiveCharacterTextSplitter

## Environment Management
- python-dotenv



⚙️ Installation
1. Create Virtual Environment
Windows
python -m venv venv

Activate Virtual Environment

venv\Scripts\activate
Linux / macOS
python3 -m venv venv

source venv/bin/activate
2. Install Dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file inside the project directory.

MISTRAL_API_KEY=your_api_key
TAVILY_API_KEY=your_api_key

▶️ Run the Application
streamlit run app.py


📚 RAG Pipeline
          PDF
           │
           ▼
   Load Document
           │
           ▼
 Text Chunking
           │
           ▼
Generate Embeddings
           │
           ▼
 Store in ChromaDB
           │
           ▼
Similarity Search
           │
           ▼
Relevant Context
           │
           ▼
      Mistral AI
           │
           ▼
    Final Response



    # 🔄 LangGraph Workflow

```text
                User Query
                     │
                     ▼
             LangGraph State
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   RAG Node     Tool Node     Chat Node
        │            │            │
        └────────────┼────────────┘
                     ▼
            Response Generation
                     │
                     ▼
            SQLite Checkpointer
                     │
                     ▼
             Streamlit Interface
```

LangGraph is responsible for:

- Managing conversation state
- Routing requests between nodes
- Calling tools when required
- Integrating the RAG pipeline
- Maintaining persistent memory
- Coordinating the complete chatbot workflow


### 🔄 LangGraph Workflow
- Graph-based AI workflow orchestration
- Stateful conversation management
- Intelligent node routing
- Tool calling integration
- Persistent memory using SQLite Checkpointer
- Modular and scalable architecture


💡 Supported Use Cases
PDF Question Answering
Research Assistant
Resume Analysis
Knowledge Base Chatbot
AI Learning Assistant
Technical Documentation Assistant
Coding Assistant
General AI Conversation
Current Affairs
Latest News
Technology Queries


📌 Technologies Used
Technology	Purpose
Python	Backend Development
LangChain	LLM Orchestration
Mistral AI	Language Model
Mistral Embeddings	Embedding Generation
ChromaDB	Vector Database
SQLite	Persistent Chat History
Streamlit	User Interface
PyPDFLoader	PDF Processing
python-dotenv	Environment Variables

🔒 Persistent Memory

The chatbot stores:

Chat history
Session data
Previous conversations
User interaction logs

SQLite ensures that conversations remain available even after restarting the application.


📈 Future Enhancements
Multi-user authentication
Voice input/output
Image understanding (Vision Models)
OCR support
Multiple document retrieval
Conversation export (PDF/Word)
Docker deployment
Cloud deployment
User feedback system
Multi-language support
Hybrid Search (Keyword + Semantic)
Agentic AI workflows
Advanced memory management


🤝 Contributing

Contributions are welcome!

Fork the repository.
Create a new feature branch.
Commit your changes.
Push to your branch.
Open a Pull Request.


📜 License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this project under the terms of the license.


🙌 Acknowledgements

Special thanks to the amazing open-source community and the developers behind:

LangChain
Mistral AI
Streamlit
ChromaDB
SQLite
Python

⭐ Show Your Support

If you found this project useful:

⭐ Star this repository

🍴 Fork the repository

🐞 Report bugs by opening an Issue

💡 Suggest new features through GitHub Discussions or Issues

Your support motivates further improvements and development.

👨‍💻 Author

Harshvardhan Singh

If you like this project, don't forget to ⭐ Star the repository!
