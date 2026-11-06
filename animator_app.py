import streamlit as st
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ApexMorph OPC — Animation Engine",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("⚡ ApexMorph OPC")
    st.caption("Motion & Animation Studio")
    st.divider()
    
    st.subheader("⚙️ Animation Parameters")
    animation_effect = st.selectbox("Core Motion Effect:", [
        "Spring Zoom-In & Bounce",
        "Magnetic Hover & Scale",
        "Smooth Pulse & Glow",
        "Kinetic Text Reveal"
    ])
    
    target_element = st.selectbox("Target UI Element:", [
        "Hero Headline / Title",
        "Call-to-Action (CTA) Button",
        "Feature Card / Container",
        "Product Mockup / Badge"
    ])
    
    animation_speed = st.slider("Duration (seconds):", 0.2, 3.0, 0.6, 0.1)
    
    st.divider()
    with st.expander("📖 Animation Guide"):
        st.markdown("""
        * **Purpose:** Generates production-ready CSS keyframes and conversion playbooks for landing pages.
        * **Usage:** Select your effect, inspect the live preview, and copy-paste into your project.
        """)
    st.info("💡 **Pro Utility:** High-converting micro-interactions for Netlify & Streamlit apps.")

# --- DYNAMIC DEFAULT MAPPING BASED ON SIDEBAR SELECTION ---
default_selectors = {
    "Hero Headline / Title": (".hero-title", "Hero Main Headline"),
    "Call-to-Action (CTA) Button": (".hero-cta-button", "Get Started Now Button"),
    "Feature Card / Container": (".feature-card-item", "Service Tier Container"),
    "Product Mockup / Badge": (".product-badge-pill", "Instant Access Badge")
}

default_class, default_label = default_selectors.get(target_element, (".hero-element", "Target Element"))

# --- MAIN HEADER ---
st.markdown("<h1 style='text-align: center;'>✨ ApexMorph Animation Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Generate production-ready CSS keyframes, conversion strategy notes, and live interactive previews for your web assets.</p>", unsafe_allow_html=True)

# --- INPUT SECTION ---
col_i1, col_i2 = st.columns(2)
with col_i1:
    element_selector = st.text_input("CSS Selector / Class Name:", value=default_class)
with col_i2:
    custom_label = st.text_input("Element Description / Label:", value=default_label)

col_btn1, _ = st.columns([1, 4])
with col_btn1:
    generate_anim_btn = st.button("🚀 Generate Animation & Conversion Guide", type="primary")

# --- EXECUTION & CODE GENERATION LOGIC ---
if generate_anim_btn:
    with st.spinner("Synthesizing high-performance motion keyframes and conversion playbook..."):
        
        # Build CSS cleanly without f-string brace conflicts
        if "Zoom" in animation_effect:
            keyframes_code = "@keyframes springZoom {{\n  0% {{ transform: scale(0.85); opacity: 0; }}\n  60% {{ transform: scale(1.05); opacity: 1; }}\n  100% {{ transform: scale(1); opacity: 1; }}\n}}\n\n{} {{\n  animation: springZoom {}s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;\n}}".format(element_selector, animation_speed)
            preview_anim_css = "animation: springZoom {}s cubic-bezier(0.175, 0.885, 0.32, 1.275) infinite alternate;".format(animation_speed)
            conversion_tip = "**Conversion Playbook:** Best used on primary CTA buttons or urgent limited-time discount badges. The slight spring bounce creates a subconscious focal point without feeling obnoxious."
        elif "Magnetic" in animation_effect:
            keyframes_code = "{} {{\n  transition: transform {}s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.3s ease;\n}}\n{}:hover {{\n  transform: translateY(-4px) scale(1.02);\n  box-shadow: 0 12px 24px rgba(0,0,0,0.15);\n}}".format(element_selector, animation_speed, element_selector)
            preview_anim_css = "transition: transform 0.3s ease;"
            conversion_tip = "**Conversion Playbook:** Ideal for interactive feature cards, pricing tiers, and clickable product mockups. It gives users immediate tactile feedback that an element is interactive."
        elif "Pulse" in animation_effect:
            pulse_speed = animation_speed * 2
            keyframes_code = "@keyframes softPulse {{\n  0% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.4); }}\n  70% {{ transform: scale(1.03); box-shadow: 0 0 0 12px rgba(79, 70, 229, 0); }}\n  100% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }}\n}}\n\n{} {{\n  animation: softPulse {}s infinite ease-in-out;\n}}".format(element_selector, pulse_speed)
            preview_anim_css = "animation: softPulse {}s infinite ease-in-out;".format(pulse_speed)
            conversion_tip = "**Conversion Playbook:** Use sparingly on high-intent conversion triggers like 'Book a Call' or 'Instant Download' buttons to subtly draw wandering eyes back to your main offer."
        else:
            keyframes_code = "@keyframes kineticReveal {{\n  0% {{ transform: translateY(20px); opacity: 0; filter: blur(4px); }}\n  100% {{ transform: translateY(0); opacity: 1; filter: blur(0); }}\n}}\n\n{} {{\n  animation: kineticReveal {}s ease-out forwards;\n}}".format(element_selector, animation_speed)
            preview_anim_css = "animation: kineticReveal {}s infinite alternate ease-out;".format(animation_speed)
            conversion_tip = "**Conversion Playbook:** Perfect for hero headlines and value proposition text. The smooth blur-to-focus reveal naturally paces the visitor's reading flow from top to bottom."

        st.success("✨ Animation code and conversion playbook successfully generated!")

        # --- DISPLAY TABS ---
        tab_code, tab_preview, tab_export = st.tabs(["💻 CSS Code & Playbook", "👁️ Live Element Preview", "📦 JSON Export"])

        with tab_code:
            st.markdown("### 💻 Production-Ready CSS Keyframes")
            st.code(keyframes_code, language="css")
            st.markdown("### 📈 Expert Conversion Playbook")
            st.info(conversion_tip)
            st.download_button("📥 Download Animation Code (.css)", data=keyframes_code, file_name="animation_styles.css", mime="text/css")

        with tab_preview:
            st.markdown("### 👁️ True Live Animated Preview")
            st.markdown("---")
            st.write(f"Below is a live browser rendering of the spring bounce animation applied to **{custom_label}**:")
            
            # True CSS-injected HTML preview container that actually animates live
            live_preview_html = f"""
            <style>
            @keyframes springZoom {{
              0% {{ transform: scale(0.85); opacity: 0; }}
              60% {{ transform: scale(1.05); opacity: 1; }}
              100% {{ transform: scale(1); opacity: 1; }}
            }}
            @keyframes softPulse {{
              0% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.4); }}
              70% {{ transform: scale(1.03); box-shadow: 0 0 0 12px rgba(79, 70, 229, 0); }}
              100% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }}
            }}
            @keyframes kineticReveal {{
              0% {{ transform: translateY(20px); opacity: 0; filter: blur(4px); }}
              100% {{ transform: translateY(0); opacity: 1; filter: blur(0); }}
            }}
            .live-box-wrapper {{
              padding: 50px;
              background: #f8fafc;
              border-radius: 12px;
              text-align: center;
              border: 1px dashed #cbd5e1;
            }}
            .live-target-element {{
              display: inline-block;
              padding: 18px 36px;
              background: #4f46e5;
              color: white;
              font-family: sans-serif;
              font-size: 16px;
              font-weight: bold;
              border-radius: 8px;
              box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);
              {preview_anim_css}
            }}
            </style>
            <div class="live-box-wrapper">
              <div class="live-target-element">✨ {custom_label}</div>
              <p style="color: #64748b; font-size: 12px; margin-top: 20px; font-family: sans-serif;">Active Effect: <b>{animation_effect}</b> | Selector: <code>{element_selector}</code></p>
            </div>
            """
            st.components.v1.html(live_preview_html, height=240)

        with tab_export:
            st.markdown("### 📦 Animation Metadata & Strategy Package (JSON)")
            json_package = {
                "effect": animation_effect,
                "selector": element_selector,
                "speed": animation_speed,
                "code": keyframes_code,
                "conversion_tip": conversion_tip
            }
            json_code = json.dumps(json_package, indent=2)
            st.code(json_code, language="json")
            st.download_button("📥 Download JSON Package", data=json_code, file_name="animation_package.json", mime="application/json")