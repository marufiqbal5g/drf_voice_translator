import os
import sherpa_onnx

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
    "sherpa-onnx-streaming-zipformer-bn-vosk-2026-02-09"
)


recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(
    tokens=os.path.join(MODEL_DIR, "tokens.txt"),
    encoder=os.path.join(MODEL_DIR, "encoder-epoch-99-avg-1.int8.onnx"),
    decoder=os.path.join(MODEL_DIR, "decoder-epoch-99-avg-1.onnx"),
    joiner=os.path.join(MODEL_DIR, "joiner-epoch-99-avg-1.int8.onnx"),

    num_threads=2,          # good for Celeron
    sample_rate=16000,
    feature_dim=80,

    enable_endpoint_detection=True
)


class StreamingASR:

    def __init__(self):
        self.stream = recognizer.create_stream()

    def accept_audio(self, audio_chunk):

        self.stream.accept_waveform(
            16000,
            audio_chunk
        )

        while recognizer.is_ready(self.stream):
            recognizer.decode_stream(self.stream)

        # return self.stream.result
        return recognizer.get_result(self.stream)

    def finish(self):
        self.stream.input_finished()

        while recognizer.is_ready(self.stream):
            recognizer.decode_stream(self.stream)

        return recognizer.get_result(self.stream)