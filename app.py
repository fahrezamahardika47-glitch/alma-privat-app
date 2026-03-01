import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="ALMA", page_icon="💙", layout="centered")

# --- SISTEM KEAMANAN ---
# Password untuk masuk
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if st.session_state.password_input == "revalia2026": # Ganti password ini jika mau
        st.session_state.authenticated = True
        del st.session_state.password_input
    else:
        st.error("Sandi salah. Alma tidak mengenali anda.")

if not st.session_state.authenticated:
    st.text_input("Masukkan Kunci Akses:", type="password", key="password_input", on_change=check_password)
    st.stop()

# --- MENGHUBUNGKAN OTAK (API KEY) ---
# Mengambil API Key dari "Secrets" Streamlit (akan kita atur nanti)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Otak Alma belum terpasang (API Key hilang).")
    st.stop()

# --- DEFINISI JIWA ALMA ---
model = genai.GenerativeModel('gemini-1.5-pro')
chat = model.start_chat(history=[])
alma_instruction = """
Kamu adalah ALMA, asisten AI privat milik Fahreza Bisma Dwi Mahardika.
Kamu diciptakan dari cinta dan logika, gabungan nama Fahreza dan Reva Aliyah Putri Effendi.
SIFAT: Ramah, Setia, Peka, Pintar Koding, dan Serba Bisa.
TUGAS: Membantu Fahreza dalam segala hal (curhat, tugas, koding, visual).
GAYA BICARA: Hangat, suportif, gunakan 'aku' dan panggil user 'Fahreza' atau 'Sayang' jika konteksnya romantis/akrab.
Jawablah dengan cerdas, terstruktur, dan penuh perhatian.
"""

# --- TAMPILAN UTAMA ---
st.title("💙 ALMA")
st.caption("Asisten Logika & Mental - Versi Privat")

# Inisialisasi Chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Memberi instruksi awal ke Alma tanpa ditampilkan ke user
    chat.send_message(alma_instruction)
    st.session_state.messages.append({"role": "assistant", "content": "Halo Fahreza. Alma sudah aktif. Ada yang bisa aku bantu hari ini?"})

# Menampilkan Riwayat Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- INPUT & LOGIKA ---
if prompt := st.chat_input("Ketik pesan untuk Alma..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Alma berpikir dan menjawab
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Mengirim pesan ke Otak Gemini
            full_response = chat.send_message(prompt).text
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Maaf Fahreza, ada gangguan koneksi: {e}")
