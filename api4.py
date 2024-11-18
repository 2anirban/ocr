#Set up load env
import os
import base64
import requests
import fitz  # PyMuPDF
import json
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
from openai.types.chat.chat_completion import ChatCompletion
load_dotenv()


# Get the PDF document and convert it into image(PNG)
#Create a streamlit app for uploading the pdf document

#https://api.openai.com/v1/chat/completions
client= OpenAI()
LLM= os.environ.get("OPEN_AI_MODEL")
api_key = os.environ.get("OPENAI_API_KEY")


def convert_pdf_to_images(pdf_path):
    pdf_file = fitz.open(pdf_path)
    image_files = []

    for page_num in range(pdf_file.page_count):
        page = pdf_file.load_page(page_num)  # Load the page
        pixmap = page.get_pixmap()  # Get the pixmap (image) of the page
        output_name = f"page-{page_num + 1}.png"  # Define output file name
        pixmap.save(output_name)  # Save the image
        image_files.append(output_name)  # Add to list of image files

    pdf_file.close()
    return image_files

#img=convert_pdf_to_images(pdf_path)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

#image_path="image/image-1.png"
#bs64_image=encode_image(image_path)
# def ask_openai(
#     user_question: str,
#     temperature: float = 1.0,
#     top_p: float = 1.0,
#     max_tokens: int = 500,
# ) -> requests.Response:
#     print(f"LLM : {LLM}")

#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

#     payload = {
#         "model": "gpt-4o-mini",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": user_question},
#                     {
#                         "type": "image_url",
#                         "image_url": {"url": f"data:image/jpeg;base64,{bs64_image}"},
#                     },
#                 ],
#             }
#         ],
#         "max_tokens": max_tokens,
#         "temperature": temperature,
#     }

#     response = requests.post(
#         "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
#     )

#     print(f"response  type : {type(response)}")
#     return response

user_question = """Hello, Extract the info from this finance doc image in json format.
         Do not include ```json in the response."""

def main():
    st.title("PDF to Image and OpenAI Integration")
    st.write("Upload a PDF file, convert it to images, and send them to OpenAI API based on your question.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file:
        st.success(f"Uploaded file: {uploaded_file.name}")

        # Save uploaded file temporarily
        with open("temp_uploaded.pdf", "wb") as temp_file:
            temp_file.write(uploaded_file.getbuffer())

        # Convert PDF to images
        image_files = convert_pdf_to_images("temp_uploaded.pdf")

        # Encode each image file to Base64
        encoded_images = []
        for image_file in image_files:
            bs64_image = encode_image(image_file)
            #encoded_images.append(encoded_image)
            st.write(f"Encoded image {image_file}:")
            #st.text(encoded_image[:100])  # Display the first 100 characters of the Base64 string for preview


   
        

            # Convert PDF to images
        # image_files = convert_pdf_to_images("temp_uploaded.pdf")
        # bs64_image=encode_image(image_files)

    
        def ask_openai(
                user_question: str,
                temperature: float = 1.0,
                top_p: float = 1.0,
                max_tokens: int = 500,
                ) -> requests.Response:
            print(f"LLM : {LLM}")

            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_question},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{bs64_image}"},
                            },
                        ],
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
            )

            print(f"response  type : {type(response)}")
            return response
        
        response = ask_openai(user_question)

        response_json = response.content
        print(response_json)


        

        # response_dict = json.loads(response_json)

        # content = response_dict["choices"][0]["message"]["content"]
        # clean_content_dict = json.loads(content)
        # clean_content_json = json.dumps(clean_content_dict, indent=4)
        # print(clean_content_json)
       
        # st.write(clean_content_json)




if __name__ == "__main__":
    main()