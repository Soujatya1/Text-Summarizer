import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from typing_extensions import Concatenate
from langchain.text_splitter import RecursiveCharacterTextSplitter

#Streamlit interface
st.title("Text Summary Generator")
uploaded_file = st.file_uploader("Upload a PDF file", type = "pdf")

if uploaded_file is not None:
  pdf = PdfReader(uploaded_file)

  #Read text from pdf
  text = ''
  for i, page in enumerate(pdf.pages):
      content = page.extract_text()
      if content:
          text += content
    
  api_key = "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"

  llm = ChatGroq(groq_api_key = api_key, model_name = 'llama-3.1-70b-versatile', temperature = 0.2, top_p = 0.2)

  #Splittting the text
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=50)
  chunks = text_splitter.create_documents([text])

  chain = load_summarize_chain(
    llm,
    chain_type='map_reduce',
    verbose=False
  )
  summary = chain.run(chunks)

  st.write("Summary:")
  st.write(output)
else:
  st.write("Please upload a PDF file.")
