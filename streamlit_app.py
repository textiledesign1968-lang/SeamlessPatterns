import streamlit as st
from openai import OpenAI
from PIL import Image
import numpy as np
import io
import base64

st.set_page_config(page_title="AI Seamless Pattern Generator", layout="wide")

# -----------------------------
# API Key Input
# -----------------------------
st.sidebar.title("API Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# -----------------------------
# Generate image via OpenAI
# -----------------------------
def generate_image(prompt, api_key):
    client = OpenAI(api_key=api_key)

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    return Image.open(io.BytesIO(image_bytes))

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
st.title("🎨 AI Seamless Pattern Generator (Easy Version)")
st.write("Generate sellable seamless prints from text prompts.")

prompt = st.text_input("Enter your prompt:", "elegant tropical leaves, monstera, banana leaf, palm fronds, crisp edges, modern minimal")
generate = st.button("Generate Pattern")

if generate:
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    else:
        with st.spinner("Generating image…"):
            img = generate_image(prompt, api_key)

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
