# app.py (Updated ClearTune with fallback audio, online-ready & token selector)

import streamlit as st
import requests
from io import BytesIO

# App Setup
st.set_page_config(page_title="ClearTune AI", layout="centered")
st.title("\U0001F3B5 ClearTune AI – Generate Royalty-Free Music")

# Token Selector
st.sidebar.header("🔐 Hugging Face Token")
api_token = st.sidebar.text_input("Paste your Hugging Face token here:", type="password")

# Prompt & Duration
prompt = st.text_input("Describe the music you want to generate:", "Lo-fi chill with Indian drums")
duration = st.slider("Select duration (seconds):", min_value=5, max_value=30, value=10)

# Generate
if st.button("🎶 Generate Music"):
    if not api_token:
        st.warning("⚠️ Please enter a valid Hugging Face token in the sidebar.")
    else:
        st.info(f"Generating music for: {prompt}")
        with st.spinner("Calling Hugging Face MusicGen..."):
            API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
            headers = {"Authorization": f"Bearer {api_token}"}
            payload = {"inputs": prompt, "parameters": {"duration": duration}}

            try:
                response = requests.post(API_URL, headers=headers, json=payload)
                if response.status_code == 200:
                    audio_bytes = response.content
                    st.audio(audio_bytes, format='audio/wav')
                    st.download_button("⬇️ Download Music", data=audio_bytes, file_name="generated_music.wav", mime="audio/wav")
                else:
                    st.error("❌ Failed to generate music. Showing fallback audio.")
                    st.write("Status Code:", response.status_code)
                    st.write("Error:", response.text)

                    # Fallback sample audio (from Pixabay - public domain)
                    fallback_url = "https://cdn.pixabay.com/download/audio/2023/03/09/audio_48ab67fcb6.mp3"
                    fallback_audio = requests.get(fallback_url).content
                    st.audio(BytesIO(fallback_audio), format='audio/mp3')
                    st.download_button("⬇️ Download Fallback Audio", data=fallback_audio, file_name="fallback_music.mp3", mime="audio/mp3")
            except Exception as e:
                st.error("Unexpected error occurred.")
                st.exception(e)

# Footer for Deployment
st.markdown("---")
st.caption("Deploy this on [Streamlit Cloud](https://streamlit.io/cloud) and share your app globally!")

