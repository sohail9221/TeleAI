TeleAI
TeleAI is an AI-powered voice assistant designed to automate order-taking processes in restaurants and fast-food chains via phone calls. By leveraging cutting-edge technologies in Automatic Speech Recognition (ASR), Natural Language Processing (NLP), and Text-to-Speech (TTS), TeleAI facilitates seamless, human-like interactions with customers, enhancing efficiency and customer satisfaction.​

🧠 Features
Automated Order Processing: Handles customer orders over phone calls without human intervention.

Speech Recognition: Transcribes customer speech into text using ASR.

Intent Classification: Determines customer intent to process orders accurately.

Natural Language Understanding: Employs NLP to understand and respond to customer queries.

Text-to-Speech Conversion: Converts system responses into natural-sounding speech.

Database Integration: Retrieves and updates order and menu information from a structured MySQL database.

Modular Architecture: Designed with separate modules for easy maintenance and scalability.​

📁 Project Structure

TeleAI/
├── app.py                 # Main application entry point
├── asr.py                 # Handles Automatic Speech Recognition
├── intent_classify.py     # Classifies customer intents
├── llm.py                 # Integrates Language Learning Model for response generation
├── xtts.py                # Manages Text-to-Speech conversion
├── db.sql                 # SQL script for database setup
├── building_rag_sql.py    # Builds Retrieval-Augmented Generation (RAG) SQL structures
├── query_rag.py           # Queries RAG for relevant information
├── main.py                # Orchestrates module interactions
├── requirements.txt       # Python dependencies
└── output2.wav            # Sample audio output

🚀 Installation
Clone the Repository

git clone https://github.com/sohail9221/TeleAI.git
cd TeleAI

Set Up a Virtual Environment (Optional but Recommended)


python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

Configure the MySQL Database

Create a New Database:

CREATE DATABASE teleai_db;

You can execute this command by logging into the MySQL shell:

mysql -u your_username -p

Then run the CREATE DATABASE command within the MySQL prompt.

Import the SQL Schema:

mysql -u your_username -p teleai_db < db.sql

Replace your_username with your MySQL username. You'll be prompted to enter your MySQL password.

Run the Application

python app.py

🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
