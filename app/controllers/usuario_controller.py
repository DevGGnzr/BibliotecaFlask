from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models.models import Usuario
from app.utils.pdf_utils import generate_pdf
from datetime import datetime
import re

@app.route('/usuarios')
def usuarios():
    """Lista todos os usuários"""
    usuarios = Usuario.query.all()
    return render_template('usuarios/usuarios.html', usuarios=usuarios)

@app.route('/create_usuario', methods=['GET', 'POST'])
def create_usuario():
    """Criar um novo usuário"""
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
    
    return render_template('usuarios/create_usuario.html')

@app.route('/update_usuario/<int:id>', methods=['GET', 'POST'])
def update_usuario(id):
    """Atualizar um usuário existente"""
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
    
    return render_template('usuarios/update_usuario.html', usuario=usuario)

@app.route('/delete_usuario/<int:id>')
def delete_usuario(id):
    """Deletar um usuário"""
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

@app.route('/usuarios/pdf')
def usuarios_pdf():
    """Exportar lista de usuários para PDF"""
    usuarios = Usuario.query.all()
    
    context = {
        'usuarios': usuarios,
        'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
        'ano_atual': datetime.now().year
    }
    
    pdf = generate_pdf('usuarios/usuarios_pdf.html', context, filename='relatorio_usuarios.pdf')
    
    if pdf:
        return pdf
    else:
        flash('Erro ao gerar o PDF!', 'danger')
        return redirect(url_for('usuarios'))
