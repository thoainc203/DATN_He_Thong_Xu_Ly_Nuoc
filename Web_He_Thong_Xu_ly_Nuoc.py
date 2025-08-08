import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Wastewater Treatment WebApp", layout="wide")

# --- LOGO ---
st.image("logo.png", width=120)  # Logo trường

# --- CHỌN NGÔN NGỮ ---
lang = st.sidebar.selectbox("🌐 Language / Ngôn ngữ", ["Tiếng Việt", "English"])
vi = lang == "Tiếng Việt"

def _(vi_text, en_text):
    return vi_text if vi else en_text

# --- ĐĂNG NHẬP ---
def login():
    st.sidebar.markdown("### 🔐 " + _("Đăng nhập", "Login"))
    password = st.sidebar.text_input(_("Nhập mật khẩu:", "Enter password:"), type="password")
    if password == "1234":
        return True
    elif password:
        st.sidebar.error(_("Sai mật khẩu!", "Incorrect password!"))
        return False
    return False

if not login():
    st.stop()

# --- ĐIỀU KHIỂN ĐỘNG CƠ ---
st.markdown("## 🚦 " + _("Điều khiển động cơ", "Motor Control"))
col1, col2 = st.columns(2)

with col1:
    motor1 = st.button(_("BẬT BƠM NƯỚC 1", "TURN ON PUMP 1"))
    motor2 = st.button(_("TẮT BƠM NƯỚC 1", "TURN OFF PUMP 1"))

with col2:
    motor3 = st.button(_("BẬT BƠM NƯỚC 2", "TURN ON PUMP 2"))
    motor4 = st.button(_("TẮT BƠM NƯỚC 2", "TURN OFF PUMP 2"))

# --- THEO DÕI THÔNG SỐ VÀ GIAI ĐOẠN ---
st.markdown("## 📊 " + _("Theo dõi chất lượng nước & Giai đoạn xử lý", "Water Parameters Monitoring & Treatment Stage"))

ph = round(random.uniform(6.5, 8.5), 2)
turbidity = round(random.uniform(0, 5), 2)
temp = round(random.uniform(25, 35), 1)

st.write(_("- Độ pH:", "- pH level:"), ph)
st.write(_("- Độ đục (NTU):", "- Turbidity (NTU):"), turbidity)
st.write(_("- Nhiệt độ (°C):", "- Temperature (°C):"), temp)

if 6.5 <= ph <= 8.5 and turbidity < 5 and 25 <= temp <= 35:
    st.success(_("✔️ Nước đạt chuẩn theo QCVN.", "✔️ Water meets QCVN standards."))
else:
    st.error(_("❌ Nước KHÔNG đạt chuẩn!", "❌ Water does NOT meet standards!"))

st.markdown("### 🔄 " + _("Giai đoạn xử lý hiện tại:", "Current treatment stage:"))
processing_stage = random.choice([
    _("Lắng sơ cấp", "Primary Sedimentation"),
    _("Lọc sinh học", "Biological Filtration"),
    _("Khử trùng", "Disinfection"),
    _("Lắng thứ cấp", "Secondary Sedimentation")
])
st.info(processing_stage)

# --- HIỂN THỊ DỮ LIỆU CẢM BIẾN (cuối giao diện) ---
st.markdown("---")
st.markdown("## 📥 " + _("Dữ liệu cảm biến nhận được", "Sensor Data Received"))

sensor_data = {
    _("pH", "pH"): ph,
    _("Độ đục", "Turbidity"): turbidity,
    _("Nhiệt độ", "Temperature"): temp
}

st.table(sensor_data)
