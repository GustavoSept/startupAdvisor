# Mestre Supremo das Ideias de Startup
Este projeto é uma demo de aplicação construída com Streamlit e a API da OpenAI, projetada para gerar ideias inovadoras de startups com uma interação divertida com o usuário.

A IA foi programada para fazer perguntas ao usuário (temática, escala, orçamento, etc) antes de dar a sugestão de ideias.

## Manual de Uso

### Pré-Requisitos

1. **Instalar Python**: Certifique-se de ter Python instalado em sua máquina. Se não, você pode baixá-lo em [python.org](https://www.python.org/downloads/).
2. **Obter uma API Key da OpenAI**: Você precisará de uma chave de API da OpenAI para interagir com a GPT-3.5. Registre-se ou faça login em [openai.com](https://openai.com/), e siga as instruções para criar uma chave de API.

### Configuração do Projeto

1. **Clone o Repositório ou Baixe o Projeto**: Faça o download dos arquivos do projeto para a sua máquina local.
2. **Crie e Ative um Ambiente Virtual**:
    ```bash
    python -m venv env_aistartup
    source env_aistartup/bin/activate  # No Linux ou macOS
    env_aistartup\Scripts\activate  # No Windows
    ```
3. **Instale as Dependências**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Configure a Chave de API da OpenAI**:
    - Crie um arquivo `.env` no diretório raiz do projeto.
    - Adicione sua chave de API da OpenAI ao arquivo como mostrado abaixo:
        ```plaintext
        OPENAI_API_KEY="sk-iiKGd[...]JAyUJ"
        ```
    
### Executando a Aplicação

1. **Inicie a Aplicação com Streamlit**:
    ```bash
    streamlit run app.py
    ```
2. **Interagir com a Aplicação**: Após iniciar a aplicação, o Streamlit abrirá uma janela no navegador onde você pode interagir com o assistente virtual para gerar ideias de startups.

### Notas Adicionais

- Para **deletar a conversa** e reiniciar, utilize o botão "Deletar Conversa" disponível na barra lateral da aplicação.
- Os **emojis do usuário** mudam aleatoriamente a cada interação para adicionar um toque lúdico à conversa.

## Documentação

 O projeto é estruturado da seguinte forma:

- `app.py`: O arquivo principal que contém a lógica da aplicação, incluindo a interface do usuário Streamlit, integração com a API OpenAI, e gerenciamento de histórico de conversas.
- `chat_history.bak`, `chat_history.dat`, `chat_history.dir`: Arquivos utilizados para armazenar o histórico de conversas do usuário com o assistente virtual, permitindo persistência entre sessões.
- `.env`: Um arquivo no diretório raiz contendo a chave de API da OpenAI necessária para a autenticação e a realização de chamadas à API.

### Como Funciona

1. **Inicialização e Gerenciamento de Estado com Streamlit**: A aplicação utiliza o Streamlit para criar uma interface de usuário interativa. O estado da sessão é gerenciado para armazenar o modelo OpenAI selecionado, o histórico de mensagens e o estado dos emojis.
2. **Integração com a API OpenAI**: Utiliza-se a API OpenAI para gerar respostas com base nas instruções definidas e no histórico de conversas. O modelo `gpt-3.5-turbo-16k` é utilizado para gerar ideias de startups inovadoras.
3. **Gerenciamento de Histórico de Conversas**: As conversas são armazenadas e recuperadas usando o módulo `shelve`, permitindo persistência e continuidade das conversas entre as sessões.
