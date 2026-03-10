# Media Streaming API (Backend)


Projeto backend simulando uma plataforma de streaming 

# Tecnologias

- Python 3.14+
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-CORS
- SQLite 
- python-dotenv


# Pré-requisitos

## 1. Instalar Python
Baixe em:  
https://www.python.org/downloads/

Durante a instalação marque:  
 Add Python to PATH  

Verifique:

  bash
python --version

# Criar Ambiente Virtual (venv)

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

# Criar arquivo .env

Crie um arquivo .env na pasta backend:

SECRET_KEY=super_secret_key
DATABASE_URL=sqlite:///database.db

# Autenticação

A API utiliza JWT Token.

Fluxo:
    1. Registrar usuário
    2. Fazer login
    3. usar token nas rotas protegidas

# Funcionalidades

 - Registro e Login de usuários
 - CRUD de Filmes
 - CRUD de Séries
 - CRUD de Episódios
 - Histórico de progresso 
 - Favoritos (em progresso)

# Testes

Recomendado usar:
 - Postman
