# Media Streaming API (Backend)

Backend de uma plataforma de streaming inspirado em serviços como Netflix.  
A API permite gerenciamento de usuários, catálogo de mídias e reprodução de vídeos com autenticação JWT.

---

# Tecnologias

- Python 3.14+
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-CORS
- SQLite
- python-dotenv

---

# Pré-requisitos

Antes de iniciar, instale:

- Python 3.14 ou superior

Download:  
https://www.python.org/downloads/

Durante a instalação marque:

Add Python to PATH

Verifique a instalação:

```
python --version
```
Instalação

Clone o projeto e instale as dependências.

1. Criar ambiente virtual
```
python -m venv venv
```
3. Ativar ambiente virtual
```
venv\Scripts\activate
```
3. Instalar dependências
```
pip install -r requirements.txt
```
 Configuração

Crie um arquivo .env na pasta backend.

No arquivo `.env`, ajuste o caminho do banco SQLite conforme seu sistema:

Exemplo:
```
SECRET_KEY=super_secret_key
DATABASE_URL=sqlite:///C:/caminho/para/seu/projeto/backend/database.db
```
 Testes da API

Para testar os endpoints recomenda-se utilizar:

 - Postman
