import os
from datetime import datetime

def is_audio_file(filename):
    return filename.lower().endswith(('.mp3', '.wav'))

def safe_open(path, mode='r'):
    try:
        return open(path, mode, encoding='utf-8')
    except Exception as e:
        print(f"Nie mogę otworzyć pliku! {path}: {e}")
        return None

def clean_text(text):
    return text.strip().replace('\n', ' ')

def timestamped_filename(prefix, ext):
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
