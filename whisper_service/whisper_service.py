from whisper_service.transcribe import transcribe as transcribe_function
from whisper_service import load_model as load_model_function


class TranscribeResult:
    def __init__(self, is_success: bool = False, text: str = ""):
        self.is_success = is_success
        self.text = text


def recognize(
    audio: str, model_name: str, partial_result_received=None, output_data_received=None
):
    """Returned True, if recognition process finished successefully."""
    try:
        loaded_model = load_model_function(
            model_name, output_data_receive=output_data_received
        )
        result = transcribe_function(
            model=loaded_model,
            audio=audio,
            verbose=True,
            partial_result_receive=partial_result_received,
            output_data_receive=output_data_received,
        )
        return TranscribeResult(True, result["text"])
    except Exception as e:
        output_data_received(str(e))
        return TranscribeResult()
