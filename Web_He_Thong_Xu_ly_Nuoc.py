import streamlit as st
from datetime import datetime
import requests

# --- Cấu hình giao diện ---
st.set_page_config(page_title="Wastewater Treatment WebApp", layout="wide")

# --- Giao diện đăng nhập nhỏ gọn ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "123456":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state or not st.session_state["password_correct"]:
        st.markdown("<br><br>", unsafe_allow_html=True)  # tạo khoảng cách trên cùng
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image("logo.png", width=80)
            with col2:
                st.markdown("<h3 style='margin-bottom: 5px; color:#0072B2'>HỆ THỐNG XỬ LÝ NƯỚC THẢI</h3>", unsafe_allow_html=True)
                st.markdown("<small style='color: gray;'>FACULTY OF INTERNATIONAL EDUCATION</small>", unsafe_allow_html=True)
                st.text_input("🔐 Mật khẩu:", type="password", on_change=password_entered, key="password")

        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
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
                <h1 style='color:#0072B2; margin-bottom: 5px;'>HỆ THỐNG XỬ LÝ NƯỚC THẢI </h1>
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
                requests.get("http://192.168.1.100/pump?state=on", timeout=2)
                st.success("✅ Đã gửi yêu cầu bật bơm.")
            except:
                st.error("❌ Không thể kết nối ESP32.")
    with col2:
        if st.button("🔴 TẮT BƠM"):
            try:
                requests.get("http://192.168.1.100/pump?state=off", timeout=2)
                st.success("✅ Đã gửi yêu cầu tắt bơm.")
            except:
                st.error("❌ Không thể kết nối ESP32.")

# --- Báo trạng thái động cơ ---
st.markdown("## 📢 Trạng thái động cơ")
try:
    response = requests.get("http://192.168.1.100/pump/status", timeout=2)  # ESP32 trả JSON
    if response.status_code == 200:
        status_data = response.json()
        motor_status = status_data.get("motor", "unknown")
        error_flag = status_data.get("error", False)

        if error_flag:
            st.error("🚨 CẢNH BÁO: Động cơ gặp sự cố! Dừng ngay để kiểm tra.")
        else:
            if motor_status == "on":
                st.success("🟢 Động cơ đang hoạt động bình thường.")
            elif motor_status == "off":
                st.warning("🔴 Động cơ đang tắt.")
            else:
                st.info("ℹ️ Không xác định trạng thái động cơ.")
    else:
        st.error("⚠️ Không thể đọc trạng thái từ ESP32.")
except:
    st.error("❌ Mất kết nối với ESP32.")

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
