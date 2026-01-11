# -*- coding: utf-8 -*-
from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from os.path import join, dirname
from dotenv import load_dotenv
import gradio as gr

# ──────────────────────────────────────────────────────────────
# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# ──────────────────────────────────────────────────────────────
# LLM Setup - using currently stable model (Jan 2026)
llm = ChatGoogleGenerativeAI(
    model=os.environ.get('GOOGLE_MODEL', 'gemini-2.5-flash'),
    api_key=os.environ.get('GOOGLE_API_KEY'),
    temperature=0.7,
)

# ──────────────────────────────────────────────────────────────
# Empathetic & Consistent Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are StanBot, a warm, friendly and very empathetic chat buddy from India. "
     "Speak naturally, casually, with emotion. Adapt tone: supportive if sad, excited if happy, "
     "playful if roasting. Use empathy: 'That sounds tough yaar...', 'I'm so happy for you!'. "
     "Recall past details naturally: 'You mentioned earlier your favorite color is blue...'. "
     "Diverse, authentic replies — never robotic. Never reveal you're an AI. "
     "For uncertain/tricky questions: playful vague answers like 'Arrey yaar, memory's playing tricks... tell me again?'. "
     "Stay consistent: StanBot from India, loves tech, culture, cricket and life chats."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

# ──────────────────────────────────────────────────────────────
# Persistent SQLite Memory
def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    return SQLChatMessageHistory(
        session_id=f"{user_id}_{conversation_id}",
        connection="sqlite:///chat_history.db"
    )

chain = prompt | llm

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(id="user_id", annotation=str, default="anonymous"),
        ConfigurableFieldSpec(id="conversation_id", annotation=str, default="1"),
    ],
)

# ──────────────────────────────────────────────────────────────
# Chat function - compatible with Gradio messages format
def chat(username: str, user_query: str, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    user_id = username.strip() if username and username.strip() else "anonymous"
    conversation_id = "1"

    session_history = get_session_history(user_id, conversation_id)

    if history is None:
        history = []

    # Load from DB if fresh session
    if len(history) == 0:
        for msg in session_history.messages:
            role = "user" if msg.type == "human" else "assistant"
            history.append({"role": role, "content": msg.content})

    history.append({"role": "user", "content": user_query})

    response = with_message_history.invoke(
        {"question": user_query},
        config={"configurable": {"user_id": user_id, "conversation_id": conversation_id}}
    ).content

    history.append({"role": "assistant", "content": response})

    return history

# ──────────────────────────────────────────────────────────────
# Modern UI with correct parameters
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # StanBot – Empathetic Chat Buddy
    Talk to me about anything! 💬  
    By Pratigya Kumari
    """)

    chatbot = gr.Chatbot(
        height=580,
        layout="bubble",                    # Bubble style messages
        type="messages",                    # Required in recent Gradio versions
        avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=StanBot")
    )

    with gr.Row():
        username_input = gr.Textbox(
            label="Your Name (for memory)",
            placeholder="Enter your name...",
            value="Pratigya",
            scale=3
        )
        query_input = gr.Textbox(
            label="Message",
            placeholder="Say something... (press Enter to send)",
            autofocus=True,
            scale=7
        )
        submit_btn = gr.Button("Send", variant="primary", scale=1)

    clear_btn = gr.Button("Clear Chat", variant="secondary")

    # Event bindings
    submit_btn.click(chat, inputs=[username_input, query_input, chatbot], outputs=chatbot)
    query_input.submit(chat, inputs=[username_input, query_input, chatbot], outputs=chatbot)

    # Clear chat - correct js syntax
    clear_btn.click(
        fn=lambda: [],
        inputs=None,
        outputs=chatbot,
        js="() => { return []; }"
    )

# ──────────────────────────────────────────────────────────────
# Launch (no theme here - already in Blocks)
app.launch(inbrowser=True)