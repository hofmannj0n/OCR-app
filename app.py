
import streamlit as st
import os

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

API_KEY = st.secrets['API_KEY']
ENDPOINT = st.secrets["ENDPOINT"]

def extract_text_from_document(document_path):
    document_analysis = DocumentAnalysisClient(endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY))

    with open(document_path, 'rb') as f:
        poller = document_analysis.begin_analyze_document("prebuilt-document", f.read())
        result = poller.result()

        extracted_text = " "

        for page in result.pages:
            for line in page.lines:
                extracted_text += line.content + " "

        return extracted_text.strip()
    
st.header('PDF Text Extraction', divider='rainbow')

uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])

if uploaded_file is not None:
    
    st.write("Uploaded PDF file:", uploaded_file.name)

    st.write("Running OCR...")

    # saving file temporarily
    temp_file_path = "/tmp/uploaded_pdf.pdf"
    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(uploaded_file.read())

    # text extract
    extracted_text = extract_text_from_document(temp_file_path)

    # removing temporary save 
    os.remove(temp_file_path)

    st.text_area("Extracted Text From Document:", extracted_text)