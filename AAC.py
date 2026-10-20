import streamlit as st
from gtts import gTTS

#page config
st.set_page_config(page_title="لوحة المحادثة", page_icon="🗣️", layout="wide")

#styling
st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%; height: 80px;
        font-size: 24px !important;
        font-weight: bold;
        background-color: #f1f5f9;
        border: 2px solid #cbd5e1;
        border-radius: 12px;
        color: #1e293b;
    }
    .stButton>button:hover {
        background-color: #e2e8f0;
        border-color: #94a3b8;
    }
    .chat-display {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px; border: 2px solid #cbd5e1;
        font-size: 32px; font-weight: bold;
        text-align: right;
        direction: rtl;
        margin-bottom: 20px;
        color: #1e293b;
        min-height: 70px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

#initialize sentence storage
if "sentence" not in st.session_state:
  st.session_state.sentence = []

def speak_sentence():
  if st.session_state.sentence:
    full_text = " ".join(st.session_state.sentence)
    tts = gTTS(text=full_text, lang="ar", slow=False)
    audio_file = "output.mp3"
    tts.save(audio_file)
    st.audio(audio_file, format="audio/mp3", autoplay=True)

#app header
st.markdown(
    '<h2 style="direction: rtl; text-align: right;">🗣️ لوحة المحادثة (Arabic AAC)</h2>',
    unsafe_allow_html=True,
)

#sentence display 
current_sentence_str = (
    " ".join(st.session_state.sentence)
    if st.session_state.sentence
    else "اختر كلمات..."
)
st.markdown(
    f'<div class="chat-display">{current_sentence_str}</div>',
    unsafe_allow_html=True,
)

#control buttons
col1, col2, col3 = st.columns(3)
with col1:
  if st.button("🔊 نطق الجملة"):
    speak_sentence()
with col2:
  if st.button("🗑️ مسح الكل"):
    st.session_state.sentence = []
    st.rerun()
with col3:
  if st.button("⬅️ حذف كلمة"):
    if st.session_state.sentence:
      st.session_state.sentence.pop()
      st.rerun()

st.divider()

#vocab
categories = {
    "الضمائر": ["أنا", "أنتَ", "أنتِ", "هو", "هي", "نحن"],
    "الأفعال": ["أريد", "أحب", "أكل", "أشرب", "أذهب", "أرى", "ألعب"],
    "الاحتياجات": ["ماء", "طعام", "حمام", "مساعدة", "نوم", "دواء"],
    "المشاعر": ["سعيد", "حزين", "متعب", "جائع", "عطشان", "ألم"],
}

tab_names = list(categories.keys())
tabs = st.tabs(tab_names)
for i, tab_name in enumerate(tab_names):
  with tabs[i]:
    words = categories[tab_name]
    cols = st.columns(3)
    for index, word in enumerate(words):
      col_idx = index % 3
      with cols[col_idx]:
        if st.button(word, key=f"{tab_name}_{index}"):
          st.session_state.sentence.append(word)
          st.rerun()
