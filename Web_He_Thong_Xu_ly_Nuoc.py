import streamlit as st
from datetime import datetime
import requests
import random

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

# --- THEO DÕI THÔNG SỐ ---
st.subheader(_("📊 Theo dõi thông số nước", "📊 Water Parameter Monitoring"))

# Giả lập dữ liệu
ph = round(random.uniform(5.5, 9.0), 2)
turbidity = round(random.uniform(10, 100), 1)  # NTU
temperature = round(random.uniform(20, 40), 1)

col1, col2, col3 = st.columns(3)
col1.metric("🌡️ " + _("Nhiệt độ (°C)", "Temperature (°C)"), f"{temperature} °C")
col2.metric("🧪 " + _("pH", "pH"), ph)
col3.metric("🌫️ " + _("Độ đục (NTU)", "Turbidity (NTU)"), turbidity)

# --- SO SÁNH TIÊU CHUẨN ---
st.subheader(_("📏 So sánh với tiêu chuẩn nước đầu ra", "📏 Comparison to Water Standards"))

standard_ph = (6.5, 8.5)
standard_turbidity = 50
standard_temp = 35

st.write(_("✅ Giá trị trong phạm vi an toàn." if (standard_ph[0] <= ph <= standard_ph[1] and turbidity <= standard_turbidity and temperature <= standard_temp)
         else "⚠️ Một hoặc nhiều thông số vượt giới hạn tiêu chuẩn.", 
         "✅ Safe range." if (standard_ph[0] <= ph <= standard_ph[1] and turbidity <= standard_turbidity and temperature <= standard_temp)
         else "⚠️ One or more parameters exceed standard limits."))

# --- GIAI ĐOẠN XỬ LÝ NƯỚC ---
st.subheader(_("🚧 Giai đoạn xử lý nước", "🚧 Water Treatment Stage"))

if turbidity > 80:
    stage = _("❌ Đầu vào chưa xử lý", "❌ Untreated input")
elif 50 < turbidity <= 80:
    stage = _("🔄 Đang xử lý: Lắng và lọc", "🔄 In process: Settling and filtering")
elif turbidity <= 50 and ph >= 6.5 and ph <= 8.5:
    stage = _("✅ Đã xử lý đạt chuẩn", "✅ Treated and safe")
else:
    stage = _("⚠️ Cần điều chỉnh pH hoặc nhiệt độ", "⚠️ Adjust pH or temperature needed")

st.success(stage)

# --- DỮ LIỆU NHẬN TỪ ESP32 (CUỐI) ---
st.markdown("---")
st.subheader(_("📥 Dữ liệu nhận từ ESP32", "📥 Data received from ESP32"))
st.code({
    "time": now.strftime('%H:%M:%S'),
    "pH": ph,
    "turbidity": turbidity,
    "temperature": temperature,
    "status": "Đang giám sát..." if vi else "Monitoring..."
}, language="json")
