import streamlit as st
from main import generate_persona

st.set_page_config(page_title="Reddit Intel", layout="wide")

st.title("🧠 Reddit Intel: Reddit User Persona Generator")

profile_url = st.text_input("🔗 Enter Reddit Profile URL")


if profile_url:
    with st.spinner("Analyzing Reddit profile..."):
        result = generate_persona(profile_url)
        print("Result:", result)
    
    if "error" in result:
        st.error(result["error"])
    else:
        raw_output = result["raw_text"]
        st.subheader("👤 Generated Persona")
        st.image(result.get("profile_image", "No image available"), width=100)
        st.markdown(raw_output)
        st.download_button("📥 Download Persona", raw_output, file_name=f"{result['username']}_persona.txt")
        st.success("Persona generated successfully!")