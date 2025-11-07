# EcoMind: Mental Wellness & Eco Awareness App (Updated for OpenAI >=1.0.0)
# Run: streamlit run eco_mind_app.py

import streamlit as st
import requests
import random
from openai import OpenAI
import os

# ---------- SETTINGS ----------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#OPENAI_API_KEY = "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"  # Replace with your key
#AQI_API = "https://api.waqi.info/feed/{city}/?token=c2cc8ae86fd56ff95a132b7edf26cb68e69ae99e"
AQI_API = f"https://api.waqi.info/feed/{{city}}/?token={os.getenv('AQI_API_TOKEN')}"

client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(page_title="🌿 EcoMind", layout="wide")

# ---------- AESTHETIC UI ----------
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #c3f0ca, #a8e6cf, #dcedc1);
        color: #222;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 48px;
        color: #2e7d32;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🌱 EcoMind</div>", unsafe_allow_html=True)
st.subheader("Connecting your emotions with the Earth 🌍")

# ---------- SIDEBAR NAVIGATION ----------
st.sidebar.title("Navigate")
section = st.sidebar.radio("Go to:", [
    "Eco-Mood Tracker",
    "Mindfulness Hub",
    "Community Forum",
    "Climate Action Feed",
    "AI Support Chatbot"
])

# ---------- ECO-MOOD TRACKER ----------
if section == "Eco-Mood Tracker":
    st.header("💚 Track Your Mood & Environment")

    city = st.text_input("Enter your city:")
    mood = st.select_slider("How are you feeling today?", 
                             options=["Sad", "Anxious", "Calm", "Happy", "Excited"])

    if st.button("Log Mood"):
        if city:
            try:
                data = requests.get(AQI_API.format(city=city)).json()
                aqi = data['data']['aqi']
                temp = data['data']['iaqi']['t']['v'] if 't' in data['data']['iaqi'] else "N/A"
                st.success(f"🌤 Air Quality Index in {city}: {aqi}, Temperature: {temp}°C")
            except Exception as e:
                st.warning("Could not fetch environmental data.")
        st.write(f"🌿 You are feeling **{mood}** today. Remember: Nature feels with you!")

# ---------- MINDFULNESS HUB ----------
elif section == "Mindfulness Hub":
    st.header("🧘‍♀️ Mindfulness & Eco-Therapy")
    st.write("Choose a guided meditation theme:")
    theme = st.selectbox("Theme", ["Forest Calm", "Ocean Breathing", "Mountain Stillness", "Eco-Gratitude"])
    st.audio("https://www2.cs.uic.edu/~i101/SoundFiles/PinkPanther30.wav")  # Example audio link
    st.info(f"Relax with the {theme} meditation. Close your eyes, breathe deeply, and feel your connection to nature.")

# ---------- COMMUNITY FORUM ----------
elif section == "Community Forum":
    st.header("🌍 Community Forum: Share Your Climate Stories")
    post = st.text_area("Share your experience or thought about climate and emotions:")
    if st.button("Post"):
        st.success("Your story has been shared with the community 💬")
    st.write("🗨️ *Sample Posts:*")
    st.markdown("- *'I started walking to work — it feels great to breathe cleaner air!'*")
    st.markdown("- *'The heatwave made me anxious, but meditating outdoors helps.'*")

# ---------- CLIMATE ACTION FEED ----------
elif section == "Climate Action Feed":
    st.header("💡 Daily Eco-Actions")
    actions = [
        "Bring your own cup when buying coffee.",
        "Spend 10 minutes outdoors connecting with nature.",
        "Reduce plastic use today.",
        "Water a plant or plant a seed.",
        "Turn off lights when not in use."
    ]
    st.success(random.choice(actions))

# ---------- AI SUPPORT CHATBOT ----------
elif section == "AI Support Chatbot":
    st.header("🤖 AI Emotional Support Chatbot")
    st.write("I'm here to listen. How are you feeling?")

    user_input = st.text_input("You:")
    if user_input:
        try:
            # NEW OpenAI API format
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a kind emotional support assistant with eco-awareness."},
                    {"role": "user", "content": user_input}
                ]
            )

            bot_reply = response.choices[0].message.content
            st.write(f"**EcoMind Bot:** {bot_reply}")

        except Exception as e:
            st.error(f"Error: {e}")
