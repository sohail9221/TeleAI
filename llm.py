import ollama
import uuid
import os
import datetime
# Store sessions in memory (cached)
chat_sessions = {}

def create_new_session():
    """Creates a new chat session with a unique ID."""
    session_id = str(uuid.uuid4())  # Unique session ID
    chat_sessions[session_id] = [
       {
    "role": "system",
    "content": (
        "You are a professional restaurant assistant handling customer calls for orders and delivery.Just Ask for order and confirm what customer said Nothing other than this. Always keep response short.  "
        # "Keep responses short (4-5 words), friendly, and precise. "
        # "Only answer relevant questions. If unsure, ask for clarification. "
        # "If context is provided, incorporate it naturally. "
        # "Speak naturally and professionally, like a real waiter. "
        # "Do NOT add any explanations, disclaimers, or notes. "
        # "NEVER include messages like '(Note:... )' or any reasoning behind your answer. "
        # "Your responses should be direct, conversational, and customer-friendly."
    )
}
    ]
    return session_id

import re
def clean_response(response: str) -> str:
    """Removes unwanted notes or AI reasoning from LLM response."""
    response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    response = re.sub(r"\(.*?\)", "", response)  # Remove text inside parentheses
    response = re.sub(r"(?i)note:.*", "", response)  # Remove lines starting with "Note:"
    return response.strip()  # Remove extra spaces or newlines



def get_llm_response(session_id: str, query: str, rag_context: str = "") -> tuple:
    """Handles chat with context and memory, maintaining session state."""

    # if session_id not in chat_sessions:
    #     session_id = create_new_session()

    # Append RAG context if available
    if rag_context:
        chat_sessions[session_id].append({"role": "system", "content": f"Context: {rag_context}"})

    # Append user query
    chat_sessions[session_id].append({"role": "user", "content": query})

    # Call Ollama API with chat history
    response = ollama.chat(
        model="deepseek-r1:1.5b",
        messages=chat_sessions[session_id],
        options={"temperature": 0.2, "max_tokens": 5}  # Short, precise responses
    )

    # Extract assistant response
    assistant_reply = response['message']['content'].strip()

    # Append AI response to session history
    chat_sessions[session_id].append({"role": "assistant", "content": assistant_reply})

    return clean_response(assistant_reply), session_id

def save_session_history(session_id: str, chat_history: list):
    """Saves chat history to a text file for logging purposes."""
    os.makedirs("chat_logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"chat_logs/{session_id}_{timestamp}.txt"

    with open(file_path, "w") as log_file:
        for entry in chat_history:
            log_file.write(str(entry) + "\n")

    print(f"✅ Chat session {session_id} saved to {file_path}")
