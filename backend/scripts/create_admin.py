from database.db_connection import db
from models.tabelas import Usuario
from app import app



import sys

if len(sys.argv) < 2:
    print("Use: python -m backend.scripts.create_admin email@exemplo.com")
    exit()

EMAIL_ADMIN = sys.argv[1].lower()


with app.app_context():
    # garante que as tabelas existem
    #db.create_all()

    user = Usuario.query.filter_by(email=EMAIL_ADMIN).first()

    if not user:
        print("Usuário não encontrado. Cadastre o usuário antes.")
        exit()

    if user.role == "admin":
        print("Usuário já é admin.")
        exit()

    user.role = "admin"
    db.session.commit()

    print("Usuário promovido a admin com sucesso!")


