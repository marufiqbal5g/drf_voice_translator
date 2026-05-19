import wave
import numpy as np
import sherpa_onnx
import os
import soundfile as sf

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
    "sherpa-onnx-streaming-zipformer-bn-vosk-2026-02-09"
)


def load_recognizer():

    return sherpa_onnx.OnlineRecognizer.from_transducer(
        tokens=os.path.join(MODEL_DIR, "tokens.txt"),
        encoder=os.path.join(MODEL_DIR, "encoder-epoch-99-avg-1.int8.onnx"),
        decoder=os.path.join(MODEL_DIR, "decoder-epoch-99-avg-1.onnx"),
        joiner=os.path.join(MODEL_DIR, "joiner-epoch-99-avg-1.int8.onnx"),
        num_threads=2,
        sample_rate=16000,
        feature_dim=80,
    )


recognizer = load_recognizer()


def transcribe_audio(path):

    # 🔥 read audio safely (handles 22050/44100/etc)
    audio, sr = sf.read(path, dtype="float32")

    # 🔥 convert stereo → mono if needed
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)

    # 🔥 resample if not 16k
    if sr != 16000:
        import librosa
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        sr = 16000

    stream = recognizer.create_stream()

    stream.accept_waveform(
        sr,
        audio.tolist()
    )

    recognizer.decode_stream(stream)

    stream.input_finished()   # ✅ FIXED (correct place)

    while recognizer.is_ready(stream):
        recognizer.decode_stream(stream)

    return recognizer.get_result(stream)