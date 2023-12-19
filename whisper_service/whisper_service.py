import whisper
from whisper_service.transcribe import transcribe as transcribe_function


def recognize(audio: str, model_name: str, partial_result_received, output_data_received):
    loaded_model = whisper.load_model(model_name)
    transcribe_function(
        model=loaded_model,
        audio=audio,
        verbose=True,
        partial_result_received=partial_result_received,
        output_data_received=output_data_received
    )
