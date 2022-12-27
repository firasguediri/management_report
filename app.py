import streamlit as st
import pdf2image
from pdf2image import convert_from_path
import pytesseract
from deep_translator import GoogleTranslator
import openai
import tabula
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

import pandas as pd
def from_pdf_bytes_to_image_to_text(uploaded_pdf: bytes) -> str:
  
    pdf_pages = pdf2image.convert_from_bytes(uploaded_pdf, dpi=200)
    st.image(pdf_pages[0])
    text = pytesseract.image_to_string(pdf_pages[0])
    first_line = text.find("ACTIFS")
    last_line = text.find("TOTAL DES ACTIFS:")
    
    translated = GoogleTranslator(source='auto', target='en').translate(text[first_line:last_line])
    
    return translated




pdf_file = st.file_uploader("Choisir un ficher de votre ordinateur")
if pdf_file is not None:
  text = from_pdf_bytes_to_image_to_text(pdf_file.getvalue())
  col1,col2,col3 = st.columns([2,1,2])
  if col2.button("Extraire le rapport"):
    openai.api_key = "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"
    
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="write  buisness report using the text below:                                                                                " + text ,
    temperature=0.7,
    max_tokens=700,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    translated = GoogleTranslator(source='auto', target='fr').translate(response["choices"][0]["text"])
    print(response)
    st.write(translated)