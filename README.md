# Email Classification & PII Masking API

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This project implements an email classification system with PII masking capabilities. It automatically detects and masks Personally Identifiable Information (PII) in support emails and classifies them into predefined categories (Incident, Request, Change, Problem).

## Features

- 🛡️ **PII Detection & Masking** - Automatically detects and masks names, emails, phone numbers, credit cards, etc.
- 📧 **Email Classification** - Categorizes emails into 4 predefined categories
- ⚙️ **FastAPI REST API** - Clean and documented API endpoint
- 🐳 **Docker Support** - Containerized deployment ready
- ☁️ **Hugging Face Spaces** - Cloud deployment compatible

## Setup Instructions

### Prerequisites

- Python 3.9+
- pip package manager
- Docker (optional)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Adrian7305/Akaike_Email_Classification.git
   cd Akaike_Email_Classification
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/MacOS
   .\.venv\Scripts\activate   # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

### Running Locally

Start the API server:
```bash
uvicorn main:app --port 7860 --reload
```

The API will be available at: `http://localhost:7860`

## Usage

### API Endpoint

- **URL:** `/classify`
- **Method:** `POST`
- **Content-Type:** `application/json`

### Request Format

```json
{
  "input_email_body": "Your support email text here..."
}
```

### Example Request

```bash
curl -X POST "http://localhost:7860/classify" \
-H "Content-Type: application/json" \
-d '{
  "input_email_body": "Hello, my name is John Doe. My email is john@example.com and my phone is 555-123-4567. Credit card: 4111 1111 1111 1111, exp 12/25. I cannot access my account."
}'
```

### Response Format

```json
{
  "input_email_body": "Original email text",
  "list_of_masked_entities": [
    {
      "position": [start_index, end_index],
      "classification": "entity_type",
      "entity": "original_value"
    }
  ],
  "masked_email": "Email with PII masked",
  "category_of_the_email": "Classification result"
}
```

### Testing with Sample Script

A test script is included to verify functionality:
```bash
python test_api.py
```

## Deployment to Hugging Face Spaces

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Select "Docker" as the SDK
3. Configure hardware (CPU Basic is sufficient)
4. Push your code to the Space repository
5. The application will build automatically

Once deployed, your API endpoint will be:
```
https://adrian7305-email-classifier-api.hf.space/classify
```

## Problems Faced & Solutions

### 1. Dependency Conflicts
**Problem:** Existing packages in environment caused version conflicts during installation.

**Solution:**
- Created a clean virtual environment
- Pinned specific package versions in requirements.txt
- Added `HF_HUB_ENABLE_HF_TRANSFER=1` environment variable to fix model download issues

### 2. PII Masking Challenges
**Problem:** Overlapping entities and index shifting during replacement.

**Solution:**
- Implemented entity detection in two phases (regex patterns + spaCy NER)
- Sorted entities by start position in descending order before replacement
- Used character position indexing instead of word-based

### 3. Model Loading in Hugging Face Spaces
**Problem:** Slow model download during container build.

**Solution:**
- Pre-downloaded model in Dockerfile build stage
- Implemented caching mechanism
- Reduced image size with python:3.9-slim base

### 4. API Response Format
**Problem:** Automated evaluation required strict JSON structure.

**Solution:**
- Created Pydantic models to enforce response format
- Added comprehensive test cases
- Implemented error handling for edge cases

### 5. Multi-line PII Detection
**Problem:** Standard regex failed with multi-line credit card numbers.

**Solution:**
- Enhanced regex patterns with DOTALL flag
- Implemented custom preprocessing for multi-line entities
- Added test cases for complex PII patterns

## File Structure

```
├── .gitignore
├── README.md
├── requirements.txt
├── main.py              # FastAPI application
├── models.py            # Model loading and classification
├── utils.py             # PII masking utilities
├── test_api.py          # API test script
├── Dockerfile           # Docker configuration
```
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ for email classification and PII protection**