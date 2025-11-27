from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models.models import Emprestimo, Usuario, Livro
from app.utils.pdf_utils import generate_pdf
from datetime import datetime

@app.route('/')
def index():
    """Página inicial com opções para ir para livros, usuários ou empréstimos"""
    return render_template('index.html')

@app.route('/emprestimos')
def emprestimos():
    """Lista todos os empréstimos"""
    emprestimos = Emprestimo.query.all()
    return render_template('emprestimos/emprestimos.html', emprestimos=emprestimos)

@app.route('/create_emprestimo', methods=['GET', 'POST'])
def create_emprestimo():
    """Criar um novo empréstimo"""
    if request.method == 'POST':
        numero_emprestimo = request.form['numero_emprestimo'].strip()
        usuario_id = request.form.get('usuario')
        livro_ids = request.form.getlist('livros')
        
        # Validações
        if not numero_emprestimo:
            flash('Número do empréstimo é obrigatório!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('emprestimos/create_emprestimo.html', usuarios=usuarios, livros=livros)
        
        if not usuario_id:
            flash('Selecione um usuário!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('emprestimos/create_emprestimo.html', usuarios=usuarios, livros=livros)
        
        if not livro_ids:
            flash('Selecione pelo menos um livro!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('emprestimos/create_emprestimo.html', usuarios=usuarios, livros=livros)
        
        # Verificar número duplicado
        if Emprestimo.query.filter_by(numero_emprestimo=numero_emprestimo).first():
            flash('Número de empréstimo já cadastrado!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('emprestimos/create_emprestimo.html', usuarios=usuarios, livros=livros)

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
    return render_template('emprestimos/create_emprestimo.html', usuarios=usuarios, livros=livros)

@app.route('/update_emprestimo/<int:id>', methods=['GET', 'POST'])
def update_emprestimo(id):
    """Atualizar um empréstimo existente"""
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
            return render_template('emprestimos/update_emprestimo.html', emprestimo=emprestimo, usuarios=usuarios, livros=livros)
        
        if not usuario_id:
            flash('Selecione um usuário!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('emprestimos/update_emprestimo.html', emprestimo=emprestimo, usuarios=usuarios, livros=livros)
        
        if not livro_ids:
            flash('Selecione pelo menos um livro!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('emprestimos/update_emprestimo.html', emprestimo=emprestimo, usuarios=usuarios, livros=livros)
        
        # Verificar número duplicado (exceto o próprio empréstimo)
        existing = Emprestimo.query.filter_by(numero_emprestimo=numero_emprestimo).first()
        if existing and existing.id != id:
            flash('Número de empréstimo já cadastrado!', 'danger')
            usuarios = Usuario.query.all()
            livros = Livro.query.all()
            return render_template('emprestimos/update_emprestimo.html', emprestimo=emprestimo, usuarios=usuarios, livros=livros)
        
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
    return render_template('emprestimos/update_emprestimo.html', emprestimo=emprestimo, usuarios=usuarios, livros=livros)

@app.route('/delete_emprestimo/<int:id>')
def delete_emprestimo(id):
    """Deletar um empréstimo"""
    emprestimo = Emprestimo.query.get_or_404(id)
    numero = emprestimo.numero_emprestimo
    db.session.delete(emprestimo)
    db.session.commit()
    flash(f'Empréstimo "{numero}" excluído com sucesso!', 'success')
    return redirect(url_for('emprestimos'))

@app.route('/emprestimos/pdf')
def emprestimos_pdf():
    """Exportar lista de empréstimos para PDF"""
    emprestimos = Emprestimo.query.all()
    
    context = {
        'emprestimos': emprestimos,
        'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
        'ano_atual': datetime.now().year
    }
    
    pdf = generate_pdf('emprestimos/emprestimos_pdf.html', context, filename='relatorio_emprestimos.pdf')
    
    if pdf:
        return pdf
    else:
        flash('Erro ao gerar o PDF!', 'danger')
        return redirect(url_for('emprestimos'))
