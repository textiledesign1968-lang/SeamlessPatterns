import streamlit as st
import requests
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="AI Seamless Pattern Generator", layout="wide")

# -----------------------------
# API Key Input
# -----------------------------
st.sidebar.title("API Settings")
api_key = st.sidebar.text_input("Enter your Stability API Key", type="password")

# -----------------------------
# Generate image via Stability API (Correct Format)
# -----------------------------
def generate_image(prompt, api_key):
    url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "image/*"
    }

    files = {
        "prompt": (None, prompt),
        "aspect_ratio": (None, "1:1"),
        "output_format": (None, "png")
    }

    response = requests.post(url, headers=headers, files=files)

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

    arr = np.roll(arr, shift=w//2, axis=1)
    arr = np.roll(arr, shift=h//2, axis=0)

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
st.title("🎨 AI Seamless Pattern Generator (Stability API)")
st.write("Create commercial‑grade seamless patterns from text prompts.")

prompt = st.text_input("Enter your prompt:", "elegant tropical leaves, monstera, banana leaf, palm fronds, crisp edges, modern minimal")
generate = st.button("Generate Pattern")

if generate:
    if not api_key:
        st.error("Please enter your Stability API key in the sidebar.")
    else:
        with st.spinner("Generating image…"):
            img = generate_image(prompt, api_key)

        if img:
            st.subheader("Original AI Image")
            st.image(img, use_column_width=True)

            seamless = make_seamless(img)

            st.subheader("Seamless Tile")
            st.image(seamless, use_column_width=True)

            preview = make_preview(seamless, repeat=4)

            st.subheader("Repeat Preview")
            st.image(preview, use_column_width=True)

            buf = io.BytesIO()
            seamless.save(buf, format="PNG")
            st.download_button("Download Seamless Tile", buf.getvalue(), "seamless_tile.png")
