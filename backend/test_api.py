import requests

url = "http://127.0.0.1:5000/api/invoice/analyze"

invoice_path = r"C:\Users\rudh7\Downloads\AutoPilot-AI\invoice.pdf"

with open(invoice_path, "rb") as file:

    files = {
        "invoice": (
            "invoice.pdf",
            file,
            "application/pdf"
        )
    }

    response = requests.post(
        url,
        files=files
    )

print("\nSTATUS:")
print(response.status_code)

print("\nRESPONSE:")
print(response.json())