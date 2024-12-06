# Alpine doesn't work <https://stackoverflow.com/questions/76751155/how-to-install-torch-in-alpine>
# This is the only minimal build I could find that torch/transformers could actually run on.
FROM python:3.12-slim

# Install necessary packages just to have chance to run torch and transformers

# We're being lied to , even though the docs say only for CPU, it's installing gigabytes worth of CUDA drivers
# Link for reference <https://huggingface.co/docs/transformers/en/installation>
# Fixed it I think

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    zsh \
    curl \
    build-essential \
    ffmpeg \
    libstdc++6 \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir torch --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip3 install --no-cache-dir transformers \
    psutil \
    persist-queue \
    watchdog \
    spacy && \
    python3 -m spacy download en_core_web_lg


#COPY THE ENTIRE THING INTO HOME
COPY . /home/journaly/

# Need to fix path of the ggml model being downloaded, It downloads where you executed the command [CWD], not where you downloaded it, fix soon. For now setting WORKDIR
WORKDIR /home/journaly/whisper/models

# Making sure the whisper model downloads , it would download anyway without this btw.
RUN chmod +x download-ggml-model.sh && \
    ./download-ggml-model.sh base

EXPOSE 4242

# Need to set working Dir inside the ml folder or another CWD bug will happen lmao <https://github.com/HemilTheRebel/journaly/issues/12>
WORKDIR /home/journaly/ml

CMD [ "python3", "file_watcher.py" ]