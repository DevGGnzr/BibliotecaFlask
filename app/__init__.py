from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os

# Inicializa as extensões
db = SQLAlchemy()
migrate = Migrate()

# Cria a instância da aplicação
app = Flask(__name__)
app.config.from_object(Config)

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializa as extensões com a aplicação
db.init_app(app)
migrate.init_app(app, db)

# Importa os modelos e controllers
from app.models import models
from app.controllers import livro_controller, usuario_controller, emprestimo_controller
