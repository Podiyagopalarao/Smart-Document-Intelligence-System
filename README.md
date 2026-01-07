# Smart Document Intelligence System

A robust, enterprise-grade web application for analyzing, searching, and extracting insights from unstructured documents (PDFs and DOCX). Built with **Flask**, **SentenceTransformers**, and **FAISS**.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.0%2B-green)

## 🚀 Features

-   **📄 Document Ingestion**: Drag-and-drop upload for PDF and DOCX files.
-   **🔍 Intelligent Search**:
    -   **Semantic Search**: Ask natural language questions (e.g., "What are the termination conditions?") and get AI-powered results.
    -   **Keyword Search**: Find exact matches with high precision.
-   **🧠 AI-Powered Insights**: Uses `all-MiniLM-L6-v2` embeddings and FAISS vector indexing for fast, context-aware retrieval.
-   **📊 Structured Reporting**: Export analysis results to CSV with page numbers and `UTF-8` encoding (Excel-ready).
-   **🎨 Enterprise UI**: A clean, professional Dark/Neutral theme designed for business use cases.
-   **⚡ Page-Level Metadata**: Tracks source page numbers for every extracted chunk of text.

## 🛠️ Tech Stack

-   **Backend**: Python, Flask
-   **NLP & ML**: `sentence-transformers`, `faiss-cpu`, `numpy`
-   **Document Processing**: `pdfplumber`, `python-docx`
-   **Data Handling**: `pandas`
-   **Frontend**: HTML5, CSS3 (Enterprise Theme), JavaScript

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/smart-doc-intel.git
    cd smart-doc-intel
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Pytorch and Transformers libraries are large and may take a few minutes to install.*

## 🏃 Usage

1.  **Start the Application**
    ```bash
    python app.py
    ```

2.  **Access the UI**
    Open your browser and navigate to `http://127.0.0.1:5000`.

3.  **Analyze Documents**
    -   Upload a PDF or DOCX file.
    -   Use the **semantic search** tab to ask questions.
    -   Switch to **keyword search** for specific terms.
    -   Download the **CSV report** for offline analysis.

## 📂 Project Structure

```
├── app.py                 # Main Flask Application
├── requirements.txt       # Python Dependencies
├── static/
│   └── css/
│       └── style.css      # Enterprise Stylesheet
├── templates/
│   ├── base.html          # Base Layout
│   ├── index.html         # Upload Page
│   └── analysis.html      # Analysis & Search Dashboard
├── utils/
│   ├── extractor.py       # PDF/DOCX Parsing Logic
│   └── search_engine.py   # FAISS & Embedding Logic
└── uploads/               # Temp storage for uploads
```

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements.

## 📄 License

This project is licensed under the MIT License.
