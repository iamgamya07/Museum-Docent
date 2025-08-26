import streamlit as st
from utils.rag_utils import retrieve_similar_artworks
from models.llm import generate_llm

# ---------------------------
# Sidebar Navigation
# ---------------------------
st.set_page_config(
    page_title="Museum Docent Chatbot",
    page_icon="🎨",
    layout="wide"
)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Chat", "Instructions"], index=0)

# ---------------------------
# Instructions Page
# ---------------------------
def instructions_page():
    st.title(" Instructions")
    st.markdown("""
    Welcome to the **Museum Docent Chatbot**!

    This AI-powered assistant helps you explore artworks and artists using information retrieved from museum archives.

    ## 🔧 Setup
    1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    2. Add your **Groq API key** to `.env` file:
    ```env
    GROQ_API_KEY=your_key_here
    ```

    ##  Example Questions
    - What is 'The Starry Night'?
    - Who made this bronze sculpture?
    - Describe the painting of a woman with flowers

    ##  Modes
    - **Concise**: Short summary-like responses
    - **Detailed**: In-depth contextual information from the museum database

    ##  Tips
    - Ask about **artists**, **exhibits**, or **specific works**
    - The bot uses both RAG (document retrieval) and LLM (Groq) for intelligent replies

    ---
    Enjoy your tour of the art world! 
    """)

# ---------------------------
# Chat Page
# ---------------------------
def chat_page():
    st.markdown("""
        <h1 style='text-align: center; color: #4B0082;'>Museum Docent Chatbot</h1>
        <p style='text-align: center; font-size: 18px;'>Ask questions about artworks, artists, and exhibits – powered by AI + museum archives</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([3, 2])

    with col1:
        query = st.text_input(" Ask a question:", placeholder="e.g. Tell me about Van Gogh's self portrait")
        mode = st.radio("Response Style:", ["concise", "detailed"], horizontal=True)

    with col2:
        st.info("""
        **Try questions like:**
        - What is 'The Starry Night'?
        - Who created this sculpture?
        - Describe the painting with flowers

        Select **Concise** for summaries or **Detailed** for full context.
        """)

    st.markdown("---")

    if query:
        with st.spinner("Searching the museum archive..."):
            try:
                context_chunks = retrieve_similar_artworks(query, index_path="faiss_index")
                context = "\n---\n".join(context_chunks)
                full_prompt = f"Use the following context to answer the user's question.\n---\n{context}\n---\nQuestion: {query}"

                response = generate_llm(full_prompt, mode=mode)

                st.markdown("""
                <h3 style='color: #2E8B57;'>Docent Bot's Answer:</h3>
                """, unsafe_allow_html=True)
                st.success(response)

            except Exception as e:
                st.error(f" Error: {str(e)}")
    else:
        st.markdown("<p style='text-align: center;'>Enter a question above to begin exploring the art world!</p>", unsafe_allow_html=True)

# ---------------------------
# Route Pages
# ---------------------------
if page == "Instructions":
    instructions_page()
else:
    chat_page()
