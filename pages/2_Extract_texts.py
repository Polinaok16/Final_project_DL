#!/usr/bin/env python
# coding: utf-8

import os
import io
import pytesseract
import pandas as pd
import streamlit as st
from PIL import Image
from pdf2image import convert_from_bytes

####################################
########## YOUR CODE HERE ##########
####################################
# You will need to download a model
# to implement summarization from 
# HugginFace Hub.
#
# You may want to use following models:
# https://huggingface.co/Falconsai/text_summarization
# https://huggingface.co/knkarthick/MEETING_SUMMARY
# ...or any other you like, but think of 
# the size of the model (<1GB recommended)
#
# Your code may look like this:
from transformers import pipeline

####################################

# page headers and info text
st.set_page_config(
    page_title='Extract text', 
    page_icon=':microscope:'
)
st.sidebar.header('Extract text')
st.header('AI-assistant for text extraction from images and pdf', divider='rainbow')

st.markdown(
    f"""
    You can upload image with text or pdf file.
    The assistantwill etract text and write it on the page.
    """
)
st.divider()

with st.spinner('Please wait, application is initializing...'):
    MODEL_SUM_NAME = 'Falconsai/text_summarization'
    SUMMARIZATOR = pipeline("summarization", model=MODEL_SUM_NAME)

def pdf2img(pdf_bytes):
    """
    Turns pdf file to set of jpeg images.

    """
    images = convert_from_bytes(pdf_bytes.read())
    return images


def ocr_text(img, lang='eng'):
    """
    Takes the text from image.
    
    :lang: language is `eng` by default,
           use `eng+rus` for two languages in document

    """
    text = str(pytesseract.image_to_string(
        img,
        lang=lang
    ))
    return text


def ocr_text_dir(img_dir, lang='eng'):
    """
    Takes the text from images in a folder.

    """
    text = ''
    for img_name in tqdm(sorted(os.listdir(img_dir))):
        if '.jpg' in img_name:
            img = Image.open(f'{IMG_PATH}/{img_name}')
            text_tmp = ocr_text(img, lang=lang)
            text = ' '.join([text, text_tmp])
    return text



st.write('#### Upload you file or image')
uploaded_file = st.file_uploader('Select a file (JPEG or PDF)')
if uploaded_file is not None:
    file_name = uploaded_file.name
    lang = st.selectbox(
            'Select language to extract ',
            ('eng', 'rus', 'eng+rus')
        )
    if '.jpg' in file_name:
        with st.spinner('Please wait...'):
            bytes_data = uploaded_file.read()
            img = Image.open(io.BytesIO(bytes_data))
            
            # image caption model for uploaded image
            text = ocr_text(img, lang=lang)
            st.divider()
            st.write('#### Text extracted')
            st.write(text)
    elif '.pdf' in file_name:
        with st.spinner('Please wait...'):
            imgs = pdf2img(uploaded_file)
            text = ''
            for img in imgs:
                text_tmp = ocr_text(img, lang=lang)
                text = ' '.join([text, text_tmp])
            st.divider()
            st.write('#### Text extracted')
            st.write(text)
    else:
        st.error('File read error', icon='⚠️')

####################################
########## YOUR CODE HERE ##########
####################################
# Use example from the class with
# OCR model for text extracting from 
# the image or PDF file.
#
# Do not forget to add text summarization 
# model and display the output to the OCR 
# application's page  
####################################