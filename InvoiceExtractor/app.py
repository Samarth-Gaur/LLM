from dotenv import load_dotenv 

## Now we will load all the environment variables from .env file
load_dotenv()

import streamlit as st 
import os 
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Now we will load Gemini Pro Vision
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input, image, prompt):
    response=model.generate_content([input, image[0], prompt])
    return response.text 

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Reading the file into bytes 
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        return FileNotFoundError("No File Provided")

# Now we will create a streamlit application

st.set_page_config(page_title="MULTI LANGUAGE INVOICE EXTRACTOR")

st.header("MULTI LANGUAGE INVOICE EXTRACTOR")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an Image of Invoice...", type=["jpg", "jpeg", "png"])

# Detecting whether user has input any image or not
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
submit = st.button("Tell me some specifications of the Invoice")

# Now we will guide our model to behave accordingly
input_prompt = """
You are an expert in understanding invoices. We will upload the image of an invoice and
you will have to answer any question based on the uploaded invoice image 
""" 

# if submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Here is your Response: ")
    st.write(response)
    


