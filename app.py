from main import generate_persona
import streamlit as st

st.set_page_config(page_title="RedPersona", layout="wide")

st.title("🧠 RedPersona: Reddit User Persona Generator")

profile_url = st.text_input("🔗 Enter Reddit Profile URL")

if profile_url:
    with st.spinner("Fetching and analyzing user data..."):
        # fetch posts/comments → call GPT → build persona dict
        persona = generate_persona(profile_url)
    
    st.header(f"👤 Persona: {persona['name']}")
    st.subheader(f"📌 Quote: “{persona['quote']}”")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("default-avatar.png")
        st.markdown(f"**Age:** {persona['age']}")
        st.markdown(f"**Occupation:** {persona['occupation']}")
        st.markdown(f"**Location:** {persona['location']}")
        st.markdown(f"**Archetype:** {persona['archetype']}")
    
    with col2:
        st.markdown("### 🟧 Motivations")
        st.markdown("\n".join(f"- {m}" for m in persona["motivations"]))
        
        st.markdown("### 😤 Frustrations")
        st.markdown("\n".join(f"- {f}" for f in persona["frustrations"]))
        
        st.markdown("### 🎯 Goals & Needs")
        st.markdown("\n".join(f"- {g}" for g in persona["goals"]))
        
        st.markdown("### 🧬 Personality")
        st.markdown(", ".join(persona["personality"]))

    st.download_button("📄 Download Persona (Text)", data=persona["raw_text"], file_name="persona.txt")
