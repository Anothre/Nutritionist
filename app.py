from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

load_dotenv()
from PIL import Image
if "GOOGLE_API_KEY" in st.secrets:
    st.write(
        "Has environment variables been set:",
        os.environ["GOOGLE_API_KEY"] == st.secrets["GOOGLE_API_KEY"]
    )
else:
    st.error("GOOGLE_API_KEY is not set in secrets. Please add it to secrets.toml.")
    
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    #Check if a file has been uploaded
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data=uploaded_file.getvalue()

        image_parts =[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")




st.header("Gemini Health App")
uploaded_file=st.file_uploader("Choose an image...",type=["jpg","png","jpeg"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Tell me about the total calories")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of
every food items with calories intake
in below format

1. Item 1 - no of calories
2. Item 2 - no of calories
----
----
Finally you can also mention whether the food is healthy or not
and also mention the percentage split of the ratio of carbohydrates, fats, fibers, sugar and
things required in our diet
"""

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.subheader("The response is:")
    st.write(response)
