from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os, shelve, random

load_dotenv()

st.title("Mestre Supremo das Ideias de Startup")

AVATAR_USUARIO = ["🙂","🙂","🙂","🙂", "😲", "🤔", "🫣", "🤗", "😖", "😌", "🤫"]
AVATAR_BOT = "🥸"

# guarda o contexto da lista de emojis do AVATAR_USUARIO
if 'emoji_idxList' not in st.session_state:
    st.session_state['emoji_idxList'] = [0]
if 'emoji_counter' not in st.session_state:
    st.session_state['emoji_counter'] = 0

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

# ----------------------- Interface
    
def randNum():
    """
        Retorna um número aleatório para escolher um emoji aleatório para o usuário.
        Mantém o histórico de qual emoji já foi usado, para ser consistente a cada rodada de resposta.
    """
    num = random.randint(0, len(AVATAR_USUARIO) - 1)

    # guardando no contexto da sessão
    st.session_state['emoji_idxList'].append(num)
    st.session_state['emoji_counter'] += 1

    print(f"emoji_idxList: {st.session_state['emoji_idxList']}")
    print(f"emoji_counter: {st.session_state['emoji_counter']}")
    return num

with st.sidebar:
    if st.button("Deletar Conversa"):
        st.session_state.messages = []        
        
        # Limpa chat
        saveChatHistory([])

        # Insere mensagem padrão
        defaultMessage()

        # Reseta os emojis
        st.session_state['emoji_idxList'] = [0]
        st.session_state['emoji_counter'] = 0

# Renderizando as mensagens do chat
for message in st.session_state.messages:
    avatar = AVATAR_USUARIO[st.session_state['emoji_idxList'][st.session_state['emoji_counter']]] if message["role"] == "user" else AVATAR_BOT
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Interface principal do chat | streaming de mensagens
if prompt := st.chat_input("Como posso ajudá-lo?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=AVATAR_USUARIO[st.session_state['emoji_idxList'][st.session_state['emoji_counter']]]):
        if st.session_state.messages:
            randNum()            
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=AVATAR_BOT):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "system", "content": assistant_instructions}] + st.session_state["messages"],
            stream=True,
        ):
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

saveChatHistory(st.session_state.messages)
