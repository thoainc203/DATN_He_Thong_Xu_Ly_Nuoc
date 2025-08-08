import streamlit as st
from datetime import datetime
from PIL import Image

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Wastewater Treatment WebApp", layout="wide")

# --- TẢI LOGO & HIỂN THỊ TIÊU ĐỀ ---
col1, col2 = st.columns([1, 5])
with col1:
    logo = Image.open("logo.png")
    st.image(logo, width=100)
with col2:
    st.markdown("<h3 style='margin-bottom:0;'>FACULTY OF INTERNATIONAL EDUCATION</h3>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#0275d8;'>HỆ THỐNG XỬ LÝ NƯỚC THẢI</h1>", unsafe_allow_html=True)

# --- CHỌN NGÔN NGỮ ---
lang = st.sidebar.selectbox("🌐 Language / Ngôn ngữ", ["Tiếng Việt", "English"])
vi = lang == "Tiếng Việt"
def _(vi_text, en_text):
    return vi_text if vi else en_text

# --- ĐĂNG NHẬP ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 Đăng nhập hệ thống")
    password = st.text_input("Nhập mật khẩu", type="password")
    if password == "1234":
        st.session_state.authenticated = True
        st.success("✅ Đăng nhập thành công!")
        st.rerun()
    elif password:
        st.error("❌ Mật khẩu không đúng.")
    st.stop()

# --- THỜI GIAN HIỆN TẠI ---
now = datetime.now()
st.markdown(f"**🕒 { _('Thời gian hiện tại', 'Current time') }:** {now.strftime('%d/%m/%Y %H:%M:%S')}")

# --- THÔNG BÁO ---
st.info(_("Hệ thống đang chờ dữ liệu từ cảm biến ESP32 hoặc người dùng nhập tay.",
          "System is waiting for sensor data from ESP32 or manual input."))

# --- ĐIỀU KHIỂN ĐỘNG CƠ ---
st.subheader("⚙️ " + _("Điều khiển động cơ từ xa", "Remote Motor Control"))
motor_status = st.radio(_("Trạng thái động cơ", "Motor Status"), ["ON", "OFF"], horizontal=True)
if motor_status == "ON":
    st.success(_("Động cơ đang hoạt động", "Motor is ON"))
    # Gửi lệnh ON đến ESP32 tại đây (sử dụng MQTT, HTTP request...)
else:
    st.warning(_("Động cơ đã tắt", "Motor is OFF"))
    # Gửi lệnh OFF đến ESP32 tại đây

# --- THEO DÕI CẢM BIẾN ---
st.subheader("📊 " + _("Thông số cảm biến", "Sensor Monitoring"))
col1, col2, col3 = st.columns(3)
with col1:
    ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=7.0)
with col2:
    turbidity = st.number_input(_("Độ đục (NTU)", "Turbidity (NTU)"), min_value=0.0, value=1.0)
with col3:
    temp = st.number_input(_("Nhiệt độ (°C)", "Temperature (°C)"), min_value=0.0, value=25.0)

# --- ĐÁNH GIÁ TIÊU CHUẨN NƯỚC ---
st.subheader("✅ " + _("So sánh với tiêu chuẩn nước", "Compare with Water Standards"))
def check_standard(ph, turbidity, temp):
    ph_ok = 6.5 <= ph <= 8.5
    turbidity_ok = turbidity <= 5
    temp_ok = 15 <= temp <= 35
    return ph_ok, turbidity_ok, temp_ok

ph_ok, turbidity_ok, temp_ok = check_standard(ph, turbidity, temp)
st.markdown(f"**pH:** {'✅' if ph_ok else '❌'} ({ph})")
st.markdown(f"**{_('Độ đục', 'Turbidity')}:** {'✅' if turbidity_ok else '❌'} ({turbidity} NTU)")
st.markdown(f"**{_('Nhiệt độ', 'Temperature')}:** {'✅' if temp_ok else '❌'} ({temp} °C)")

# --- GIAI ĐOẠN XỬ LÝ NƯỚC ---
st.subheader("🔄 " + _("Giai đoạn xử lý nước", "Water Treatment Stages"))
st.markdown("""
- 🟢 **Bể thu gom**: Nước thải được gom từ nhiều nguồn.
- 🔵 **Bể lắng sơ cấp**: Loại bỏ chất rắn lớn.
- 🧪 **Bể xử lý sinh học**: Phân hủy chất hữu cơ.
- ⚙️ **Bể lắng thứ cấp**: Loại bỏ bùn hoạt tính.
- 💧 **Khử trùng**: Dùng Clo/UV diệt vi khuẩn.
- 🏁 **Xả thải đạt chuẩn**: Xả nước ra môi trường.
""")

# --- DỮ LIỆU NHẬN TỪ ESP32 (dưới cùng) ---
st.divider()
st.subheader(_("📥 Dữ liệu nhận từ ESP32", "📥 Data received from ESP32"))
st.code({
    "time": now.strftime('%H:%M:%S'),
    "pH": ph,
    "turbidity": turbidity,
    "temperature": temp,
    "motor_status": motor_status
}, language="json")
