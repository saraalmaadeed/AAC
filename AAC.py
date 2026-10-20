import streamlit as st
from gtts import gTTS

# page config
st.set_page_config(page_title="لوحة المحادثة", page_icon="🗣️", layout="wide")

st.markdown(
    """
    <style>

    .stButton>button {
        width: 280px !important;
        height: 140px !important;
        background-color: #f1f5f9 !important;
        border: 3px solid #cbd5e1 !important;
        border-radius: 16px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        margin: 0 auto !important;
    }
    
    .stButton>button p {
        font-size: 40px !important;
        font-weight: bold !important;
        color: #1e293b !important;
        text-align: center !important;
        width: 100% !important;
        margin: 0 !important;
    }

    .stButton>button:hover {
        background-color: #e2e8f0 !important;
        border-color: #94a3b8 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 32px !important;
        direction: rtl !important;
        justify-content: center !important;
    }

    .stTabs [data-baseweb="tab"] {
        width: 200px
        height: 120px !important;
        padding: 10px 30px !important;
        background-color: #f8fafc !important;
        border: 3px solid #cbd5e1 !important;
        border-radius: 16px 16px 0px 0px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    .stTabs [data-baseweb="tab"] *, 
    .stTabs [data-baseweb="tab"] p, 
    .stTabs [data-baseweb="tab"] span {
        font-size: 40px !important;
        font-weight: bold !important;
        color: #1e293b !important;
        text-align: center !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #e2e8f0 !important;
        border-bottom: 6px solid #0284c7 !important;
    }

    .chat-display {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px; 
        border: 3px solid #cbd5e1;
        font-size: 38px; 
        font-weight: bold;
        text-align: center;
        direction: rtl;
        margin-bottom: 20px;
        color: #1e293b;
        min-height: 80px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# initialize sentence storage
if "sentence" not in st.session_state:
    st.session_state.sentence = []

def speak_sentence():
    if st.session_state.sentence:
        full_text = " ".join(st.session_state.sentence)
        tts = gTTS(text=full_text, lang="ar", slow=False)
        audio_file = "output.mp3"
        tts.save(audio_file)
        st.audio(audio_file, format="audio/mp3", autoplay=True)

# app header
st.markdown(
    '<h2 style="direction: rtl; text-align: center;">🗣️ لوحة المحادثة</h2>',
    unsafe_allow_html=True,
)

# sentence display 
current_sentence_str = (
    " ".join(st.session_state.sentence)
    if st.session_state.sentence
    else "اختر كلمات..."
)
st.markdown(
    f'<div class="chat-display">{current_sentence_str}</div>',
    unsafe_allow_html=True,
)

# control buttons
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

# vocab
categories = {
    "الضمائر": ["أنا", "أنتَ", "أنتِ", "هو", "هي", "نحن"],
    "الأفعال": ["أريد", "أحب", "أكل", "أشرب", "أذهب", "أرى"],
    "الاحتياجات": ["ماء", "أكل", "حمام", "مساعدة", "نوم", "دواء"],
    "المشاعر": ["مستانسة", "زعلانة", "تعبانة", "جوعانة", "عطشانة", "ألم"],
    "الأشخاص": ["نور", "سلطان", "طفلة"],
    "آخر": ["شلون", "ما أعرف", "خلاص", "وين", "بعدين", "الحين"],

}

tab_names = list(categories.keys())
tabs = st.tabs(tab_names)
for i, tab_name in enumerate(tab_names):
    with tabs[i]:
        words = categories[tab_name]
        cols = st.columns(2)
        for index, word in enumerate(words):
            col_idx = index % 2
            with cols[col_idx]:
                if st.button(word, key=f"{tab_name}_{index}"):
                    st.session_state.sentence.append(word)
                    st.rerun()
