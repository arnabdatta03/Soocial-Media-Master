import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

st.title('Social Media Master')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

API_KEY = st.text_input("Enter your API Key:  Get your Google Studio API key from [here](https://makersuite.google.com/app/apikey)", type="password")


translate_bengali = st.checkbox("Generate Bengali Caption")
translate_hindi = st.checkbox("Generate Hindi Caption")

if uploaded_file is not None:
    if st.button('Upload'):
        if API_KEY.strip() == '':
            st.error('Enter a valid API key')
        else:
            temp_dir = "temp"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            img = Image.open(file_path)
            try:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                if translate_bengali:
                    caption_bn = model.generate_content(["Write a caption for the image in Bengali", img])
                    tags_bn = model.generate_content(["Generate 5 hashtags for the image in Bengali", img])
                    st.image(img, caption=f"Bengali Caption: {caption_bn.text}")
                    st.write(f"Tags: {tags_bn.text}")
                elif translate_hindi:
                    caption_hi = model.generate_content(["Write a caption for the image in Hindi", img])
                    tags_hi = model.generate_content(["Generate 5 hashtags for the image in Hindi", img])
                    st.image(img, caption=f"Hindi Caption: {caption_hi.text}")
                    st.write(f"Tags: {tags_hi.text}")
                else:
                    caption = model.generate_content(["Write a caption for the image in English", img])
                    tags = model.generate_content(["Generate 5 hashtags for the image in English", img])
                    st.image(img, caption=f"Caption: {caption.text}")
                    st.write(f"Tags: {tags.text}")
                
            except Exception as e:
                error_msg = str(e)
                if "API_KEY_INVALID" in error_msg:
                    st.error("Invalid API Key. Please enter a valid API Key.")
                else:
                    st.error(f"Failed to configure API due to {error_msg}")


footer = """
  <style>
        a:link, a:visited {
            color: blue;
            text-decoration: dotted;
        }

        a:hover, a:active {
            color: skyblue;
        }
        .footer .p{
            font-size:10px;
        }

        .footer {
            position:fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            height:10%;
            font-size:15px;
            color: white; 
            text-align: center;
            padding: 10px 0; 
        }
        .footer p{
            font-size:20px;
        }

        .footer a:hover {
            color: white;
        }
    </style>

    <div class="footer">
        <p>Developed ❤ by <a href="https://arnabdatta03.github.io/" target="_blank">DELTA Team</a></p>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)
