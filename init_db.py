"""Script para inicializar o banco de dados"""
from app import app, db

with app.app_context():
    # Cria todas as tabelas
    db.create_all()
    print("✅ Banco de dados criado com sucesso!")
    print("✅ Todas as tabelas foram criadas!")
