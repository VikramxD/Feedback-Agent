import glob
import json
import os
import sys
import time
import en_core_web_lg
from pathlib import Path
from transformers import pipeline
from rake_nltk import Rake

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

def text_analysis(working_directory, transcript_file, audio_file):
        text = load_transcript_data(transcript_file).strip()
        out_file_name = working_directory + "/" + Path(transcript_file).stem + ".json"
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
            print(out_file_name)
    
def get_file_with_extension(working_directory, glob_extension):
    files = glob.glob(working_directory + "/" + glob_extension)
    for file in files:
        return os.path.abspath(file)
    return None

def voice_text_emo_er(working_directory):
    audio_file = get_file_with_extension(working_directory, "*.wav")
    transcription_file = get_file_with_extension(working_directory, "*.txt")
    text_analysis(working_directory, transcription_file, audio_file)

if __name__ == '__main__':
    voice_text_emo_er(sys.argv[1])