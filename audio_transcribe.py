import io
import yaml
import torch
import librosa
from transformers import pipeline
import streamlit as st

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def convert_bytes_to_array(audio_bytes):
    audio_bytes = io.BytesIO(audio_bytes)
    audio, sr = librosa.load(audio_bytes)
    return audio

def load_whisper():
    return pipeline(task=config['asr_model']['task'], 
                    model=config['asr_model']['model_tag'], 
                    chunk_length_s=config['asr_model']['chunk_length'], 
                    generate_kwargs={"language": "english"},
                    device="cuda:0" if torch.cuda.is_available() else "cpu")

def transcribe_audio(audio_bytes):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    if "asr_model" in st.session_state.keys():
        res = st.session_state["asr_model"](inputs=convert_bytes_to_array(audio_bytes), batch_size=1)["text"]
    else:
        pipe = pipeline(task=config['asr_model']['task'], 
                        model=config['asr_model']['model_tag'], 
                        chunk_length_s=config['asr_model']['chunk_length'], 
                        generate_kwargs={"language": "english"},
                        device=device)
        res = pipe(inputs=convert_bytes_to_array(audio_bytes), batch_size=1)["text"]
    return res