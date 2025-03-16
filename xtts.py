import pyaudio
import soundfile as sf
from TTS.api import TTS

class XTTS:
    def __init__(self, output_file="output.wav", speaker_wav=None, language="en", use_gpu=True):
        self.output_file = output_file
        self.speaker_wav = speaker_wav
        self.language = language
        self.tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=use_gpu)

    def play_audio(self, text):
        """Convert input text to speech and play it."""
        if not text:
            print("Error: No text provided.")
            return
        
        # Convert text to speech
        self.tts_model.tts_to_file(
            text=text,
            file_path=self.output_file,
            speaker_wav=self.speaker_wav,
            language=self.language
        )
        print(f"Generated speech file: {self.output_file}")

        # Play the generated audio
        try:
            data, samplerate = sf.read(self.output_file, dtype="int16")

            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16,
                            channels=len(data.shape) if len(data.shape) > 1 else 1,
                            rate=samplerate,
                            output=True)

            stream.write(data.tobytes())

            # Cleanup
            stream.stop_stream()
            stream.close()
            p.terminate()

            print("Audio playback finished.")
        except Exception as e:
            print(f"Error playing audio: {e}")

# # Example Usage:
# xtts = XTTS(speaker_wav="/home/pc/teleai/OpenVoice/resources/example_reference.mp3")

# user_text = "Enter text to synthesize: "
# xtts.play_audio(user_text)
