from langchain_community.document_loaders import PyPDFLoader


def load_invoice(pdf_path):
    """
    Load invoice PDF and extract text using LangChain.
    """

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    invoice_text = "\n".join(
        document.page_content
        for document in documents
    )

    return invoice_text
