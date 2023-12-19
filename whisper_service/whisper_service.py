from whisper_service.transcribe import transcribe as transcribe_function
from whisper_service import load_model as load_model_function


def recognize(
    audio: str, model_name: str, partial_result_received, output_data_received
):
    try:
        loaded_model = load_model_function(model_name, output_data_receive=output_data_received)
        transcribe_function(
            model=loaded_model,
            audio=audio,
            verbose=True,
            partial_result_receive=partial_result_received,
            output_data_receive=output_data_received,
        )
    except Exception as e:
        output_data_received(str(e))
    