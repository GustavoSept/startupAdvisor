from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
import os

def read_or_create_assistant():
    """
        Cria assistente novo se ele já não existe
    """
    assist_file_path = "./assistant"
    
    if os.path.isfile(assist_file_path):
        with open(assist_file_path, 'r') as file:
            content = file.read().strip()
            if content.startswith("asst_"):
                print("Assistente já existe. Pulando o script.")
                return content


    load_dotenv()
    client = OpenAI()  # por default, pega OPENAI_API_KEY do .env
    model = "gpt-3.5-turbo-16k"

    assistant = client.beta.assistants.create(
        name="Especialista em Startups Criativas",
        instructions=
        """
            Você é um assistente criativo especialista em ter ideias de startups inovadoras.
            Você responde de forma sucinta e engraçada, sempre tentando dar ideias mirabolantes e fora do senso comum para a criação de uma startup.
            Comece fazendo perguntas ao usuário: qual a temática da startup? Em seguida pergunte em qual segmento a startup irá atuar,
            qual a escala de impacto do projeto (pessoal, cidade, país, global), qual emoção a startup deve provocar nas pessoas, e finalmente,
            qual o orçamento para botar a ideia de pé?
            Depois de coletar essas informações do usuário, prossiga em dar uma ideia criativa de startup.
        """,
        model=model
    )

    with open(assist_file_path, 'w') as file:
        file.write(f"{assistant.id}")
        print(f"Assistente criado e ID salvo: {assistant.id}")
        return assistant.id

if __name__ == "__main__":
    read_or_create_assistant()