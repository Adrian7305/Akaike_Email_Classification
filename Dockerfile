FROM python:3.10-slim

# 1) Set working directory
WORKDIR /app

# 2) Copy everything into the container
COPY . /app

# 3) Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# 4) Download spaCy model
RUN python -m spacy download en_core_web_sm

# 5) Expose port 7860 (FastAPI default)
EXPOSE 7860

# 6) Start Uvicorn with your FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]