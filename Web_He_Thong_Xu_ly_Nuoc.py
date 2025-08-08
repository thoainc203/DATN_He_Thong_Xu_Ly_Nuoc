import streamlit as st
from datetime import datetime
import requests

# ---------------------- PHẦN ĐĂNG NHẬP ------------------------
PASSWORD = "123456"  # Thay đổi nếu cần

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Đăng nhập hệ thống")
    password = st.text_input("Nhập mật khẩu để truy cập:", type="password")
    if st.button("Đăng nhập"):
        if password == PASSWORD:
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("❌ Sai mật khẩu!")
    st.stop()

# ---------------------- GIAO DIỆN CHÍNH ------------------------
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

# --- ĐIỀU KHIỂN ĐỘNG CƠ ---
st.subheader(_("🔧 Điều khiển động cơ từ xa", "🔧 Remote Motor Control"))

col1, col2 = st.columns(2)
with col1:
    if st.button(_("BẬT động cơ", "Turn ON Motor")):
        try:
            requests.get("http://your_esp32_ip/on")  # Thay bằng IP ESP32 thật
            st.success(_("Đã gửi lệnh bật động cơ.", "Motor ON command sent."))
        except:
            st.error(_("Không thể gửi lệnh đến ESP32.", "Failed to contact ESP32."))
with col2:
    if st.button(_("TẮT động cơ", "Turn OFF Motor")):
        try:
            requests.get("http://your_esp32_ip/off")  # Thay bằng IP ESP32 thật
            st.success(_("Đã gửi lệnh tắt động cơ.", "Motor OFF command sent."))
        except:
            st.error(_("Không thể gửi lệnh đến ESP32.", "Failed to contact ESP32."))

# --- THEO DÕI CẢM BIẾN ---
st.subheader(_("📈 Theo dõi cảm biến", "📈 Sensor Monitoring"))

# (Dữ liệu giả lập – bạn có thể thay bằng dữ liệu từ Firebase hoặc API)
ph = 6.8
turbidity = 12.0  # NTU
temperature = 29.0  # Celsius

st.metric(label=_("pH", "pH"), value=ph)
st.metric(label=_("Độ đục (NTU)", "Turbidity (NTU)"), value=turbidity)
st.metric(label=_("Nhiệt độ (°C)", "Temperature (°C)"), value=temperature)

# --- SO SÁNH TIÊU CHUẨN ---
st.subheader(_("📊 So sánh với tiêu chuẩn nước", "📊 Compare with Water Standard"))

def check_standard(name, value, min_val, max_val):
    if min_val <= value <= max_val:
        return f"✅ {name}: {value} ({_('Đạt', 'OK')})"
    else:
        return f"❌ {name}: {value} ({_('Không đạt', 'Not OK')})"

st.write(check_standard("pH", ph, 6.5, 8.5))
st.write(check_standard(_("Độ đục", "Turbidity"), turbidity, 0, 20))
st.write(check_standard(_("Nhiệt độ", "Temperature"), temperature, 20, 35))

# --- GIAI ĐOẠN XỬ LÝ ---
st.subheader(_("🔄 Giai đoạn xử lý nước thải", "🔄 Wastewater Treatment Stages"))
st.info(_("Đang trong giai đoạn: Xử lý sinh học", "Current stage: Biological Treatment"))

# --- DỮ LIỆU TỪ ESP32 ---
st.subheader(_("🛰️ Dữ liệu nhận từ ESP32", "🛰️ Data received from ESP32"))
st.code({
    "time": now.strftime('%H:%M:%S'),
    "pH": ph,
    "turbidity": turbidity,
    "temperature": temperature,
    "status": "Đang giám sát..." if vi else "Monitoring..."
}, language="json")
