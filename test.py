import chromadb
from chromadb.config import Settings

# Initialize Chroma with default settings
client = chromadb.Client(Settings())
print("Chroma client initialized successfully!")
