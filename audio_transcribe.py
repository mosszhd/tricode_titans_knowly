import torch
from transformers import pipeline
import librosa
import io
import yaml


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


def convert_bytes_to_array(audio_bytes):
    audio_bytes = io.BytesIO(audio_bytes)
    audio, sr = librosa.load(audio_bytes)
    return audio


def transcribe_audio(audio_bytes):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    pipe = pipeline(task=config['asr_model']['task'], 
                    model=config['asr_model']['model_tag'], 
                    chunk_length_s=config['asr_model']['chunk_length'], 
                    generate_kwargs={"language": "english"},
                    device=device)
    res = pipe(inputs=convert_bytes_to_array(audio_bytes), batch_size=1)["text"]
    return res