import whisper

def recognize(audio:str, model_name:str):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio=audio, verbose=True)
    return result["text"]
    