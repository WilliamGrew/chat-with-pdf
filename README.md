# Chat-With-Pdf
This project highlights how to leverage a ChromaDB vector store in a Langchain pipeline to create a chat with a Pdf application. You can load in a pdf based document and use it alongside an LLM without fine-tuning. 


# Startup 🚀
1. Create a virtual environment `python -m venv chatpdf`
2. Activate it: 
   - Windows:`.\chatpdf\Scripts\activate`
   - Mac: `source chatpdf/bin/activate'
3. Clone this repo `git clone this_repo`
4. Go into the directory `cd this_repo`
5. Install the required dependencies `pip install -r requirements.txt`
6. You’ll use the HuggingFace models to generate word embeddings of the text in the PDFs. 
    These search results will then be used to generate responses to the questions asked using the GPT-3 LLM by OpenAI.
    
    You’ll provide the following API keys in the /.env file:
    
    HuggingFace: Use this Answer to get the access token for HuggingFace.
    OpenAI: Use this Answer to get an API key for GPT.
7. Start the app `streamlit run app.py`
8. Load the Pdf you would like to ask questions
9. Ask questions and get the answers

