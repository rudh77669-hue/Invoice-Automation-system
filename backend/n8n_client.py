# import os
# import requests

# from dotenv import load_dotenv


# load_dotenv()


# N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


# def send_to_n8n(invoice_data, decision):

#     if not N8N_WEBHOOK_URL:
#         raise RuntimeError(
#             "N8N_WEBHOOK_URL not found in .env"
#         )

#     payload = {
#         "event": "invoice_analyzed",

#         "invoice": invoice_data,

#         "decision": decision
#     }

#     print("\nSending invoice data to n8n...")

#     response = requests.post(
#         N8N_WEBHOOK_URL,
#         json=payload,
#         timeout=30
#     )

#     response.raise_for_status()

#     print("Invoice data successfully sent to n8n.")

#     try:
#         return response.json()

#     except ValueError:
#         return {
#             "status": "success",
#             "response": response.text
#         }

import os
import json
import requests

from dotenv import load_dotenv


load_dotenv()


N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


def send_to_n8n(invoice_data, decision, filepath):

    if not N8N_WEBHOOK_URL:
        raise RuntimeError(
            "N8N_WEBHOOK_URL not found in .env"
        )

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Invoice PDF not found: {filepath}"
        )

    payload = {
        "event": "invoice_analyzed",
        "invoice": invoice_data,
        "decision": decision
    }

    print("\nSending invoice data + PDF to n8n...")

    with open(filepath, "rb") as pdf_file:

        files = {
            "invoice_pdf": (
                os.path.basename(filepath),
                pdf_file,
                "application/pdf"
            )
        }

        response = requests.post(
            N8N_WEBHOOK_URL,
            data={
                "event": "invoice_analyzed",
                "invoice": json.dumps(invoice_data),
                "decision": json.dumps(decision)
            },
            files=files,
            timeout=30
        )

    response.raise_for_status()

    print("Invoice data + PDF successfully sent to n8n.")

    try:

        return response.json()

    except ValueError:

        return {
            "status": "success",
            "response": response.text
        }   