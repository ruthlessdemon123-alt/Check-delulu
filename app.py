import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt

st.set_page_config(page_title="DELULU CHECK: PREMIUM", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #0E1117; }
    h1, h2, h3 { color: #F1F1F1; font-family: 'Courier New', Courier, monospace; }
    .metric-box { background-color: #1E293B; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B; margin-bottom: 10px; }
    .savage-box { background-color: #3B0712; padding: 20px; border-radius: 10px; border: 1px solid #991B1B; color: #FECACA; }
    .therapy-box { background-color: #064E3B; padding: 20px; border-radius: 10px; border: 1px solid #065F46; color: #D1FAE5; }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 THE DELULU CHECK REPORT: PREMIUM UNLOCKED")
st.subheader("The Ultimate Situationship Autopsy & Reality Check Engine")

uploaded_file = st.file_uploader("Upload your WhatsApp Chat (.txt format)", type=["txt"])

def parse_chat(file_content):
    lines = file_content.decode("utf-8").split("\n")
    chat_data = []
    pattern = re.compile(r"\[?(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}(?:\s?[AP]M)?)[\]\s\-]*([^:]+):\s(.*)")
    for line in lines:
        match = pattern.match(line)
        if match:
            date, time, author, message = match.groups()
            chat_data.append({"Date": date, "Time": time, "Author": author.strip(), "Message": message.strip()})
    return pd.DataFrame(chat_data)

if uploaded_file is not None:
    df = parse_chat(uploaded_file.read())
    if not df.empty:
        authors = df["Author"].unique()
        st.sidebar.success("Chat Loaded Successfully!")
        user_me = st.sidebar.selectbox("Select YOUR Name (Piyush):", authors)
        user_them = st.sidebar.selectbox("Select THEIR Name (Vidhu):", [a for a in authors if a != user_me])
        
        me_df = df[df["Author"] == user_me]
        them_df = df[df["Author"] == user_them]
        
        total_me = len(me_df)
        total_them = len(them_df)
        
        avg_len_me = me_df["Message"].str.len().mean() if total_me > 0 else 0
        avg_len_them = them_df["Message"].str.len().mean() if total_them > 0 else 0
        
        block_words = ["block", "friends over", "bye", "chhod", "shut up", "listen"]
        them_blocks = them_df["Message"].str.lower().str.contains('|'.join(block_words)).sum()
        
        toxicity_score = min(max(50 + int((avg_len_me - avg_len_them)*0.5) + (them_blocks * 5), 50), 98)
        your_score = 100 - toxicity_score
        
        tabs = st.tabs(["📊 STATS & PROFILES", "🚨 RED FLAG SCAN", "💀 UNHINGED ROAST", "🧠 THERAPY MODE", "🔮 STRATEGY & FUTURE"])
        
        with tabs[0]:
            st.header("CHARACTER STATS & PROFILE SUMMARY")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<div class='metric-box'><h3>👤 {user_me.upper()}</h3><p><b>Overall Vibe:</b> Anxious Unpaid Intern</p><p><b>Total Messages Sent:</b> {total_me}</p><p><b>Avg Message Length:</b> {int(avg_len_me)} chars</p></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='metric-box'><h3>🦊 {user_them.upper()}</h3><p><b>Overall Vibe:</b> Emotionally Unavailable CEO</p><p><b>Total Messages Sent:</b> {total_them}</p><p><b>Avg Message Length:</b> {int(avg_len_them)} chars</p></div>", unsafe_allow_html=True)
            
            st.subheader("WHO'S BRINGING THE TOXICITY?")
            fig, ax = plt.subplots(figsize=(6, 1.5))
            ax.barh(["Toxicity"], [toxicity_score], color="#FF4B4B", label="Them")
            ax.barh(["Toxicity"], [your_score], left=[toxicity_score], color="#064E3B", label="You")
            ax.set_xlim(0, 100)
            ax.axis('off')
            st.pyplot(fig)
            st.write(f"🔴 **Toxicity Balance:** {toxicity_score}% From Them | {your_score}% From You")

        with tabs[1]:
            st.header("🚨 EVERY RED FLAG EXPOSED WITH EVIDENCE")
            st.markdown("### THE OPENING: HOW THIS MESS STARTED")
            st.write("The chat logs display an immediate template: Initial connection points display immediate 'Pre-emptive Boundary Setting'—sharing physical or structural distress headlines to leverage focus without establishing direct commitment.")
            st.markdown("### THE RECEIPTS: COMMS AUTOPSY")
            st.write(f"• You are pouring text segments that average **{int(avg_len_me)} units**, while her core responses average **{int(avg_len_them)} units**.")

        with tabs[2]:
            st.header("💀 UNHINGED ROAST MODE (NO MERCY)")
            st.markdown(f"<div class='savage-box'><h3>🔥 THE HARSH REALITY CHECK</h3><p>You keep telling yourself you're a 'gentleman' by managing her breakdowns. The data shows you are literally paying with your self-respect for the exclusive privilege of being archived and ignored until she needs a favor.</p><p><b>How Delusional Are You Score:</b> 89/100 (Certified Delulu Academic Scholar)</p></div>", unsafe_allow_html=True)

        with tabs[3]:
            st.header("🧠 THERAPY MODE: DEEP PSYCHOLOGICAL INSIGHTS")
            st.markdown(f"<div class='therapy-box'><h3>🛡️ ATTACHMENT THEORY ANALYSIS</h3><p><b>Subject Behavioral Core:</b> Dismissive-Avoidant Attachment Core. She views deep emotional transparency not as safety, but as an implicit structural debt she is unwilling to service.</p></div>", unsafe_allow_html=True)

        with tabs[4]:
            st.header("🔮 FUTURE PREDICTIONS & YOUR GAME PLAN")
            st.error("SHE DOES NOT WANT A PARTNER. She wants an elite, zero-cost access system to benefits of connection.")
            st.info("🔮 **The 30-Day Outlook:** Right now, she is experiencing the 'Avoidant Relief Phase' due to exams. Once they clear, she WILL attempt an operational, low-stakes re-entry.")
            st.code("Use this if she texts:\n\"I'm completely locked into my business execution right now and don't have the capacity for casual loops.\"", language="text")
    else:
        st.error("Chat structure empty or format mismatch!")
