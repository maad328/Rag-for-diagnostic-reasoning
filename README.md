# 🏥 RAG for Diagnostic Reasoning

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green?style=for-the-badge)
![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-blue?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-LLM-4285F4?style=for-the-badge&logo=google&logoColor=white)

**An AI-powered clinical diagnostic reasoning assistant using Retrieval-Augmented Generation (RAG)**

[📖 Read the Article](https://medium.com/@maad78150/rag-for-diagnostic-reasoning-for-clinical-notes-67ab0ded38ad) · [🐛 Report Bug](https://github.com/maad328/Rag-for-diagnostic-reasoning/issues) · [✨ Request Feature](https://github.com/maad328/Rag-for-diagnostic-reasoning/issues)

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Dataset](#-dataset)
- [Contributing](#-contributing)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## 🎯 About

This project implements a **Retrieval-Augmented Generation (RAG)** system for clinical diagnostic reasoning. It leverages clinical case data from the MIMIC-IV database to provide evidence-based diagnostic assistance.

The system retrieves relevant clinical cases based on user queries and uses Google's Gemini 2.0 Flash model to generate structured diagnostic reasoning, helping medical professionals and students understand diagnostic pathways.

---

## ✨ Features

- 🔍 **Semantic Search** - Find similar clinical cases using vector similarity
- 🧠 **AI-Powered Reasoning** - Generate evidence-based diagnostic reasoning
- 📚 **Rich Knowledge Base** - Built on MIMIC-IV clinical case data
- 🎨 **Modern UI** - Clean, professional Streamlit interface
- 📜 **Query History** - Track and review previous queries
- ⚡ **Fast Retrieval** - FAISS-powered vector search for quick results

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA PIPELINE                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   JSON Files ──► loader.py ──► Documents ──► storingdocs.py         │
│   (Clinical       (Parse &      (LangChain     (Embed &              │
│    Cases)          Clean)        Documents)     Store)               │
│                                                     │                │
│                                                     ▼                │
│                                              FAISS Vector DB         │
│                                                     │                │
├─────────────────────────────────────────────────────────────────────┤
│                         QUERY PIPELINE                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                     │                │
│   User Query ──► response.py ──► Similarity Search ─┘                │
│                       │                                              │
│                       ▼                                              │
│              Retrieved Context                                       │
│                       │                                              │
│                       ▼                                              │
│              Gemini 2.0 Flash                                        │
│                       │                                              │
│                       ▼                                              │
│           Diagnostic Reasoning Response                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

| Component           | Technology                            |
| ------------------- | ------------------------------------- |
| **Framework**       | LangChain                             |
| **Embeddings**      | HuggingFace `all-MiniLM-L6-v2`        |
| **Vector Database** | FAISS (Facebook AI Similarity Search) |
| **LLM**             | Google Gemini 2.0 Flash               |
| **Frontend**        | Streamlit                             |
| **Language**        | Python 3.12                           |

### Dependencies

```
langchain>=0.1.0
langchain-core>=0.1.0
langchain-huggingface>=0.0.1
langchain-community>=0.0.1
faiss-cpu>=1.7.4
torch>=2.0.0
transformers>=4.34.0
numpy>=1.24.0
google-generativeai>=0.1.6
sentence-transformers
streamlit>=1.28.0
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- Git
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Step 1: Clone the Repository

```bash
git clone https://github.com/maad328/Rag-for-diagnostic-reasoning.git
cd Rag-for-diagnostic-reasoning
```

### Step 2: Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Key

Set your Google Gemini API key as an environment variable:

**Windows (PowerShell):**

```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Windows (CMD):**

```cmd
set GEMINI_API_KEY=your-api-key-here
```

**macOS/Linux:**

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Step 5: Prepare the Dataset

Place your clinical case JSON files in the following directory structure:

```
mimic-iv-ext-direct-1.0.0/
└── Finished/
    ├── Acute Coronary Syndrome/
    │   ├── NSTEMI/
    │   ├── STEMI/
    │   └── UA/
    ├── Alzheimer/
    ├── COPD/
    └── ... (other conditions)
```

### Step 6: Build the Vector Database (First Time Only)

```bash
cd app
python storingdocs.py
cd ..
```

This creates the FAISS index in `app/faiss_index/`.

---

## 💻 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

### Example Queries

Try these clinical queries:

- _"What are the diagnostic criteria for NSTEMI?"_
- _"Patient presents with chest pain and elevated troponin levels"_
- _"Differentiate between Type A and Type B aortic dissection"_
- _"Signs and symptoms of pulmonary embolism"_

---

## 📁 Project Structure

```
Rag-for-diagnostic-reasoning/
│
├── app/
│   ├── __init__.py
│   ├── loader.py           # Document loading and preprocessing
│   ├── storingdocs.py      # Vector database creation
│   ├── response.py         # Query processing and LLM integration
│   └── faiss_index/        # Stored FAISS vector index
│       ├── index.faiss
│       └── index.pkl
│
├── mimic-iv-ext-direct-1.0.0/
│   └── Finished/           # Clinical case JSON files
│       ├── Acute Coronary Syndrome/
│       ├── Alzheimer/
│       ├── COPD/
│       └── ... (30+ conditions)
│
├── app.py                  # Streamlit frontend
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

### Key Files Explained

| File                 | Description                                                          |
| -------------------- | -------------------------------------------------------------------- |
| `app/loader.py`      | Parses JSON clinical cases, cleans text, creates LangChain Documents |
| `app/storingdocs.py` | Generates embeddings and builds FAISS vector database                |
| `app/response.py`    | Handles queries, retrieves similar cases, calls Gemini API           |
| `app.py`             | Streamlit web interface with professional styling                    |

---

## 📊 Dataset

This project uses clinical case data structured as JSON files with the following format:

```json
{
  "DIAGNOSIS$ID": "...",
  "input1": "Chief complaint and history",
  "input2": "Physical examination findings",
  "input3": "Laboratory results",
  "input4": "Imaging findings",
  "input5": "Treatment plan",
  "input6": "Clinical outcome"
}
```

### Supported Conditions

The system includes clinical cases for 30+ medical conditions including:

- Acute Coronary Syndrome (NSTEMI, STEMI, UA)
- Cardiomyopathy (Dilated, Hypertrophic, Restrictive)
- Pulmonary Conditions (COPD, Asthma, Pneumonia)
- Neurological (Stroke, Epilepsy, Multiple Sclerosis)
- Endocrine (Diabetes, Thyroid Disease, Adrenal Insufficiency)
- Gastrointestinal (Gastritis, Peptic Ulcer, GERD)
- And many more...

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

---

## ⚠️ Disclaimer

> **This is an educational tool for diagnostic reasoning. It does NOT replace clinical judgment or professional medical consultation.**

- This system is designed for educational and research purposes only
- Always consult qualified healthcare professionals for medical decisions
- The AI-generated responses should be verified by medical experts
- Do not use this tool for actual patient diagnosis or treatment

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 📚 Learn More

📖 **Read the full article on Medium:** [RAG for Diagnostic Reasoning for Clinical Notes](https://medium.com/@maad78150/rag-for-diagnostic-reasoning-for-clinical-notes-67ab0ded38ad)

---

<div align="center">

**Built with ❤️ for advancing clinical AI education**

[⬆ Back to Top](#-rag-for-diagnostic-reasoning)

</div>
