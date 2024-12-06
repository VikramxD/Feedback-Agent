import os
import time
import json
import en_core_web_lg
from transformers import pipeline
from rake_nltk import Rake
from pathlib import Path
from subprocess import Popen

nlp = en_core_web_lg.load()
text_emotion = pipeline("text-classification", model="j-hartmann/emotion-english-roberta-large", top_k=None, device=-1)
rating = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment", device=-1)
ternary = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", top_k=None, device=-1)
voice_emotion = pipeline("audio-classification", model="antonjaragon/emotions_6_classes_small", device=-1)

def load_transcript_data(file_name):
    with open(file_name) as file:
        text = ""
        for line in file:
            line = line.rstrip()
            if ']' not in line:
                continue
            line = line[line.index(']') + 1:].strip()
            text += line + "\n"
        return text

def text_analysis(text, audio_file):
        out_file_name = "data/current/json/" + Path(audio_file).stem + ".json"
        obj = nlp(text)
        labels = voice_emotion(audio_file)
        results = {"timestamp" : int(time.time() * 1000),"rating": rating(text)[0]['label'],"voice_emo": [{label['label'].lower(): label['score']} for label in labels] , "sentences": []}
        for sentence in obj.sents:
            sample = sentence.text.strip()
            rake_nltk_var = Rake()
            rake_nltk_var.extract_keywords_from_text(sample)
            results['sentences'].append({
                "sentence": sample,
                "keywords": list(set(rake_nltk_var.get_ranked_phrases())),
                "ternary": {item['label']: item['score'] for item in ternary(sample)[0]},
                "emotion": [{item['label']: item['score']} for item in text_emotion(sample)[0]]
            })
            with open(out_file_name, 'w') as f:
                json.dump(results, f, separators=(",", ":"))
    
def whisper_process(temp_file):
    p = Popen(["/usr/bin/zsh", "ml/voice-2-text.sh", str(temp_file)])
    p.wait()

def initialize_files():
    directories = [
    'data/current/audios',
    'data/current/json',
    'data/current/transcripts',

    # Setting up directories for prerecorded audios, shouldn't need them later
    'data/prerecorded/arabic', 
    'data/prerecorded/bengali',
    'data/prerecorded/english',
    'data/prerecorded/french',
    'data/prerecorded/hindi',
    'data/prerecorded/japanese',
    'data/prerecorded/russian',
    'data/prerecorded/spanish',
    'data/prerecorded/telugu',
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def process_file(temp_file):
    os.path.exists('data/current') or initialize_files() # Reduce the number of polling to the files
    whisper_process(temp_file)
    audio_path = f"data/current/audios/{os.path.splitext(os.path.basename(temp_file))[0]}.wav".strip()
    transcript = load_transcript_data(f"data/current/transcripts/{os.path.splitext(os.path.basename(temp_file))[0]}.txt").strip()
    text_analysis(transcript, audio_path)
    