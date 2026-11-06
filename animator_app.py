import streamlit as st
import json
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Kinetic Motion Animator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🎬 Animation Studio")
    
    theme_mode = st.radio("Styling Mode:", ["Preset Themes", "Custom Brand Hex"])
    
    if theme_mode == "Preset Themes":
        theme_options = {
            "High-Contrast Canary": "⚡ High-Contrast Canary (Black & Yellow)",
            "Warning Red Alert": "🚨 Warning Red Alert (Charcoal & Crimson)",
            "Minimalist Clean": "💎 Minimalist Clean (White & Charcoal)",
            "Warm Editorial": "☕ Warm Editorial (Cream & Terracotta)",
            "Neon Cyber/Tech": "⚡ Neon Cyber/Tech (Obsidian & Cyan)",
            "Midnight Luxury": "👑 Midnight Luxury (Dark Obsidian & Gold)",
            "Emerald Growth": "📈 Emerald Growth (Deep Forest & Mint)",
            "Nordic Slate": "❄️ Nordic Slate (Slate Grey & Soft Ice Blue)"
        }
        selected_theme_label = st.selectbox("Choose Visual Design Theme:", list(theme_options.values()))
        style_theme = [k for k, v in theme_options.items() if v == selected_theme_label][0]
        custom_colors = None
    else:
        st.subheader("🎨 Custom Brand Colors")
        custom_bg = st.color_picker("Background Color", "#0e1117")
        custom_text = st.color_picker("Main Text Color", "#ffffff")
        custom_body = st.color_picker("Body Text Color", "#b0c4de")
        custom_tag = st.color_picker("Accent / Tag Color", "#ff4b4b")
        custom_colors = {"bg": custom_bg, "text": custom_text, "body": custom_body, "tag": custom_tag}
        style_theme = "Custom"

    st.divider()
    st.subheader("⚙️ Motion Settings")
    fps = st.slider("Animation Frame Rate (FPS):", min_value=10, max_value=30, value=15)
    slide_duration = st.slider("Seconds per Slide:", min_value=1.5, max_value=5.0, value=3.0, step=0.5)
    transition_frames = st.slider("Intro Slide-In Easing Frames:", min_value=2, max_value=10, value=5)
    brand_handle = st.text_input("Brand Handle Watermark:", "@nikki.coachpages")

    st.divider()
    st.subheader("👑 Creator Partner Program")
    keep_watermark = st.checkbox("Keep 'Made with Carousel Engine' Watermark\n*(Unlocks 15% Monthly Subscriber Discount)*", value=True)
    if keep_watermark:
        st.success("🎉 15% Creator Discount Active!")
    
    st.info("🚀 *Kinetic Animator Ready:* Dual-Mode Loader Active.")

# --- MAIN HEADER ---
st.markdown("<h1 style='text-align: center;'>🎬 Kinetic Motion Animator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Transform your static carousel JSON decks into thumb-stopping motion loops and viral social assets.</p>", unsafe_allow_html=True)

# --- DUAL-MODE DECK LOADER (Uploader + Downloads Auto-Fallback) ---
st.markdown("### 📥 Import Carousel JSON Deck")
uploaded_file = st.file_uploader("Click 'Browse files' to upload your exported JSON deck:")

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

# If nothing uploaded, automatically check Downloads for deck.json
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
    # Fallback to demo deck
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

# --- THEME COLOR MAPPING ---
if style_theme == "Custom" and custom_colors:
    bg_hex, text_hex, body_hex, tag_hex = custom_colors["bg"], custom_colors["text"], custom_colors["body"], custom_colors["tag"]
elif style_theme == "Warning Red Alert":
    bg_hex, text_hex, body_hex, tag_hex = "#181212", "#ffffff", "#e5cdc5", "#ef4444"
elif style_theme == "Minimalist Clean":
    bg_hex, text_hex, body_hex, tag_hex = "#ffffff", "#111111", "#444444", "#0066cc"
elif style_theme == "Warm Editorial":
    bg_hex, text_hex, body_hex, tag_hex = "#fbf9f5", "#2c221e", "#5c4e47", "#a85732"
elif style_theme == "Neon Cyber/Tech":
    bg_hex, text_hex, body_hex, tag_hex = "#0b0f19", "#f8fafc", "#94a3b8", "#06b6d4"
elif style_theme == "Midnight Luxury":
    bg_hex, text_hex, body_hex, tag_hex = "#121212", "#f5e6c8", "#d4c5a9", "#d4af37"
elif style_theme == "Emerald Growth":
    bg_hex, text_hex, body_hex, tag_hex = "#0a1f1c", "#e6f4f1", "#a3cbd0", "#10b981"
elif style_theme == "Nordic Slate":
    bg_hex, text_hex, body_hex, tag_hex = "#1e242b", "#f1f5f9", "#cbd5e1", "#38bdf8"
else:
    bg_hex, text_hex, body_hex, tag_hex = "#1a1a1a", "#ffffff", "#d1d1d1", "#ffcc00"

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

bg_rgb = hex_to_rgb(bg_hex)
text_rgb = hex_to_rgb(text_hex)
body_rgb = hex_to_rgb(body_hex)
tag_rgb = hex_to_rgb(tag_hex)

# --- RENDER SUITE ---
st.divider()
st.markdown("### 🎬 Render Kinetic Motion Loops & Auto-Captions")

with st.expander(f"📁 Active Deck: {filename} ({len(slides)} slides loaded)", expanded=True):
    col_preview, col_export = st.columns([1, 1])
    
    with col_preview:
        st.markdown("#### Slide Breakdown")
        for idx, s in enumerate(slides):
            st.markdown(f"**Slide {idx+1}:** {s.get('title', 'Untitled')}")
            
    with col_export:
        st.markdown("#### Render & Viral Suite")
        
        if st.button(f"🚀 Render Kinetic GIF Loop ({filename})", type="primary"):
            with st.spinner(f"Compiling kinetic motion loop for all {len(slides)} slides..."):
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
                        if f_i < intro_frames:
                            progress = f_i / intro_frames
                            offset_y = int(35 * (1 - progress))
                        
                        current_y = 180 + offset_y
                        draw.text((120, current_y), f"SLIDE {idx+1} • {s_tag}", fill=tag_rgb, font=font_tag)
                        current_y += 110
                        
                        for line in wrapped_title_lines:
                            draw.text((120, current_y), line, fill=text_rgb, font=font_title)
                            current_y += 90
                            
                        current_y += 50
                        
                        for line in wrapped_body_lines:
                            draw.text((120, current_y), line, fill=body_rgb, font=font_body)
                            current_y += 65
                            
                        if brand_handle:
                            draw.text((1080 - 120 - len(brand_handle)*20, 1220), brand_handle, fill=body_rgb, font=font_handle)
                            
                        if keep_watermark:
                            draw.text((120, 1220), "⚡ Made with Carousel Engine", fill=tag_rgb, font=font_watermark)
                            
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
                
                st.success(f"Successfully compiled all {len(slides)} slides into kinetic loop!")
                st.download_button(
                    label="📥 Download Full Kinetic GIF Loop",
                    data=gif_buffer,
                    file_name=f"kinetic_loop_{filename.replace('.json', '')}.gif",
                    mime="image/gif",
                    use_container_width=True
                )
        
        st.markdown("---")
        st.markdown("💬 **Ready-to-Post Social Caption:**")
        first_title = slides[0].get('title', 'Check this out') if slides else 'Check this out'
        sample_caption = f"""🔥 {first_title}

Read through this breakdown to completely transform your workflow. 

Which slide hit home for you the most? Drop your thoughts below! 👇

---
✨ Built & animated seamlessly using Carousel Engine ({brand_handle if brand_handle else '@nikki.coachpages'}). #CoachLife #DigitalProducts #ContentStrategy #CreatorEconomy"""
        
        st.code(sample_caption, language="markdown")