# import os

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from werkzeug.utils import secure_filename

# from invoice_reader import load_invoice
# from invoice_ai import analyze_invoice
# from rule_engine import evaluate_invoice
# from approval import create_approval_request
# from n8n_client import send_to_n8n


# # ============================================================
# # FLASK APP
# # ============================================================

# app = Flask(__name__)
# CORS(app)


# # ============================================================
# # CONFIGURATION
# # ============================================================

# UPLOAD_FOLDER = "temp_invoices"

# ALLOWED_EXTENSIONS = {"pdf"}

# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)


# # ============================================================
# # HELPER
# # ============================================================

# def allowed_file(filename):

#     return (
#         "." in filename
#         and filename.rsplit(".", 1)[1].lower()
#         in ALLOWED_EXTENSIONS
#     )


# # ============================================================
# # ROOT
# # ============================================================

# @app.route("/")
# def root():

#     return {
#         "status": "running",
#         "system": "AutoPilot AI",
#         "message": "AI Invoice Automation System is running"
#     }


# # ============================================================
# # HEALTH
# # ============================================================

# @app.route("/health")
# def health():

#     return {
#         "status": "healthy"
#     }


# # ============================================================
# # ANALYZE INVOICE
# # ============================================================

# @app.route("/api/invoice/analyze", methods=["POST"])
# def analyze_invoice_api():

#     # --------------------------------------------------------
#     # CHECK FILE
#     # --------------------------------------------------------

#     if "file" not in request.files:

#         return jsonify({
#             "success": False,
#             "error": "No invoice file provided."
#         }), 400


#     file = request.files["file"]


#     if file.filename == "":

#         return jsonify({
#             "success": False,
#             "error": "No file selected."
#         }), 400


#     if not allowed_file(file.filename):

#         return jsonify({
#             "success": False,
#             "error": "Only PDF files are allowed."
#         }), 400


#     # --------------------------------------------------------
#     # SAVE FILE
#     # --------------------------------------------------------

#     filename = secure_filename(file.filename)

#     filepath = os.path.join(
#         app.config["UPLOAD_FOLDER"],
#         filename
#     )

#     file.save(filepath)

#     try:

#         # ====================================================
#         # STEP 1 — READ PDF
#         # ====================================================

#         print("\n======================================")
#         print("READING INVOICE")
#         print("======================================")

#         invoice_text = load_invoice(filepath)


#         # ====================================================
#         # STEP 2 — AI ANALYSIS
#         # ====================================================

#         print("\n======================================")
#         print("ANALYZING INVOICE")
#         print("======================================")

#         invoice_data = analyze_invoice(invoice_text)


#         print("\nEXTRACTED INVOICE DATA")
#         print(invoice_data)


#         # ====================================================
#         # STEP 3 — RULE ENGINE
#         # ====================================================

#         print("\n======================================")
#         print("RULE ENGINE")
#         print("======================================")

#         decision = evaluate_invoice(invoice_data)


#         print(decision)


#         # ====================================================
#         # STEP 4 — HUMAN APPROVAL
#         # ====================================================

#         approval_request = create_approval_request(
#             invoice_data,
#             decision
#         )


#         print("\n======================================")
#         print("APPROVAL")
#         print("======================================")

#         print(approval_request)


#         # ====================================================
#         # STEP 5 — SEND TO N8N
#         # ====================================================

#         print("\n======================================")
#         print("N8N")
#         print("======================================")


#         n8n_response = send_to_n8n(
#             invoice_data,
#             decision
#         )


#         # ====================================================
#         # FINAL RESPONSE
#         # ====================================================

#         return jsonify({

#             "success": True,

#             "invoice": invoice_data,

#             "decision": decision,

#             "approval": approval_request,

#             "n8n": n8n_response

#         })


#     except Exception as e:

#         print("\nERROR:")
#         print(str(e))

#         return jsonify({

#             "success": False,

#             "error": str(e)

#         }), 500


#     finally:

#         # ----------------------------------------------------
#         # DELETE TEMP FILE
#         # ----------------------------------------------------

#         if os.path.exists(filepath):

#             os.remove(filepath)


# # ============================================================
# # RUN SERVER
# # ============================================================

# if __name__ == "__main__":

#     app.run(
#         host="0.0.0.0",
#         port=5000,
#         debug=True
#     )

# # import requests

# # url = "http://127.0.0.1:5000/api/invoice/analyze"

# # invoice_path = r"C:\Users\rudh7\Downloads\AutoPilot-AI\invoice.pdf"

# # with open(invoice_path, "rb") as file:

# #     files = {
# #         "invoice": (
# #             "invoice.pdf",
# #             file,
# #             "application/pdf"
# #         )
# #     }

# #     response = requests.post(
# #         url,
# #         files=files
# #     )

# # print("\nSTATUS:")
# # print(response.status_code)

# # print("\nRESPONSE:")
# # print(response.json())


import os
import threading

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from invoice_reader import load_invoice
from invoice_ai import analyze_invoice
from rule_engine import evaluate_invoice
from approval import create_approval_request
from n8n_client import send_to_n8n


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
# CONFIGURATION
# ============================================================

UPLOAD_FOLDER = "temp_invoices"

ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ============================================================
# HELPER
# ============================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ============================================================
# BACKGROUND INVOICE PROCESSING
# ============================================================

def process_invoice_in_background(filepath):

    try:

        # ====================================================
        # STEP 1 — READ PDF
        # ====================================================

        print("\n======================================")
        print("BACKGROUND: READING INVOICE")
        print("======================================")

        invoice_text = load_invoice(filepath)


        # ====================================================
        # STEP 2 — AI ANALYSIS
        # ====================================================

        print("\n======================================")
        print("BACKGROUND: ANALYZING INVOICE")
        print("======================================")

        invoice_data = analyze_invoice(invoice_text)

        print("\nEXTRACTED INVOICE DATA")
        print(invoice_data)


        # ====================================================
        # STEP 3 — RULE ENGINE
        # ====================================================

        print("\n======================================")
        print("BACKGROUND: RULE ENGINE")
        print("======================================")

        decision = evaluate_invoice(invoice_data)

        print(decision)


        # ====================================================
        # STEP 4 — HUMAN APPROVAL
        # ====================================================

        approval_request = create_approval_request(
            invoice_data,
            decision
        )

        print("\n======================================")
        print("BACKGROUND: APPROVAL")
        print("======================================")

        print(approval_request)


        # ====================================================
        # STEP 5 — SEND TO N8N
        # ====================================================

        print("\n======================================")
        print("BACKGROUND: N8N")
        print("======================================")

        try:

            n8n_response = send_to_n8n(
                invoice_data,
                decision,
                filepath
            )

            print("\nN8N RESPONSE:")
            print(n8n_response)

        except Exception as n8n_error:

            # IMPORTANT:
            # n8n/email failure does NOT mean
            # invoice submission failed.

            print("\nN8N/EMAIL ERROR:")
            print(str(n8n_error))


        print("\n======================================")
        print("BACKGROUND PROCESSING COMPLETE")
        print("======================================")


    except Exception as e:

        print("\n======================================")
        print("BACKGROUND PROCESSING ERROR")
        print("======================================")

        print(str(e))


    finally:

        # ====================================================
        # DELETE TEMP FILE
        # ====================================================

        if os.path.exists(filepath):

            try:

                os.remove(filepath)

                print("\nTemporary invoice file deleted.")

            except Exception as cleanup_error:

                print(
                    "\nCould not delete temporary file:",
                    cleanup_error
                )


# ============================================================
# ROOT
# ============================================================

@app.route("/")
def root():

    return {
        "status": "running",
        "system": "AutoPilot AI",
        "message": "AI Invoice Automation System is running"
    }


# ============================================================
# HEALTH
# ============================================================

@app.route("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# INVOICE UPLOAD
# ============================================================

@app.route("/api/invoice/analyze", methods=["POST"])
def analyze_invoice_api():

    # --------------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------------

    if "file" not in request.files:

        return jsonify({
            "success": False,
            "error": "No invoice file provided."
        }), 400


    file = request.files["file"]


    if file.filename == "":

        return jsonify({
            "success": False,
            "error": "No file selected."
        }), 400


    if not allowed_file(file.filename):

        return jsonify({
            "success": False,
            "error": "Only PDF files are allowed."
        }), 400


    # --------------------------------------------------------
    # SAVE FILE
    # --------------------------------------------------------

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    try:

        file.save(filepath)

    except Exception as e:

        print("\nFILE SAVE ERROR:")
        print(str(e))

        return jsonify({
            "success": False,
            "error": "Invoice could not be saved."
        }), 500


    # ========================================================
    # START BACKGROUND PROCESSING
    # ========================================================

    processing_thread = threading.Thread(
        target=process_invoice_in_background,
        args=(filepath,),
        daemon=True
    )

    processing_thread.start()


    # ========================================================
    # IMMEDIATE RESPONSE TO FRONTEND
    # ========================================================

    return jsonify({

        "success": True,

        "message": "Invoice submitted successfully.",

        "status": "SUBMITTED"

    }), 200


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )