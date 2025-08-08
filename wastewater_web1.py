import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Wastewater Treatment WebApp", layout="wide")

# --- CHỌN NGÔN NGỮ ---
lang = st.sidebar.selectbox("🌐 Language / Ngôn ngữ", ["Tiếng Việt", "English"])
vi = lang == "Tiếng Việt"

def _(vi_text, en_text):
    return vi_text if vi else en_text

# --- TIÊU ĐỀ ---
st.markdown(f"<h2 style='text-align: center;'>💧 { _('Hệ thống xử lý nước thải thông minh', 'Smart Wastewater Treatment System') } 💧</h2>", unsafe_allow_html=True)

# --- THỜI GIAN HIỆN TẠI ---
now = datetime.now()
st.markdown(f"**⏰ { _('Thời gian hiện tại', 'Current time') }:** {now.strftime('%d/%m/%Y – %H:%M:%S')}")

# --- THÔNG BÁO ---
st.info(_("👋 Hệ thống đang chờ dữ liệu từ cảm biến ESP32 hoặc người dùng nhập tay.", "👋 System is waiting for sensor data from ESP32 or manual input."))

# --- NƠI HIỂN THỊ DỮ LIỆU (TÙY BIẾN SAU NÀY) ---
st.subheader(_("📡 Dữ liệu nhận từ ESP32", "📡 Data received from ESP32"))
st.code({
    "time": now.strftime('%H:%M:%S'),
    "pH": "N/A",
    "turbidity": "N/A",
    "temperature": "N/A",
    "status": "Waiting for data..."
}, language="json")
