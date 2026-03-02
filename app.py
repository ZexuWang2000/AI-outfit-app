import streamlit as st
import random
import requests

# =========================
# 页面基础设置
# =========================
st.set_page_config(page_title="今日穿搭助手", page_icon="👕")

st.title("👕 今日穿搭助手")
st.write("根据实时天气，为你生成今日穿搭建议")

# =========================
# 输入城市
# =========================
city = st.text_input("请输入城市（英文，例如：Suzhou, CN）", "Suzhou, CN")

# =========================
# 你的 OpenWeather API Key
# =========================
WEATHER_API_KEY = "WEATHER_API_KEY = "613fdb1143395403779c4747ff94bb2c"

# =========================
# 获取天气
# =========================
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=zh_cn"
    r = requests.get(url).json()

    if "main" not in r:
        return None, None

    temp = r["main"]["temp"]
    weather_main = r["weather"][0]["main"]

    if weather_main.lower() in ["clear"]:
        w = "晴"
    elif weather_main.lower() in ["rain", "drizzle", "thunderstorm"]:
        w = "雨"
    elif weather_main.lower() in ["snow"]:
        w = "雪"
    elif weather_main.lower() in ["clouds"]:
        w = "多云"
    else:
        w = "晴"

    return temp, w

# =========================
# 保暖计算
# =========================
def base_warmth_needed(temperature):
    if temperature <= 0: return 5
    elif temperature <= 5: return 4
    elif temperature <= 15: return 3
    elif temperature <= 25: return 2
    else: return 1

def weather_modifier(weather):
    if weather == "雨": return 1
    elif weather == "雪": return 2
    elif weather == "多云": return 0
    return 0

def warmth_needed(temp, weather):
    base = base_warmth_needed(temp)
    return max(1, min(5, base + weather_modifier(weather)))

# =========================
# 随机衣物库
# =========================
tops = ["针织衫", "衬衫", "卫衣", "T恤"]
bottoms = ["西裤", "牛仔裤", "运动裤"]
outerwear = ["风衣", "夹克", "大衣", "羽绒服"]

# =========================
# 生成搭配
# =========================
def generate_outfit(temp, weather):
    needed = warmth_needed(temp, weather)

    top = random.choice(tops)
    bottom = random.choice(bottoms)

    if needed >= 3:
        coat = random.choice(outerwear)
        outfit = f"{top} + {bottom} + {coat}"
    else:
        outfit = f"{top} + {bottom}"

    return outfit, needed

# =========================
# 按钮触发
# =========================
if st.button("生成今日穿搭"):
    temp, weather = get_weather(city)

    if temp is None:
        st.error("天气获取失败，请检查城市名称或API Key")
    else:
        outfit, needed = generate_outfit(temp, weather)

        st.subheader("🌤 今日天气")
        st.write(f"温度：{temp} ℃")
        st.write(f"天气：{weather}")

        st.subheader("👗 穿搭建议")
        st.success(f"推荐搭配：{outfit}")
        st.write(f"保暖等级：{needed}/5")
