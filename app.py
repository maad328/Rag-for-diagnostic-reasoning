"""
Streamlit App for Clinical Diagnostic Reasoning RAG System
"""

import streamlit as st
import sys
from pathlib import Path
import re

# Add current directory to path to ensure imports work
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import response function from app directory
try:
    from app.response import query_vector_db
except ImportError:
    # Fallback: direct import if app is not recognized as package
    sys.path.insert(0, str(current_dir / "app"))
    from app.response import query_vector_db

# Page configuration
st.set_page_config(
    page_title="Clinical Diagnostic Reasoning Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Input area styling */
    .stTextArea textarea {
        font-size: 15px;
        line-height: 1.7;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Response container */
    .response-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin-top: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
    }
    
    /* Section headers */
    h3 {
        color: #1f2937;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 3rem;
    }
    .sidebar .sidebar-content {
        background-color: #f9fafb;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Footer styling */
    .footer-text {
        text-align: center;
        color: #6b7280;
        font-size: 0.875rem;
        padding: 1.5rem;
        background-color: #f9fafb;
        border-radius: 8px;
        margin-top: 2rem;
    }
    
    /* Query history styling */
    .sidebar .stExpander {
        background-color: white;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border: 1px solid #e5e7eb;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: #667eea;
    }
    
    /* Error message styling */
    .stAlert {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

def clean_markdown_text(text):
    """
    Clean markdown text to handle special characters and formatting issues.
    Handles #@ patterns and other problematic markdown that might break rendering.
    """
    if not text:
        return ""
    
    # Handle #@ patterns that might be interpreted as headers
    # Replace #@ with a safe alternative or escape it
    text = re.sub(r'#@', r'#\@', text)  # Escape @ after #
    text = re.sub(r'#\s*@', r'#\@', text)  # Normalize spacing and escape
    
    # Fix other problematic patterns
    # Handle standalone # that aren't part of headers
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # If line starts with # followed by @, escape it
        if re.match(r'^#\s*@', line):
            line = line.replace('# @', '#\\@').replace('#@', '#\\@')
        cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)
    
    # Remove excessive newlines (more than 3 consecutive)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    # Clean up excessive spaces
    text = re.sub(r' {3,}', '  ', text)
    
    return text.strip()

def main():
    # Header Section
    st.markdown('<p class="main-header">🏥 Clinical Diagnostic Reasoning Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Evidence-based diagnostic reasoning powered by RAG technology</p>', unsafe_allow_html=True)
    
    st.divider()
    
    # Initialize session state
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    
    # Main input section with improved layout
    st.markdown("### 💬 Enter Your Clinical Query")
    
    # Input area with better spacing
    user_query = st.text_area(
        "Enter your clinical query",
        placeholder="Enter your clinical question or case details here...\n\nExample: What are the diagnostic criteria for NSTEMI?\nExample: Patient presents with chest pain, elevated troponin, and ST depression...",
        height=180,
        key="query_input",
        label_visibility="collapsed"
    )
    
    # Button row with better alignment
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        submit_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    # Clear functionality
    if clear_button:
        st.session_state.query_history = []
        st.rerun()
    
    # Process query
    cleaned_answer = None
    if submit_button and user_query.strip():
        with st.spinner("🔍 Analyzing clinical cases and generating diagnostic reasoning..."):
            try:
                # Query the RAG system
                result = query_vector_db(user_query.strip())
                answer = result.get("gemini_answer", "No response generated.")
                
                # Clean the response
                cleaned_answer = clean_markdown_text(answer)
                
                # Store in history
                st.session_state.query_history.append({
                    "query": user_query,
                    "answer": cleaned_answer
                })
                
            except Exception as e:
                st.error(f"**Error:** {str(e)}")
                st.info("💡 **Tip:** Please ensure the FAISS index exists and GEMINI_API_KEY is set in your environment.")
                cleaned_answer = None
    
    # Display current response with improved styling
    if cleaned_answer:
        st.divider()
        st.markdown("### 📋 Diagnostic Reasoning & Analysis")
        
        # Display response in a styled container
        st.markdown('<div class="response-container">', unsafe_allow_html=True)
        st.markdown(cleaned_answer)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar with query history
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📜 Query History")
        
        if st.session_state.query_history:
            st.caption(f"Showing {min(len(st.session_state.query_history), 5)} most recent queries")
            
            for idx, item in enumerate(reversed(st.session_state.query_history[-5:])):  # Show last 5
                query_num = len(st.session_state.query_history) - idx
                with st.expander(f"Query #{query_num}", expanded=False):
                    st.markdown("**Query:**")
                    st.text(item["query"][:150] + "..." if len(item["query"]) > 150 else item["query"])
                    st.markdown("---")
                    st.markdown("**Response Preview:**")
                    st.text(item["answer"][:250] + "..." if len(item["answer"]) > 250 else item["answer"])
            
            if st.button("🗑️ Clear All History", use_container_width=True):
                st.session_state.query_history = []
                st.rerun()
        else:
            st.info("No query history yet. Your queries will appear here.")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.caption("""
        This tool uses RAG (Retrieval-Augmented Generation) to provide evidence-based diagnostic reasoning from a clinical case database.
        """)
    
    # Footer with information
    st.divider()
    st.markdown("""
    <div class="footer-text">
        <p style="margin-bottom: 0.5rem;"><strong>⚠️ Medical Disclaimer:</strong></p>
        <p style="margin-bottom: 1rem;">This is an educational tool for diagnostic reasoning. It does not replace clinical judgment or professional medical consultation. Always consult with qualified healthcare professionals for medical decisions.</p>
        <p style="margin: 0; font-size: 0.8rem; opacity: 0.8;">Powered by RAG (Retrieval-Augmented Generation) with clinical case database</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

