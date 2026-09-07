# import os
# import json
# import re

# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_mistralai import ChatMistralAI
# from langchain_core.prompts import ChatPromptTemplate


# def analyze_invoice(invoice_path):

#     # ============================================================
#     # LOAD ENVIRONMENT
#     # ============================================================

#     load_dotenv()

#     api_key = os.getenv("MISTRAL_AI")

#     if not api_key:
#         raise RuntimeError(
#             "MISTRAL_AI API key not found in .env file."
#         )

#     # ============================================================
#     # CHECK FILE
#     # ============================================================

#     if not os.path.exists(invoice_path):
#         raise FileNotFoundError(
#             f"Invoice file not found: {invoice_path}"
#         )

#     # ============================================================
#     # LOAD PDF USING LANGCHAIN
#     # ============================================================

#     loader = PyPDFLoader(invoice_path)

#     docs = loader.load()

#     invoice_text = "\n".join(
#         doc.page_content
#         for doc in docs
#     )

#     if not invoice_text.strip():
#         raise ValueError(
#             "Could not extract text from the invoice."
#         )

#     print("Invoice loaded successfully.")

#     # ============================================================
#     # MISTRAL MODEL
#     # ============================================================

#     llm = ChatMistralAI(
#         model="mistral-small-latest",
#         api_key=api_key,
#         temperature=0
#     )

#     # ============================================================
#     # PROMPT
#     # ============================================================

#     prompt = ChatPromptTemplate.from_messages([
#         (
#             "system",
#             """
# You are an expert AI invoice extraction and analysis system.

# Your job is to carefully read the COMPLETE invoice and extract
# accurate structured information.

# IMPORTANT RULES:

# 1. Read the complete invoice.

# 2. Only extract information that is actually present in the invoice.

# 3. NEVER invent or guess information.

# 4. If a field is not present, return null.

# 5. Monetary values must be returned as numbers.

# 6. Do not include currency symbols inside monetary values.

# 7. Convert dates to YYYY-MM-DD format whenever possible.

# 8. Identify the invoice vendor/supplier.

# 9. Identify the invoice number.

# 10. Identify invoice date and due date.

# 11. Extract subtotal, tax and total.

# 12. Identify the currency.

# 13. Return ONLY valid JSON.

# Use exactly this structure:

# {{
#     "vendor": null,
#     "invoice_number": null,
#     "invoice_date": null,
#     "due_date": null,
#     "subtotal": null,
#     "tax": null,
#     "total": null,
#     "currency": null
# }}

# Return ONLY JSON.
# """
#         ),
#         (
#             "human",
#             """
# INVOICE:

# {invoice}
# """
#         )
#     ])

#     # ============================================================
#     # CREATE CHAIN
#     # ============================================================

#     chain = prompt | llm

#     print("Analyzing invoice...")

#     # ============================================================
#     # CALL MISTRAL
#     # ============================================================

#     try:

#         response = chain.invoke({
#             "invoice": invoice_text
#         })

#     except Exception as e:

#         raise RuntimeError(
#             f"Mistral API error: {str(e)}"
#         )

#     # ============================================================
#     # GET RESPONSE
#     # ============================================================

#     raw_response = response.content.strip()

#     print("\nMistral invoice analysis:")
#     print(raw_response)

#     # ============================================================
#     # CLEAN MARKDOWN
#     # ============================================================

#     raw_response = raw_response.replace(
#         "```json",
#         ""
#     )

#     raw_response = raw_response.replace(
#         "```",
#         ""
#     )

#     raw_response = raw_response.strip()

#     # ============================================================
#     # PARSE JSON
#     # ============================================================

#     try:

#         invoice_data = json.loads(raw_response)

#     except json.JSONDecodeError:

#         match = re.search(
#             r"\{.*\}",
#             raw_response,
#             re.DOTALL
#         )

#         if not match:
#             raise ValueError(
#                 "Mistral did not return valid JSON."
#             )

#         try:

#             invoice_data = json.loads(
#                 match.group()
#             )

#         except json.JSONDecodeError:

#             raise ValueError(
#                 "Invalid JSON returned by Mistral."
#             )

#     return invoice_data
"""original runned"""
# import os
# import json
# import re

# from dotenv import load_dotenv
# from langchain_mistralai import ChatMistralAI
# from langchain_core.prompts import ChatPromptTemplate


# def analyze_invoice(invoice_text):

#     # ============================================================
#     # LOAD ENVIRONMENT
#     # ============================================================

#     load_dotenv()

#     api_key = os.getenv("MISTRAL_AI")

#     if not api_key:
#         raise RuntimeError(
#             "MISTRAL_AI API key not found in .env file."
#         )

#     # ============================================================
#     # CHECK EXTRACTED TEXT
#     # ============================================================

#     if not invoice_text or not invoice_text.strip():
#         raise ValueError(
#             "Invoice text is empty."
#         )

#     # ============================================================
#     # MISTRAL MODEL
#     # ============================================================

#     llm = ChatMistralAI(
#         model="mistral-small-latest",
#         api_key=api_key,
#         temperature=0
#     )

#     # ============================================================
#     # PROMPT
#     # ============================================================

#     prompt = ChatPromptTemplate.from_messages([
#         (
#             "system",
#             """
# You are an expert AI invoice extraction and analysis system.

# Your job is to carefully read the COMPLETE invoice and extract
# accurate structured information.

# IMPORTANT RULES:

# 1. Read the complete invoice.

# 2. Only extract information that is actually present in the invoice.

# 3. NEVER invent or guess information.

# 4. If a field is not present, return null.

# 5. Monetary values must be returned as numbers.

# 6. Do not include currency symbols inside monetary values.

# 7. Convert dates to YYYY-MM-DD format whenever possible.

# 8. Identify the invoice vendor/supplier.

# 9. Identify the invoice number.

# 10. Identify invoice date and due date.

# 11. Extract subtotal, tax and total.

# 12. Identify the currency.

# 13. Return ONLY valid JSON.

# Use exactly this structure:

# {{
#     "vendor": null,
#     "invoice_number": null,
#     "invoice_date": null,
#     "due_date": null,
#     "subtotal": null,
#     "tax": null,
#     "total": null,
#     "currency": null
# }}

# Return ONLY JSON.
# """
#         ),
#         (
#             "human",
#             """
# INVOICE:

# {invoice}
# """
#         )
#     ])

#     # ============================================================
#     # CREATE CHAIN
#     # ============================================================

#     chain = prompt | llm

#     print("Analyzing invoice...")

#     # ============================================================
#     # CALL MISTRAL
#     # ============================================================

#     try:

#         response = chain.invoke({
#             "invoice": invoice_text
#         })

#     except Exception as e:

#         raise RuntimeError(
#             f"Mistral API error: {str(e)}"
#         )

#     # ============================================================
#     # GET RESPONSE
#     # ============================================================

#     raw_response = response.content.strip()

#     print("\nMistral invoice analysis:")
#     print(raw_response)

#     # ============================================================
#     # CLEAN MARKDOWN
#     # ============================================================

#     raw_response = raw_response.replace(
#         "```json",
#         ""
#     )

#     raw_response = raw_response.replace(
#         "```",
#         ""
#     )

#     raw_response = raw_response.strip()

#     # ============================================================
#     # PARSE JSON
#     # ============================================================

#     try:

#         invoice_data = json.loads(raw_response)

#     except json.JSONDecodeError:

#         match = re.search(
#             r"\{.*\}",
#             raw_response,
#             re.DOTALL
#         )

#         if not match:
#             raise ValueError(
#                 "Mistral did not return valid JSON."
#             )

#         try:

#             invoice_data = json.loads(
#                 match.group()
#             )

#         except json.JSONDecodeError:

#             raise ValueError(
#                 "Invalid JSON returned by Mistral."
#             )

#     return invoice_data


import os
import json
import re
import time

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate


def analyze_invoice(invoice_text):

    # ============================================================
    # LOAD ENVIRONMENT
    # ============================================================

    load_dotenv()

    api_key = os.getenv("MISTRAL_AI")

    if not api_key:
        raise RuntimeError(
            "MISTRAL_AI API key not found."
        )

    # ============================================================
    # CHECK EXTRACTED TEXT
    # ============================================================

    if not invoice_text or not invoice_text.strip():
        raise ValueError(
            "Invoice text is empty."
        )

    # ============================================================
    # MISTRAL MODEL
    # ============================================================

    llm = ChatMistralAI(
        model="ministral-8b-2512",
        api_key=api_key,
        temperature=0
    )

    # ============================================================
    # PROMPT
    # ============================================================

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are an expert AI invoice extraction and analysis system.
            
            Your job is to carefully read the COMPLETE invoice and extract
            accurate structured information.
            
            IMPORTANT RULES:
            
            1. Read the complete invoice.
            2. Only extract information actually present in the invoice.
            3. NEVER invent or guess information.
            4. If a field is not present, return null.
            5. Monetary values must be returned as numbers.
            6. Do not include currency symbols inside monetary values.
            7. Convert dates to YYYY-MM-DD format whenever possible.
            8. Identify the invoice vendor/supplier.
            9. Identify the invoice number.
            10. Identify invoice date and due date.
            11. Extract subtotal, tax and total.
            12. Identify the currency.
            13. Return ONLY valid JSON.
            
            Use exactly this structure:
            
            {{
                "vendor": null,
                "invoice_number": null,
                "invoice_date": null,
                "due_date": null,
                "subtotal": null,
                "tax": null,
                "total": null,
                "currency": null
            }}
            
            Return ONLY JSON.
            """
                    ),
                    (
                        "human",
                        """
            INVOICE:
            
            {invoice}
            """
                    )
                ])

    # ============================================================
    # CREATE CHAIN
    # ============================================================

    chain = prompt | llm

    print("Analyzing invoice with Mistral...")

    # ============================================================
    # CALL MISTRAL WITH RETRY
    # ============================================================

    max_retries = 3
    response = None

    for attempt in range(max_retries):

        try:

            print(
                f"Mistral request attempt "
                f"{attempt + 1}/{max_retries}"
            )

            response = chain.invoke({
                "invoice": invoice_text
            })

            print("Mistral request successful.")

            break

        except Exception as e:

            error_message = str(e)

            print("\nMistral error:")
            print(error_message)

            # ----------------------------------------------------
            # HANDLE RATE LIMIT
            # ----------------------------------------------------

            if "429" in error_message or "rate_limit" in error_message.lower():

                if attempt < max_retries - 1:

                    wait_time = 2 ** (attempt + 1)

                    print(
                        f"Mistral rate limit detected."
                    )

                    print(
                        f"Waiting {wait_time} seconds "
                        f"before retry..."
                    )

                    time.sleep(wait_time)

                    continue

                else:

                    raise RuntimeError(
                        "Mistral API rate limit exceeded "
                        "after multiple retries."
                    )

            # ----------------------------------------------------
            # OTHER MISTRAL ERRORS
            # ----------------------------------------------------

            raise RuntimeError(
                f"Mistral API error: {error_message}"
            )

    # ============================================================
    # CHECK RESPONSE
    # ============================================================

    if response is None:
        raise RuntimeError(
            "Mistral did not return a response."
        )

    # ============================================================
    # GET RESPONSE
    # ============================================================

    raw_response = response.content.strip()

    print("\nMistral invoice analysis:")
    print(raw_response)

    # ============================================================
    # CLEAN MARKDOWN
    # ============================================================

    raw_response = raw_response.replace(
        "```json",
        ""
    )

    raw_response = raw_response.replace(
        "```",
        ""
    )

    raw_response = raw_response.strip()

    # ============================================================
    # PARSE JSON
    # ============================================================

    try:

        invoice_data = json.loads(
            raw_response
        )

    except json.JSONDecodeError:

        match = re.search(
            r"\{.*\}",
            raw_response,
            re.DOTALL
        )

        if not match:

            raise ValueError(
                "Mistral did not return valid JSON."
            )

        try:

            invoice_data = json.loads(
                match.group()
            )

        except json.JSONDecodeError:

            raise ValueError(
                "Invalid JSON returned by Mistral."
            )

    # ============================================================
    # RETURN RESULT
    # ============================================================

    return invoice_data