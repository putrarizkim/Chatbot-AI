import streamlit as st
import requests

OPENROUTER_API_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct" 

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://localhost:8501",
    "Content-Type": "application/json",
    "X-title": "NgobrolBOT"
}

API_URL = "https://openrouter.ai/api/v1/chat/completions"

st.title("🤖NgobrolBOT")
st.markdown("powered by [Mistral AI](https://mistral.ai) & [OpenRouter](https://openrouter.ai)")

# Inisialisasi riwayat percakapan
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tampilkan percakapan sebelumnya
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Input pengguna
user_input = st.chat_input("Ketik pesan Anda di sini...")

if user_input:
    # Tampilkan dan simpan input pengguna
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Kirim ke OpenRouter
    with st.spinner("Memproses..."):
        payload = {
            "model": MODEL,
            "messages": st.session_state.chat_history
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            response_json = response.json()
            ai_reply = response_json["choices"][0]["message"]["content"]

            # Tampilkan dan simpan balasan AI
            with st.chat_message("assistant"):
                st.markdown(ai_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
        else:
            st.error(f"❌ Gagal mendapatkan respon: {response.status_code}")
            st.error(response.text)
