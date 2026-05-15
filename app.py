import streamlit as st
from dotenv import load_dotenv
from rag import generate_response

load_dotenv()

# page config
st.set_page_config(
    page_title="UMD Assistant",
    page_icon="〽️",
    layout="wide"
)

# UMD colors CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #00274C;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Header banner */
    .umd-header {
        background-color: #00274C;
        padding: 20px 30px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 6px solid #FFCB05;
    }
    .umd-header h1 {
        color: #FFCB05;
        margin: 0;
        font-size: 2rem;
    }
    .umd-header p {
        color: white;
        margin: 5px 0 0 0;
        font-size: 0.9rem;
        opacity: 0.85;
    }

    /* Answer box */
    .answer-box {
        background-color: #f8f9fa;
        border-left: 4px solid #FFCB05;
        padding: 20px;
        border-radius: 6px;
        margin-top: 15px;
        color: #00274C;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* Question display */
    .question-box {
        background-color: #00274C;
        color: #FFCB05;
        padding: 12px 18px;
        border-radius: 6px;
        margin-top: 20px;
        font-weight: 600;
    }

    /* Input styling */
    .stTextInput input {
        border: 2px solid #00274C !important;
        border-radius: 6px !important;
        font-size: 1rem !important;
        padding: 10px !important;
    }

    /* Button styling */
    .stButton button {
        background-color: #00274C !important;
        color: #FFCB05 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
        font-size: 1rem !important;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #FFCB05 !important;
        color: #00274C !important;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True) 




# sidebar
with st.sidebar: # create a sidebar for the app, which will contain an image, some introductory text, and information about the technologies used
    st.image("images/download.jpeg", width=300)
    st.markdown("---")
    st.markdown("### 〽️ UMD Assistant")
    st.markdown("Ask anything about University of Michigan-Dearborn — admissions, programs, campus life, and more.")
    st.markdown("---")
    st.markdown("⚠️ **Disclaimer**")
    st.markdown("This tool is not affiliated with or endorsed by the University of Michigan-Dearborn. Responses are AI-generated and may contain errors. Always verify important information with official UMD sources.")
    st.markdown("---")
    st.markdown("**Powered by**")
    st.markdown("• Claude AI (Anthropic)")
    st.markdown("• RAG Pipeline")
    st.markdown("• ChromaDB")
    st.markdown("---")
    st.markdown("*Data sourced from umdearborn.edu*")
    st.markdown("---")

# main content
st.markdown("""
<div class="umd-header">
    <h1>〽️ UMD Student Assistant</h1>
    <p>Ask questions about academics, admissions, campus life, and more.</p>
</div>
""", unsafe_allow_html=True)

# chat history
if "history" not in st.session_state:
    st.session_state.history = []

# input
query = st.text_input("Your question:", placeholder="e.g. What is the phone number for campus safety?") # text input box for the user to enter their question, with a placeholder example question to guide them

col1, col2 = st.columns([1, 5]) # create two columns for layout, with the first column being narrower than the second
with col1:
    ask = st.button("Ask") # button that the user clicks to submit their question, which will trigger the generation of a response and update the chat history

if ask and query: # when the user clicks the "Ask" button and there is a query in the input box, we want to generate a response and update the chat history
    with st.spinner("Searching UMD knowledge base..."):
        answer = generate_response(query) # call the generate_response function from our rag.py file, passing in the user's query, which will return a generated answer based on the retrieved context from our ChromaDB knowledge base
    st.session_state.history.append({"question": query, "answer": answer})

# display history
for item in reversed(st.session_state.history):
    st.markdown(f'<div class="question-box">Q: {item["question"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="answer-box">{item["answer"]}</div>', unsafe_allow_html=True)