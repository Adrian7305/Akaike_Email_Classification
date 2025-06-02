import pandas as pd
import json
from utils import mask_pii

def preprocess_dataset(input_path: str, output_path: str):
    # Load the original dataset (columns are "email" and "type")
    df = pd.read_csv(input_path)

    masked_texts = []
    entities_list = []

    for text in df["email"]:
        masked, entities = mask_pii(text)
        masked_texts.append(masked)
        entities_list.append(json.dumps(entities))

    out_df = pd.DataFrame({
        "original_email_body": df["email"],
        "masked_email_body": masked_texts,
        "label": df["type"],
        "entities_json": entities_list
    })

    out_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    preprocess_dataset(
        "combined_emails_with_natural_pii.csv",
        "masked_combined_emails.csv"
    )
