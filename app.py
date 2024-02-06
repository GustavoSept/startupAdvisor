from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os, shelve, random

load_dotenv()

st.title("Mestre Supremo das Ideias de Startup")

AVATAR_USUARIO = ["🙂","🙂","🙂","🙂","🙂","🙂","🙂","🙂", "😲", "🤔", "🫣", "🤗", "😖", "😌", "🤫"]
AVATAR_BOT = "🥸"

# guarda o estado dos emojis
state_dir = './state/'
if not os.path.exists(state_dir):
    os.makedirs(state_dir)

emoji_mapping_file = os.path.join(state_dir, 'emoji_mapping.txt')
if not os.path.exists(emoji_mapping_file):
    with open(emoji_mapping_file, 'w') as f:
        f.write("0\n")

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
        Retorna um número aleatório para escolher um emoji para o usuário.
    """
    
    return random.randint(0, len(AVATAR_USUARIO) - 1)

def loadEmojiMapping():
    try:
        with open('./state/emoji_mapping.txt', 'r') as file:
            mapping = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        mapping = []
    return mapping

def appendToEmojiMapping(num):
    with open('./state/emoji_mapping.txt', 'a') as file:
        file.write(f"{num}\n")
        file.write(f"0\n")

emoji_mapping = loadEmojiMapping()
print(emoji_mapping)

def assignEmojiForNewMessage():
    new_emoji_index = randNum()
    emoji_mapping.append(new_emoji_index)
    appendToEmojiMapping(new_emoji_index)
    return new_emoji_index

with st.sidebar:
    if st.button("Deletar Conversa"):
        st.session_state.messages = []        
        
        # Limpa chat
        saveChatHistory([])

        # Insere mensagem padrão
        defaultMessage()

        # Reseta os emojis
        emoji_mapping = []
        with open(emoji_mapping_file, 'w') as f:
            f.write("0\n")

# Renderizando as mensagens do chat
for idx, message in enumerate(st.session_state.messages):
    print(f"idx: {idx}")
    print(f"message: {message['role']}\n")
    if message['role'] == 'user':
        avatar = AVATAR_USUARIO[emoji_mapping[idx]]
    else:
        avatar = AVATAR_BOT
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# Interface principal do chat | streaming de mensagens
if prompt := st.chat_input("Como posso ajudá-lo?"):
    assignEmojiForNewMessage()
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    saveChatHistory(st.session_state.messages)
    
    # lógica de streaming
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

    # força um update da interface, pra mostrar a mensagem do usuário
    st.experimental_rerun()