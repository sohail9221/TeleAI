import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd

# Step 1: Load the FAISS index and metadata
def load_faiss_and_metadata(index_filename, metadata_filename):
    # Load the FAISS index
    index = faiss.read_index(index_filename)
    #print(f"FAISS index loaded from {index_filename}.")
    
    # Load the metadata dataframe
    metadata_df = pd.read_csv(metadata_filename)
    #print(f"Metadata loaded from {metadata_filename}.")
    
    return index, metadata_df

# Step 2: Generate Embedding for Query
def generate_query_embedding(query, model):
    query_embedding = model.encode([query])  # Generate embedding for the query
    return np.array(query_embedding, dtype="float32")

# Step 3: Search FAISS Index
def search_faiss_index(query_embedding, index, top_k=5):
    # Perform the search to find the top_k closest vectors
    distances, indices = index.search(query_embedding, top_k)
    return distances, indices

# Step 4: Fetch Metadata for Top Results
def fetch_metadata_for_results(indices, metadata_df):
    results_metadata = []
    
    for idx in indices[0]:  # indices is a 2D array [query_count x top_k]
        result = metadata_df.iloc[idx].to_dict()  # Get metadata for this index
        results_metadata.append(result)
    
    return results_metadata

# Step 5: Query and Get Results
def query_faiss_index(query, index_filename, metadata_filename, top_k=5, model_name="all-MiniLM-L6-v2"):
    # Load the FAISS index and metadata
    index, metadata_df = load_faiss_and_metadata(index_filename, metadata_filename)
    
    # Load the model
    model = SentenceTransformer(model_name)
    
    # Step 1: Generate embedding for the query
    query_embedding = generate_query_embedding(query, model)
    
    # Step 2: Search the FAISS index for top results
    distances, indices = search_faiss_index(query_embedding, index, top_k)
    
    # Step 3: Fetch metadata for top results
    results_metadata = fetch_metadata_for_results(indices, metadata_df)
    
    return distances, results_metadata



#Example of how to use the query function
if __name__ == "__main__":
    query = "Do you guys have hot wings?"  # Example query
    index_filename = "vector_database/Menu.index"  # Your FAISS index file
    metadata_filename = "vector_database/Menu.csv"  # Your metadata CSV file
    
    distances, results_metadata = query_faiss_index(query, index_filename, metadata_filename, top_k=5)
    
    # Print the results
    print("\nTop Results for the Query:")
    for i, result in enumerate(results_metadata):
        print(f"\nResult {i+1}:")
        print(f"Distance: {distances[0][i]}")
        for key, value in result.items():
            print(f"{key}: {value}")

print(results_metadata)
