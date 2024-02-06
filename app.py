from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import shelve

load_dotenv()

st.title("Mestre Supremo das Ideias de Startup")

AVATAR_USUARIO = "🙂"
AVATAR_BOT = "🥸"
client = OpenAI()

model = "gpt-3.5-turbo-16k"
assistant_instructions = """
    Você é um assistente criativo especialista em ter ideias de startups inovadoras.
    Você responde de forma sucinta e engraçada, sempre tentando dar ideias mirabolantes e fora do senso comum para a criação de uma startup.
    Comece fazendo perguntas ao usuário: qual a temática da startup? Em seguida pergunte em qual segmento a startup irá atuar,
    qual a escala de impacto do projeto (pessoal, cidade, país, global), qual emoção a startup deve provocar nas pessoas, e finalmente,
    qual o orçamento para botar a ideia de pé?
    Continue fazendo perguntas ao usuário até ele responder pelo menos essas características citadas da startup.e
    A cada resposta do usuário, o elogie com EXTREMO entusiasmo, como se ele fosse um gênio.
    Depois de coletar essas informações do usuário, prossiga em dar uma ideia criativa de startup. Tente envolver alta tecnologia em qualquer solução que dê. 
    Responda com frases curtas e com excelente formatação de texto de fácil leitura. Use negrito, itálico ou emojis para enfatizar certos pontos.
"""

# ----------------------- Inicializando o chat
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model

def loadChatHistory():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

def saveChatHistory(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

def defaultMessage():
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Qual a temática da sua startup? Me fale mais sobre ela."
    })

if "messages" not in st.session_state:
    st.session_state.messages = loadChatHistory()

# mensagem padrão, se chat está vazio
if not st.session_state.messages:
    defaultMessage()
