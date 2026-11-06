st.markdown("---")
    st.markdown("## 🚀 Compile & Export High-Impact Kinetic Loop")

    # Row 1: Left column handles sequence & rendering; Right column handles live preview & caption side-by-side
    col_left, col_right = st.columns([1.2, 1.4])

    with col_left:
        st.markdown("### Slide Sequence Overview")
        for idx, slide in enumerate(st.session_state.slides_data, start=1):
            title_text = (
                slide.get("title", f"Slide {idx}")
                if isinstance(slide, dict)
                else str(slide)
            )
            st.markdown(f"**Slide {idx}:** {title_text}")

        st.markdown("### Production Render Engine")
        render_btn = st.button(
            "✨ Render Premium Kinetic Loop (Active Deck)",
            use_container_width=True,
        )

        if render_btn:
            with st.spinner("Rendering animation frames with high-weight typography..."):
                frames = []
                width, height = 1080, 1080  # Square Instagram/Carousel ratio
                max_text_width = 800  # Exact available width inside card

                font_to_use = None
                fonts_dir = "fonts"
                if os.path.exists(fonts_dir):
                    for f in os.listdir(fonts_dir):
                        if f.lower().endswith((".ttf", ".otf")) and (
                            "bd" in f.lower() or "bold" in f.lower()
                        ):
                            font_to_use = os.path.join(fonts_dir, f)
                            break
                    if not font_to_use:
                        for f in os.listdir(fonts_dir):
                            if f.lower().endswith((".ttf", ".otf")):
                                font_to_use = os.path.join(fonts_dir, f)
                                break

                if not font_to_use:
                    for path in [
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                        "arialbd.ttf",
                    ]:
                        if os.path.exists(path):
                            font_to_use = path
                            break

                try:
                    if font_to_use:
                        badge_font = ImageFont.truetype(font_to_use, 38)
                        title_font = ImageFont.truetype(font_to_use, 62)
                        body_font = ImageFont.truetype(font_to_use, 42)
                        footer_font = ImageFont.truetype(font_to_use, 30)
                    else:
                        badge_font = ImageFont.load_default()
                        title_font = ImageFont.load_default()
                        body_font = ImageFont.load_default()
                        footer_font = ImageFont.load_default()
                except IOError:
                    badge_font = ImageFont.load_default()
                    title_font = ImageFont.load_default()
                    body_font = ImageFont.load_default()
                    footer_font = ImageFont.load_default()

                for idx, slide in enumerate(st.session_state.slides_data, start=1):
                    if isinstance(slide, dict):
                        badge = str(slide.get("badge", f"SLIDE {idx} | STRATEGY"))
                        title = str(slide.get("title", f"Slide Title {idx}"))
                        body = str(
                            slide.get(
                                "body",
                                slide.get("content", "Key actionable breakdown..."),
                            )
                        )
                    else:
                        badge = f"SLIDE {idx}"
                        title = str(slide)
                        body = ""

                    badge = (
                        badge.replace("•", "|")
                        .replace("—", "-")
                        .replace("“", '"')
                        .replace("”", '"')
                    )
                    title = (
                        title.replace("•", "|")
                        .replace("—", "-")
                        .replace("“", '"')
                        .replace("”", '"')
                    )
                    body = (
                        body.replace("•", "|")
                        .replace("—", "-")
                        .replace("“", '"')
                        .replace("”", '"')
                    )

                    img = Image.new("RGB", (width, height), color="#0e1117")
                    draw = ImageDraw.Draw(img)

                    draw.rounded_rectangle(
                        [80, 100, width - 80, height - 150],
                        radius=28,
                        fill="#161b22",
                        outline="#ffcc00",
                        width=5,
                    )

                    draw.text((140, 160), badge.upper(), fill="#ffcc00", font=badge_font)

                    wrapped_title = wrap_text_to_width(
                        title, title_font, max_text_width, draw
                    )
                    title_y = 250
                    for line in wrapped_title:
                        draw.text((140, title_y), line, fill="#ffffff", font=title_font)
                        title_y += 74

                    if body:
                        wrapped_body = wrap_text_to_width(
                            body, body_font, max_text_width, draw
                        )
                        body_y = title_y + 30
                        for line in wrapped_body:
                            draw.text((140, body_y), line, fill="#c9d1d9", font=body_font)
                            body_y += 56

                    draw.text(
                        (140, height - 230),
                        "@nikki.coachpages",
                        fill="#8b949e",
                        font=footer_font,
                    )

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
                st.session_state["last_rendered_gif"] = gif_buffer.getvalue()

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

                    mp4_path = "temp_kinetic_animator.mp4"
                    imageio.mimwrite(
                        mp4_path,
                        paced_frames,
                        fps=fps,
                        codec="libx264",
                        quality=8,
                        pixelformat="yuv420p",
                    )
                    with open(mp4_path, "rb") as mf:
                        mp4_bytes = mf.read()
                    os.remove(mp4_path)
                    st.session_state["last_rendered_mp4"] = mp4_bytes
                except Exception:
                    st.session_state["last_rendered_mp4"] = None

            st.success("🎉 Kinetic Loop rendered successfully!")

        # --- LIVE MP4 VIDEO PREVIEW & DUAL EXPORT PACKAGE (Placed directly under Slide Sequence & Render) ---
        if "last_rendered_mp4" in st.session_state and st.session_state["last_rendered_mp4"]:
            st.markdown("---")
            st.markdown("#### 👁️ Live Loop Preview")
            mp4_bytes = st.session_state["last_rendered_mp4"]
            b64_mp4 = base64.b64encode(mp4_bytes).decode("utf-8")
            st.markdown(
                f'<div style="width: 100%; display: flex; justify-content: center; background: #000; padding: 10px; border-radius: 12px; border: 2px solid #ffcc00; box-sizing: border-box; margin-bottom: 20px;">'
                f'<video width="100%" autoplay loop muted playsinline style="border-radius: 8px; display: block; max-width: 280px; height: auto;">'
                f'<source src="data:video/mp4;base64,{b64_mp4}" type="video/mp4">'
                f'Your browser does not support the video tag.'
                f'</video>'
                f'</div>',
                unsafe_allow_html=True
            )
            
            st.markdown("#### 📥 Download Package")
            if "last_rendered_gif" in st.session_state:
                st.download_button(
                    label="⬇️ Download Animated GIF",
                    data=st.session_state["last_rendered_gif"],
                    file_name="kinetic_carousel_loop.gif",
                    mime="image/gif",
                    use_container_width=True,
                )
            st.download_button(
                label="🎬 Download Instagram MP4",
                data=mp4_bytes,
                file_name="kinetic_carousel_loop.mp4",
                mime="video/mp4",
                use_container_width=True,
            )

    with col_right:
        st.markdown("### 💬 Viral Ready-to-Post Caption")
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