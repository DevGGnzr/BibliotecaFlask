from flask import render_template, request, redirect, url_for, flash, send_file, abort
from app import app, db
from app.models.models import Livro
from app.utils.pdf_utils import generate_pdf
from datetime import datetime
import io

# Função para verificar extensão de arquivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/livros')
def livros():
    """Lista todos os livros"""
    livros = Livro.query.all()
    return render_template('livros/livros.html', livros=livros)

@app.route('/create_livro', methods=['GET', 'POST'])
def create_livro():
    """Criar um novo livro"""
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
        capa_dados = None
        capa_tipo = None
        if 'capa' in request.files:
            file = request.files['capa']
            if file and file.filename and allowed_file(file.filename):
                capa_dados = file.read()
                capa_tipo = file.mimetype
            elif file and file.filename and not allowed_file(file.filename):
                flash('Formato de imagem inválido! Use PNG, JPG ou JPEG.', 'warning')
        
        new_livro = Livro(titulo=titulo, autor=autor, isbn=isbn, 
                         ano_publicacao=ano, categoria=categoria,
                         capa_dados=capa_dados, capa_tipo=capa_tipo)
        db.session.add(new_livro)
        db.session.commit()
        flash(f'Livro "{titulo}" cadastrado com sucesso!', 'success')
        return redirect(url_for('livros'))
    
    return render_template('livros/create_livro.html')

@app.route('/update_livro/<int:id>', methods=['GET', 'POST'])
def update_livro(id):
    """Atualizar um livro existente"""
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
                livro.capa_dados = file.read()
                livro.capa_tipo = file.mimetype
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
    
    return render_template('livros/update_livro.html', livro=livro)

@app.route('/capa_livro/<int:id>')
def capa_livro(id):
    livro=Livro.query.get_or_404(id)
    if livro.capa_dados and livro.capa_tipo:
        return send_file(
            io.BytesIO(livro.capa_dados),
            mimetype=livro.capa_tipo,
    )
    else:
        abort(404)
@app.route('/livros/pdf')
def livros_pdf():
    """Exportar lista de livros para PDF"""
    livros = Livro.query.all()
    
    context = {
        'livros': livros,
        'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
        'ano_atual': datetime.now().year
    }
    
    pdf = generate_pdf('livros/livros_pdf.html', context, filename='relatorio_livros.pdf')
    
    if pdf:
        return pdf
    else:
        flash('Erro ao gerar o PDF!', 'danger')
        return redirect(url_for('livros'))

@app.route('/delete_livro/<int:id>')
def delete_livro(id):
    """Deletar um livro"""
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
