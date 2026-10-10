# MedShield AI 🛡️🩺

**Enterprise Multimodal Clinical Decision Support & Diagnostic Intelligence Platform**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python)](https://www.python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.3.0-EE4C2C.svg?style=flat&logo=pytorch)](https://pytorch.org)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F00.svg?style=flat)](https://www.trychroma.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 📌 Executive Summary

**MedShield AI** is an enterprise-grade multimodal clinical AI platform engineered to assist physicians, radiologists, and healthcare professionals in rapid, accurate diagnostic evaluation. By unifying deep learning computer vision, Retrieval-Augmented Generation (RAG) over clinical records, and Explainable AI (XAI), MedShield AI provides clinicians with transparent, evidence-backed medical insights.

---

## 🌟 Key Capabilities

### 🩻 1. Multimodal Medical Imaging & Diagnostics
- **Chest X-Ray Pathology Detection**: Deep convolutional neural network (DenseNet-121) pipeline specialized in pulmonary lesion, opacity, and pneumonia detection.
- **Explainable AI (Grad-CAM)**: Visual diagnostic attribution heatmaps overlayed onto radiological scans, providing clinicians with verifiable anatomical focus areas for each prediction.

### 📄 2. Clinical RAG (Retrieval-Augmented Generation)
- **Document & Lab Report Ingestion**: OCR and text extraction for patient records, discharge summaries, and laboratory panels (PDF, DOCX, images).
- **Dense Vector Search**: Powered by ChromaDB and SentenceTransformer embeddings for semantic search across clinical documentation.
- **Hallucination-Resistant Synthesis**: Integration with Google Gemini and Groq engines featuring placeholder filtering and evidence grounding to prevent clinical misinformation.

### 👨‍⚕️ 3. Clinical Workflow & Doctor Portal
- **Consultation Management**: Interactive clinical case workflow, tracking patient cases from intake to diagnostic report.
- **Role-Based Security**: Doctor authentication, bcrypt password hashing, and JWT bearer access controls.
- **Comprehensive Audit Trails**: Automated timestamped audit logs for clinical review and compliance standards.
- **Clinical Reporting Engine**: Automated structured report generation summarizing diagnostic predictions, XAI visual findings, and therapeutic recommendations.

---

## 🏗️ Architecture & Technology Stack

```
MedShield AI/
├── backend/                  # FastAPI Application Core
│   ├── api/                  # RESTful API routers (auth, chat, consultations, reports, UI)
│   ├── database/             # SQLAlchemy ORM models, migrations, & session lifecycle
│   ├── repositories/         # Clinical database repositories
│   ├── schemas/              # Pydantic validation schemas
│   └── services/             # Authentication, consultation, and audit business logic
├── frontend/                 # Clinical Portal UI
│   ├── static/               # Enterprise CSS styling, icons, and client scripts
│   └── templates/            # Jinja2 clinical templates (dashboard, chat, reports)
├── rag/                      # Clinical Document RAG Engine
│   ├── chunkers/             # Semantic document chunking
│   ├── embeddings/           # SentenceTransformer embedding generators
│   ├── loaders/              # PDF and document parser utilities
│   ├── pipelines/            # Dual Gemini & Groq RAG execution pipelines
│   └── retrievers/           # ChromaDB dense vector retrieval
├── multimodal/               # Imaging & Neural Network Pipelines
├── explainability/           # Grad-CAM heatmap visualization & metrics
├── ai_engine/                # LLM orchestration & prompt templates
└── tests/                    # Pytest test suite
```

### Technology Matrix
| Layer | Technologies |
|---|---|
| **Backend & API** | FastAPI, Uvicorn, Pydantic v2, Python 3.10+ |
| **Frontend UI** | Jinja2, Modern Vanilla CSS Design System, Responsive Glassmorphism |
| **Database & ORM** | SQLite / MySQL, SQLAlchemy 2.0, Alembic |
| **AI / Deep Learning** | PyTorch, torchvision, DenseNet-121, Transformers |
| **Explainable AI** | Grad-CAM, SHAP, Pillow |
| **RAG & Vector Search** | ChromaDB, LangChain, Sentence-Transformers (`all-MiniLM-L6-v2`) |
| **LLM Providers** | Google Gemini Generative AI, Groq Llama-3 |
| **Security** | Python-JOSE (JWT), Passlib (Bcrypt), Dotenv |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Kavin86080/MedShield-AI.git
cd MedShield-AI
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```ini
# Application Configuration
APP_NAME=MedShield-AI
SECRET_KEY=your_secure_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database Configuration
DATABASE_URL=sqlite:///./medshield.db

```

### 5. Launch Application
```bash
uvicorn backend.main:app --reload --port 8000
```
Open your browser and navigate to `http://localhost:8000` to access the Clinical Dashboard.

---

## 🔒 Security & Privacy Notice
MedShield AI is developed as a clinical decision-support tool. It is designed to assist qualified healthcare professionals and should not replace certified medical diagnosis or physician judgment. All confidential credentials, API keys, and patient identifiers must remain guarded within `.env` and secured data storage.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
