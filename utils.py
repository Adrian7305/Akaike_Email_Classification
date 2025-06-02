import re
import spacy
from typing import Tuple, List, Dict

nlp = spacy.load("en_core_web_sm")

PATTERN_ORDER = [
    ("credit_debit_no", r"\b(?:\d[ -]*?){13,19}\b"),
    ("aadhar_num",      r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"),
    ("phone_number",    r"(?:(?:\+91|0)[-\s]?)?[6-9]\d{4}[-\s]?\d{5}"),
    ("email",           r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    ("dob",             r"\b(?:0?[1-9]|1[0-2])[\/-](?:0?[1-9]|[12][0-9]|3[01])[\/-](?:\d{4}|\d{2})\b"),
    ("expiry_no",       r"\b(?:0[1-9]|1[0-2])[\/-]?(?:\d{2}|\d{4})\b"),
    ("cvv_no",          r"\b\d{3,4}\b"),
]

def mask_pii(text: str) -> Tuple[str, List[Dict]]:
    entities: List[Dict] = []
    occupied_spans: List[Tuple[int, int]] = []
    masked_text = text

    def overlaps_existing(start: int, end: int) -> bool:
        for os_, oe_ in occupied_spans:
            if not (end <= os_ or start >= oe_):
                return True
        return False

    for pii_type, pattern in PATTERN_ORDER:
        for match in re.finditer(pattern, text):
            start, end = match.span()
            if not overlaps_existing(start, end):
                entities.append({
                    "position": [start, end],
                    "classification": pii_type,
                    "entity": text[start:end]
                })
                occupied_spans.append((start, end))

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            start, end = ent.start_char, ent.end_char
            if not overlaps_existing(start, end):
                entities.append({
                    "position": [start, end],
                    "classification": "full_name",
                    "entity": ent.text
                })
                occupied_spans.append((start, end))

    entities.sort(key=lambda x: x["position"][0], reverse=True)

    for entity in entities:
        start, end = entity["position"]
        placeholder = f"[{entity['classification']}]"
        masked_text = masked_text[:start] + placeholder + masked_text[end:]

    return masked_text, entities
def demask_pii(masked_text: str, entities: List[Dict]) -> str:
    """
    Given `masked_text` (with placeholders like “[email]”) and the
    `entities` list (each entry has position, classification, entity),
    restore the original substrings at their exact positions.
    """
    result = masked_text
    # Sort in ascending order of start‐index, so that earlier replacements
    # don’t break the indices of later ones.
    for ent in sorted(entities, key=lambda x: x["position"][0]):
        start, end = ent["position"]
        placeholder = f"[{ent['classification']}]"
        original = ent["entity"]
        # Replace the placeholder at the exact location with the original text.
        result = result[:start] + original + result[start + len(placeholder):]
    return result
