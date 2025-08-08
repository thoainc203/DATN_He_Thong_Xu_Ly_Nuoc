import streamlit as st

# --- Authentication ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "123456":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Nhập mật khẩu để truy cập:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Nhập mật khẩu để truy cập:", type="password", on_change=password_entered, key="password")
        st.error("Sai mật khẩu, vui lòng thử lại.")
        return False
    else:
        return True

if check_password():
    # Giao diện chính
    st.set_page_config(layout="wide")
    st.title("🛠️ Điều khiển hệ thống xử lý nước thải")

    # Điều khiển động cơ
    st.subheader("🔌 Điều khiển động cơ")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Bật bơm nước"):
            st.success("✅ Đã bật bơm nước")
            # Gửi lệnh đến thiết bị ở đây

    with col2:
        if st.button("Tắt bơm nước"):
            st.warning("🛑 Đã tắt bơm nước")
            # Gửi lệnh đến thiết bị ở đây

    st.markdown("---")

    # Theo dõi thông số chất lượng nước
    st.subheader("📊 Theo dõi thông số nước")
    col3, col4, col5 = st.columns(3)
    with col3:
        ph = st.slider("pH", 0.0, 14.0, 7.0)
        if ph < 6.5 or ph > 8.5:
            st.error("❌ pH nằm ngoài tiêu chuẩn (6.5 - 8.5)")
        else:
            st.success("✅ pH đạt chuẩn")

    with col4:
        turbidity = st.slider("Độ đục (NTU)", 0.0, 100.0, 5.0)
        if turbidity > 10:
            st.error("❌ Độ đục cao, cần xử lý")
        else:
            st.success("✅ Độ đục trong giới hạn cho phép")

    with col5:
        temp = st.slider("Nhiệt độ (°C)", 0.0, 100.0, 25.0)
        if temp < 10 or temp > 45:
            st.warning("⚠️ Nhiệt độ bất thường")
        else:
            st.success("✅ Nhiệt độ ổn định")

    # Hiển thị giai đoạn xử lý nước
    st.markdown("---")
    st.subheader("🧪 Giai đoạn xử lý nước")
    giai_doan = st.radio("Chọn giai đoạn:", [
        "1. Tiếp nhận nước thải",
        "2. Xử lý cơ học",
        "3. Xử lý sinh học",
        "4. Lắng và khử trùng",
        "5. Thoát nước sạch ra môi trường"
    ])
    st.info(f"Đang ở giai đoạn: {giai_doan}")

    # Hiển thị dữ liệu nhận được từ thiết bị
    st.markdown("---")
    st.subheader("📥 Dữ liệu cảm biến nhận được")
    st.write("(Ví dụ: hiển thị dữ liệu từ cảm biến, thiết bị IoT...)")
