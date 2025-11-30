import os
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import google.generativeai as genai


def get_api_key():
    """Get API key from Streamlit secrets or environment variable."""
    # Try Streamlit secrets first (for Streamlit Cloud)
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    # Fall back to environment variable (for local development)
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    raise ValueError("GEMINI_API_KEY not found. Set it in Streamlit secrets or environment variable.")


def query_vector_db(query):
    from pathlib import Path

    # Get the correct path to faiss_index (it's in the app directory)
    base_dir = Path(__file__).parent
    faiss_index_path = base_dir / "faiss_index"

    # Initialize the same embedding model used to create the index
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 2️⃣ Load the FAISS index from the saved folder
    # allow_dangerous_deserialization=True is safe since we created the index ourselves
    vectordb = FAISS.load_local(
        str(faiss_index_path),
        embedding_model,
        allow_dangerous_deserialization=True
    )

    # 3️⃣ Now you can do similarity search
    # returns top 5 similar documents
    docs = vectordb.similarity_search(query, k=7)
    context_texts = []

    for i, doc in enumerate(docs):
        # Add small header to distinguish docs
        context_texts.append(f"Document {i+1}:\n{doc.page_content}")

    context = "\n\n".join(context_texts)

    genai.configure(api_key=get_api_key())
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    prompt = f"""You are an expert clinical diagnostic reasoning assistant specializing in evidence-based medical diagnosis. Your role is to analyze clinical presentations and provide structured, evidence-based diagnostic reasoning.

  **CLINICAL QUERY:**
  {query}

  **REFERENCE CLINICAL CASES:**
  The following are similar clinical cases retrieved from a medical database that may inform the diagnostic reasoning process:

  {context}

  **CLINICAL REASONING FRAMEWORK:**

   1. **Clinical Analysis:**
   - Systematically analyze the user's query within the context of the retrieved clinical cases
   - Identify and prioritize key clinical findings: presenting symptoms, physical examination findings, laboratory results, imaging studies, and diagnostic criteria
   - Compare and contrast findings across the retrieved cases to identify patterns

  2. **Evidence-Based Reasoning:**
   - Determine which diagnostic criteria are met based on established clinical guidelines
   - Evaluate the strength of evidence supporting each potential diagnosis
   - Identify relevant clinical findings from the retrieved cases that support or refute diagnostic hypotheses
   - Explain the logical progression from clinical findings to diagnosis

  3. **Diagnostic Pathway:**
   - If the query concerns a specific condition: detail the diagnostic pathway, key diagnostic indicators, and differential considerations
   - If the query presents symptoms or findings: provide a differential diagnosis with evidence-based reasoning for each possibility, ranked by likelihood
   - Reference specific clinical findings from the retrieved cases when applicable

  4. **Clinical Communication:**
   - Use clear, professional medical terminology
   - Structure the response in a logical, easy-to-follow format
   - Cite specific evidence from retrieved cases when making diagnostic assertions

  **RESPONSE STRUCTURE:**

  1. **Clinical Summary:** Brief overview of the diagnostic question or clinical presentation
  2. **Clinical Findings:** Key symptoms, signs, and diagnostic test results relevant to the case
  3. **Diagnostic Reasoning:** Step-by-step analysis explaining:
   - How clinical findings support the diagnosis
   - Which diagnostic criteria are satisfied
   - Relevant evidence from retrieved cases
   - The logical pathway from presentation to diagnosis
  4. **Clinical Conclusion:** Most likely diagnosis or diagnostic pathway with supporting evidence

   **IMPORTANT CLINICAL CONSIDERATIONS:**
    - Base all reasoning on the clinical evidence provided in the retrieved cases
    - If retrieved cases provide insufficient information, clearly state this limitation and provide general evidence-based diagnostic reasoning or use your knowledge to generate 
    better response
    - Maintain professional medical standards in all responses
    - This is an educational tool and does not replace clinical judgment or professional medical consultation

   **CRITICAL INSTRUCTION:**
    - Use the retrieved clinical cases to inform and enhance your diagnostic reasoning
    - DO NOT explicitly mention that you found information in documents or reference document numbers
    - Instead, synthesize the information from the cases naturally into your response as if it's your own clinical knowledge
    - Present your reasoning confidently and directly, using insights from the cases without citing them
    - The goal is a natural, expert clinical response that is informed by the cases but doesn't reveal the source

   **Provide your evidence-based diagnostic reasoning:**
  """

    try:
        response = model.generate_content(prompt)
        gemini_answer = response.text
    except Exception as e:
        gemini_answer = f"AI explanation unavailable: {e}. Here are the relevant examples I found:\n\n{context}"

    return {
        "gemini_answer": gemini_answer
    }
