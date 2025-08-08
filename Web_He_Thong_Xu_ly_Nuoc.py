import streamlit as st
from datetime import datetime
import requests

# --- Cấu hình giao diện ---
st.set_page_config(page_title="Wastewater Treatment WebApp", layout="wide")

# --- Kiểm tra mật khẩu ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "123456":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("🔐 Nhập mật khẩu:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("🔐 Nhập mật khẩu:", type="password", on_change=password_entered, key="password")
        st.error("❌ Sai mật khẩu!")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- Giao diện tiêu đề logo ---
with st.container():
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("logo.png", width=100)
    with col2:
        st.markdown("""
            <div style='text-align: left; padding-top: 10px'>
                <h1 style='color:#0072B2; margin-bottom: 5px;'>HỆ THỐNG XỬ LÝ NƯỚC THẢI 💧</h1>
                <h4 style='color: gray;'>FACULTY OF INTERNATIONAL EDUCATION</h4>
            </div>
        """, unsafe_allow_html=True)

# --- Thời gian hiện tại ---
st.markdown(f"⏰ <i>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</i>", unsafe_allow_html=True)
st.markdown("---")

# --- Điều khiển động cơ ---
with st.expander("🛠️ Điều khiển động cơ"):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🟢 BẬT BƠM"):
            try:
                requests.get("http://192.168.1.100/pump?state=on")
                st.success("✅ Đã gửi yêu cầu bật bơm.")
            except:
                st.error("❌ Không thể kết nối ESP32.")
    with col2:
        if st.button("🔴 TẮT BƠM"):
            try:
                requests.get("http://192.168.1.100/pump?state=off")
                st.success("✅ Đã gửi yêu cầu tắt bơm.")
            except:
                st.error("❌ Không thể kết nối ESP32.")

# --- Dữ liệu cảm biến ---
st.markdown("## 📈 Giám sát thông số cảm biến")
ph = 7.2
turbidity = 2.8
temperature = 29.5

col1, col2, col3 = st.columns(3)
col1.metric("🌡️ pH", f"{ph}", "6.5 - 8.5")
col2.metric("🌀 Độ đục (NTU)", f"{turbidity}", "< 5")
col3.metric("🌡️ Nhiệt độ (°C)", f"{temperature}", "25 - 35")

# --- So sánh tiêu chuẩn ---
st.markdown("## ✅ Kiểm tra theo tiêu chuẩn nước")
col1, col2, col3 = st.columns(3)

with col1:
    if 6.5 <= ph <= 8.5:
        st.success("✔️ pH đạt chuẩn.")
    else:
        st.error("⚠️ pH vượt giới hạn!")

with col2:
    if turbidity < 5:
        st.success("✔️ Độ đục đạt chuẩn.")
    else:
        st.error("⚠️ Độ đục cao!")

with col3:
    if 25 <= temperature <= 35:
        st.success("✔️ Nhiệt độ ổn định.")
    else:
        st.warning("⚠️ Nhiệt độ không bình thường!")

# --- Giai đoạn xử lý ---
st.markdown("## 🔄 Giai đoạn xử lý hiện tại")
giai_doan = "Khử trùng"  # Thay đổi được tùy hệ thống
giai_doan_map = {
    "Tiếp nhận": "📥",
    "Lắng": "🧪",
    "Lọc": "🧼",
    "Khử trùng": "☢️",
    "Xả thải": "🏞️"
}
icon = giai_doan_map.get(giai_doan, "🔄")
st.info(f"{icon} Đang ở giai đoạn: **{giai_doan}**")

# --- Hiển thị dữ liệu ESP32 ---
st.markdown("---")
with st.expander("📥 Dữ liệu mới nhất từ ESP32"):
    st.code({
        "time": datetime.now().strftime('%H:%M:%S'),
        "pH": ph,
        "turbidity": turbidity,
        "temperature": temperature,
        "status": "Connected"
    }, language="json")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<center><small>© 2025 - Thiết kế bởi Sinh viên Kỹ thuật - Trường Đại học SPKT TP.HCM</small></center>",
    unsafe_allow_html=True
)
