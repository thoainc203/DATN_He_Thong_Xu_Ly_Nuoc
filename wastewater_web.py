# wastewater_web.py
import streamlit as st
from datetime import datetime
import random
from PIL import Image
import os
import json
#from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Wastewater Treatment WebApp", layout="wide")
st_autorefresh(interval=3600 * 1000, key="refresh")

# --- CHỌN NGÔN NGỮ ---
lang = st.sidebar.selectbox("🌐 Language / Ngôn ngữ", ["Tiếng Việt", "English"])
vi = lang == "Tiếng Việt"

def _(vi_text, en_text):
    return vi_text if vi else en_text

# --- LOGO ---
col1, col2 = st.columns([1, 6])
with col1:
    try:
        logo = Image.open("logo.png")
        st.image(logo, width=180)
    except:
        st.warning(_("❌ Không tìm thấy logo.png", "❌ logo.png not found"))
with col2:
    st.markdown("<h3 style='color: #004aad;'>Ho Chi Minh City University of Technology and Education</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #004aad;'>International Training Institute</h4>", unsafe_allow_html=True)

st.markdown(f"<h2 style='text-align: center;'>💧 { _('Hệ thống xử lý nước thải thông minh', 'Smart Wastewater Treatment System') } 💧</h2>", unsafe_allow_html=True)

now = datetime.now()
st.markdown(f"**⏰ { _('Thời gian hiện tại', 'Current time') }:** {now.strftime('%d/%m/%Y – %H:%M:%S')}")

# --- PHÂN QUYỀN ---
st.sidebar.title(_("🔐 Chọn vai trò người dùng", "🔐 Select User Role"))
user_type = st.sidebar.radio(_("Bạn là:", "You are:"), [_("Người giám sát", " Monitoring Officer"), _("Người điều khiển", "Control Administrator")])

if user_type == _("Người điều khiển", "Control Administrator"):
    password = st.sidebar.text_input(_("🔑 Nhập mật khẩu:", "🔑 Enter password:"), type="password")
    if password != "admin123":
        st.sidebar.error(_("❌ Mật khẩu sai. Truy cập bị từ chối.", "❌ Incorrect password. Access denied."))
        st.stop()
    else:
        st.sidebar.success(_("✅ Xác thực thành công.", "✅ Authentication successful."))

# --- ĐỊA ĐIỂM NHÀ MÁY ---
locations = {
    "KCN Tân Bình": (10.8015, 106.6395),
    "KCN Hiệp Phước": (10.5907, 106.7425),
    "KCN VSIP Bình Dương": (10.9446, 106.7548),
}
selected_city = st.selectbox(_("🏭 Chọn nhà máy xử lý:", "🏭 Select treatment plant:"), list(locations.keys()))

# --- GIẢ LẬP DỮ LIỆU CẢM BIẾN ---
st.subheader(_("🧪 Dữ liệu cảm biến (giả lập)", "🧪 Sensor Data (Simulated)"))
sensor_ph = round(random.uniform(5.0, 9.0), 2)
sensor_turbidity = round(random.uniform(0, 100), 1)  # Độ đục NTU
sensor_temp = round(random.uniform(25, 35), 1)

st.write(f"🌡️ { _('Nhiệt độ nước', 'Water temperature') }: **{sensor_temp} °C**")
st.write(f"🧪 pH: **{sensor_ph}**")
st.write(f"💦 { _('Độ đục', 'Turbidity') }: **{sensor_turbidity} NTU**")

# --- SO SÁNH VỚI TIÊU CHUẨN ---
st.subheader(_("📏 So sánh với tiêu chuẩn xử lý", "📏 Compare with Treatment Standards"))
is_ok = 6.5 <= sensor_ph <= 8.5 and sensor_turbidity <= 50 and sensor_temp <= 35

if is_ok:
    st.success(_("✅ Thoả tiêu chuẩn xả thải.", "✅ Meets discharge standards."))
else:
    st.warning(_("⚠️ Không đạt tiêu chuẩn, cần xử lý.", "⚠️ Not within standard, treatment required."))

# --- GIAI ĐOẠN XỬ LÝ ---
st.subheader(_("🔄 Giai đoạn xử lý", "🔄 Treatment Stage"))
if sensor_turbidity > 80:
    stage = _("🚧 Tiền xử lý", "🚧 Pre-treatment")
elif sensor_turbidity > 50:
    stage = _("🌀 Lọc thô", "🌀 Coarse filtration")
elif sensor_ph < 6.5 or sensor_ph > 8.5:
    stage = _("⚗️ Trung hòa pH", "⚗️ pH Neutralization")
else:
    stage = _("✅ Sẵn sàng xả", "✅ Ready to discharge")
st.info(f"{_('Giai đoạn hiện tại', 'Current stage')}: **{stage}**")

# --- QUYẾT ĐỊNH ĐIỀU KHIỂN ---
st.subheader(_("🚨 Quyết định điều khiển", "🚨 Control Decision"))
action_needed = not is_ok
if action_needed:
    st.error(_("🛠️ Kích hoạt hệ thống xử lý nước thải.", "🛠️ Activate wastewater treatment system."))
else:
    st.success(_("💤 Hệ thống tạm nghỉ (dữ liệu ổn định).", "💤 System idle (data stable)."))

# --- DỮ LIỆU GỬI VỀ ESP32 ---
st.subheader(_("📡 Dữ liệu gửi về ESP32", "📡 Data sent to ESP32"))
esp_data = {
    "time": now.strftime('%H:%M:%S'),
    "treatment_required": action_needed,
    "pH": sensor_ph,
    "turbidity": sensor_turbidity,
    "temp": sensor_temp
}
st.code(esp_data, language="json")


