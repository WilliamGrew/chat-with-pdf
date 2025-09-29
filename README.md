# Chat-With-PDF 📚

A powerful AI-powered PDF chat application that lets you ask questions about your PDF documents and get intelligent answers. No technical knowledge required!

![PDF Chat App](PDF-Chat%20App.png)

## 🌐 Try It Online (No Setup Required!)

**🚀 [Launch the App Online](https://chatpdfonline.streamlit.app/)**

You can use the application directly in your browser without any installation! Just click the link above and start chatting with your PDFs immediately.

## ✨ Features

- 🤖 **AI-Powered Chat**: Ask questions about your PDF content
- 🔒 **Secure API Key Management**: Easy setup with built-in key validation
- 📱 **Smart Interface**: Auto-minimizing sidebar for clean experience
- 🔍 **Intelligent Search**: Find relevant information quickly
- 💬 **Conversational**: Maintains chat history for better context

## 🚀 Quick Start Guide (For Everyone)

### Option A: Use Online (Recommended for Beginners)

**🌐 [Use the App Online](https://chatpdfonline.streamlit.app/)** - No installation required!

Simply click the link above and start using the application immediately in your browser. You'll still need to get your API keys (see Step 3 below), but you won't need to install anything on your computer.

### Option B: Install Locally

### Step 1: Download and Install

1. **Download Python** (if you don't have it):
   - Go to [python.org](https://www.python.org/downloads/)
   - Download the latest version
   - During installation, check "Add Python to PATH"

2. **Download this app**:
   - Click the green "Code" button on this page
   - Select "Download ZIP"
   - Extract the ZIP file to your desired folder

### Step 2: Set Up the Application

1. **Open Command Prompt/Terminal**:
   - **Windows**: Press `Win + R`, type `cmd`, press Enter
   - **Mac**: Press `Cmd + Space`, type "Terminal", press Enter

2. **Navigate to the app folder**:
   ```bash
   cd path/to/your/downloaded/folder
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Get Your API Keys

#### 🔑 OpenAI API Key
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign up or log in to your OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. **Important**: Save this key somewhere safe - you won't see it again!

#### 🤗 Hugging Face API Key
1. Go to [Hugging Face Tokens](https://huggingface.co/settings/tokens)
2. Sign up or log in to your Hugging Face account
3. Click "New token"
4. Give it a name (e.g., "PDF Chat App")
5. Select "Read" access
6. Click "Generate a token"
7. Copy the token (starts with `hf_`)

### Step 4: Run the Application

1. **Start the app**:
   ```bash
   streamlit run app.py
   ```

2. **Your browser will open automatically** to the app

### Step 5: Configure API Keys

1. **In the sidebar**, you'll see "🔑 API Keys Configuration"
2. **Enter your OpenAI key**:
   - Paste your OpenAI API key in the first field
   - Click "Load OpenAI Key"
   - Wait for the green success message
3. **Enter your Hugging Face key**:
   - Paste your Hugging Face token in the second field
   - Click "Load Hugging Face Key"
   - Wait for the green success message
4. **Sidebar will minimize automatically** when both keys are loaded! 🎉

### Step 6: Use the Application

1. **Upload a PDF**:
   - Click "Choose file" in the "Your documents" section
   - Select your PDF file
   - Click "Process" and wait for processing to complete

2. **Start chatting**:
   - Type your question in the text box
   - Press Enter or click the send button
   - Get AI-powered answers about your PDF!

## 🛠️ Advanced Setup (For Developers)

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/chat-with-pdf.git
   cd chat-with-pdf
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv chatpdf
   ```

3. **Activate virtual environment**:
   - **Windows**: `.\chatpdf\Scripts\activate`
   - **Mac/Linux**: `source chatpdf/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables** (optional):
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_key_here
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
   ```

6. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 🔧 Troubleshooting

### Common Issues

**"Module not found" error**:
- Make sure you've installed all requirements: `pip install -r requirements.txt`

**"Invalid API key" error**:
- Double-check your API keys are correct
- Make sure you copied the full key (including the `sk-` or `hf_` prefix)

**App won't start**:
- Make sure Python is installed and in your PATH
- Try running: `python --version` to check if Python is working

**Browser doesn't open automatically**:
- The app will be available at `http://localhost:8501`
- Copy this URL into your browser

### Getting Help

If you encounter issues:
1. Check that all steps were followed correctly
2. Make sure your API keys are valid and have sufficient credits
3. Try restarting the application
4. Check the terminal/command prompt for error messages

## 📋 Requirements

- Python 3.8+
- OpenAI API key (with credits)
- Hugging Face account and API token
- Internet connection

## 🎯 How It Works

1. **PDF Processing**: Your PDF is broken down into chunks for analysis
2. **AI Embeddings**: Hugging Face models create vector representations of your text
3. **Smart Search**: When you ask a question, the system finds relevant sections
4. **AI Response**: OpenAI's GPT model generates answers based on the found content
5. **Chat History**: Your conversation is maintained for context

## 🔒 Privacy & Security

- API keys are stored securely in your browser session
- Keys are automatically cleared from input fields after loading
- No data is stored on external servers
- Your PDF content is processed locally

## 📞 Support

Need help? Check the troubleshooting section above or create an issue in the repository.

---

**Happy PDF Chatting! 🎉**

