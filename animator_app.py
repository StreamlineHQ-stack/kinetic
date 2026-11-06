import io
import json
import os
import base64
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Page Configuration
st.set_page_config(
    page_title="Kinetic Motion Suite — Carousel Engine Studio",
    page_icon="🎬",
    layout="wide",
)

# --- STATE & DECK INITIALIZATION ---
if "slides_data" not in st.session_state:
    st.session_state.slides_data = None

# Try loading deck from query params if passed from Carousel Studio / SIA
try:
    deck_param = st.query_params.get("deck", None)
    if deck_param and st.session_state.slides_data is None:
        encoded_deck = deck_param[0] if isinstance(deck_param, list) else deck_param
        padded_deck = encoded_deck + "=" * (-len(encoded_deck) % 4)
        decoded_bytes = base64.urlsafe_b64decode(padded_deck.encode("utf-8"))
        deck_content = json.loads(decoded_bytes.decode("utf-8"))
        if isinstance(deck_content, list) and len(deck_content) > 0:
            st.session_state.slides_data = deck_content
except Exception:
    pass

# Fallback default slides if nothing is loaded yet
if st.session_state.slides_data is None:
    st.session_state.slides_data = [
        {
            "category": "HOOK",
            "title": "Welcome to Kinetic Motion Suite",
            "content": "Transform static slide decks into high-impact animated loops instantly.",
            "bg_color": "#000000"
        }
    ]

# Custom Dark Styling
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #ffcc00;
        color: #0e1117;
        font-weight: bold;
        border-radius: 6px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #e6b800;
        color: #0e1117;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Motion Controls
st.sidebar.title("🎬 Kinetic Motion Suite")
st.sidebar.markdown("---")
frame_rate = st.sidebar.slider("Frame Rate (FPS):", 10, 60, 20)
seconds_per_slide = st.sidebar.slider("Seconds per Slide:", 1.0, 5.0, 2.5, step=0.25)

def wrap_text_to_width(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if draw.textlength(test_line, font=font) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

# Main UI
st.markdown("## 🎞️ Kinetic Animator Workspace")
st.success(f"🚀 Active Deck Loaded: {len(st.session_state.slides_data)} slide(s) ready for animation.")

# JSON Upload Fallback
uploaded_file = st.file_uploader("Or upload a JSON deck file manually:", type=["json"])
if uploaded_file is not None:
    try:
        deck_content = json.load(uploaded_file)
        if isinstance(deck_content, list):
            st.session_state.slides_data = deck_content
            st.success(f"Successfully loaded {len(deck_content)} slides from {uploaded_file.name}!")
            st.rerun()
    except Exception as e:
        st.error(f"Error parsing uploaded JSON: {e}")

st.markdown("---")
st.markdown("## 🚀 Compile & Export High-Impact Kinetic Loop")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("### Slide Sequence Overview")
    for idx, slide in enumerate(st.session_state.slides_data, start=1):
        title_text = slide.get("title", f"Slide {idx}") if isinstance(slide, dict) else str(slide)
        st.markdown(f"**Slide {idx}:** {title_text}")

with col2:
    st.markdown("### Production Render Engine")
    if st.button("✨ Render Premium Kinetic Loop", use_container_width=True):
        with st.spinner("Rendering animation frames..."):
            frames = []
            width, height = 1080, 1080
            max_text_width = 880

            try:
                badge_font = ImageFont.truetype("arialbd.ttf", 28)
                title_font = ImageFont.truetype("arialbd.ttf", 52)
                body_font = ImageFont.truetype("arialbd.ttf", 36)
                footer_font = ImageFont.truetype("arialbd.ttf", 24)
            except IOError:
                badge_font = title_font = body_font = footer_font = ImageFont.load_default()

            total_slides = len(st.session_state.slides_data)
            for idx, slide in enumerate(st.session_state.slides_data, start=1):
                if isinstance(slide, dict):
                    category = str(slide.get("category", f"STEP {idx}")).upper()
                    title = str(slide.get("title", f"Slide {idx}"))
                    body = str(slide.get("content", ""))
                    bg_hex = slide.get("bg_color", "#000000")
                else:
                    category = f"STEP {idx}"
                    title = str(slide)
                    body = ""
                    bg_hex = "#000000"

                img = Image.new("RGB", (width, height), color=bg_hex)
                draw = ImageDraw.Draw(img)

                margin_x, current_y = 100, 160
                draw.text((margin_x, current_y), f"SLIDE {idx} OF {total_slides} • {category}", fill="#ffcc00", font=badge_font)
                current_y += 70

                for line in wrap_text_to_width(title, title_font, max_text_width, draw):
                    draw.text((margin_x, current_y), line, fill="#ffffff", font=title_font)
                    current_y += 65

                current_y += 30
                if body:
                    for line in wrap_text_to_width(body, body_font, max_text_width, draw):
                        draw.text((margin_x, current_y), line, fill="#d1d1d1", font=body_font)
                        current_y += 48

                draw.text((width - 380, height - 100), "Nikki's Salon • ApexMorph", fill="#d1d1d1", font=footer_font)
                frames.append(img)

            # Render GIF buffer
            gif_buffer = io.BytesIO()
            if frames:
                frames[0].save(
                    gif_buffer,
                    format="GIF",
                    save_all=True,
                    append_images=frames[1:],
                    duration=int(seconds_per_slide * 1000),
                    loop=0,
                )
            gif_bytes = gif_buffer.getvalue()

            # Render MP4 video buffer
            mp4_bytes = None
            try:
                import imageio
                import numpy as np

                fps = int(frame_rate)
                frames_per_slide = int(fps * seconds_per_slide)
                paced_frames = []
                for f in frames:
                    np_f = np.array(f)
                    for _ in range(frames_per_slide):
                        paced_frames.append(np_f)

                mp4_path = "temp_animator.mp4"
                imageio.mimwrite(mp4_path, paced_frames, fps=fps, codec="libx264", quality=8, pixelformat="yuv420p")
                with open(mp4_path, "rb") as mf:
                    mp4_bytes = mf.read()
                os.remove(mp4_path)
            except Exception:
                mp4_bytes = None

        st.success("🎉 Kinetic Loop rendered successfully!")
        
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.download_button("⬇️ Download Animated GIF", data=gif_bytes, file_name="kinetic_loop.gif", mime="image/gif", use_container_width=True)
        with d_col2:
            if mp4_bytes:
                st.download_button("🎬 Download Instagram MP4", data=mp4_bytes, file_name="kinetic_loop.mp4", mime="video/mp4", use_container_width=True)
            else:
                st.info("MP4 export requires imageio-ffmpeg.")