
# Import the Libraries
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader, PdfWriter
from tempfile import NamedTemporaryFile
import base64
from htmlTemplates import expander_css, css, bot_template, user_template
import os
import requests
import time

# API Key Validation Functions
def validate_openai_key(api_key):
    """Validate OpenAI API key by making a test request"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Test with a simple completion request
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": 1
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        return response.status_code == 200
    except Exception as e:
        return False

def validate_huggingface_key(api_key):
    """Validate Hugging Face API key by making a test request"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Test with a simple API call to get user info
        response = requests.get(
            "https://huggingface.co/api/whoami",
            headers=headers,
            timeout=10
        )
        
        return response.status_code == 200
    except Exception as e:
        return False

# Process the Input PDF
def process_file(doc, openai_key=None, huggingface_key=None):
    model_name = "thenlper/gte-small"
    model_kwargs={"device":"cpu"}
    encode_kwargs={"normalize_embeddings":False}

    # Set API keys if provided
    if huggingface_key:
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = huggingface_key
    
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name, 
        model_kwargs=model_kwargs, 
        encode_kwargs=encode_kwargs
    )
    pdf_search = Chroma.from_documents(doc, embeddings)

    chain = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.3),
        retriever=pdf_search.as_retriever(search_kwargs={"k":2}),
        return_source_documents=True
    )
    return chain



# Method for Handling User Input
def handle_userinput(query):
    reponse = st.session_state.conversaton({"question":query, 'chat_history':st.session_state.chat_history}, return_only_outputs=True)
    st.session_state.chat_history += [(query, response['answer'])]
    st.session_state.N = list(reponse['source_documents'[0]])[1][1]['page']

    for i, message in enumerate(st.session_state.chat_history):
        st.session_state.expander1.write(user_template.replace("{{MSG}}", message[0]), unsafe_allow_html=True)
        st.session_state.expander1.write(bot_template.repalce("{{MSG}}", message[1]), unsafe_allow_html=True)


def main():
# Create Web-page Layout
    load_dotenv(".env")
    
    st.set_page_config(layout="wide",
                        page_title="Interactive Reader",
                        page_icon=":books:")

    st.write(css, unsafe_allow_html=True)
    
    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=[]
    if "N" not in st.session_state:
        st.session_state.N=0
    if "openai_key" not in st.session_state:
        st.session_state.openai_key = None
    if "huggingface_key" not in st.session_state:
        st.session_state.huggingface_key = None
    if "clear_openai_input" not in st.session_state:
        st.session_state.clear_openai_input = False
    if "clear_hf_input" not in st.session_state:
        st.session_state.clear_hf_input = False

    # Initialize sidebar state
    if "sidebar_minimized" not in st.session_state:
        st.session_state.sidebar_minimized = False
    
    # API Keys Section
    with st.sidebar:
        # Sidebar header with minimize/expand button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.header("🔑 API Keys Configuration")
        with col2:
            if st.button("📱", help="Minimize/Expand Sidebar"):
                st.session_state.sidebar_minimized = not st.session_state.sidebar_minimized
        
        # Show content only if not minimized
        if not st.session_state.sidebar_minimized:
            st.markdown("Load your API keys to use the application:")
            
            # OpenAI API Key
            st.subheader("OpenAI API Key")
            
            # Clear input if flag is set
            if st.session_state.clear_openai_input:
                openai_key_input = st.text_input(
                    "Enter your OpenAI API key:",
                    type="password",
                    value="",
                    help="Get your OpenAI API key from https://platform.openai.com/api-keys",
                    label_visibility="collapsed"
                )
                st.session_state.clear_openai_input = False  # Reset flag
            else:
                openai_key_input = st.text_input(
                    "Enter your OpenAI API key:",
                    type="password",
                    value=st.session_state.openai_key or "",
                    help="Get your OpenAI API key from https://platform.openai.com/api-keys",
                    label_visibility="collapsed"
                )
        
            if st.button("Load OpenAI Key"):
                if openai_key_input:
                    with st.spinner("Validating OpenAI API key..."):
                        if validate_openai_key(openai_key_input):
                            st.session_state.openai_key = openai_key_input
                            st.session_state.clear_openai_input = True
                            st.success("✅ OpenAI API key validated and loaded successfully!")
                            
                            # Check if both keys are loaded for auto-minimization
                            if st.session_state.openai_key and st.session_state.huggingface_key:
                                st.info("🎉 Both API keys loaded! Sidebar will minimize automatically.")
                                st.session_state.sidebar_minimized = True
                        else:
                            st.error("❌ Invalid OpenAI API key. Please check your key and try again.")
                else:
                    st.error("Please enter a valid OpenAI API key")
        
            # Hugging Face API Key
            st.subheader("Hugging Face API Key")
            
            # Clear input if flag is set
            if st.session_state.clear_hf_input:
                huggingface_key_input = st.text_input(
                    "Enter your Hugging Face API key:",
                    type="password",
                    value="",
                    help="Get your Hugging Face API key from https://huggingface.co/settings/tokens"
                )
                st.session_state.clear_hf_input = False  # Reset flag
            else:
                huggingface_key_input = st.text_input(
                    "Enter your Hugging Face API key:",
                    type="password",
                    value=st.session_state.huggingface_key or "",
                    help="Get your Hugging Face API key from https://huggingface.co/settings/tokens"
                )
        
            if st.button("Load Hugging Face Key"):
                if huggingface_key_input:
                    with st.spinner("Validating Hugging Face API key..."):
                        if validate_huggingface_key(huggingface_key_input):
                            st.session_state.huggingface_key = huggingface_key_input
                            st.session_state.clear_hf_input = True
                            st.success("✅ Hugging Face API key validated and loaded successfully!")
                            
                            # Check if both keys are loaded for auto-minimization
                            if st.session_state.openai_key and st.session_state.huggingface_key:
                                st.info("🎉 Both API keys loaded! Sidebar will minimize automatically.")
                                st.session_state.sidebar_minimized = True
                        else:
                            st.error("❌ Invalid Hugging Face API key. Please check your key and try again.")
                else:
                    st.error("Please enter a valid Hugging Face API key")
        
            # Helpful links
            st.markdown("---")
            st.markdown("### 🔗 Get Your API Keys:")
            st.markdown("[OpenAI API Keys](https://platform.openai.com/api-keys)")
            st.markdown("[Hugging Face Tokens](https://huggingface.co/settings/tokens)")
            
            # Status indicators
            st.markdown("---")
            st.markdown("### 📊 API Key Status:")
            
            if st.session_state.openai_key:
                openai_status = "✅ Validated & Loaded"
            else:
                openai_status = "❌ Not loaded"
                
            if st.session_state.huggingface_key:
                huggingface_status = "✅ Validated & Loaded"
            else:
                huggingface_status = "❌ Not loaded"
            
            st.markdown(f"**OpenAI:** {openai_status}")
            st.markdown(f"**Hugging Face:** {huggingface_status}")
            
            # Show validation info
            if st.session_state.openai_key or st.session_state.huggingface_key:
                st.info("🔒 API keys are validated and stored securely in your session.")

    st.session_state.col1, st.session_state.col2 = st.columns([1,1])
    st.session_state.col1.header("Interactive Reader :books:")
    user_question = st.session_state.col1.text_input("Ask a question on the contents of the uploaded PDF:")
    st.session_state.expander1 = st.session_state.col1.expander("Your Chat", expanded=True)
    st.session_state.col1.markdown(expander_css, unsafe_allow_html=True)
   

    # Load and Process the PDF 
    st.session_state.col1.subheader("Your documents")
    st.session_state.pdf_doc = st.session_state.col1.file_uploader("Upload your PDF here and click on 'Process")

    if st.session_state.col1.button("Process",key='a'):
        # Check if API keys are available
        if not st.session_state.openai_key and not os.getenv("OPENAI_API_KEY"):
            st.session_state.col1.error("⚠️ Please load your OpenAI API key in the sidebar to process PDFs.")
            return
        if not st.session_state.huggingface_key and not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
            st.session_state.col1.error("⚠️ Please load your Hugging Face API key in the sidebar to process PDFs.")
            return
            
        with st.spinner("Processing..."):
            if st.session_state.pdf_doc is not None:
                with NamedTemporaryFile(suffix="pdf") as temp:
                    temp.write(st.session_state.pdf_doc.getvalue())
                    temp.seek(0)
                    loader = PyPDFLoader(temp.name)
                    pdf = loader.load()
                    st.session_state.conversation = process_file(
                        pdf, 
                        openai_key=st.session_state.openai_key,
                        huggingface_key=st.session_state.huggingface_key
                    )
                    st.session_state.col1.markdown("✅ Done Processing. You may now ask a question.")

    
    # Handle Query and Display Pages
    if user_question:
        handle_userinput(user_question)
        with NamedTemporaryFile(suffix="pdf") as temp:
            temp.write(st.session_state.pdf_doc.getvalue())
            temp.seek(0)
            reader = PdfReader(temp.name)

            pdf_writer = PdfWriter()
            start = max(st.session_state.N-2,0)
            end = min(st.session_state.N+2, len(reader.pages)-1)
            while start <= end:
                pdf_writer.add_page(reader.pages[start])
                start+=1
            with NamedTemporaryFile(suffix="pdf") as temp2:
                pdf_write.write(temp2.name)
                with open(temp2.name, "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

                    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}#page={3}"\
                        width="100%" height="900" type="application/pdf frameborder="0"></iframe>'

                    st.session_state.col2.markdown(pdf_display, unsafe_allow_html=True)
                    



if __name__ == '__main__':
    main()

