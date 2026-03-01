import streamlit as st
import google.generativeai as genai

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="ALMA", page_icon="💙")

# 2. SISTEM KEAMANAN (Login)
if "auth" not in st.session_state:
    st.session_state.auth = False

def check_password():
    if st.session_state.pwd == "revalia2026":
        st.session_state.auth = True

if not st.session_state.auth:
    st.text_input("Masukkan Sandi Alma:", type="password", key="pwd", on_change=check_password)
    st.stop()

# 3. KONEKSI KE OTAK (Versi Langsung)
# Kita langsung panggil kuncinya tanpa 'try-except' biar tidak error syntax
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Menggunakan model Flash (Paling Cepat & Stabil)
model = genai.GenerativeModel("gemini-1.5-flash")

# 4. MEMULAI OBROLAN
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    
    # Instruksi Jiwa Alma
    instruksi = """
    Kamu adalah ALMA, asisten pribadi Fahreza.
    Sifat: Ramah, Setia, Peka, Pintar Koding.
    Tugas: Membantu Fahreza dalam segala hal.
    """
    st.session_state.chat.send_message(instruksi)
    st.session_state.messages = []

# 5. TAMPILAN CHAT
st.title("💙 ALMA")
st.caption("Asisten Logika & Mental - Versi Privat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ketik pesan untuk Alma..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Alma Menjawab
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Maaf, ada gangguan koneksi: {e}")
