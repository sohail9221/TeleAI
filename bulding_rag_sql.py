import mysql.connector
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
import os

# Step 1: Connect to MySQL Database
def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passw0rd!",
        database="CulinaryAI"
    )
    return connection

# Step 2: Get Non-ID Columns Dynamically
def get_non_id_columns(connection, table_name):
    cursor = connection.cursor()
    query = f"SHOW COLUMNS FROM {table_name};"
    cursor.execute(query)
    columns = cursor.fetchall()
    cursor.close()
    
    # Filter out columns that contain 'id' in their name
    non_id_columns = [col[0] for col in columns if 'id' not in col[0].lower()]
    
    return non_id_columns

# Step 3: Fetch Data from Table
def fetch_table_data(connection, table_name):
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM {table_name};"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

# Step 4: Generate Text Embeddings
def generate_text_embeddings(data, text_columns, model):
    # Combine text columns for embedding
    texts = [
        " ".join(str(row[col]) for col in text_columns if row[col]) 
        for row in data
    ]
    embeddings = model.encode(texts)  # Generate embeddings
    return embeddings, texts

# Step 5: Process a Single Table
def process_table(connection, table_name, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    data = fetch_table_data(connection, table_name)
    
    if not data:
        print(f"Table {table_name} is empty. Skipping.")
        return None, None
    
    # Get non-ID columns for metadata
    non_id_columns = get_non_id_columns(connection, table_name)
    
    # Select text-based columns for embeddings
    text_columns = [col for col in non_id_columns if isinstance(data[0].get(col), str)]  # Columns with text data
    
    # Generate embeddings for the combined text columns
    embeddings, texts = generate_text_embeddings(data, text_columns, model)
    embeddings = np.array(embeddings, dtype="float32")
    
    # Initialize FAISS index
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index = faiss.IndexIDMap(index)
    
    # Add embeddings to FAISS index
    ids = np.arange(len(embeddings))
    index.add_with_ids(embeddings, ids)
    
    # Create metadata for the table (all non-ID columns except text columns)
    metadata_columns = [col for col in non_id_columns if col not in text_columns]
    metadata = []
    for i, row in enumerate(data):
        row_metadata = {col: row[col] for col in metadata_columns}
        row_metadata.update({
            "faiss_id": ids[i],
            "text": texts[i]
        })
        metadata.append(row_metadata)
    
    metadata_df = pd.DataFrame(metadata)
    return index, metadata_df

# Step 6: Save FAISS Index and Metadata
def save_faiss_and_metadata(index, metadata_df, table_name):
    # Ensure directory exists
    os.makedirs("vector_database", exist_ok=True)
    
    index_filename = f"vector_database/{table_name}.index"
    metadata_filename = f"vector_database/{table_name}.csv"
    
    # Save FAISS index
    faiss.write_index(index, index_filename)
    print(f"FAISS index for {table_name} saved to {index_filename}.")
    
    # Save metadata
    metadata_df.to_csv(metadata_filename, index=False)
    print(f"Metadata for {table_name} saved to {metadata_filename}.")

# Step 7: Main Workflow
if __name__ == "__main__":
    # List of tables to process (we no longer need to specify text columns manually)
    tables = ["Menu", "GeneralInfo", "Reservations","Customers","OrderTracking"]
    
    connection = connect_to_db()
    
    try:
        for table_name in tables:
            print(f"Processing table: {table_name}")
            index, metadata_df = process_table(connection, table_name)
            
            if index and metadata_df is not None:
                save_faiss_and_metadata(index, metadata_df, table_name)
    finally:
        connection.close()
        print("Database connection closed.")