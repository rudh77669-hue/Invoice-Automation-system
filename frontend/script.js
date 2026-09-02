// const invoiceFile = document.getElementById("invoiceFile");

// const chooseFileButton =
//     document.getElementById("chooseFileButton");

// const selectedFile =
//     document.getElementById("selectedFile");

// const analyzeButton =
//     document.getElementById("analyzeButton");

// const loadingSection =
//     document.getElementById("loadingSection");

// const resultSection =
//     document.getElementById("resultSection");


// /* =========================
//    CHOOSE FILE
// ========================= */

// chooseFileButton.addEventListener("click", () => {
//     invoiceFile.click();
// });


// /* =========================
//    FILE SELECTED
// ========================= */

// invoiceFile.addEventListener("change", () => {

//     const file = invoiceFile.files[0];

//     if (!file) {

//         selectedFile.textContent = "";

//         analyzeButton.disabled = true;

//         return;
//     }


//     if (file.type !== "application/pdf") {

//         selectedFile.textContent =
//             "Please select a PDF invoice.";

//         analyzeButton.disabled = true;

//         return;
//     }


//     selectedFile.textContent =
//         `Selected: ${file.name}`;

//     analyzeButton.disabled = false;

// });


// /* =========================
//    ANALYZE INVOICE
// ========================= */

// analyzeButton.addEventListener("click", async () => {

//     const file = invoiceFile.files[0];

//     if (!file) {
//         return;
//     }


//     loadingSection.classList.remove("hidden");

//     resultSection.classList.add("hidden");

//     analyzeButton.disabled = true;


//     try {

//         const formData = new FormData();

//         /*
//          * IMPORTANT:
//          * Flask expects the uploaded file
//          * under the field name "file".
//          */
//         formData.append("file", file);


//         /*
//          * FRONTEND → FLASK
//          *
//          * Do NOT put the n8n webhook URL here.
//          *
//          * Flask will call n8n through n8n_client.py.
//          */
//         const response = await fetch(
//             "http://127.0.0.1:5000/api/invoice/analyze",
//             {
//                 method: "POST",
//                 body: formData
//             }
//         );


//         const data = await response.json();


//         if (!response.ok || !data.success) {

//             throw new Error(
//                 data.error || "Invoice analysis failed."
//             );

//         }


//         console.log("Backend response:", data);


//         /*
//          * Display invoice + AI decision
//          */
//         displayResult(
//             data.invoice,
//             data.decision
//         );


//         resultSection.classList.remove("hidden");


//     } catch (error) {

//         console.error("Invoice analysis error:", error);

//         alert(
//             "Invoice analysis failed:\n" +
//             error.message
//         );

//     } finally {

//         loadingSection.classList.add("hidden");

//         analyzeButton.disabled = false;

//     }

// });


// /* =========================
//    DISPLAY RESULT
// ========================= */

// function displayResult(invoice, decision) {

//     document.getElementById("vendor").textContent =
//         invoice.vendor ?? "-";


//     document.getElementById("invoiceNumber").textContent =
//         invoice.invoice_number ?? "-";


//     document.getElementById("invoiceDate").textContent =
//         invoice.invoice_date ?? "-";


//     document.getElementById("dueDate").textContent =
//         invoice.due_date ?? "-";


//     document.getElementById("subtotal").textContent =
//         invoice.subtotal != null
//             ? `₹${invoice.subtotal}`
//             : "-";


//     document.getElementById("tax").textContent =
//         invoice.tax != null
//             ? `₹${invoice.tax}`
//             : "-";


//     document.getElementById("total").textContent =
//         invoice.total != null
//             ? `₹${invoice.total}`
//             : "-";


//     document.getElementById("currency").textContent =
//         invoice.currency ?? "-";


//     /* =========================
//        RISK
//     ========================= */

//     const riskLevel =
//         document.getElementById("riskLevel");

//     riskLevel.textContent =
//         `${decision.risk_level} RISK`;


//     /* =========================
//        DECISION
//     ========================= */

//     const decisionText =
//         document.getElementById("decisionText");


//     if (decision.approval_required) {

//         decisionText.textContent =
//             "Human approval is required before this invoice can be processed.";

//     } else {

//         decisionText.textContent =
//             "This invoice can be processed automatically.";

//     }


//     /* =========================
//        REASON
//     ========================= */

//     document.getElementById("decisionReason").textContent =
//         decision.reason ?? "-";


//     /* =========================
//        STATUS BADGE
//     ========================= */

//     const statusBadge =
//         document.getElementById("statusBadge");


//     if (decision.approval_required) {

//         statusBadge.textContent =
//             "AWAITING APPROVAL";

//     } else {

//         statusBadge.textContent =
//             "AUTO APPROVED";

//     }


//     /* =========================
//        APPROVAL WORKFLOW STEP
//     ========================= */

//     const approvalStep =
//         document.getElementById("approvalStep");


//     if (decision.approval_required) {

//         approvalStep.classList.remove("completed");

//         approvalStep.classList.add("pending");

//         approvalStep.querySelector("div").textContent = "3";

//     } else {

//         approvalStep.classList.remove("pending");

//         approvalStep.classList.add("completed");

//         approvalStep.querySelector("div").textContent = "✓";

//     }

// }

const invoiceFile = document.getElementById("invoiceFile");

const chooseFileButton =
    document.getElementById("chooseFileButton");

const selectedFile =
    document.getElementById("selectedFile");

const analyzeButton =
    document.getElementById("analyzeButton");

const loadingSection =
    document.getElementById("loadingSection");

const successSection =
    document.getElementById("successSection");

const resultSection =
    document.getElementById("resultSection");


/* =========================
   CHOOSE FILE
========================= */

chooseFileButton.addEventListener("click", () => {

    invoiceFile.click();

});


/* =========================
   FILE SELECTED
========================= */

invoiceFile.addEventListener("change", () => {

    const file = invoiceFile.files[0];

    if (!file) {

        selectedFile.textContent = "";

        analyzeButton.disabled = true;

        return;
    }


    if (file.type !== "application/pdf") {

        selectedFile.textContent =
            "Please select a PDF invoice.";

        analyzeButton.disabled = true;

        return;
    }


    selectedFile.textContent =
        `Selected: ${file.name}`;

    analyzeButton.disabled = false;


    // Hide previous messages/results
    successSection.classList.add("hidden");

    resultSection.classList.add("hidden");

});


/* =========================
   SUBMIT INVOICE
========================= */

analyzeButton.addEventListener("click", async () => {

    const file = invoiceFile.files[0];

    if (!file) {
        return;
    }


    /* -------------------------
       SHOW PROCESSING
    ------------------------- */

    loadingSection.classList.remove("hidden");

    successSection.classList.add("hidden");

    resultSection.classList.add("hidden");

    analyzeButton.disabled = true;


    try {

        const formData = new FormData();

        /*
         * Flask expects:
         *
         * request.files["file"]
         */

        formData.append("file", file);


        /* -------------------------
           SEND TO FLASK
        ------------------------- */

        const response = await fetch(
            "http://127.0.0.1:5000/api/invoice/analyze",
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        console.log("Backend response:", data);


        /* -------------------------
           CHECK RESPONSE
        ------------------------- */

        if (!response.ok || !data.success) {

            throw new Error(
                data.error || "Invoice submission failed."
            );

        }


        /* -------------------------
           INVOICE SUBMITTED
        ------------------------- */

        /*
         * IMPORTANT:
         *
         * We DO NOT wait for:
         *
         * AI analysis
         * Rule engine
         * Approval
         * n8n
         * Email
         *
         * Flask has already accepted the invoice.
         */

        successSection.classList.remove("hidden");


        /*
         * Hide processing
         */

        loadingSection.classList.add("hidden");


        /*
         * Scroll to success message
         */

        successSection.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });


        console.log(
            "Invoice submitted successfully."
        );


    } catch (error) {

        console.error(
            "Invoice submission error:",
            error
        );


        loadingSection.classList.add("hidden");


        alert(
            "Invoice submission failed:\n" +
            error.message
        );


    } finally {

        analyzeButton.disabled = false;

    }

});