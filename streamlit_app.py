import streamlit as st
import requests
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="AI Seamless Pattern Generator", layout="wide")

# -----------------------------
# User API Key
# -----------------------------
st.sidebar.title("API Settings")
api_key = st.sidebar.text_input("Enter your Stability API Key", type="password")

# -----------------------------
# Generate image via API
# -----------------------------
def generate_image(prompt, api_key):
    url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "image/png"
    }
    data = {
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "output_format": "png"
    }

    response = requests.post(url, headers=headers, files=None, data=data)

    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        st.error("API Error: " + response.text)
        return None

# -----------------------------
# Make image seamless
# -----------------------------
def make_seamless(img):
    w, h = img.size
    arr = np.array(img)

    # Shift image by half
    arr = np.roll(arr, shift=w//2, axis=1)
    arr = np.roll(arr, shift=h//2, axis=0)

    # Blend seams
    blend = arr.copy()
    blend[:, :20] = arr[:, :20] // 2 + arr[:, -20:] // 2
    blend[:, -20:] = arr[:, :20] // 2 + arr[:, -20:] // 2
    blend[:20, :] = arr[:20, :] // 2 + arr[-20:, :] // 2
    blend[-20:, :] = arr[:20, :] // 2 + arr[-20:, :] // 2

    return Image.fromarray(blend)

# -----------------------------
# Repeat preview grid
# -----------------------------
def make_preview(tile, repeat=4):
    w, h = tile.size
    canvas = Image.new("RGB", (w * repeat, h * repeat))
    for i in range(repeat):
        for j in range(repeat):
            canvas.paste(tile, (i * w, j * h))
    return canvas

# -----------------------------
# UI
# -----------------------------
st.title("🎨 AI Seamless Pattern Generator (Streamlit Cloud Compatible)")
st.write("Create commercial‑grade seamless patterns from text prompts.")

prompt = st.text_input("Enter your prompt:", "pastel daisy floral, kawaii, crisp edges, modern minimal")
generate = st.button("Generate Pattern")

if generate:
    if not api_key:
        st.error("Please enter your Stability API key in the sidebar.")
    else:
        with st.spinner("Generating image…"):
            img = generate_image(prompt, api_key)

        if img:
            st
