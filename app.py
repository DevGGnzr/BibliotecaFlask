from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from extensions import db
import re
from werkzeug.utils import secure_filename

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuração de upload de imagens
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', 'capas')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max

# Criar pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Inicializa o SQLAlchemy e o Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Importar os modelos
from models import Livro, Usuario, Emprestimo

# Função para verificar extensão de arquivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Página inicial com opções para ir para livros, usuários ou empréstimos
@app.route('/')
def index():
    return render_template('index.html')

# Rotas para Livros
@app.route('/livros')
def livros():
    livros = Livro.query.all()
    return render_template('livros.html', livros=livros)

@app.route('/create_livro', methods=['GET', 'POST'])
def create_livro():
    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        autor = request.form['autor'].strip()
        isbn = request.form['isbn'].strip()
        ano_publicacao = request.form['ano_publicacao'].strip()
        categoria = request.form['categoria'].strip()
        
        # Validações
        if not all([titulo, autor, isbn, ano_publicacao, categoria]):
            flash('Todos os campos obrigatórios devem ser preenchidos!', 'danger')
            return redirect(url_for('create_livro'))
        
        # Validar ISBN (formato básico: 10 ou 13 dígitos, pode ter hífens)
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        if not (isbn_clean.isdigit() and len(isbn_clean) in [10, 13]):
            flash('ISBN inválido! Deve conter 10 ou 13 dígitos.', 'danger')
            return redirect(url_for('create_livro'))
        
        # Validar ano
        try:
            ano = int(ano_publicacao)
            if ano < 1000 or ano > 2100:
                flash('Ano de publicação inválido!', 'danger')
                return redirect(url_for('create_livro'))
        except ValueError:
            flash('Ano de publicação deve ser um número!', 'danger')
            return redirect(url_for('create_livro'))
        
        # Verificar ISBN duplicado
        if Livro.query.filter_by(isbn=isbn).first():
            flash('ISBN já cadastrado!', 'danger')
            return redirect(url_for('create_livro'))
        
        # Processar upload de imagem
        capa_filename = None
        if 'capa' in request.files:
            file = request.files['capa']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Adicionar timestamp para evitar conflitos
                import time
                timestamp = str(int(time.time()))
                name, ext = os.path.splitext(filename)
                capa_filename = f"{name}_{timestamp}{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], capa_filename))
            elif file and file.filename and not allowed_file(file.filename):
                flash('Formato de imagem inválido! Use PNG, JPG ou JPEG.', 'warning')
        
        new_livro = Livro(titulo=titulo, autor=autor, isbn=isbn, 
                         ano_publicacao=ano, categoria=categoria,
                         capa_url=capa_filename)
        db.session.add(new_livro)
        db.session.commit()
        flash(f'Livro "{titulo}" cadastrado com sucesso!', 'success')
        return redirect(url_for('livros'))
    return render_template('create_livro.html')

@app.route('/update_livro/<int:id>', methods=['GET', 'POST'])
def update_livro(id):
    livro = Livro.query.get_or_404(id)
    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        autor = request.form['autor'].strip()
        isbn = request.form['isbn'].strip()
        ano_publicacao = request.form['ano_publicacao'].strip()
        categoria = request.form['categoria'].strip()
        
        # Validações
        if not all([titulo, autor, isbn, ano_publicacao, categoria]):
            flash('Todos os campos obrigatórios devem ser preenchidos!', 'danger')
            return redirect(url_for('update_livro', id=id))
        
        # Validar ISBN
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        if not (isbn_clean.isdigit() and len(isbn_clean) in [10, 13]):
            flash('ISBN inválido! Deve conter 10 ou 13 dígitos.', 'danger')
            return redirect(url_for('update_livro', id=id))
        
        # Validar ano
        try:
            ano = int(ano_publicacao)
            if ano < 1000 or ano > 2100:
                flash('Ano de publicação inválido!', 'danger')
                return redirect(url_for('update_livro', id=id))
        except ValueError:
            flash('Ano de publicação deve ser um número!', 'danger')
            return redirect(url_for('update_livro', id=id))
        
        # Verificar ISBN duplicado (exceto o próprio livro)
        existing = Livro.query.filter_by(isbn=isbn).first()
        if existing and existing.id != id:
            flash('ISBN já cadastrado em outro livro!', 'danger')
            return redirect(url_for('update_livro', id=id))
        
        # Processar upload de nova imagem
        if 'capa' in request.files:
            file = request.files['capa']
            if file and file.filename and allowed_file(file.filename):
                # Deletar imagem antiga se existir
                if livro.capa_url:
                    old_file = os.path.join(app.config['UPLOAD_FOLDER'], livro.capa_url)
                    if os.path.exists(old_file):
                        os.remove(old_file)
                
                # Salvar nova imagem
                filename = secure_filename(file.filename)
                import time
                timestamp = str(int(time.time()))
                name, ext = os.path.splitext(filename)
                capa_filename = f"{name}_{timestamp}{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], capa_filename))
                livro.capa_url = capa_filename
            elif file and file.filename and not allowed_file(file.filename):
                flash('Formato de imagem inválido! Use PNG, JPG ou JPEG.', 'warning')
        
        livro.titulo = titulo
        livro.autor = autor
        livro.isbn = isbn
        livro.ano_publicacao = ano
        livro.categoria = categoria
        db.session.commit()
        flash(f'Livro "{titulo}" atualizado com sucesso!', 'success')
        return redirect(url_for('livros'))
    return render_template('update_livro.html', livro=livro)

@app.route('/delete_livro/<int:id>')
def delete_livro(id):
    livro = Livro.query.get_or_404(id)
    
    # Verificar se o livro está em algum empréstimo
    if livro.emprestimos:
        flash(f'Não é possível excluir o livro "{livro.titulo}" pois ele está vinculado a {len(livro.emprestimos)} empréstimo(s)!', 'danger')
        return redirect(url_for('livros'))
    
    titulo = livro.titulo
    db.session.delete(livro)
    db.session.commit()
    flash(f'Livro "{titulo}" excluído com sucesso!', 'success')
    return redirect(url_for('livros'))

# Rotas para Usuários
@app.route('/usuarios')
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/create_usuario', methods=['GET', 'POST'])
def create_usuario():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()
        
        # Validações
        if not nome or not email:
            flash('Nome e email são obrigatórios!', 'danger')
            return redirect(url_for('create_usuario'))
        
        # Validar formato de email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            flash('Email inválido!', 'danger')
            return redirect(url_for('create_usuario'))
        
        # Verificar email duplicado
        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'danger')
            return redirect(url_for('create_usuario'))
        
        new_usuario = Usuario(nome=nome, email=email)
        db.session.add(new_usuario)
        db.session.commit()
        flash(f'Usuário "{nome}" cadastrado com sucesso!', 'success')
        return redirect(url_for('usuarios'))
    return render_template('create_usuario.html')

@app.route('/update_usuario/<int:id>', methods=['GET', 'POST'])
def update_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()
        
        # Validações
        if not nome or not email:
            flash('Nome e email são obrigatórios!', 'danger')
            return redirect(url_for('update_usuario', id=id))
        
        # Validar formato de email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            flash('Email inválido!', 'danger')
            return redirect(url_for('update_usuario', id=id))
        
        # Verificar email duplicado (exceto o próprio usuário)
        existing = Usuario.query.filter_by(email=email).first()
        if existing and existing.id != id:
            flash('Email já cadastrado em outro usuário!', 'danger')
            return redirect(url_for('update_usuario', id=id))
        
        usuario.nome = nome
        usuario.email = email
        db.session.commit()
        flash(f'Usuário "{nome}" atualizado com sucesso!', 'success')
        return redirect(url_for('usuarios'))
    return render_template('update_usuario.html', usuario=usuario)

@app.route('/delete_usuario/<int:id>')
def delete_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    
    # Verificar se o usuário tem empréstimos
    if usuario.emprestimos:
        flash(f'Não é possível excluir o usuário "{usuario.nome}" pois ele possui {len(usuario.emprestimos)} empréstimo(s) vinculado(s)!', 'danger')
        return redirect(url_for('usuarios'))
    
    nome = usuario.nome
    db.session.delete(usuario)
    db.session.commit()
    flash(f'Usuário "{nome}" excluído com sucesso!', 'success')
    return redirect(url_for('usuarios'))


# Rotas para Empréstimos
@app.route('/emprestimos')
def emprestimos():
    emprestimos = Emprestimo.query.all()
    return render_template('emprestimos.html', emprestimos=emprestimos)

@app.route('/create_emprestimo', methods=['GET', 'POST'])
def create_emprestimo():
    if request.method == 'POST':
        numero_emprestimo = request.form['numero_emprestimo'].strip()
        usuario_id = request.form.get('usuario')
        livro_ids = request.form.getlist('livros')
        
        # Validações
        if not numero_emprestimo:
            flash('Número do empréstimo é obrigatório!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('create_emprestimo.html', usuarios=usuarios, livros=livros)
        
        if not usuario_id:
            flash('Selecione um usuário!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('create_emprestimo.html', usuarios=usuarios, livros=livros)
        
        if not livro_ids:
            flash('Selecione pelo menos um livro!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('create_emprestimo.html', usuarios=usuarios, livros=livros)
        
        # Verificar número duplicado
        if Emprestimo.query.filter_by(numero_emprestimo=numero_emprestimo).first():
            flash('Número de empréstimo já cadastrado!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('create_emprestimo.html', usuarios=usuarios, livros=livros)

        new_emprestimo = Emprestimo(numero_emprestimo=numero_emprestimo, usuario_id=usuario_id)

        # Adicionar os livros selecionados ao empréstimo
        for livro_id in livro_ids:
            livro = Livro.query.get(livro_id)
            if livro:
                new_emprestimo.livros.append(livro)

        db.session.add(new_emprestimo)
        db.session.commit()
        flash(f'Empréstimo "{numero_emprestimo}" cadastrado com sucesso!', 'success')
        return redirect(url_for('emprestimos'))

    usuarios = Usuario.query.all()
    livros = Livro.query.all()
    return render_template('create_emprestimo.html', usuarios=usuarios, livros=livros)

@app.route('/update_emprestimo/<int:id>', methods=['GET', 'POST'])
def update_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)

    if request.method == 'POST':
        numero_emprestimo = request.form['numero_emprestimo'].strip()
        usuario_id = request.form.get('usuario')
        livro_ids = request.form.getlist('livros')
        
        # Validações
        if not numero_emprestimo:
            flash('Número do empréstimo é obrigatório!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('update_emprestimo.html', emprestimo=emprestimo, usuarios=usuarios, livros=livros)
        
        if not usuario_id:
            flash('Selecione um usuário!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('update_emprestimo.html', emprestimo=emprestimo, usuarios=usuarios, livros=livros)
        
        if not livro_ids:
            flash('Selecione pelo menos um livro!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('update_emprestimo.html', emprestimo=emprestimo, usuarios=usuarios, livros=livros)
        
        # Verificar número duplicado (exceto o próprio empréstimo)
        existing = Emprestimo.query.filter_by(numero_emprestimo=numero_emprestimo).first()
        if existing and existing.id != id:
            flash('Número de empréstimo já cadastrado!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('update_emprestimo.html', emprestimo=emprestimo, usuarios=usuarios, livros=livros)
        
        emprestimo.numero_emprestimo = numero_emprestimo
        emprestimo.usuario_id = usuario_id
        
        # Atualizar livros do empréstimo
        emprestimo.livros = []
        for livro_id in livro_ids:
            livro = Livro.query.get(livro_id)
            if livro:
                emprestimo.livros.append(livro)

        db.session.commit()
        flash(f'Empréstimo "{numero_emprestimo}" atualizado com sucesso!', 'success')
        return redirect(url_for('emprestimos'))

    usuarios = Usuario.query.all()
    livros = Livro.query.all()
    return render_template('update_emprestimo.html', emprestimo=emprestimo, usuarios=usuarios, livros=livros)

@app.route('/delete_emprestimo/<int:id>')
def delete_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    numero = emprestimo.numero_emprestimo
    db.session.delete(emprestimo)
    db.session.commit()
    flash(f'Empréstimo "{numero}" excluído com sucesso!', 'success')
    return redirect(url_for('emprestimos'))

if __name__ == '__main__':
    app.run(debug=True)
