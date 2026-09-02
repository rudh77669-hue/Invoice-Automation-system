# from invoice_ai import analyze_invoice


# invoice_path = "C:/Users/rudh7/Downloads/AutoPilot-AI/documents/invoices/test_invoice.pdf"


# result = analyze_invoice(invoice_path)


# print("/n======================================")
# print("FINAL INVOICE DATA")
# print("======================================")

# print(result)

# from invoice_ai import analyze_invoice
# from rule_engine import evaluate_invoice


# # ============================================================
# # INVOICE
# # ============================================================

# # invoice_path = "../documents/invoices/test_invoice.pdf"
# invoice_path = "C:/Users/rudh7/Downloads/AutoPilot-AI/documents/invoices/test_invoice.pdf"


# # ============================================================
# # MODULE 1 — AI EXTRACTION
# # ============================================================

# invoice_data = analyze_invoice(invoice_path)


# print("\n======================================")
# print("EXTRACTED INVOICE DATA")
# print("======================================")

# print(invoice_data)


# # ============================================================
# # MODULE 2 — RULE ENGINE
# # ============================================================

# decision = evaluate_invoice(invoice_data)


# print("\n======================================")
# print("RULE ENGINE DECISION")
# print("======================================")

# print(decision)
""""""
# from invoice_ai import analyze_invoice
# from rule_engine import evaluate_invoice
# from approval import create_approval_request

# # from invoice_ai import analyze_invoice
# # from rule_engine import evaluate_invoice
# from n8n_client import send_to_n8n
# # ============================================================
# # INVOICE
# # ============================================================

# # invoice_path = "../documents/invoices/test_invoice.pdf"
# invoice_path = "C:/Users/rudh7/Downloads/AutoPilot-AI/documents/invoices/test_invoice.pdf"


# # ============================================================
# # MODULE 1 — AI EXTRACTION
# # ============================================================

# invoice_data = analyze_invoice(invoice_path)

# print("\n======================================")
# print("EXTRACTED INVOICE DATA")
# print("======================================")

# print(invoice_data)


# # ============================================================
# # MODULE 2 — RULE ENGINE
# # ============================================================

# decision = evaluate_invoice(invoice_data)

# # ============================================================
# # MODULE 3 — SEND TO N8N
# # ============================================================

# n8n_response = send_to_n8n(
#     invoice_data,
#     decision
# )

# print("\n======================================")
# print("N8N RESPONSE")
# print("======================================")

# print(n8n_response)


# print("\n======================================")
# print("RULE ENGINE DECISION")
# print("======================================")

# print(decision)


# # ============================================================
# # MODULE 3 — HUMAN APPROVAL
# # ============================================================

# approval_request = create_approval_request(
#     invoice_data,
#     decision
# )

# print("\n======================================")
# print("APPROVAL REQUEST")
# print("======================================")

# print(approval_request)

from invoice_reader import load_invoice
from invoice_ai import analyze_invoice
from rule_engine import evaluate_invoice
from approval import create_approval_request
from n8n_client import send_to_n8n

# ============================================================
# INVOICE
# ============================================================

invoice_path = (
    "C:/Users/rudh7/Downloads/"
    "AutoPilot-AI/documents/invoices/test_invoice.pdf"
)


# ============================================================
# MODULE 1 — READ INVOICE
# ============================================================

print("\n======================================")
print("READING INVOICE")
print("======================================")

invoice_text = load_invoice(invoice_path)

print("Invoice loaded successfully.")


# ============================================================
# MODULE 2 — AI EXTRACTION
# ============================================================

print("\n======================================")
print("ANALYZING INVOICE")
print("======================================")

invoice_data = analyze_invoice(invoice_text)

print("\n======================================")
print("EXTRACTED INVOICE DATA")
print("======================================")

print(invoice_data)


# ============================================================
# MODULE 3 — RULE ENGINE
# ============================================================

print("\n======================================")
print("RULE ENGINE DECISION")
print("======================================")

decision = evaluate_invoice(invoice_data)

print(decision)

# ============================================================
# MODULE 4 — SEND TO N8N
# ============================================================

print("\n======================================")
print("SENDING TO N8N")
print("======================================")

n8n_response = send_to_n8n(
    invoice_data,
    decision,
    
)

print("\n======================================")
print("N8N RESPONSE")
print("======================================")

print(n8n_response)

# ============================================================
# MODULE 5 — HUMAN APPROVAL
# ============================================================

print("\n======================================")
print("APPROVAL REQUEST")
print("======================================")

approval_request = create_approval_request(
    invoice_data,
    decision
)

print(approval_request)