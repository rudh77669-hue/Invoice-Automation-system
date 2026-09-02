# ============================================================
# INVOICE RULE ENGINE
# ============================================================

APPROVAL_THRESHOLD = 50000


def evaluate_invoice(invoice_data):

    total = invoice_data.get("total")

    if total is None:
        raise ValueError(
            "Invoice total is missing."
        )

    # ========================================================
    # HIGH VALUE INVOICE
    # ========================================================

    if total > APPROVAL_THRESHOLD:

        return {
            "decision": "HUMAN_APPROVAL",
            "risk_level": "HIGH",
            "reason": (
                f"Invoice total ₹{total} is above "
                f"the approval threshold of "
                f"₹{APPROVAL_THRESHOLD}."
            ),
            "approval_required": True
        }

    # ========================================================
    # LOW VALUE INVOICE
    # ========================================================

    return {
        "decision": "AUTO_PROCESS",
        "risk_level": "LOW",
        "reason": (
            f"Invoice total ₹{total} is within "
            f"the automatic processing limit."
        ),
        "approval_required": False
    }