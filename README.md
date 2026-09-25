# Whisper Translator

Mój projekt transkrypcji audio z GUI oparty na Whisper, PyQt5 i deep-translator.

## Wymagania

- Python 3.10+
- FFmpeg dostępny w `PATH` albo w lokalnym katalogu `ffmpeg/bin`

> `ffmpeg-python` z `requirements.txt` nie instaluje samego programu FFmpeg. Whisper nadal potrzebuje binarki `ffmpeg` do odczytu plików audio.

## Jak uruchomić

```bash
pip install -r requirements.txt
python main.py
```

Aplikacja obsługuje pliki MP3, WAV i M4A.

## Status

- ✅ Działa w PyCharm
- ❌ `.exe` nie działa jeszcze poprawnie z PyInstallerem
