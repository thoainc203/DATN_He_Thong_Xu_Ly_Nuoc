import streamlit as st

# --- Thiết lập giao diện ---
st.set_page_config(page_title="Hệ Thống Xử Lý Nước Thải", layout="wide")

# --- Logo và tiêu đề ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("logo.png", width=100)
with col_title:
    st.markdown("### FACULTY OF INTERNATIONAL EDUCATION")
    st.markdown("<h1 style='color: #008080;'>HỆ THỐNG XỬ LÝ NƯỚC THẢI</h1>", unsafe_allow_html=True)

# --- Đăng nhập ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 Đăng nhập hệ thống")
    password = st.text_input("Nhập mật khẩu", type="password")
    if password == "1234":
        st.session_state.authenticated = True
        st.success("✅ Đăng nhập thành công!")
        st.experimental_rerun()
    elif password:
        st.error("❌ Mật khẩu không đúng.")
    st.stop()

# --- Điều khiển động cơ ---
st.subheader("🛠️ Điều Khiển Động Cơ")
col1, col2 = st.columns(2)
with col1:
    if st.button("Bật máy bơm"):
        st.success("✅ Máy bơm đã bật")
with col2:
    if st.button("Tắt máy bơm"):
        st.warning("⚠️ Máy bơm đã tắt")

# --- Theo dõi thông số ---
st.subheader("📈 Theo Dõi Thông Số Nước")

ph = st.slider("pH", 0.0, 14.0, 7.0)
turbidity = st.slider("Độ đục (NTU)", 0.0, 100.0, 30.0)
temperature = st.slider("Nhiệt độ (°C)", 0.0, 100.0, 25.0)

# --- So sánh với tiêu chuẩn ---
st.subheader("📊 So Sánh Với Tiêu Chuẩn")

ph_ok = 6.5 <= ph <= 8.5
turbidity_ok = turbidity <= 50
temp_ok = 20 <= temperature <= 35

col_ph, col_turbidity, col_temp = st.columns(3)

with col_ph:
    st.metric("pH", ph, "✅" if ph_ok else "❌")
with col_turbidity:
    st.metric("Độ đục (NTU)", turbidity, "✅" if turbidity_ok else "❌")
with col_temp:
    st.metric("Nhiệt độ (°C)", temperature, "✅" if temp_ok else "❌")

# --- Giai đoạn xử lý nước ---
st.subheader("🌀 Giai Đoạn Xử Lý Nước")

if not ph_ok or not turbidity_ok or not temp_ok:
    stage = "⚠️ Đang xử lý - Thông số chưa đạt chuẩn"
elif 6.5 <= ph <= 7.5 and turbidity <= 10 and 20 <= temperature <= 30:
    stage = "✅ Hoàn tất xử lý - Nước đạt chuẩn"
else:
    stage = "♻️ Đang lọc và xử lý"

st.info(f"Giai đoạn hiện tại: **{stage}**")

# --- Hiển thị dữ liệu nhận được (đặt cuối giao diện) ---
st.subheader("📥 Dữ Liệu Nhận Được (giả lập)")
st.text_area("Dữ liệu từ cảm biến hoặc hệ thống", height=150)
