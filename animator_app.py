import io
import json
import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
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
      6,
  )


# Pixel-perfect text wrapping helper function
def wrap_text_to_width(text, font, max_width, draw):
  words = text.split()
  lines = []
  current_line = []
  for word in words:
    test_line = " ".join(current_line + [word])
    # Use getlength for precise pixel measurement
    if draw.textlength(test_line, font=font) <= max_width:
      current_line.append(word)
    else:
      if current_line:
        lines.append(" ".join(current_line))
      current_line = [word]
  if current_line:
    lines.append(" ".join(current_line))
  return lines


# Main App Execution
if is_licensed:
  st.sidebar.title("🎬 Carousel Engine")
  st.sidebar.markdown("### Kinetic Motion Suite")

  st.markdown("## 🎞️ Import Carousel JSON Deck")

  # Initialize session state for slides if not present
  if "slides_data" not in st.session_state:
    st.session_state.slides_data = [
        {
            "badge": "SLIDE 1 • HOOK",
            "title": "Why Your Coaching Page Gets Clicks But Zero Bookings",
            "body": (
                "Most coaches optimize for traffic instead of conversion"
                " friction points."
            ),
        },
        {
            "badge": "SLIDE 2 • THE MYTH",
            "title": "Stop Committing The 'Me-Monster' Mistake",
            "body": (
                "Your bio talks about you instead of addressing the client's"
                " exact pain."
            ),
        },
        {
            "badge": "SLIDE 3 • ROOT CAUSE",
            "title": "Win Above The Fold",
            "body": (
                "Visitors decide within 3 seconds whether to stay or bounce."
            ),
        },
        {
            "badge": "SLIDE 4 • SOLUTION",
            "title": "Replace Fluffy Praise With Metrics",
            "body": (
                "Specific conversion numbers build instant authority and trust."
            ),
        },
        {
            "badge": "SLIDE 5 • FRAMEWORK",
            "title": "The 4-Section Conversion Stack",
            "body": "Hook, Agitation, Solution, and Frictionless Call-to-Action.",
        },
        {
            "badge": "SLIDE 6 • CTA",
            "title": "Audit Your Page Today",
            "body": (
                "Click the link in bio to run your full conversion audit"
                " instantly."
            ),
        },
    ]

  # Hybrid Input: Streamlit Cloud Uploader + Local Workspace Selector
  uploaded_file = st.file_uploader(
      "Upload JSON deck file (Cloud / Live Mode):",
      type=["json"],
      help="Drop your exported JSON file here",
  )

  deck_loaded = False

  if uploaded_file is not None:
    try:
      deck_content = json.load(uploaded_file)
      if isinstance(deck_content, list):
        st.session_state.slides_data = deck_content
      elif isinstance(deck_content, dict) and "slides" in deck_content:
        st.session_state.slides_data = deck_content["slides"]
      else:
        st.session_state.slides_data = [
            {"title": k, "body": v} for k, v in deck_content.items()
        ]
      deck_loaded = True
      st.success(
          f"Successfully loaded {len(st.session_state.slides_data)} slides from"
          f" {uploaded_file.name}!"
      )
    except Exception as e:
      pass

  # Local Workspace Dropdown Selector (Local Dev Mode)
  if not deck_loaded:
    json_files = [f for f in os.listdir(".") if f.endswith(".json")]
    if json_files:
      selected_json = st.selectbox(
          "Or select a local workspace deck (Local Mode):", json_files
      )
      if selected_json:
        try:
          with open(selected_json, "r", encoding="utf-8") as f:
            deck_content = json.load(f)
            if isinstance(deck_content, list):
              st.session_state.slides_data = deck_content
            elif isinstance(deck_content, dict) and "slides" in deck_content:
              st.session_state.slides_data = deck_content["slides"]
            else:
              st.session_state.slides_data = [
                  {"title": k, "body": v} for k, v in deck_content.items()
              ]
            st.success(
                f"Successfully loaded {len(st.session_state.slides_data)} slides"
                f" from {selected_json}!"
            )
        except Exception as e:
          st.error(f"Error loading {selected_json}: {e}")
    else:
      st.info(
          "📁 Using active preview deck. Upload or place a JSON deck in your"
          " workspace anytime."
      )

  st.markdown("---")
  st.markdown("## 🚀 Compile & Export High-Impact Kinetic Loop")

  with st.container():
    col1, col2 = st.columns([1.2, 1])

    with col1:
      st.markdown("### Slide Sequence Overview")
      for idx, slide in enumerate(st.session_state.slides_data, start=1):
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
            "Rendering animation frames with pixel-perfect typography..."
        ):
          frames = []
          width, height = 1080, 1080  # Square Instagram/Carousel ratio
          max_text_width = 800  # Exact available width inside card (1080 - 280 margins)

          # Temporary image to initialize draw context for font measurement
          temp_img = Image.new("RGB", (width, height))
          temp_draw = ImageDraw.Draw(temp_img)

          # Robust Cloud & Local Font Resolution
          try:
            badge_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36
            )
            title_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54
            )
            body_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38
            )
            footer_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28
            )
          except IOError:
            try:
              badge_font = ImageFont.truetype("arialbd.ttf", 36)
              title_font = ImageFont.truetype("arialbd.ttf", 54)
              body_font = ImageFont.truetype("arial.ttf", 38)
              footer_font = ImageFont.truetype("arial.ttf", 28)
            except IOError:
              badge_font = ImageFont.load_default()
              title_font = ImageFont.load_default()
              body_font = ImageFont.load_default()
              footer_font = ImageFont.load_default()

          for idx, slide in enumerate(st.session_state.slides_data, start=1):
            if isinstance(slide, dict):
              badge = slide.get("badge", f"SLIDE {idx} • STRATEGY")
              title = slide.get("title", f"Slide Title {idx}")
              body = slide.get(
                  "body", slide.get("content", "Key actionable breakdown...")
              )
            else:
              badge = f"SLIDE {idx}"
              title = str(slide)
              body = ""

            # Create base background (Dark theme #0e1117)
            img = Image.new("RGB", (width, height), color="#0e1117")
            draw = ImageDraw.Draw(img)

            # Draw Main Card Box (#161b22 with Canary Yellow border #ffcc00)
            draw.rounded_rectangle(
                [80, 100, width - 80, height - 150],
                radius=28,
                fill="#161b22",
                outline="#ffcc00",
                width=5,
            )

            # Draw Badge / Header
            draw.text((140, 170), badge.upper(), fill="#ffcc00", font=badge_font)

            # Pixel-width wrapped Title rendering
            wrapped_title = wrap_text_to_width(
                title, title_font, max_text_width, draw
            )
            title_y = 270
            for line in wrapped_title:
              draw.text((140, title_y), line, fill="#ffffff", font=title_font)
              title_y += 66

            # Pixel-width wrapped Body Paragraph rendering
            if body:
              wrapped_body = wrap_text_to_width(
                  body, body_font, max_text_width, draw
              )
              body_y = title_y + 35
              for line in wrapped_body:
                draw.text((140, body_y), line, fill="#c9d1d9", font=body_font)
                body_y += 50

            # Draw Footer Handle
            draw.text(
                (140, height - 240),
                "@nikki.coachpages",
                fill="#8b949e",
                font=footer_font,
            )

            frames.append(img)

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

        st.success("🎉 Kinetic Loop rendered successfully!")
        st.download_button(
            label="⬇️ Download Rendered Animated GIF",
            data=gif_bytes,
            file_name="kinetic_carousel_loop.gif",
            mime="image/gif",
            use_container_width=True,
        )

      st.markdown("---")
      st.markdown("### 💬 Viral Ready-to-Post Caption:")
      first_title = (
          st.session_state.slides_data[0].get("title", "Check this out")
          if st.session_state.slides_data
          else "Check this out"
      )
      st.info(
          f"🔥 {first_title}...\n\nRead through this complete breakdown to"
          " completely transform your conversion rate.\n\nWhich slide hit home"
          " for you the most? Drop your thoughts below! 👇\n\n--- \n⚡ Built &"
          " animated seamlessly using Carousel Engine & Kinetic Animator."
      )
else:
  st.title("🎬 Kinetic Motion Suite — Restricted Access")
  st.warning(
      "🔒 Please enter a valid license key in the sidebar to unlock the Kinetic"
      " Animator Studio."
  )