import time
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
import gradio as gr
from scripts.read_or_create_assistant import read_or_create_assistant
import os

def generate_startup_idea(theme, sector, scale, emotion, budget):
    """
    Generates a creative startup idea based on user inputs.
    """
    load_dotenv()
    client = OpenAI()  # Automatically uses OPENAI_API_KEY from .env
    assistant_id = read_or_create_assistant() # reusa ou cria um assistente
    
    if not assistant_id:
        return "Não foi possível criar ou reutilizar um assistente. Tente novamente."
    
    thread = client.beta.threads.create()
    message_content = f"Tema: {theme}, Setor: {sector}, Escala: {scale}, Emoção: {emotion}, Orçamento: {budget}."
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message_content
    )
    
    # de fato processando o input do usuário
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    
    print("Run Object:", run, "\n")
    
    # Espera a API retornar sucesso/falha
    run_status = run.status
    while run_status not in ["completed", "failed"]:
        time.sleep(1.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        run_status = run.status

    # Seleciona a conversa toda
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    
    print("Messages Object:", messages, "\n")
    
    # retorna a última resposta (primeiro item)
    if messages.data:
        latest_message = messages.data[0]
        response_content = latest_message.content[0].text.value
        return response_content
    else:
        return "Não consegui gerar uma ideia agora. Tente novamente."

# Interface Gradio
iface = gr.Interface(
    fn=generate_startup_idea,
    inputs=[
        gr.Textbox(label="Tema: Qual o assunto da startup?"),
        gr.Textbox(label="Setor: Onde você espera operá-la?"),
        gr.Textbox(label="Escala: Quantas pessoas espera impactar? [indivíduo, cidade, país, global]"),
        gr.Textbox(label="Emoção: Como quer tocar o coração das pessoas?"),
        gr.Textbox(label="Orçamento: baixo, alto, infinito?")
    ],
    outputs=gr.Textbox(label="Creative Startup Idea"),
    title="Gerador criativo de Startups",
    description="Esta ferramenta ajuda você a gerar ideias criativas de startups com base em suas contribuições. Preencha os detalhes abaixo para começar!"
)

if __name__ == "__main__":
    iface.launch()
