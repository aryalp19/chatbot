import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# ================================
# 1. CUSTOM CSS STYLING - DARK MODE
# ================================

st.markdown("""
<style>
/* Reset & Dark Theme */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* Main Container */
.main-container {
    max-width: 850px;
    margin: auto;
}

/* Header Styling */
.header-container {
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
    padding: 20px 25px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
}

.header-title {
    font-size: 26px;
    font-weight: 700;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.header-subtitle {
    font-size: 13px;
    opacity: 0.95;
    margin-top: 8px;
}

/* Chat Container */
.chat-container {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 20px;
    min-height: 500px;
    max-height: 600px;
    overflow-y: auto;
    border: 1px solid rgba(148, 163, 184, 0.1);
}

/* Scrollbar Dark */
.chat-container::-webkit-scrollbar {
    width: 8px;
}

.chat-container::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.5);
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: rgba(148, 163, 184, 0.3);
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
    background: rgba(148, 163, 184, 0.5);
}

/* User Message (Right Side) */
.user-message {
    display: flex;
    justify-content: flex-end;
    align-items: flex-start;
    margin: 20px 0;
    animation: slideInRight 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-left: 10px;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    flex-shrink: 0;
}

.user-bubble {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    max-width: 65%;
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
    line-height: 1.5;
    word-wrap: break-word;
}

/* Bot Message (Left Side) */
.bot-message {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    margin: 20px 0;
    animation: slideInLeft 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.bot-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-right: 10px;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    flex-shrink: 0;
}

.bot-bubble {
    background: rgba(51, 65, 85, 0.8);
    backdrop-filter: blur(10px);
    color: #e2e8f0;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    max-width: 65%;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    border-left: 3px solid #10b981;
    line-height: 1.6;
    word-wrap: break-word;
}

/* Timestamp */
.timestamp {
    font-size: 10px;
    color: #94a3b8;
    margin-top: 6px;
    opacity: 0.7;
}

/* Typing Indicator */
.typing-indicator {
    display: flex;
    gap: 6px;
    padding: 14px 18px;
    background: rgba(51, 65, 85, 0.8);
    backdrop-filter: blur(10px);
    border-radius: 18px;
    width: fit-content;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.typing-dot {
    width: 8px;
    height: 8px;
    background: #10b981;
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
@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(40px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-40px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
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
    background: rgba(51, 65, 85, 0.6) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(148, 163, 184, 0.2) !important;
    border-radius: 12px !important;
    padding: 10px 16px !important;
    font-size: 13px !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: rgba(59, 130, 246, 0.3) !important;
    border-color: #3b82f6 !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
}

/* Expander Dark Mode */
.streamlit-expanderHeader {
    background: rgba(51, 65, 85, 0.6) !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(148, 163, 184, 0.2) !important;
}

.streamlit-expanderContent {
    background: rgba(30, 41, 59, 0.8) !important;
    color: #cbd5e1 !important;
    border-radius: 0 0 12px 12px !important;
}

/* Chat Input Dark */
.stChatInput > div {
    background: rgba(51, 65, 85, 0.6) !important;
    border: 1px solid rgba(148, 163, 184, 0.2) !important;
    border-radius: 15px !important;
}

.stChatInput input {
    color: #e2e8f0 !important;
}

/* Divider */
hr {
    border-color: rgba(148, 163, 184, 0.2) !important;
    margin: 20px 0 !important;
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

CONTOH FORMAT JAWABAN YANG BENAR:

SALAH (pakai format markdown):
"Aerox 155 Connected ABS harganya Rp 31.380.000

Fitur unggulannya:
- SmartKey System
- Y-Connect
- ABS"

BENAR (teks biasa bersih):
"Aerox 155 Connected ABS harganya Rp 31.380.000 nih!

Fitur unggulannya ada SmartKey System, Y-Connect, dan ABS. Motor sporty banget dan cocok buat harian maupun weekend riding 👍"

CONTOH PERCAKAPAN:

User: "Bedanya NMAX sama Aerox apa?"
Bot: "Oke aku jelasin ya!

NMAX itu lebih ke premium scooter, nyaman buat jarak jauh, jok lebar, ban lebih gede (13 inci). Cocok buat yang suka touring atau daily commute yang agak jauh.

Aerox lebih sporty dan agile, handling lebih lincah, desain lebih aggressive. Pas banget buat yang suka gaya sporty dan sering belok-belok di kota.

Harganya beda tipis kok, NMAX sekitar 30-31 jutaan, Aerox juga segituan. Mau yang mana nih?"

User: "Tips rawat motor Yamaha biar awet?"
Bot: "Siap! Ini tips dari aku ya:

Pertama, servis rutin sesuai jadwal itu PENTING banget. Jangan sampe telat ganti oli.

Kedua, panasin dulu sebelum riding, jangan langsung gas poll.

Ketiga, cuci motor teratur biar cat dan body tetep kinclong.

Keempat, pake suku cadang original Yamaha biar performa tetep maksimal.

Terakhir, parkir di tempat teduh kalo bisa. Panas terus-terusan bikin cat kusam.

Kalo mau servis, langsung ke dealer kita aja ya. Mekanik kita berpengalaman dan pake parts original semua!"

Inget: Jawab dengan teks biasa yang bersih TANPA SIMBOL FORMAT APAPUN. Jangan pakai bintang, pagar, garis bawah, atau simbol markdown lainnya!
"""
    
    # Create model
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction=system_prompt
    )
    
    return model

# ================================
# 4. CHAT FUNCTION
# ================================

def get_bot_response(model, user_message, chat_history):
    """Get response from Gemini AI"""
    try:
        # Create conversation context
        conversation = []
        
        # Add chat history (last 10 messages for context)
        for msg in chat_history[-10:]:
            if msg["role"] == "user":
                conversation.append({"role": "user", "parts": [msg["text"]]})
            else:
                conversation.append({"role": "model", "parts": [msg["text"]]})
        
        # Add current message
        conversation.append({"role": "user", "parts": [user_message]})
        
        # Generate response
        chat = model.start_chat(history=conversation[:-1])
        response = chat.send_message(user_message)
        
        return response.text.strip()
    
    except Exception as e:
        return f"Waduh, ada error nih 😅\nCoba lagi ya, atau langsung hubungi dealer kami aja!"

# ================================
# 5. MAIN APPLICATION
# ================================

def main():
    # Page config
    st.set_page_config(
        page_title="Yamaha Mustika Anitika",
        page_icon="🏍️",
        layout="centered"
    )
    
    # Initialize session state
    if "model" not in st.session_state:
        with st.spinner("Loading..."):
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
    <div style='text-align: center; color: #94a3b8; font-size: 11px;'>
        Powered by Google Gemini AI • © 2025 Yamaha Mustika Anitika
    </div>
    """, unsafe_allow_html=True)

# ================================
# 6. RUN APPLICATION
# ================================

if __name__ == "__main__":
    main()