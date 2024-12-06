import os
import time
import json
import numpy as np
import streamlit as st
from annotated_text import annotated_text
from streamlit_mic_recorder import mic_recorder
import re

LOREM_IPSUM = """
The natural world is a marvel of complexity and beauty, a tapestry woven from the intricate threads of ecosystems that interconnect and support life in myriad forms. 
From the towering peaks of the Himalayas to the depths of the Mariana Trench, the Earth hosts a vast array of habitats, each uniquely adapted to its environment.
In the lush rainforests, vibrant flora and fauna coexist, with countless species vying for sunlight and resources, creating a dynamic competition that drives evolution. Meanwhile, the arid deserts exhibit resilience, where life adapts to extreme conditions, revealing the tenacity of nature.

In stark contrast, the rapid advancement of technology has reshaped human existence, pushing the boundaries of what was once thought possible.
The digital revolution has transformed communication, enabling instantaneous connections across the globe, breaking down barriers of distance and time.
The internet serves as a vast repository of knowledge, democratizing access to information and empowering individuals to learn and share ideas.
However, this same technology raises questions about privacy, data security, and the ethical implications of artificial intelligence.
As machines become increasingly capable, humanity must grapple with the consequences of creating entities that can surpass human intelligence in specific domains.
"""

recordings = {
    "English": ["Recording001", "Recording002"],
    "हिन्दी": ["Recording013", "Recording014"],
    "తెలుగు": ["Recording015", "Recording016"],
    "বাংলা": ["Recording009", "Recording010"],
    "عربي": ["Recording003", "Recording004"],
    "Español": ["Recording007", "Recording008"],
    "Français": ["Recording005", "Recording006"],
    "Русский": ["Recording019", "Recording020"],  
    "日本語": ["Recording017", "Recording018"]  
}

st.set_page_config(page_title="listenn", layout="wide")

def random_stuff():
    status_text = st.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)
    progress_bar = st.progress(0)
    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text(f"{i}% Complete")
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.01)
    progress_bar.empty()
    status_text.text("Completed!")

def stream_data():
    # Load the full JSON data
    data_json = '''{
        "sentences": [
            {
                "sentence": "Hi, this is Sireesha.",
                "keywords": ["Sireesha"],
                "ternary": {
                    "neutral": 0.8239796161651611,
                    "positive": 0.16092152893543243,
                    "negative": 0.015098854899406052
                }
            },
            {
                "sentence": "Recently I have been to Javed Habib Salon for hair straightening.",
                "keywords": ["Salon", "Javed", "Habib", "hair"],
                "ternary": {
                    "neutral": 0.8863248229026794,
                    "positive": 0.10396180301904678,
                    "negative": 0.009713374078273773
                }
            },
            {
                "sentence": "I must say that the services they are providing and the employees over there are really skilled trained, especially one employee, Sirfras, he made my hair straightening on all.",
                "keywords": ["services", "employees", "hair", "employee", "Sirfras"],
                "ternary": {
                    "positive": 0.9552183151245117,
                    "neutral": 0.03763286769390106,
                    "negative": 0.007148817181587219
                }
            },
            {
                "sentence": "He was very skilled and the ambience and the hyzen levels and the patients levels the way they treat the customers, the way they escort the customer is I felt good.",
                "keywords": ["patients", "levels", "customers", "customer", "way", "ambience", "hyzen"],
                "ternary": {
                    "positive": 0.9418646097183228,
                    "neutral": 0.04793179780244827,
                    "negative": 0.010203592479228973
                }
            },
            {
                "sentence": "Around I have spent 5-6 hours or there and in that duration they really cared like they were escorting in a better way which made me comfortable and happy.",
                "keywords": ["way", "hours", "duration"],
                "ternary": {
                    "positive": 0.9139651656150818,
                    "neutral": 0.07810298353433609,
                    "negative": 0.007931850850582123
                }
            },
            {
                "sentence": "For that reason I gave them enough good tips also.",
                "keywords": ["reason", "tips"],
                "ternary": {
                    "positive": 0.8134773969650269,
                    "neutral": 0.17315159738063812,
                    "negative": 0.013371005654335022
                }
            },
            {
                "sentence": "So overall it was a good experience I must say and the products are also they are using branded and after that hair straightening also they recommended me one shampoo and conditioner which I have been using since a month.",
                "keywords": ["month", "experience", "products", "hair", "shampoo", "conditioner"],
                "ternary": {
                    "positive": 0.004803374409675598,
                    "neutral": 0.05047832429409027,
                    "negative": 0.9447183012962341
                }
            },
            {
                "sentence": "That also I liked.",
                "keywords": [],
                "ternary": {
                    "positive": 0.9397140145301819,
                    "neutral": 0.05549309775233269,
                    "negative": 0.004792887717485428
                }
            },
            {
                "sentence": "So overall I had a good experience and I wish there to go again.",
                "keywords": ["experience"],
                "ternary": {
                    "positive": 0.9782518148422241,
                    "neutral": 0.017815321683883667,
                    "negative": 0.003932863473892212
                }
            },
            {
                "sentence": "So apart from all these things one thing I must share that prices are little bit high compared to other saloons.",
                "keywords": ["thing", "prices", "bit", "saloons", "things"],
                "ternary": {
                    "neutral": 0.6659771203994751,
                    "negative": 0.3009066879749298,
                    "positive": 0.03311619162559509
                }
            },
            {
                "sentence": "Prices are high little bit definitely but the services are good.",
                "keywords": ["services", "Prices", "bit"],
                "ternary": {
                    "positive": 0.5838066339492798,
                    "neutral": 0.3526648283004761,
                    "negative": 0.06352853775024414
                }
            },
            {
                "sentence": "That is what the experience I had.",
                "keywords": ["experience"],
                "ternary": {
                    "neutral": 0.8905409574508667,
                    "positive": 0.06906857341527939,
                    "negative": 0.04039046913385391
                }
            },
            {
                "sentence": "Thank you.",
                "keywords": [],
                "ternary": {
                    "positive": 0.8344848155975342,
                    "neutral": 0.14667844772338867,
                    "negative": 0.01883673667907715
                }
            }
        ]
    }'''

    data = json.loads(data_json)    

   
    keyword_colors = {}
    sentiment_color = {
        'positive': 'green',
        'negative': 'red',
        'neutral': 'grey'
    }

    full_text = ''
    for item in data['sentences']:
        sentence = item['sentence']
        keywords = item['keywords']
        ternary = item['ternary']
        sentiment = max(ternary, key=ternary.get)
        color = sentiment_color[sentiment]
        full_text += sentence + ' '  

        for kw in keywords:
            keyword_colors[kw.lower()] = color  


    words = re.findall(r'\b\w+\b|\S', full_text)
    annotated_words = []
    for word in words:
        word_lower = word.lower()
      
        if word_lower in keyword_colors:
            word_color = keyword_colors[word_lower]
        else:
            word_color = 'black'
        annotated_words.append((word, '', word_color))

        yield annotated_words.copy()
        time.sleep(0.025)

def manage_session_state():
    if 'stream_trigger' not in st.session_state:
        st.session_state.stream_trigger = False
    if 'selected_recording' not in st.session_state:
        st.session_state.selected_recording = ""

def sidebar():
    with st.sidebar:
        st.markdown("### Pre-recorded Audios")
        for language, rec_list in recordings.items():
            st.markdown(f"#### {language}")
            for rec in rec_list:
                with st.expander(f"🎧 {rec}", expanded=False):
                    st.audio("http://commondatastorage.googleapis.com/codeskulptor-assets/week7-brrring.m4a")
                    if st.button(f"Submit {rec}", key=f"{rec}_{language}", use_container_width=True):
                        st.session_state.stream_trigger = True

def record_audio():
    st.markdown("### Record Audio")
    st.write("Recording functionality is disabled in this version.")

def f_uploader():
    st.markdown("### Upload File")
    st.write("File upload functionality is disabled in this version.")

def upper_columns():
    col1, col2 = st.columns(2, vertical_alignment="center", gap="large")
    with col1:
        f_uploader()
    with col2:
        st.text("")
        st.text("")  # needed vertical padding
        record_audio()

def bottom_columns():
    col1, col2 = st.columns(2, vertical_alignment="center", gap="large")
    with col1:
        if st.session_state.stream_trigger:
            placeholder = st.empty()
            for annotated_words in stream_data():
                with placeholder.container():
                    annotated_text(*annotated_words)
            st.session_state.stream_trigger = False
    with col2:
        random_stuff()

def main():
    manage_session_state()
    sidebar()
    st.markdown("<h2 style='text-align: center; color: black;'>You can either upload 📤 or record 🎤!</h2>", unsafe_allow_html=True)
    upper_columns()
    st.markdown("---")
    bottom_columns()

if __name__ == "__main__":
    main()
