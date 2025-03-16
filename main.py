from asr import TranscriptionService
from intent_classify import get_user_intent
from query_rag import query_faiss_index
from llm import get_llm_response, create_new_session, save_session_history
from xtts import XTTS
import threading
import time
import os
import os
import tensorflow as tf

# Store active chat sessions in memory
chat_sessions = {}

def main():
    # Initialize services
    transcriber = TranscriptionService()  # ASR (running in background)
    #tts = TTSHandler()
    tts = XTTS(speaker_wav="/home/pc/teleai/OpenVoice/resources/example_reference.mp3")  # give any 6-7 second voice clip here

   

    # Ensure logs directory exists
    os.makedirs("chat_logs", exist_ok=True)

    # Start ASR in a background thread
    threading.Thread(target=transcriber.start_listening, daemon=True).start()
    print("🎤 TeleAI is now listening...")
    while True:
        transcript = transcriber.get_latest_transcription()
        if not transcript or not transcript.strip():
            time.sleep(0.5)  # Prevent excessive CPU usage
            continue  # Ignore empty transcriptions

        print(f"User: {transcript}")

        # Step 1: Assign or retrieve session ID (per customer session)
        if not chat_sessions:
            session_id = create_new_session()
            chat_sessions[session_id] = []  # Store session history in memory
        else:
            session_id = list(chat_sessions.keys())[-1]  # Use last active session

        chat_sessions[session_id].append({"Human": transcript})

        # Step 2: Get intent
        intent = get_user_intent(transcript)
        print(f"🔹 Recognized Intent: {intent}")

        # Step 3: Query RAG context based on intent
        rag_context = ""
        if intent in ['Menu', 'GeneralInfo', 'Reservations', 'OrderTracking']:
            index_filename = f"vector_database/{intent}.index"
            metadata_filename = f"vector_database/{intent}.csv"
            _, results_metadata = query_faiss_index(transcript, index_filename, metadata_filename, top_k=2)
            
            if results_metadata:
                if isinstance(results_metadata, dict):
                    rag_context = "\n".join(str(value) for value in results_metadata.values())
                elif isinstance(results_metadata, list):
                    rag_context = "\n".join(str(item) for item in results_metadata)

        # Step 4: Get response from LLM with session memory
        response, session_id = get_llm_response(session_id, transcript, rag_context)
        print(f"🤖 Assistant: {response}")

        chat_sessions[session_id].append({"Bot": response})
        tts.play_audio(text=response)
        # Step 5: Convert text response to speech
        #tts.generate_speech(response) using chatTTS
        # tts.speak_response(response)   #using pyttsx3
        # Step 6: If the session is over, save and reset
        if "goodbye" in transcript.lower() or "thank you" in transcript.lower():
            save_session_history(session_id, chat_sessions[session_id])
            del chat_sessions[session_id] 
            break # Remove session from memory

if __name__ == "__main__":
    main()
