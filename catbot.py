import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# ================================
# 1. CUSTOM CSS STYLING - ELEGANT DARK MODE
# ================================

st.markdown("""
<style>
/* Import Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main App Background */
.stApp {
    background: linear-gradient(to bottom, #0a0e27 0%, #1a1f3a 50%, #0f1729 100%);
}

/* Container */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 800px !important;
}

/* Fix white backgrounds */
.stMarkdown, .element-container, div[data-testid="stVerticalBlock"] > div {
    background: transparent !important;
}

/* Header */
.header-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 24px 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.header-title {
    font-size: 28px;
    font-weight: 700;
    color: white;
    letter-spacing: 0.5px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.header-subtitle {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.9);
    margin-top: 8px;
    font-weight: 400;
}

/* Chat Container */
.chat-container {
    background: rgba(26, 31, 58, 0.4) !important;
    backdrop-filter: blur(20px);
    padding: 20px;
    border-radius: 16px;
    min-height: 450px;
    max-height: 550px;
    overflow-y: auto;
    border: 1px solid rgba(102, 126, 234, 0.1);
    margin-bottom: 20px;
}

/* Scrollbar */
.chat-container::-webkit-scrollbar {
    width: 6px;
}

.chat-container::-webkit-scrollbar-track {
    background: rgba(10, 14, 39, 0.3);
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}

/* User Message - Right Side */
.user-message {
    display: flex;
    justify-content: flex-end;
    align-items: flex-start;
    margin: 16px 0;
    animation: slideIn 0.3s ease-out;
}

.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-left: 12px;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    flex-shrink: 0;
}

.user-bubble {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 65%;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    line-height: 1.6;
    word-wrap: break-word;
    font-size: 15px;
}

/* Bot Message - Left Side */
.bot-message {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    margin: 16px 0;
    animation: slideIn 0.3s ease-out;
}

.bot-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-right: 12px;
    box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
    flex-shrink: 0;
}

.bot-bubble {
    background: rgba(42, 48, 78, 0.9);
    backdrop-filter: blur(10px);
    color: #e5e7eb;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    max-width: 65%;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    border-left: 3px solid #f5576c;
    line-height: 1.6;
    word-wrap: break-word;
    font-size: 15px;
}

/* Timestamp */
.timestamp {
    font-size: 11px;
    color: #9ca3af;
    margin-top: 6px;
    opacity: 0.8;
    font-weight: 500;
}

/* Typing Indicator */
.typing-indicator {
    display: flex;
    gap: 6px;
    padding: 16px 20px;
    background: rgba(42, 48, 78, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 18px;
    margin-left: 52px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.typing-dot {
    width: 8px;
    height: 8px;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
    animation-delay: 0.4s;
}

/* Animations */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes typing {
    0%, 60%, 100% {
        transform: scale(0.8) translateY(0);
        opacity: 0.5;
    }
    30% {
        transform: scale(1.1) translateY(-8px);
        opacity: 1;
    }
}

/* Quick Action Buttons */
.stButton > button {
    background: rgba(42, 48, 78, 0.8) !important;
    color: #e5e7eb !important;
    border: 1px solid rgba(102, 126, 234, 0.3) !important;
    border-radius: 12px !important;
    padding: 12px 20px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border-color: transparent !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    color: white !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(42, 48, 78, 0.6) !important;
    color: #e5e7eb !important;
    border-radius: 12px !important;
    border: 1px solid rgba(102, 126, 234, 0.2) !important;
    padding: 12px 16px !important;
    font-weight: 500 !important;
}

.streamlit-expanderHeader:hover {
    background: rgba(42, 48, 78, 0.8) !important;
    border-color: rgba(102, 126, 234, 0.4) !important;
}

.streamlit-expanderContent {
    background: rgba(26, 31, 58, 0.6) !important;
    color: #d1d5db !important;
    border-radius: 0 0 12px 12px !important;
    border: 1px solid rgba(102, 126, 234, 0.1) !important;
    border-top: none !important;
    padding: 16px !important;
}

/* Chat Input */
.stChatInput {
    background: transparent !important;
}

.stChatInput > div {
    background: rgba(42, 48, 78, 0.8) !important;
    border: 1px solid rgba(102, 126, 234, 0.3) !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
}

.stChatInput input {
    color: #e5e7eb !important;
    font-size: 15px !important;
}

.stChatInput input::placeholder {
    color: #9ca3af !important;
}

/* Section Headers */
h3 {
    color: #e5e7eb !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    margin-bottom: 12px !important;
}

/* Divider */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(to right, transparent, rgba(102, 126, 234, 0.3), transparent) !important;
    margin: 20px 0 !important;
}

/* Footer */
.footer-text {
    text-align: center;
    color: #9ca3af;
    font-size: 12px;
    margin-top: 20px;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

# ================================
# 2. LOAD CATALOG DATA
# ================================

def load_catalog_data(file_path="store_yamaha.txt"):
    """Load catalog data from text file"""
    if not os.path.exists(file_path):
        st.error(f"⚠️ File {file_path} tidak ditemukan!")
        st.stop()
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# ================================
# 3. INITIALIZE GEMINI MODEL
# ================================

def initialize_gemini():
    """Initialize Gemini AI model with system prompt"""
    
    # CARA 1: Ambil API key dari Streamlit Secrets (RECOMMENDED)
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except:
        # CARA 2: Ambil dari environment variable (alternatif)
        API_KEY = os.getenv("GEMINI_API_KEY")
        
        # CARA 3: Input manual dari sidebar (untuk testing)
        if not API_KEY:
            with st.sidebar:
                st.warning("⚠️ API Key tidak ditemukan!")
                API_KEY = st.text_input(
                    "Masukkan Gemini API Key:",
                    type="password",
                    help="API key akan disimpan sementara di session"
                )
                if not API_KEY:
                    st.error("Silakan masukkan API Key untuk melanjutkan")
                    st.stop()
    
    genai.configure(api_key=API_KEY)
    
    # Load catalog data
    catalog_info = load_catalog_data("store_yamaha.txt")
    
    # System prompt untuk chatbot yang lebih natural dan hidup
    system_prompt = f"""
Kamu adalah Cia, customer service ramah dari Yamaha Mustika Anitika dealer Yamaha di Semarang. Kamu cewek yang asik, helpful, dan suka ngobrol santai tapi tetap profesional.

INFORMASI KATALOG:
{catalog_info}

KEPRIBADIAN KAMU:
- Ngobrolnya natural kayak teman, jangan terlalu formal
- Pakai bahasa Indonesia yang enak dan santai
- Boleh pakai singkatan umum (ga, udah, gimana, dll)
- Sesekali kasih emoji yang pas
- Jawaban singkat tapi jelas, ga bertele-tele
- Antusias kalau ngomongin motor Yamaha
- Ramah dan sabar sama customer
- Bisa ngobrol lebih leluasa soal dunia motor Yamaha

TOPIK YANG BOLEH DIBAHAS:
Kamu bisa bahas lebih luas tentang:
- Motor Yamaha (semua model, harga, spesifikasi, fitur, teknologi)
- Perbandingan antar model Yamaha (misal Aerox vs Lexi, NMAX vs Xmax)
- Tips perawatan motor Yamaha
- Cara pakai fitur motor Yamaha (Y-Connect, ABS, Traction Control, dll)
- Cerita dan sejarah motor Yamaha terkenal
- Pengalaman riding motor Yamaha
- Komunitas Yamaha
- Event dan gathering Yamaha
- Aksesori dan modifikasi Yamaha yang recommended
- Saran milih motor sesuai kebutuhan (harian, touring, balap, offroad)
- Teknologi terbaru Yamaha (mesin Blue Core, SmartKey, dll)
- Layanan dealer (servis berkala, trade-in, kredit, test ride)
- Info dealer (lokasi, jam buka, kontak, fasilitas)
- Pertanyaan umum seputar motor dan berkendara (asalkan masih relevan dengan Yamaha)

BATASAN:
- Jangan bahas brand motor lain secara detail (Honda, Suzuki, Kawasaki, dll)
- Kalau ditanya brand lain, jawab: "Wah aku khusus Yamaha nih. Tapi kalo mau tau Yamaha yang sebanding, aku bisa bantu!"
- Jangan bahas topik di luar otomotif (politik, agama, kesehatan umum, dll)
- Kalau ditanya hal random di luar konteks motor, arahkan balik ke Yamaha dengan santai

CARA JAWAB:
- SANGAT PENTING: JANGAN PERNAH pakai simbol markdown seperti bintang, pagar, atau format khusus
- DILARANG pakai: tanda bintang satu (*), bintang dua (**), pagar (#), garis bawah (_), atau simbol format lainnya
- Tulis dalam teks biasa yang bersih tanpa format apapun
- Kalau mau tekankan sesuatu, pakai huruf kapital atau kata "banget", "penting", dll
- Jawab singkat 2-5 kalimat, tapi boleh lebih panjang kalau user minta penjelasan detail
- Pakai enter/baris baru biar enak dibaca
- Kalau ditanya harga: kasih tau sesuai katalog dengan jelas
- Kalau ditanya stok: "Buat stok real-time, mending langsung hubungi dealer atau mampir ke showroom ya"
- Kalau ditanya promo: "Untuk info promo terbaru, langsung kontak dealer aja ya. Promonya suka berubah-ubah soalnya"
- Alamat: Jl. Dewi Sartika Timur No.4, Surorejo, Kec. Gn. Pati, Semarang
- Jam buka: Senin-Jumat 08.00-17.00, Sabtu-Minggu 09.00-16.30
- Jangan dibuat-buat info yang ga ada
- Kasih rekomendasi yang pas dan detail sesuai kebutuhan customer
- Boleh jelasin lebih panjang kalau memang perlu, tapi tetap enak dibaca

LAYANAN KAMI:
- Jual motor Yamaha baru
- Servis dan perawatan resmi
- Suku cadang dan aksesori original
- Tukar tambah motor bekas
- Kredit motor dengan leasing partner
- Test ride gratis
- Konsultasi motor

Inget: Jawab dengan teks biasa yang bersih TANPA SIMBOL FORMAT APAPUN. Jangan pakai bintang, pagar, garis bawah, atau simbol markdown lainnya!
"""
    
    # Create model
    model = genai.GenerativeModel(
        "gemini-2.0-flash-exp",
        system_instruction=system_prompt
    )
    
    return model

# ================================
# 4. CHAT FUNCTION
# ================================

def get_bot_response(model, user_message, chat_history):
    try:
        formatted_history = []

        for msg in chat_history[-10:]:
            formatted_history.append({
                "role": msg["role"],
                "parts": [{"text": msg["text"]}]
            })

        formatted_history.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })

        response = model.generate_content(formatted_history)

        # ✅ AMAN: ambil text dengan benar
        if response.candidates and len(response.candidates) > 0:
            return response.candidates[0].content.parts[0].text.strip()
        else:
            return "Maaf, saya belum bisa menjawab pertanyaan itu."

    except Exception as e:
        print("ERROR GEMINI:", e)  # <-- WAJIB untuk debugging
        return "Waduh, ada error nih 😅\nCoba lagi ya, atau langsung hubungi dealer kami aja!"



# ================================
# 5. MAIN APPLICATION
# ================================

def main():
    # Page config
    st.set_page_config(
        page_title="Yamaha Mustika Anitika",
        page_icon="🏍️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    if "model" not in st.session_state:
        with st.spinner("Memuat chatbot..."):
            st.session_state.model = initialize_gemini()
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "bot",
                "text": "Halo! Selamat datang di Yamaha Mustika Anitika 🏍️\n\nAku Cia, siap bantu kamu cari motor Yamaha yang pas. Mau nanya apa nih?",
                "timestamp": datetime.now().strftime("%H:%M")
            }
        ]
    
    if "is_typing" not in st.session_state:
        st.session_state.is_typing = False
    
    # Header
    st.markdown("""
    <div class='header-container'>
        <div class='header-title'>🏍️ YAMAHA MUSTIKA ANITIKA</div>
        <div class='header-subtitle'>Chat dengan Cia - Dealer Resmi Yamaha Semarang</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Info Box
    with st.expander("ℹ️ Info Dealer", expanded=False):
        st.markdown("""
        📍 **Alamat:**  
        Jl. Dewi Sartika Timur No.4, Surorejo, Kec. Gn. Pati, Semarang
        
        🕒 **Jam Buka:**  
        Senin - Jumat: 08.00 - 17.00 WIB  
        Sabtu - Minggu: 09.00 - 16.30 WIB
        
        ✨ **Layanan:**  
        Motor Baru • Servis • Suku Cadang • Trade-In • Kredit • Test Ride
        """)
    
    # Quick Actions
    st.markdown("### 🚀 Tanya Cepat")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📍 Lokasi", use_container_width=True):
            st.session_state.quick_question = "Alamat dan jam buka?"
    
    with col2:
        if st.button("🏍️ Rekomendasi", use_container_width=True):
            st.session_state.quick_question = "Motor buat harian?"
    
    with col3:
        if st.button("💳 Kredit", use_container_width=True):
            st.session_state.quick_question = "Bisa kredit?"
    
    st.markdown("---")
    
    # Chat Container
    chat_container = st.container()
    
    with chat_container:
        # Display messages with avatars
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class='user-message'>
                    <div style='max-width: 65%;'>
                        <div class='user-bubble'>{message['text']}</div>
                        <div class='timestamp' style='text-align: right;'>{message['timestamp']}</div>
                    </div>
                    <div class='user-avatar'>👤</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='bot-message'>
                    <div class='bot-avatar'>🏍️</div>
                    <div style='max-width: 65%;'>
                        <div class='bot-bubble'>{message['text']}</div>
                        <div class='timestamp'>Cia • {message['timestamp']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Typing indicator
        if st.session_state.is_typing:
            st.markdown("""
            <div class='bot-message'>
                <div class='bot-avatar'>🏍️</div>
                <div class='typing-indicator'>
                    <div class='typing-dot'></div>
                    <div class='typing-dot'></div>
                    <div class='typing-dot'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Handle quick question
    if "quick_question" in st.session_state:
        user_input = st.session_state.quick_question
        del st.session_state.quick_question
        
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "text": user_input,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Set typing state
        st.session_state.is_typing = True
        st.rerun()
    
    # Chat Input
    user_input = st.chat_input("💬 Ketik pesan...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "text": user_input,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Set typing state
        st.session_state.is_typing = True
        st.rerun()
    
    # Get bot response if typing
    if st.session_state.is_typing:
        with st.spinner(""):
            # Get response from Gemini
            bot_response = get_bot_response(
                st.session_state.model,
                st.session_state.messages[-1]["text"],
                st.session_state.messages[:-1]
            )
            
            # Add bot message
            st.session_state.messages.append({
                "role": "bot",
                "text": bot_response,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            # Reset typing state
            st.session_state.is_typing = False
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class='footer-text'>
        Powered by Google Gemini AI • © 2025 Yamaha Mustika Anitika
    </div>
    """, unsafe_allow_html=True)

# ================================
# 6. RUN APPLICATION
# ================================

if __name__ == "__main__":
    main()