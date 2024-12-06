import os
import glob
import json

ORG = "kebabroaster77"
USER = "u42"
GLOB_PATTERN_PREFIX = f"apis/data/user_data/bucket/users/{USER}/**/*.json"

def keywords_schema(original_json, file_name, bucket_url):
    for i, sentence_data in enumerate(original_json["sentences"]):
        sorted_emotions = sorted(sentence_data["emotion"].items(), key=lambda item: item[1], reverse=True)
        ed_1_name, ed_2_name = [key for key, value in sorted_emotions[:2]] # Neutral included
        schema = {
            "ts": original_json["timestamp"],
            "su": bucket_url,
            "si": i,
            "s": sentence_data["sentence"],
            "keywords": sentence_data["keywords"],
            "ep": sentence_data["ternary"].get("positive", 0.0),
            "en": sentence_data["ternary"].get("negative", 0.0),
            "ed_1": ed_1_name,
            "ed_2": ed_2_name,
            "user": USER,
            "org": ORG,
        }
        json_dump(schema, f"output/{file_name}/keywords",f"{file_name}_{i}.kw.json")

def text_schema(original_json, file_name, bucket_url):
    pos_kws, neg_kws = set(), set()
    for sentence in original_json["sentences"]:
        pos_kws.update(sentence["keywords"]) if sentence["ternary"]["positive"] > sentence["ternary"]["negative"] else neg_kws.update(sentence["keywords"])
    schema = {
        "ts": original_json["timestamp"],
        "tu": bucket_url,
        "user": USER,
        "org": ORG,
        "star": float(original_json["rating"].split()[0]),
        "pos_kws": list(pos_kws),
        "neg_kws": list(neg_kws),
    }
    json_dump(schema,f"output/{file_name}",f"{file_name}.se.json")

def voice_schema(original_json, vfile_name, bucket_url):
    schema = {
        "ts": original_json["timestamp"],
        "au": bucket_url,
        "user": USER,
        "org": ORG,
        "vemo_1": sorted(original_json["emotions"], key=lambda x: x["score"], reverse=True)[0]["label"],
    }
    json_dump(schema,f"output/{vfile_name}",f"{vfile_name}.ve.json")

def json_dump(schema, path, extension):
    os.makedirs(path, exist_ok= True)
    with open(f"{path}/{extension}", "w") as f:
        json.dump(schema, f, separators=(",", ":"))

def process():
    for file in glob.glob(GLOB_PATTERN_PREFIX, recursive=True):
        if file.endswith(('.se.json', '.ve.json')):
            file_name = os.path.basename(file).rsplit('.', 2)[0] # select everything before the first "."
            bucket_url = os.path.abspath(file).split("users/", 1)[1] # Bucket url for now
            with open(file) as f:
                data = json.load(f)
            if file.endswith('.se.json'):
                text_schema(data, file_name, bucket_url)
                keywords_schema(data, file_name, bucket_url)
            else:
                voice_schema(data, file_name, bucket_url)

if __name__ == "__main__":
    process()
