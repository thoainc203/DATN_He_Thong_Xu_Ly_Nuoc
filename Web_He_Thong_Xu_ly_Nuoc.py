import requests

# --- ĐIỀU KHIỂN ĐỘNG CƠ TỪ XA ---
st.subheader(_("🚀 Điều khiển động cơ", "🚀 Remote Motor Control"))

# Nhập địa chỉ IP của ESP32
esp32_ip = st.text_input(_("🔗 Nhập địa chỉ IP của ESP32:", "🔗 Enter ESP32 IP address:"), "http://192.168.1.100")

col1, col2 = st.columns(2)

with col1:
    if st.button(_("▶️ BẬT ĐỘNG CƠ", "▶️ TURN ON MOTOR")):
        try:
            response = requests.get(f"{esp32_ip}/motor?state=on", timeout=5)
            st.success(_("✅ Đã gửi lệnh bật động cơ.", "✅ Motor ON command sent."))
            st.json(response.json() if response.headers.get("content-type") == "application/json" else response.text)
        except Exception as e:
            st.error(_("❌ Không thể kết nối đến ESP32.", "❌ Cannot connect to ESP32."))
            st.exception(e)

with col2:
    if st.button(_("⏹️ TẮT ĐỘNG CƠ", "⏹️ TURN OFF MOTOR")):
        try:
            response = requests.get(f"{esp32_ip}/motor?state=off", timeout=5)
            st.success(_("✅ Đã gửi lệnh tắt động cơ.", "✅ Motor OFF command sent."))
            st.json(response.json() if response.headers.get("content-type") == "application/json" else response.text)
        except Exception as e:
            st.error(_("❌ Không thể kết nối đến ESP32.", "❌ Cannot connect to ESP32."))
            st.exception(e)
