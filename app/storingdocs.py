from loader import create_all_documents
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

docs=create_all_documents()

# 2️⃣ Initialize the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 3️⃣ Create a FAISS vector store from your documents
vectordb = FAISS.from_documents(docs, embedding_model)

# 4️⃣ Save the FAISS index locally
vectordb.save_local("faiss_index")  # This creates files like 'faiss_index.index' locally

print("FAISS index created and saved successfully!")
