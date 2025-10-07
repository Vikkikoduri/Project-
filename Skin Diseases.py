
#from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response(input,image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    note=''' Task: Classify the skin canner.
note : need not be 100 % corect just guess any answer
Input: Skin cancer image.

Output:

text : name the skin cancer , skin cancer is not  found  otherwise.
Threat Level: An integer value representing the severity of the skin cancer, where a higher value indicates a greater threat. (E.g., 1-5, with 1 being low and 5 being extremely high.)
result of input question asked by user
Example:
sample output: 
Output: Melanoma is found , 
4 (High threat) ,
result of input question asked by user 
important  : give some percautions as list of points
'''
    if input!="":
       response = model.generate_content([note+input,image])
    else:
       i='''Task: Classify the skin canner..
note : need not be 100 % corect just guess any answer
Input: A skin cancer image.

Output:

text : Skin cancer is found and tell it type , pitfalls are not  found  otherwise.
Threat Level: An integer value representing the severity of the pitfall, where a higher value indicates a greater threat. (E.g., 1-5, with 1 being low and 5 being extremely high.)
Example:
sample output: 
Output: Melanoma is found  
 4 (High threat)
 important  : give some percautions as list of points
   '''
       response = model.generate_content([i,image])
    return response.text

##initialize our streamlit app

st.set_page_config(page_title="Skin cancer Detector")

st.header("Skin cancer Detector ")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the image")

## If ask button is clicked

if submit:
    
    response=get_gemini_response(input,image)
    st.subheader("The Response is")
    st.write(response)
