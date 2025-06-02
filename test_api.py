import requests

API_URL = "http://localhost:7860/classify"

sample_email = """
Dear Support,
My name is John Doe with email john.doe@example.com. 
My phone is +91-98765-43210. 
Credit card: 4111 1111 1111 1111, exp 12/25, CVV 123.
DOB: 01/01/1990. Aadhar: 1234-5678-9012.
I'm having issues with my account login.
"""

response = requests.post(API_URL, json={"input_email_body": sample_email})
print(response.status_code)
print(response.json())