import whisper

def transcribe_audio(file_path, language="ar"):
    model = whisper.load_model("small")
    result = model.transcribe(file_path, language=language)
    return result["text"]
