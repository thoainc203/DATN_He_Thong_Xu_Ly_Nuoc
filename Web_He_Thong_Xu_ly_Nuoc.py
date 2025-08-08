import streamlit as st
from datetime import datetime
import requests

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Wastewater Treatment WebApp", layout="wide")

# --- YÊU CẦU MẬT KHẨU ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "123456":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Nhập mật khẩu:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Nhập mật khẩu:", type="password", on_change=password_entered, key="password")
        st.error("Sai mật khẩu!")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- LOGO VÀ TIÊU ĐỀ ---
col1, col2 = st.columns([1, 6])
with col1:
    st.image("logo.png", width=100)
with col2:
    st.markdown("""
        <h1 style='margin-bottom: 0;'>Hệ Thống Xử Lý Nước Thải</h1>
        <h4 style='margin-top: 0;'>FACULTY OF INTERNATIONAL EDUCATION</h4>
    """, unsafe_allow_html=True)

# --- CHỌN NGÔN NGỮ ---
lang = st.sidebar.selectbox("🌐 Language / Ngôn ngữ", ["Tiếng Việt", "English"])
vi = lang == "Tiếng Việt"
def _(vi_text, en_text): return vi_text if vi else en_text

# --- THỜI GIAN ---
now = datetime.now()
st.write(f"⏰ { _('Thời gian hiện tại', 'Current time') }: {now.strftime('%d/%m/%Y %H:%M:%S')}")

# --- ĐIỀU KHIỂN ĐỘNG CƠ ---
st.subheader(_("🔧 Điều khiển động cơ", "🔧 Motor Control"))
col1, col2 = st.columns(2)

with col1:
    if st.button(_("Bật bơm nước 💧", "Turn ON Pump 💧")):
        try:
            requests.get("http://192.168.1.100/pump?state=on")
            st.success(_("Đã gửi yêu cầu bật bơm.", "Pump ON command sent."))
        except:
            st.error(_("Không thể kết nối ESP32.", "Failed to connect to ESP32."))

with col2:
    if st.button(_("Tắt bơm nước 🛑", "Turn OFF Pump 🛑")):
        try:
            requests.get("http://192.168.1.100/pump?state=off")
            st.success(_("Đã gửi yêu cầu tắt bơm.", "Pump OFF command sent."))
        except:
            st.error(_("Không thể kết nối ESP32.", "Failed to connect to ESP32."))

# --- THEO DÕI THÔNG SỐ CẢM BIẾN ---
st.subheader(_("📊 Theo dõi thông số cảm biến", "📊 Sensor Monitoring"))

# Giả lập dữ liệu
ph = 7.2
turbidity = 3.5  # NTU
temperature = 29.5

col1, col2, col3 = st.columns(3)
col1.metric("pH", f"{ph}", "6.5 - 8.5")
col2.metric(_("Độ đục (NTU)", "Turbidity (NTU)"), f"{turbidity}", "< 5")
col3.metric(_("Nhiệt độ (°C)", "Temperature (°C)"), f"{temperature}", "25 - 35")

# --- SO SÁNH VỚI TIÊU CHUẨN ---
st.markdown("### 🧪 " + _("So sánh với tiêu chuẩn nước", "Water Quality Standards"))
if 6.5 <= ph <= 8.5:
    st.success(_("pH đạt tiêu chuẩn.", "pH is within standard range."))
else:
    st.error(_("pH không đạt tiêu chuẩn!", "pH is out of range!"))

if turbidity < 5:
    st.success(_("Độ đục đạt tiêu chuẩn.", "Turbidity is acceptable."))
else:
    st.error(_("Độ đục vượt ngưỡng!", "Turbidity too high!"))

if 25 <= temperature <= 35:
    st.success(_("Nhiệt độ ổn định.", "Temperature is normal."))
else:
    st.warning(_("Nhiệt độ bất thường!", "Abnormal temperature!"))

# --- HIỂN THỊ GIAI ĐOẠN XỬ LÝ ---
st.markdown("### 🔄 " + _("Giai đoạn xử lý nước", "Treatment Stage"))

# Giả lập trạng thái
giai_doan = "Lắng"  # Có thể là: Tiếp nhận -> Lắng -> Lọc -> Khử trùng -> Xả thải

st.info(f"🔃 { _('Đang ở giai đoạn', 'Current stage') }: **{giai_doan}**")

# --- HIỂN THỊ DỮ LIỆU NHẬN TỪ ESP32 ---
st.markdown("---")
st.subheader(_("📥 Dữ liệu nhận từ ESP32", "📥 Data received from ESP32"))

st.code({
    "time": now.strftime('%H:%M:%S'),
    "pH": ph,
    "turbidity": turbidity,
    "temperature": temperature,
    "status": "Connected"
}, language="json")
