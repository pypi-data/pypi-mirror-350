# DocVec CLI

🚀 **Overview**  
DocVec CLI is a powerful command-line tool designed to transform your unstructured local documents (PDF, DOCX, TXT) into query-ready vector embeddings, making them instantly usable for Large Language Models (LLMs) and bolstering Retrieval Augmented Generation (RAG) workflows.
---

## ✨ Key Features

- **Multi-Format Support**: Processes `.pdf`, `.docx`, and `.txt` files.
- **Automatic Text Extraction**: Efficiently extracts raw text content from various document types.
- **Intelligent Text Cleaning**: Removes unnecessary whitespace, excessive newlines, and basic HTML tags.
- **Configurable Text Chunking**: Uses `langchain`'s `RecursiveCharacterTextSplitter`, with customizable `chunk_size` and `chunk_overlap`.
- **Offline Embedding Generation**: Uses local `sentence-transformers` models (default: `all-MiniLM-L6-v2`) to create high-quality vector embeddings directly on your machine, ensuring privacy and offline capabilities.
- **ChromaDB-Compatible Output**: Generates JSON files structured for easy ingestion into ChromaDB or other vector databases.
- **User-Friendly CLI**: Simple command-line arguments for input/output paths and processing parameters.
- **Progress Indicators**: Visual progress bars for long-running operations like embedding generation.

---

## 📦 Installation

### Prerequisites
- Python 3.8 or newer

### Steps

#### 1. Clone the repository:
```bash
git clone https://github.com/onurbaran/docvec-cli.git  
cd docvec-cli
```

#### 2. Create and activate a virtual environment:
It’s highly recommended to use a virtual environment to manage dependencies.

```bash
python -m venv .venv

# On Windows:
.\.venv\Scripts\activate

# On macOS/Linux:
source ./.venv/bin/activate
```

#### 3. Install dependencies:

Ensure your `requirements.txt` contains:
```
pypdf
python-docx
sentence-transformers
langchain-text-splitters
tqdm
numpy
```

Then run:
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Once installed, you can use `docvec-cli` from your terminal.

### Basic Command Structure
```bash
python src/main.py --input-path <path_to_document_or_directory> --output-path <path_to_output_directory> [OPTIONS]
```

### Required Arguments
- `--input-path <path>`: Path to a document file (e.g., `report.pdf`) or a directory (directory processing is planned for future updates).
- `--output-path <path>`: Path to the directory where the generated vector and metadata files will be saved.

### Optional Arguments
- `--chunk-size <int>`: Max size of each text chunk in characters (default: `1000`)
- `--chunk-overlap <int>`: Number of characters to overlap between chunks (default: `200`)
- `--model-name <str>`: Sentence-transformers model name (default: `all-MiniLM-L6-v2`)
- `--output-format <str>`: Format for output files (default: `json`, only format currently supported)

---

## 📁 Examples

### Process a single PDF file:
```bash
python src/main.py --input-path "docs/my_report.pdf" --output-path "vectors/"
```

### Process a DOCX file with custom chunking:
```bash
python src/main.py --input-path "articles/research.docx" --output-path "embeddings/" --chunk-size 500 --chunk-overlap 100
```

### Process a TXT file with a different embedding model:
```bash
python src/main.py --input-path "notes/daily_journal.txt" --output-path "processed_data/" --model-name "all-MiniLM-L12-v2"
```

---

## 📄 Output File Structure

For each processed document (e.g., `my_report.pdf`), a JSON file (`my_report_vectors.json`) will be created in the specified `--output-path`.

Example content:
```json
[
  {
    "id": "my_report-0",
    "document": "This is the text content of the first chunk...",
    "embedding": [0.123, -0.456, ..., 0.789],
    "metadata": {
      "source_file": "my_report.pdf",
      "chunk_index": 0,
      "chunk_size": 250
    }
  }
]
```

---

## 🤝 Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes.
4. Write clear, concise commit messages.
5. Push your branch: `git push origin feature/your-feature-name`
6. Open a Pull Request.

Please ensure:
- Your code follows [PEP 8](https://peps.python.org/pep-0008/)
- You include appropriate tests.

---

## 📄 License

This project is licensed under the MIT License.

---

## 📧 Contact

For questions, feedback, or issues, please open an issue.
