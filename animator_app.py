import streamlit as st
import json
import io
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Carousel Engine Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🎬 Carousel Engine")
    st.caption("Kinetic Motion Suite")

    st.divider()
    st.subheader("⚙️ Pro Motion Control")
    fps = st.slider("Frame Rate (FPS):", min_value=15, max_value=30, value=20)
    slide_duration = st.slider("Seconds per Slide:", min_value=1.5, max_value=4.0, value=2.5, step=0.5)
    
    # Premium Upgraded Transition Arsenal
    transition_effect = st.selectbox("Kinetic Transition Style:", [
        "Dynamic Slide Up (Pro Easing)", 
        "High-Velocity Slide Right", 
        "Instant Snap"
    ])
    
    transition_frames = st.slider("Transition Speed (Frames):", min_value=3, max_value=12, value=6)
    
    st.divider()
    st.subheader("🏷️ Brand Watermark")
    brand_handle = st.text_input("Custom Handle / Domain:", "carouselengine.io")
    keep_watermark = st.checkbox("Include 'Powered by Carousel Engine' Badge", value=True)

    st.info("🚀 *Carousel Engine:* Ready for High-End Production.")

# --- MAIN HEADER ---
st.markdown("<h1 style='text-align: center;'>🎬 Carousel Engine: Kinetic Studio</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Transform static decks into thumb-stopping, high-converting motion loops that command premium pricing.</p>", unsafe_allow_html=True)

# --- DECK LOADER ---
st.markdown("### 📥 Import Carousel JSON Deck")
uploaded_file = st.file_uploader("Upload your JSON deck file:")

slides = []
filename = "demo_deck.json"

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name
        raw_data = json.loads(file_bytes.decode('utf-8-sig', errors='ignore'))
        
        if isinstance(raw_data, list):
            slides = raw_data
        elif isinstance(raw_data, dict):
            for k in ["slides", "cards", "pages", "deck"]:
                if k in raw_data and isinstance(raw_data[k], list):
                    slides = raw_data[k]
                    break
            if not slides:
                vals = list(raw_data.values())
                if vals and all(isinstance(v, dict) for v in vals):
                    slides = vals
    except Exception as e:
        st.error(f"⚠️ Error parsing uploaded file: {e}")

# Downloads auto-fallback
if not slides:
    downloads_path = os.path.expanduser("~\\Downloads\\deck.json")
    if os.path.exists(downloads_path):
        try:
            with open(downloads_path, "r", encoding="utf-8-sig") as f:
                raw_data = json.load(f)
                filename = "deck.json (from Downloads)"
                if isinstance(raw_data, list):
                    slides = raw_data
                elif isinstance(raw_data, dict):
                    for k in ["slides", "cards", "pages", "deck"]:
                        if k in raw_data and isinstance(raw_data[k], list):
                            slides = raw_data[k]
                            break
        except Exception:
            pass

if slides:
    st.success(f"Successfully loaded {len(slides)} slides from `{filename}`!")
else:
    filename = "demo_deck.json"
    slides = [
        {
            "category": "HOOK",
            "title": "Stop Losing Coaching Clients on Your Page",
            "content": "90% of online coaches make 3 critical landing page mistakes."
        },
        {
            "category": "PROBLEM",
            "title": "Stop Selling the Plane, Sell the Island",
            "content": "Clients care about their transformation, not your modules."
        }
    ]

# --- DEFAULT ELITE BRAND PALETTE (Dark Obsidian & High-Contrast Canary) ---
bg_hex, text_hex, body_hex, tag_hex = "#121212", "#ffffff", "#d1d1d1", "#ffcc00"

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

bg_rgb = hex_to_rgb(bg_hex)
text_rgb = hex_to_rgb(text_hex)
body_rgb = hex_to_rgb(body_hex)
tag_rgb = hex_to_rgb(tag_hex)

# --- RENDER SUITE ---
st.divider()
st.markdown("### 🚀 Compile & Export High-Impact Kinetic Loop")

with st.expander(f"📁 Active Deck: {filename} ({len(slides)} slides loaded)", expanded=True):
    col_preview, col_export = st.columns([1, 1])
    
    with col_preview:
        st.markdown("#### Slide Sequence Overview")
        for idx, s in enumerate(slides):
            st.markdown(f"**Slide {idx+1}:** {s.get('title', 'Untitled')}")
            
    with col_export:
        st.markdown("#### Production Render Engine")
        
        if st.button(f"✨ Render Premium Kinetic GIF ({filename})", type="primary"):
            with st.spinner(f"Compiling high-impact motion loop with '{transition_effect}'..."):
                frames = []
                
                if os.name == "nt":
                    title_font_path = "arialbd.ttf"
                    body_font_path = "arial.ttf"
                else:
                    title_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                    body_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

                try:
                    font_tag = ImageFont.truetype(body_font_path, 36)
                    font_title = ImageFont.truetype(title_font_path, 68)
                    font_body = ImageFont.truetype(body_font_path, 44)
                    font_handle = ImageFont.truetype(body_font_path, 36)
                    font_watermark = ImageFont.truetype(body_font_path, 28)
                except IOError:
                    font_tag = ImageFont.load_default()
                    font_title = ImageFont.load_default()
                    font_body = ImageFont.load_default()
                    font_handle = ImageFont.load_default()
                    font_watermark = ImageFont.load_default()

                for idx, s in enumerate(slides):
                    s_tag = str(s.get("tag") or s.get("category") or f"SLIDE {idx+1}").upper()
                    s_title = s.get("title", "")
                    s_body = s.get("content") or s.get("body", "")
                    
                    wrapped_title_lines = textwrap.wrap(s_title, width=22)
                    wrapped_body_lines = textwrap.wrap(s_body, width=32)
                    
                    total_slide_frames = int(fps * slide_duration)
                    intro_frames = transition_frames
                    
                    for f_i in range(total_slide_frames):
                        img = Image.new("RGB", (1080, 1350), color=bg_rgb)
                        draw = ImageDraw.Draw(img)
                        
                        offset_y = 0
                        offset_x = 0
                        
                        # Quadratic ease-out formula for buttery smooth deceleration
                        if transition_effect == "Dynamic Slide Up (Pro Easing)" and f_i < intro_frames:
                            progress = f_i / intro_frames
                            eased_progress = 1 - (1 - progress) ** 2
                            offset_y = int(70 * (1 - eased_progress))
                        elif transition_effect == "High-Velocity Slide Right" and f_i < intro_frames:
                            progress = f_i / intro_frames
                            eased_progress = 1 - (1 - progress) ** 2
                            offset_x = int(150 * (1 - eased_progress))
                        
                        current_y = 180 + offset_y
                        base_x = 120 + offset_x
                        
                        draw.text((base_x, current_y), f"SLIDE {idx+1} • {s_tag}", fill=tag_rgb, font=font_tag)
                        current_y += 110
                        
                        for line in wrapped_title_lines:
                            draw.text((base_x, current_y), line, fill=text_rgb, font=font_title)
                            current_y += 90
                            
                        current_y += 50
                        
                        for line in wrapped_body_lines:
                            draw.text((base_x, current_y), line, fill=body_rgb, font=font_body)
                            current_y += 65
                            
                        if brand_handle:
                            draw.text((1080 - 120 - len(brand_handle)*20, 1220), brand_handle, fill=body_rgb, font=font_handle)
                            
                        if keep_watermark:
                            draw.text((120, 1220), "⚡ Powered by Carousel Engine", fill=tag_rgb, font=font_watermark)
                            
                        frames.append(img.copy())
                
                gif_buffer = io.BytesIO()
                frames[0].save(
                    gif_buffer,
                    format="GIF",
                    save_all=True,
                    append_images=frames[1:],
                    duration=int(1000 / fps),
                    loop=0
                )
                gif_buffer.seek(0)
                
                st.success(f"Successfully compiled high-impact kinetic loop ({len(slides)} slides)! 🎉")
                st.download_button(
                    label="📥 Download Production-Ready Kinetic GIF",
                    data=gif_buffer,
                    file_name=f"carousel_engine_pro_{filename.replace('.json', '')}.gif",
                    mime="image/gif",
                    use_container_width=True
                )
        
        st.markdown("---")
        st.markdown("💬 **Viral Ready-to-Post Caption:**")
        first_title = slides[0].get('title', 'Check this out') if slides else 'Check this out'
        sample_caption = f"""🔥 {first_title}

Read through this complete breakdown to completely transform your conversion rates. 

Which slide hit home for you the most? Drop your thoughts below! 👇

---
✨ Built & animated seamlessly using Carousel Engine ({brand_handle if brand_handle else 'carouselengine.io'}). #CarouselEngine #ConversionRate #ContentStrategy #CreatorEconomy"""
        
        st.code(sample_caption, language="markdown")