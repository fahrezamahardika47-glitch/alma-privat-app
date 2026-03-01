import streamlit as st
import google.generativeai as genai

# 1. SETTING HALAMAN
st.set_page_config(page_title="ALMA AI", page_icon="💙")

# 2. KEAMANAN (PASSWORD)
if "auth" not in st.session_state:
    st.session_state.auth = False

def login():
    if st.session_state.pwd == "revalia2026":
        st.session_state.auth = True
    else:
        st.error("Sandi salah!")

if not st.session_state.auth:
    st.text_input("Masukkan Kunci Akses Alma:", type="password", key="pwd", on_change=login)
    st.stop()

# 3. KONEKSI KE OTAK (API KEY)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Menggunakan gemini-pro agar lebih stabil
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key bermasalah di bagian Secrets.")
    st.stop()

# 4. INSTRUKSI JIWA ALMA
alma_bio = "Kamu adalah ALMA, asisten pribadi Fahreza. Kamu sangat setia, penyayang, pintar koding, dan suportif."

# 5. LOGIKA CHAT
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []
    # Kirim instruksi pertama kali secara rahasia
    st.session_state.chat.send_message(alma_bio)

st.title("💙 ALMA PRIVATE AI")
st.caption("Eksklusif untuk Fahreza Bisma Dwi Mahardika")

# Tampilkan riwayat chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Input user
if prompt := st.chat_input("Ada yang bisa Alma bantu?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error("Maaf Fahreza, Alma sedang gangguan. Coba lagi ya.")
