# StanBot – Empathetic Chat Buddy

This project features a smart conversational AI assistant built with LangChain for memory management, Google Generative AI for dynamic responses, and Gradio for a sleek, interactive interface. The chatbot maintains context across messages, remembers important details from previous interactions, and delivers cohesive, human-like responses. It demonstrates how memory-enabled AI can enhance conversation continuity and create more engaging dialogue experiences.
## Features

**Powered by Google Generative AI:** Generates high-quality, natural, and context-aware responses.

**Contextual Session Memory:** Remembers conversation history within a session, allowing the chatbot to reference earlier messages naturally.

**Interactive Gradio Interface:** Provides a sleek, user-friendly interface for real-time conversations, showing both user inputs and AI replies.

**Smart Prompting with LangChain:** Uses customizable prompt templates to adapt the chatbot’s tone, style, and behavior dynamically.
## Requirements

- **Python 3.10+**
- **API Key for Google Generative AI**
- **LangChain, dotenv, and Gradio** libraries

## Installation

1. **Clone the repository**:
   ```bash
   https://github.com/PratigyaIshi112/stanbot-chat.git
   ```

2. **Install dependencies**:
   ```bash
   pip3 install langchain langchain-google-genai gradio pydantic python-dotenv
   ```

3. **Set up environment variables**:
Create a .env file in the root directory.
Add your Google Generative AI API key and model configuration:

   ```plaintext
   GOOGLE_API_KEY=<your_google_api_key>
   GOOGLE_MODEL=<your_google_model>
   ```

## Usage

### Running the Chatbot

1. Start the chatbot by running the main script:

   ```bash
   python3 your_script.py
   ```

2. **Chat with the Bot**:
   - Enter a username and a query in the provided fields.
   - Each query and response will be displayed in the chat history with labels `[username]` and `[AI]`.

### Example Chat Flow

- **Username**: `Pratigya`
- **User Query 1**: "Hi, I would like to know a brief overview of AI."
- **Bot Response 1**: AI provides a brief description of artificial intelligence.
- **User Query 2**: "Do you remember my name?"
- **Bot Response 2**: "Yes, your name is Pratigya."

The chatbot remembers previous messages, allowing it to maintain context and deliver smooth, natural, and coherent conversations. By recalling earlier interactions, it provides a more engaging and seamless chat experience, making conversations feel intuitive and human-like.

## Code Overview

1. **Environment Setup**: Loads the `.env` file to get API credentials for Google Generative AI.
2. **Model and Prompt Initialization**: Sets up the Google Generative AI model and a conversational prompt template.
3. **Session Memory**: 
   - Manages conversation history with `InMemoryHistory`, a custom class to store message sequences.
   - Retrieves or creates new session histories as needed.
4. **Gradio Interface**:
   - Uses `gr.Chatbot` to display the chat history sequentially.
   - Displays each exchange with labels indicating whether it was the user's query or the bot's response.

## File Structure

```plaintext
.
├── main.py                # Main script to run the chatbot
├── README.md              # Documentation
├── .env                   # Environment variables file
└── requirements.txt       # Python dependencies
```

### Sample `.env` file

```plaintext
GOOGLE_API_KEY=your_google_api_key
GOOGLE_MODEL=your_google_model_name
```

## Dependencies

This project requires the following libraries:
- `langchain` - Core library for language model integration and prompt management.
- `gradio` - For creating a web-based chat interface.
- `pydantic` - Data validation and settings management.
- `python-dotenv` - Loads environment variables from a `.env` file.

Install dependencies using:
```bash
pip3 install -r requirements.txt
```



## License

This project is licensed under the MIT License. See `LICENSE` for details.

