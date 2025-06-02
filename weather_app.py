import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Kanav's Seasonal Weather App", layout="wide")

# -------------- Theme + Style Setup --------------
theme = st.sidebar.selectbox("Choose a theme", ["Light", "Dark", "Ocean", "Sand", "Forest", "Midnight"])

# Sidebar image under theme selector
st.sidebar.image(
    "https://c8.alamy.com/comp/JGJ85W/portrait-background-with-umbrellas-sun-rain-and-weather-thermometer-JGJ85W.jpg",
    caption="🌦 Pretty Picture :D",
    use_column_width=True
)

themes = {
    "Light": {"bg": "#fdfdfd"},
    "Dark": {"bg": "#1e1e1e"},
    "Ocean": {"bg": "#e0f7fa"},
    "Sand": {"bg": "#fff8e1"},
    "Forest": {"bg": "#e8f5e9"},
    "Midnight": {"bg": "#0d1b2a"},
}
bg = themes[theme]["bg"]
blue = "#0066cc"

# Inject custom CSS
style_block = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');

    html, body, .stApp {{
        background-color: {bg};
        color: {blue};
        font-family: 'Quicksand', sans-serif;
    }}

    h1, h2, h3, h4, h5, h6, p, label, div {{
        color: {blue} !important;
    }}

    .block-container {{
        padding: 2rem;
    }}

    .weather-box {{
        background-color: #ffffff33;
        padding: 2rem;
        border-radius: 2rem;
        margin-top: 1rem;
    }}
    </style>
"""
st.markdown(style_block, unsafe_allow_html=True)

# -------------- Load Cities --------------
@st.cache_data
def load_city_data():
    return {
        "Saratoga": {"country": "USA", "pop": 31000, "founded": "1847", "region": "West"},
        "San Jose": {"country": "USA", "pop": 1027000, "founded": "1777", "region": "West"},
        "San Francisco": {"country": "USA", "pop": 815000, "founded": "1776", "region": "West"},
        "New York": {"country": "USA", "pop": 8800000, "founded": "1624", "region": "East"},
        "Los Angeles": {"country": "USA", "pop": 3900000, "founded": "1781", "region": "West"},
        "Chicago": {"country": "USA", "pop": 2700000, "founded": "1833", "region": "Midwest"},
        "Houston": {"country": "USA", "pop": 2300000, "founded": "1837", "region": "South"},
        "Phoenix": {"country": "USA", "pop": 1600000, "founded": "1867", "region": "West"},
        "Philadelphia": {"country": "USA", "pop": 1600000, "founded": "1682", "region": "East"},
        "Dallas": {"country": "USA", "pop": 1300000, "founded": "1841", "region": "South"},
        "Austin": {"country": "USA", "pop": 970000, "founded": "1839", "region": "South"},
        "Seattle": {"country": "USA", "pop": 744000, "founded": "1851", "region": "West"},
        "Boston": {"country": "USA", "pop": 692000, "founded": "1630", "region": "East"},
        "Miami": {"country": "USA", "pop": 467000, "founded": "1896", "region": "South"},
        "Atlanta": {"country": "USA", "pop": 498000, "founded": "1847", "region": "South"},
        "Orlando": {"country": "USA", "pop": 287000, "founded": "1875", "region": "South"},
        "Denver": {"country": "USA", "pop": 715000, "founded": "1858", "region": "West"},
        "Portland": {"country": "USA", "pop": 650000, "founded": "1845", "region": "West"},
        "Las Vegas": {"country": "USA", "pop": 641000, "founded": "1905", "region": "West"},
        "San Diego": {"country": "USA", "pop": 1420000, "founded": "1769", "region": "West"}
    }

city_data = load_city_data()

# -------------- Temperature Logic --------------
def simulate_temp(region, season):
    temps = {
        "West": {"Winter": (5, 15), "Spring": (10, 20), "Summer": (18, 33), "Fall": (10, 22)},
        "East": {"Winter": (-5, 5), "Spring": (5, 15), "Summer": (18, 30), "Fall": (7, 18)},
        "Midwest": {"Winter": (-10, 3), "Spring": (5, 15), "Summer": (20, 32), "Fall": (5, 18)},
        "South": {"Winter": (5, 15), "Spring": (15, 25), "Summer": (25, 38), "Fall": (18, 28)}
    }
    return round(random.uniform(*temps[region][season]), 1)

def get_weather_icon(season, temp_c):
    if season == "Winter": return "❄️" if temp_c < 5 else "☁️"
    if season == "Spring": return "🌸" if temp_c < 18 else "🌤"
    if season == "Summer": return "🌞" if temp_c > 25 else "⛅"
    if season == "Fall": return "🍂" if temp_c < 18 else "🌥"
    return "🌡"

# -------------- UI Controls --------------
st.title("🌤 Seasonal Weather App")
selected_city = st.selectbox("Choose a city", sorted(city_data.keys()))
season = st.radio("Choose a season", ["Winter", "Spring", "Summer", "Fall"])
unit = st.radio("Temperature Unit", ["Celsius", "Fahrenheit"])

# -------------- Output --------------
if selected_city:
    info = city_data[selected_city]
    temp_c = simulate_temp(info["region"], season)
    temp = temp_c if unit == "Celsius" else round(temp_c * 9 / 5 + 32, 1)
    suffix = "°C" if unit == "Celsius" else "°F"
    icon = get_weather_icon(season, temp_c)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div class="weather-box">
            <h2>{selected_city}</h2>
            <p>🌍 {info['country']} | 🏙 Population: {info['pop']:,} | 🏛 Founded: {info['founded']}</p>
            <h3>{icon} Typical {season} Temperature: <span>{temp} {suffix}</span></h3>
            <p style="font-size: 50px;">🌡️</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.empty()
