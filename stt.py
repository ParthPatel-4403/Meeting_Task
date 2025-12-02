import whisper

def audio_to_text_whisper(audio_path):
    model = whisper.load_model("small")
    result = model.transcribe(audio_path)
    return result["text"]
