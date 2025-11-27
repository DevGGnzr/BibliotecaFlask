from app import db
from datetime import datetime

class Livro(db.Model):
    __tablename__ = 'livros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    capa_dados = db.Column(db.LargeBinary, nullable=True)
    capa_tipo = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Livro {self.titulo}>'

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

# Tabela associativa para a relação muitos-para-muitos entre empréstimos e livros
emprestimo_livro = db.Table('emprestimo_livro',
    db.Column('emprestimo_id', db.Integer, db.ForeignKey('emprestimos.id'), primary_key=True),
    db.Column('livro_id', db.Integer, db.ForeignKey('livros.id'), primary_key=True)
)

class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_emprestimo = db.Column(db.String(50), nullable=False, unique=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_emprestimo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_devolucao = db.Column(db.Date, nullable=False)
    
    # Relacionamento muitos-para-um com usuários
    usuario = db.relationship('Usuario', backref='emprestimos')
    
    # Relacionamento muitos-para-muitos com livros
    livros = db.relationship('Livro', secondary='emprestimo_livro', backref='emprestimos')

    def __repr__(self):
        return f'<Emprestimo {self.numero_emprestimo}>'
