from fastapi import FastAPI
from pydantic import BaseModel
from utils import mask_pii, demask_pii
from models import load_model, classify_email

app = FastAPI()
model = load_model()

class EmailRequest(BaseModel):
    input_email_body: str

@app.post("/classify")
def classify(request: EmailRequest):
    # Mask PII
    masked_email, entities = mask_pii(request.input_email_body)
    
    # Classify email
    category = classify_email(model, masked_email)
    
    # Demask back to original
    demasked_email = demask_pii(masked_email, entities)
    
    return {
        "input_email_body": request.input_email_body,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": category,
        "demasked_email": demasked_email
    }
