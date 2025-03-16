import threading
import time
import queue
import sounddevice as sd
import numpy as np
import faster_whisper
import librosa
import datetime

class TranscriptionService:
    def __init__(self, whisper_model="base.en", device="cuda", num_workers=3, log_file="transcription_log.txt"):
        self.ORIGINAL_SAMPLE_RATE = 44100  # PC's sample rate
        self.WHISPER_SAMPLE_RATE = 16000  # Whisper requirement
        self.BLOCKSIZE = int(self.ORIGINAL_SAMPLE_RATE * 4)  # 4-second chunks
        self.LOG_FILE = log_file

        # Initialize Whisper model
        self.model = faster_whisper.WhisperModel(whisper_model, compute_type="float16", device=device, num_workers=num_workers)

        # Queues for audio and transcriptions
        self.audio_queue = queue.Queue()
        self.transcription_queue = queue.Queue()

        # Background thread for transcribing
        self.listening_thread = threading.Thread(target=self.process_audio, daemon=True)
        self.listening_thread.start()

    def save_log(self, text):
        """ Saves transcriptions to a log file. """
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        with open(self.LOG_FILE, "a") as f:
            f.write(timestamp + text + "\n")

    def resample_audio(self, audio):
        """ Resamples audio from 44.1kHz to 16kHz and removes NaN/Inf. """
        audio = np.nan_to_num(audio)  # Fix NaN/Inf
        if np.max(np.abs(audio)) > 0:
            audio /= np.max(np.abs(audio))  # Normalize
        return librosa.resample(audio, orig_sr=self.ORIGINAL_SAMPLE_RATE, target_sr=self.WHISPER_SAMPLE_RATE).astype(np.float32)

    def callback(self, indata, frames, time, status):
        """ SoundDevice callback to continuously listen. """
        if status:
            print(f"⚠️ Warning: {status}")
        audio_data = np.frombuffer(indata, dtype=np.float32).flatten()

        # Ignore empty or invalid audio buffers
        if len(audio_data) == 0 or not np.isfinite(audio_data).all():
            print("⚠️ Skipping invalid audio buffer.")
            return

        self.audio_queue.put(audio_data)

    def process_audio(self):
        """ Background thread for transcribing speech. """
        while True:
            try:
                audio_chunk = self.audio_queue.get(timeout=1)  # Wait for audio
                audio_resampled = self.resample_audio(audio_chunk)

                segments, _ = self.model.transcribe(audio_resampled, beam_size=2, vad_filter=True)
                for segment in segments:
                    text = segment.text.strip()
                    self.save_log(text)
                    self.transcription_queue.put(text)  # Store for later retrieval

            except queue.Empty:
                continue  # No new audio, keep listening

    def start_listening(self):
        """ Start audio listening without blocking the main program. """
        with sd.InputStream(samplerate=self.ORIGINAL_SAMPLE_RATE, channels=1, blocksize=self.BLOCKSIZE, callback=self.callback):
            print("🎤 Listening... (Press Ctrl+C to stop)")
            while True:
                time.sleep(1)  # Keep the main thread running

    def get_latest_transcription(self):
        """ Retrieve the latest transcription from the queue (non-blocking). """
        try:
            return self.transcription_queue.get_nowait()
        except queue.Empty:
            return None  # No new transcription yet
