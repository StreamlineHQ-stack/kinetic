# --- LIVE MP4 VIDEO PREVIEW & DUAL EXPORT PACKAGE ---
      if "last_rendered_mp4" in st.session_state and st.session_state["last_rendered_mp4"]:
        st.markdown("---")
        st.markdown("### 🚀 Render Output & Export Studio")
        
        prev_col, cap_col = st.columns([1, 1.2])
        
        with prev_col:
          st.markdown("#### 👁️ Live Loop Preview")
          # Embed the MP4 video natively with autoplay, loop, and muted controls
          mp4_bytes = st.session_state["last_rendered_mp4"]
          b64_mp4 = base64.b64encode(mp4_bytes).decode("utf-8")
          st.markdown(
              f'<div style="display: flex; justify-content: center; background: #000; padding: 10px; border-radius: 12px; border: 2px solid #ffcc00;">'
              f'<video width="320" autoplay loop muted playsinline style="border-radius: 8px;">'
              f'<source src="data:video/mp4;base64,{b64_mp4}" type="video/mp4">'
              f'Your browser does not support the video tag.'
              f'</video>'
              f'</div>',
              unsafe_allow_html=True
          )
          
          st.markdown("<br>", unsafe_allow_html=True)
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

        with cap_col:
          st.markdown("#### 💬 Viral Ready-to-Post Caption")
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