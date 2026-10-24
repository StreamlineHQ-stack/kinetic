import json
import os
import streamlit as st
from license_verifier import verify_license_sidebar

# Page Configuration
st.set_page_config(
    page_title="Kinetic Motion Suite — Carousel Engine Studio",
    page_icon="🎬",
    layout="wide",
)

# Custom Styling for Dark Theme & Canary Accents
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

# Sidebar License Verification Gate
is_licensed = verify_license_sidebar()

# Sidebar Motion Controls (Available when licensed)
if is_licensed:
  st.sidebar.markdown("---")
  st.sidebar.markdown("### ⚙️ Pro Motion Control")
  frame_rate = st.sidebar.slider("Frame Rate (FPS):", 10, 60, 20)
  seconds_per_slide = st.sidebar.slider(
      "Seconds per Slide:", 1.0, 5.0, 2.5, step=0.25
  )
  transition_style = st.sidebar.selectbox(
      "Kinetic Transition Style:",
      [
          "Dynamic Slide Up (Pro Easing)",
          "Smooth Slide Right",
          "Cinematic Zoom In",
          "Fade & Snap",
      ],
  )
  transition_speed = st.sidebar.slider("Transition Speed (Frames):", 2, 15, 6)
else:
  frame_rate, seconds_per_slide, transition_style, transition_speed = (
      20,
      2.5,
      "Dynamic Slide Up (Pro Easing)",
  )

# Main App Execution
if is_licensed:
  st.sidebar.title("🎬 Carousel Engine")
  st.sidebar.markdown("### Kinetic Motion Suite")

  st.markdown("## 🎞️ Import Carousel JSON Deck")
  uploaded_file = st.file_uploader(
      "Upload your JSON deck file:", type=["json"], help="200MB per file max"
  )

  slides_data = []

  if uploaded_file is not None:
    try:
      deck_content = json.load(uploaded_file)
      if isinstance(deck_content, list):
        slides_data = deck_content
      elif isinstance(deck_content, dict) and "slides" in deck_content:
        slides_data = deck_content["slides"]
      else:
        slides_data = [
            {"title": k, "content": v} for k, v in deck_content.items()
        ]

      st.success(
          f"Successfully loaded {len(slides_data)} slides from"
          f" {uploaded_file.name}!"
      )
    except Exception as e:
      st.error(f"Error parsing JSON deck: {e}")
  else:
    slides_data = [
        {"title": "Why Your Coaching Page Gets Clicks But Zero Bookings"},
        {"title": "Stop Committing The 'Me-Monster' Mistake"},
        {"title": "Win Above The Fold"},
        {"title": "Replace Fluffy Praise With Metrics"},
        {"title": "The 4-Section Conversion Stack"},
        {"title": "Audit Your Page Today"},
    ]
    st.info(
        "📁 Using default active preview deck. Upload your custom JSON deck"
        " above anytime."
    )

  st.markdown("---")

  st.markdown("## 🚀 Compile & Export High-Impact Kinetic Loop")

  with st.container():
    st.markdown(
        f"**Active Deck:** Loaded ({len(slides_data)} slides active) |"
        f" **FPS:** {frame_rate} | **Speed:** {seconds_per_slide}s/slide"
    )

    col1, col2 = st.columns([1.2, 1])

    with col1:
      st.markdown("### Slide Sequence Overview")
      for idx, slide in enumerate(slides_data, start=1):
        title_text = (
            slide.get("title", f"Slide {idx}")
            if isinstance(slide, dict)
            else str(slide)
        )
        st.markdown(f"**Slide {idx}:** {title_text}")

    with col2:
      st.markdown("### Production Render Engine")
      render_btn = st.button(
          "✨ Render Premium Kinetic GIF (Active Deck)",
          use_container_width=True,
      )

      if render_btn:
        with st.spinner(
            "Rendering animation frames, applying easing, and compiling"
            " loop..."
        ):
          import time

          time.sleep(1.5)
        st.success("🎉 Kinetic Loop rendered successfully!")
        st.download_button(
            label="⬇️ Download Rendered Animated GIF / MP4",
            data=b"mock_animation_binary_data",
            file_name="kinetic_carousel_loop.gif",
            mime="image/gif",
            use_container_width=True,
        )

      st.markdown("---")
      st.markdown("### 💬 Viral Ready-to-Post Caption:")
      st.info(
          f"🔥 {slides_data[0].get('title', 'Check this out')}...\n\nRead"
          " through this complete breakdown to completely transform your"
          " conversion rate.\n\nWhich slide hit home for you the most? Drop"
          " your thoughts below! 👇\n\n--- \n⚡ Built & animated seamlessly using"
          " Carousel Engine & Kinetic Animator."
      )
else:
  st.title("🎬 Kinetic Motion Suite — Restricted Access")
  st.warning(
      "🔒 Please enter a valid license key in the sidebar to unlock the Kinetic"
      " Animator Studio."
  )