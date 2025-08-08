import streamlit as st
from datetime import datetime
import requests

# Cấu hình giao diện
st.set_page_config(page_title="Wastewater Treatment WebApp", layout="wide")

# --- CHỌN NGÔN NGỮ ---
lang = st.sidebar.selectbox("🌐 Language / Ngôn ngữ", ["Tiếng Việt", "English"])
vi = lang == "Tiếng Việt"

def _(vi_text, en_text):
    return vi_text if vi else en_text

# --- TIÊU ĐỀ ---
st.markdown(f"<h2 style='text-align: center;'> { _('Hệ thống xử lý nước thải thông minh', 'Smart Wastewater Treatment System') } </h2>", unsafe_allow_html=True)

# --- THỜI GIAN HIỆN TẠI ---
now = datetime.now()
st.markdown(f" { _('Thời gian hiện tại', 'Current time') }: {now.strftime('%d/%m/%Y')}")

# --- THÔNG BÁO ---
st.info(_(" Hệ thống đang chờ dữ liệu từ cảm biến ESP32 hoặc người dùng nhập tay.", " System is waiting for sensor data from ESP32 or manual input."))

# --- ĐIỀU KHIỂN ĐỘNG CƠ ---
st.subheader(_("🚀 Điều khiển động cơ", "🚀 Remote Motor Control"))
esp32_ip = st.text_input(_("🔗 Nhập địa chỉ IP của ESP32:", "🔗 Enter ESP32 IP address:"), "http://192.168.1.100")

col1, col2 = st.columns(2)

with col1:
    if st.button(_("▶️ BẬT ĐỘNG CƠ", "▶️ TURN ON MOTOR")):
        try:
            response = requests.get(f"{esp32_ip}/motor?state=on", timeout=5)
            st.success(_("✅ Đã gửi lệnh bật động cơ.", "✅ Motor ON command sent."))
            st.json(response.json() if "application/json" in response.headers.get("content-type", "") else response.text)
        except Exception as e:
            st.error(_("❌ Không thể kết nối đến ESP32.", "❌ Cannot connect to ESP32."))
            st.exception(e)

with col2:
    if st.button(_("⏹️ TẮT ĐỘNG CƠ", "⏹️ TURN OFF MOTOR")):
        try:
            response = requests.get(f"{esp32_ip}/motor?state=off", timeout=5)
            st.success(_("✅ Đã gửi lệnh tắt động cơ.", "✅ Motor OFF command sent."))
            st.json(response.json() if "application/json" in response.headers.get("content-type", "") else response.text)
        except Exception as e:
            st.error(_("❌ Không thể kết nối đến ESP32.", "❌ Cannot connect to ESP32."))
            st.exception(e)

# --- HIỂN THỊ DỮ LIỆU NHẬN ĐƯỢC (ĐƯA XUỐNG CUỐI) ---
st.markdown("---")
st.subheader(_("📥 Dữ liệu nhận từ ESP32", "📥 Data received from ESP32"))
st.code({
    "time": now.strftime('%H:%M:%S'),
    "pH": "N/A",
    "turbidity": "N/A",
    "temperature": "N/A",
    "status": "Waiting for data..."
}, language="json")
