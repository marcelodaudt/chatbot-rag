# Chatbot with R.A.G.

This application was developed for semantic searches in vector databases.

An intelligent assistant with R.A.G. was also developed.

**R.A.G.** (Retrieval Augmented Generation)

## Features:

- **Python** (programming language)
- **Pinecone** (vector database)
- **OpenAI** (embedding and responses)

---

## CRIAR E ATIVAR O AMBIENTE PYTHON
```bash
python -m venv venv
source venv/bin/activate
```

## INSTALAR OpenAI
```bash
pip install openai
```

## INSTALAR O Pinecone
```bash
pip install "pinecone[grpc]"
```

## INSTALAR python-dotenv PARA PODER ACESSAR AS VARIÁVEIS DO ARQUIVO .env
```bash
pip install python-dotenv
```

## INSTALAR fastapi E O uvicorn -> transforma a aplicação em um site
```bash
pip install fastapi uvicorn
```

### INSTALAR PyPDF2 PARA CONVERTER PDF PARA TEXTO
```bash
pip install PyPDF2
pip install python-multipart
```

### ATUALIZAR OS REQUISITOS
```bash
$ pip freeze > requirements.txt
```
