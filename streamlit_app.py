import streamlit as st
import torch
from diffusers import AutoPipelineForText2Image
from PIL import Image
import io

st.set_page_config(page_title="AI Seamless Pattern Generator", layout="wide")

# -----------------------------
# Load SDXL Tile Diffusion Model
# -----------------------------
@st.cache_resource
def load_model():
    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sdxl-tile-controlnet",
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True
    ).to("cuda")
    return pipe

pipe = load_model()

# -----------------------------
# Generate Seamless Tile
# -----------------------------
def generate_seamless_tile(prompt):
    result = pipe(
        prompt=prompt,
        guidance_scale=7.5,
        tile_size=1024,       # TRUE seamless generation
        tile_overlap=128,     # smooth edges
        num_inference_steps=40
    )
    return result.images[0]

# -----------------------------
# Create Repeat Preview Grid
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
st.title("🎨 AI Seamless Pattern Generator")
st.write("Create commercial‑grade seamless patterns from text prompts.")

prompt = st.text_input("Enter your prompt:", "pastel daisy floral, kawaii, crisp edges, modern minimal")
generate = st.button("Generate Pattern")

if generate:
    with st.spinner("Generating seamless pattern…"):
        tile = generate_seamless_tile(prompt)

    st.subheader("Seamless Tile")
    st.image(tile, use_column_width=True)

    preview = make_preview(tile, repeat=4)

    st.subheader("Repeat Preview")
    st.image(preview, use_column_width=True)

    # Download tile
    buf = io.BytesIO()
    tile.save(buf, format="PNG")
    st.download_button("Download Seamless Tile", buf.getvalue(), "seamless_tile.png")
