# ============================================================
# HUMAN APPROVAL MODULE
# ============================================================


def create_approval_request(invoice_data, decision):
    """
    Creates an approval requ    est for a high-risk invoice.
    """

    if not decision.get("approval_required"):
        return {
            "status": "NOT_REQUIRED",
            "message": "Human approval is not required."
        }

    approval_request = {
        "status": "PENDING",
        "vendor": invoice_data.get("vendor"),
        "invoice_number": invoice_data.get("invoice_number"),
        "total": invoice_data.get("total"),
        "currency": invoice_data.get("currency"),
        "risk_level": decision.get("risk_level"),
        "reason": decision.get("reason")
    }

    return approval_request


# ============================================================
# APPROVE
# ============================================================

def approve_invoice(approval_request):

    if approval_request.get("status") != "PENDING":
        raise ValueError(
            "Invoice is not waiting for approval."
        )

    approval_request["status"] = "APPROVED"

    approval_request["message"] = (
        "Invoice has been approved by human reviewer."
    )

    return approval_request


# ============================================================
# REJECT
# ============================================================

def reject_invoice(approval_request):

    if approval_request.get("status") != "PENDING":
        raise ValueError(
            "Invoice is not waiting for approval."
        )

    approval_request["status"] = "REJECTED"

    approval_request["message"] = (
        "Invoice has been rejected by human reviewer."
    )

    return approval_request