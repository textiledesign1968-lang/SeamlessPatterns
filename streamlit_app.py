import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import hashlib
import io

st.set_page_config(page_title="Creative Pattern Generator", layout="wide")

st.title("🎨 Creative Pattern Generator (No API, No Keys)")
st.write("Type a prompt and generate a unique abstract seamless pattern.")

# -----------------------------
# Convert prompt → seed number
# -----------------------------
def prompt_to_seed(prompt):
    return int(hashlib.sha256(prompt.encode()).hexdigest(), 16) % (10**8)

# -----------------------------
# Generate abstract pattern
# -----------------------------
def generate_pattern(prompt):
    seed = prompt_to_seed(prompt)
    np.random.seed(seed)

    size = 512
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)

    # Random shapes based on prompt seed
    for _ in range(200):
        x1 = np.random.randint(0, size)
        y1 = np.random.randint(0, size)
        x2 = x1 + np.random.randint(20, 120)
        y2 = y1 + np.random.randint(20, 120)

        color = (
            np.random.randint(50, 200),
            np.random.randint(50, 200),
            np.random.randint(50, 200)
        )

        draw.ellipse([x1, y1, x2, y2], fill=color, outline=None)

    return img

# -----------------------------
# Make seamless
# -----------------------------
def make_seamless(img):
    w, h = img.size
    arr = np.array(img)

    arr = np.roll(arr, shift=w//2, axis=1)
    arr = np.roll(arr, shift=h//2, axis=0)

    return Image.fromarray(arr)

# -----------------------------
# Repeat preview
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
prompt = st.text_input("Enter your prompt:", "tropical leaves, emerald, jade, teal")
generate = st.button("Generate Pattern")

if generate:
    img = generate_pattern(prompt)

    st.subheader("Generated Abstract Pattern")
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
