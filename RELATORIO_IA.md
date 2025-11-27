# RELATÓRIO DE USO DE INTELIGÊNCIA ARTIFICIAL

**Projeto:** Sistema de Biblioteca Digital  
**Alunos:** Gilberto, Victoria  
**Instituição:** IFRS - Campus Veranópolis  
**Disciplina:** Desenvolvimento Web II  
**Professor:** Jorge Arthur Schneider Aranda  
**Data:** Novembro/2025

---

## PROMPT 1: Estrutura de Projeto Flask com Padrão MVC

**Pergunta:**
> "Como organizar um projeto Flask seguindo o padrão arquitetural MVC (Model-View-Controller)?"

**Resposta da IA:**
A IA apresentou duas abordagens principais para organizar um projeto Flask em MVC:

**Opção 1: Estrutura com Flask Blueprints**
- Criar blueprints separados para cada módulo (livros, usuários, empréstimos)
- Cada blueprint teria seus próprios arquivos de rotas
- Maior modularidade e isolamento entre componentes
- Ideal para projetos grandes com múltiplas equipes

**Opção 2: Estrutura MVC simplificada**
- Separar Models, Controllers e Views em pastas distintas
- Controllers importam o objeto `app` diretamente
- Menos arquivos de configuração
- Mais direto para projetos pequenos/médios

A IA também explicou a necessidade de arquivos `__init__.py` e sugeriu organizar templates em subpastas por módulo.

**Análise Crítica:**
Avaliei ambas as opções considerando o escopo do projeto acadêmico. **Optei pela Opção 2 (estrutura simplificada)** porque:

1. **Escopo adequado:** Projeto tem apenas 3 entidades, Blueprints seria over-engineering
2. **Clareza didática:** Estrutura mais simples facilita entendimento do padrão MVC
3. **Manutenção:** Menos arquivos de configuração para gerenciar
4. **Tempo de desenvolvimento:** Mais rápido para implementar e testar

A única adaptação necessária foi garantir que cada controller importasse `app` e `db` do `__init__.py` para registrar as rotas. Também criei `__init__.py` vazios em `models/` e `controllers/` para torná-los pacotes Python válidos.

**Aplicação no Projeto:**
Estrutura criada conforme abaixo:
- `app/__init__.py` - Inicialização do Flask, SQLAlchemy e Migrate
- `app/models/models.py` - Classes Livro, Usuario e Emprestimo
- `app/controllers/livro_controller.py` - Rotas CRUD de livros
- `app/controllers/usuario_controller.py` - Rotas CRUD de usuários
- `app/controllers/emprestimo_controller.py` - Rotas CRUD de empréstimos
- `app/templates/` - Templates organizados em subpastas por entidade

---

## PROMPT 2: Relacionamento Muitos-para-Muitos no SQLAlchemy

**Pergunta:**
> "Como implementar um relacionamento N:N (muitos-para-muitos) entre duas entidades no SQLAlchemy? Preciso que um empréstimo possa ter vários livros e um livro possa estar em vários empréstimos."

**Resposta da IA:**
A IA apresentou duas formas de implementar relacionamento N:N no SQLAlchemy:

**Opção 1: Tabela Associativa Simples com db.Table()**
- Usar `db.Table()` para criar tabela de junção
- Apenas duas colunas: chaves estrangeiras que formam chave primária composta
- Mais simples e direta
- Não permite adicionar campos extras na tabela associativa

**Opção 2: Classe Model para Tabela Associativa**
- Criar uma classe Model completa para a tabela de junção
- Permite adicionar campos extras (ex: data de associação, quantidade)
- Mais flexível para evoluções futuras
- Requer mais código de configuração

A IA explicou que `db.relationship()` com parâmetro `secondary` cria o relacionamento bidirecional, e o `backref` gera automaticamente o acesso reverso.

**Análise Crítica:**
Para o sistema de biblioteca, **escolhi a Opção 1 (db.Table simples)** porque:

1. **Requisitos suficientes:** Não preciso armazenar dados adicionais na associação (como quantidade ou data)
2. **Simplicidade:** Menos código para manter e testar
3. **Performance:** Tabelas mais leves sem overhead de ORM completo
4. **Escopo do projeto:** Requisito acadêmico é apenas demonstrar o relacionamento N:N

Caso futuro: Se precisasse adicionar "data de devolução" ou "quantidade de renovações" por livro no empréstimo, aí sim migraria para a Opção 2. O código funcionou perfeitamente: `emprestimo.livros.append(livro)` adiciona automaticamente na tabela associativa.

**Aplicação no Projeto:**
No arquivo `app/models/models.py`:
```python
emprestimo_livro = db.Table('emprestimo_livro',
    db.Column('emprestimo_id', db.Integer, db.ForeignKey('emprestimos.id'), primary_key=True),
    db.Column('livro_id', db.Integer, db.ForeignKey('livros.id'), primary_key=True)
)

class Emprestimo(db.Model):
    # ... outros campos
    livros = db.relationship('Livro', secondary='emprestimo_livro', backref='emprestimos')
```

---

## PROMPT 3: Validação de ISBN com Expressão Regular

**Pergunta:**
> "Como validar o formato de ISBN (International Standard Book Number) em Python? Preciso aceitar tanto ISBN-10 quanto ISBN-13."

**Resposta da IA:**
A IA apresentou três abordagens para validação de ISBN:

**Opção 1: Validação Simples de Formato (Regex)**
- Verificar se contém 10 ou 13 dígitos
- Permitir hífens opcionais: `978-3-16-148410-0`
- Regex: remover hífens/espaços e checar `len() in [10, 13]`
- Rápida mas não valida dígito verificador

**Opção 2: Validação Completa com Dígito Verificador**
- Calcular dígito verificador usando algoritmo oficial
- ISBN-10: multiplicadores 10, 9, 8... módulo 11
- ISBN-13: multiplicadores 1, 3, 1, 3... módulo 10
- Garante ISBN matematicamente válido

**Opção 3: Biblioteca Especializada (python-isbn)**
- Usar biblioteca `isbnlib` ou `python-stdnum`
- Validação completa + formatação + metadados
- Pode buscar informações do livro online
- Requer dependência adicional

A IA explicou que Opção 1 é suficiente para interface, Opção 2 para sistemas críticos, Opção 3 para recursos avançados.

**Análise Crítica:**
**Escolhi Opção 1 (validação simples de formato)** pelos seguintes motivos:

1. **Escopo do projeto:** Sistema acadêmico, não é livraria comercial
2. **Experiência do usuário:** Validar apenas formato evita erros de digitação óbvios
3. **Sem dependências extras:** Apenas regex nativa do Python
4. **Performance:** Validação instantânea sem cálculos complexos
5. **Praticidade:** ISBN vem de fonte confiável (do livro físico), não precisa verificar matemática

**Trade-offs Conscientes:**
- ✅ **Aceita:** Bibliotecário digitou ISBN correto mas com erro de dígito verificador → Sistema aceita (problema na fonte)
- ❌ **Rejeita:** Bibliotecário digitou letras, menos de 10 dígitos, ou formato inválido → Sistema bloqueia

**Implementação:**
```python
isbn_clean = isbn.replace('-', '').replace(' ', '')
if not (isbn_clean.isdigit() and len(isbn_clean) in [10, 13]):
    flash('ISBN inválido! Deve conter 10 ou 13 dígitos.', 'danger')
    return redirect(url_for('create_livro'))
```

**Exemplos de Validação:**
- ✅ `978-0-306-40615-7` → Remove hífens → `9780306406157` (13 dígitos) → **Válido**
- ✅ `0306406152` → 10 dígitos → **Válido**
- ❌ `978-abc-123` → Contém letras → **Inválido**
- ❌ `12345` → Apenas 5 dígitos → **Inválido**

Em produção com integração a APIs de editoras, migraria para Opção 2 ou 3. Para o contexto acadêmico de biblioteca escolar, validação de formato é suficiente e evita complexidade desnecessária.

**Aplicação no Projeto:**
No `livro_controller.py`:
```python
# Validação de ISBN
isbn_clean = isbn.replace('-', '').replace(' ', '')
if not (isbn_clean.isdigit() and len(isbn_clean) in [10, 13]):
    flash('ISBN inválido! Deve conter 10 ou 13 dígitos.', 'danger')
    return redirect(url_for('create_livro'))
```

---

## PROMPT 4: Validação de Email com Expressão Regular em Python

**Pergunta:**
> "Como validar se um email tem formato válido em Python usando expressão regular (regex)?"

**Resposta da IA:**
A IA apresentou três abordagens para validação de email:

**Opção 1: Regex Simples**
- Padrão: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Valida formato básico
- Rápida e sem dependências externas
- Não cobre 100% dos casos da RFC 5322

**Opção 2: Biblioteca email-validator**
- Validação mais robusta e completa
- Segue padrões RFC rigorosamente
- Verifica DNS do domínio (opcional)
- Requer instalação de pacote adicional

**Opção 3: Enviar email de confirmação**
- Método mais confiável na prática
- Valida que email realmente existe e está acessível
- Requer configuração de SMTP
- Melhor para sistemas em produção

A IA explicou cada parte da regex: caracteres permitidos antes do @, domínio, e extensão com mínimo 2 letras.

**Análise Crítica:**
**Optei pela Opção 1 (regex simples)** porque:

1. **Escopo acadêmico:** Não preciso validação 100% conforme RFC 5322
2. **Sem dependências extras:** Evita adicionar biblioteca apenas para isso
3. **Performance:** Regex é instantânea, sem consultas DNS
4. **Suficiente para o caso:** Previne erros de digitação óbvios (falta @, sem domínio, etc.)

Pesquisei e descobri que validar email perfeitamente com regex é praticamente impossível - a RFC permite caracteres especiais e casos bizarros que ninguém usa na prática. Para um sistema real em produção, eu usaria a Opção 3 (email de confirmação) como padrão da indústria. Mas para validação básica de formulário, a regex simples é adequada e já pega 99% dos erros comuns.

**Aplicação no Projeto:**
No `usuario_controller.py`:
```python
import re

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
if not re.match(email_regex, email):
    flash('Email inválido!', 'danger')
    return redirect(url_for('create_usuario'))
```

---

## PROMPT 5: Proteção de Integridade Referencial na Exclusão

**Pergunta:**
> "Como impedir que um usuário seja excluído se ele tiver empréstimos vinculados? Quero proteger a integridade referencial do banco de dados."

**Resposta da IA:**
A IA apresentou três abordagens para proteger integridade referencial:

**Opção 1: Constraint no Banco de Dados**
- Configurar `ondelete='RESTRICT'` na ForeignKey do SQLAlchemy
- Banco bloqueia automaticamente a exclusão
- Gera exceção que precisa ser tratada
- Mais próximo da camada de dados

**Opção 2: Validação Manual no Controller**
- Verificar `if usuario.emprestimos` antes de deletar
- Exibir mensagem de erro personalizada
- Maior controle sobre feedback ao usuário
- Lógica explícita no código Python

**Opção 3: Soft Delete (Exclusão Lógica)**
- Adicionar campo `ativo` ou `deletado_em`
- Marcar como inativo em vez de deletar
- Mantém histórico completo
- Permite "desfazer" exclusões

A IA recomendou a Opção 1 como mais robusta, mas mencionou que qualquer uma funciona.

**Análise Crítica:**
**Escolhi a Opção 2 (validação manual)** pelos seguintes motivos:

1. **UX melhor:** Posso mostrar mensagem amigável como "Não é possível excluir o usuário 'João' pois ele possui 3 empréstimo(s) vinculado(s)!" em vez de erro genérico de SQL
2. **Informação útil:** Mostro quantos empréstimos estão bloqueando a exclusão
3. **Código explícito:** Fica claro no controller o que está acontecendo, facilitando manutenção
4. **Consistência:** Mantenho toda lógica de negócio na camada de controller

A Opção 1 seria mais segura contra bugs, mas geraria exceções SQLAlchemy que precisariam de try/except genéricos. A Opção 3 seria ideal para auditoria, mas adiciona complexidade desnecessária ao escopo acadêmico. Apliquei o mesmo padrão para livros (bloquear se estiver em empréstimos).

**Aplicação no Projeto:**
No `usuario_controller.py`:
```python
@app.route('/delete_usuario/<int:id>')
def delete_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    
    if usuario.emprestimos:
        flash(f'Não é possível excluir o usuário "{usuario.nome}" pois ele possui {len(usuario.emprestimos)} empréstimo(s) vinculado(s)!', 'danger')
        return redirect(url_for('usuarios'))
    
    db.session.delete(usuario)
    db.session.commit()
```

---

## PROMPT 6: Template Base com Herança no Jinja2

**Pergunta:**
> "Como criar um template base no Flask/Jinja2 para reaproveitar navbar, footer e mensagens flash em todas as páginas?"

**Resposta da IA:**
A IA apresentou duas formas de organizar templates com herança:

**Opção 1: Template Base com Blocos Básicos**
- Criar `base.html` com `{% block content %}`
- Templates filhos estendem e preenchem o bloco
- Estrutura simples e direta
- Suficiente para maioria dos casos

**Opção 2: Template Base com Múltiplos Blocos**
- Além de `content`, criar blocos extras: `extra_css`, `extra_js`, `title`
- Permite customização mais granular por página
- Páginas específicas podem adicionar scripts/estilos próprios
- Mais flexível mas ligeiramente mais complexo

A IA explicou o sistema de `{% extends %}` e `{% block %}`, e como usar `get_flashed_messages(with_categories=true)` para exibir mensagens coloridas.

**Análise Crítica:**
**Optei pela Opção 2 (múltiplos blocos)** porque oferece flexibilidade sem adicionar muita complexidade:

1. **Blocos extras úteis:**
   - `extra_css`: Para incluir Bootstrap Icons apenas onde necessário
   - `extra_js`: Para scripts específicos de páginas (ex: validações)
   - `title`: Cada página define seu título único

2. **Flash messages com categorias:** Permite cores diferentes (success=verde, danger=vermelho, warning=amarelo) melhorando o feedback visual

3. **Manutenção facilitada:** Se precisar mudar navbar ou footer, altero apenas `base.html` e todas as páginas herdam

4. **Código DRY:** Eliminei duplicação de navbar/footer que existiria sem herança

A implementação ficou limpa: cada página faz `{% extends 'base.html' %}` e preenche apenas os blocos que precisa customizar. O padrão de pastas organizadas (`livros/`, `usuarios/`, `emprestimos/`) dentro de `templates/` facilita localizar arquivos.

**Aplicação no Projeto:**
No `base.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Biblioteca{% endblock %}</title>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav><!-- navbar --></nav>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
    {% endwith %}
    
    {% block content %}{% endblock %}
    
    <footer><!-- footer --></footer>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## PROMPT 7: Sistema de Feedback com Flash Messages Categorizadas

**Pergunta:**
> "Como implementar mensagens de feedback (sucesso, erro, aviso) no Flask para informar o usuário sobre o resultado das operações?"

**Resposta da IA:**
A IA apresentou três abordagens para sistema de feedback em Flask:

**Opção 1: Flash Messages Simples**
- Usar `flash()` nativo do Flask
- Uma única categoria de mensagem
- Exibir todas com mesmo estilo visual
- Mais básico e rápido

**Opção 2: Flash Messages com Categorias**
- Usar `flash(mensagem, categoria)` com categorias personalizadas
- Categorias como 'success', 'danger', 'warning', 'info'
- Integra perfeitamente com classes CSS do Bootstrap
- Templates usam `get_flashed_messages(with_categories=true)`

**Opção 3: Sistema de Notificações JavaScript**
- Biblioteca como Toastr ou SweetAlert
- Notificações animadas e não-intrusivas
- Melhor UX mas requer JavaScript
- Mais complexo de implementar

A IA explicou que Opção 2 é ideal para projetos Bootstrap, pois as categorias mapeiam diretamente para classes de alerta (`alert-success`, `alert-danger`).

**Análise Crítica:**
**Escolhi a Opção 2 (Flash Messages com Categorias)** porque:

1. **Integração perfeita com Bootstrap:** Categorias do Flask → Classes CSS do Bootstrap
   - `'success'` → `alert-success` (verde)
   - `'danger'` → `alert-danger` (vermelho)
   - `'warning'` → `alert-warning` (amarelo)
   - `'info'` → `alert-info` (azul)

2. **Feedback visual claro:** Usuário distingue instantaneamente sucesso de erro pela cor

3. **Sem JavaScript adicional:** Funciona com reload de página (padrão do projeto)

4. **Código limpo:** Uma linha `flash(mensagem, categoria)` em cada controller

**Padrões de Uso Implementados:**
- ✅ **Success:** Operações bem-sucedidas (cadastro, edição, exclusão)
- ❌ **Danger:** Erros críticos (validação falhou, duplicação)
- ⚠️ **Warning:** Avisos não-críticos (formato inválido de imagem)
- ℹ️ **Info:** Informações gerais (não usado no projeto, mas disponível)

**Aplicação no Projeto:**
No template base `base.html`:
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

Nos controllers (exemplos de uso):
```python
# Sucesso
flash(f'Livro "{titulo}" cadastrado com sucesso!', 'success')

# Erro de validação
flash('ISBN inválido! Deve conter 10 ou 13 dígitos.', 'danger')

# Erro de duplicação
flash('Email já cadastrado!', 'danger')

# Erro de integridade referencial
flash(f'Não é possível excluir o usuário "{usuario.nome}" pois ele possui {len(usuario.emprestimos)} empréstimo(s) vinculado(s)!', 'danger')

# Aviso não-crítico
flash('Formato de imagem inválido! Use PNG, JPG ou JPEG.', 'warning')
```

**Decisão de Design:**
Todas as mensagens são auto-fecháveis (`alert-dismissible`) com botão X, melhorando a experiência quando há múltiplas mensagens. O Bootstrap 5 já fornece animações fade-in/fade-out, tornando o feedback visualmente agradável sem JavaScript customizado.

---

## PROMPT 8: Migração de Armazenamento Local para Banco de Dados

**Pergunta:**
> "Já tenho upload de imagens funcionando com armazenamento local em `static/uploads/capas/`. Como migrar para armazenar as imagens diretamente no banco de dados PostgreSQL?"

**Resposta da IA:**
A IA explicou o processo de migração em etapas:

**Passo 1: Modificar o Model**
- Trocar `capa_url` (String) por `capa_dados` (LargeBinary) + `capa_tipo` (String)
- `LargeBinary` vira `BYTEA` no PostgreSQL
- `capa_tipo` guarda MIME type: 'image/jpeg', 'image/png'

**Passo 2: Criar Migration**
- Executar `flask db migrate` para detectar mudanças
- Aplicar com `flask db upgrade`
- Dados antigos serão perdidos (colunas diferentes)

**Passo 3: Modificar Controllers**
- No upload: trocar `file.save()` por `file.read()` e `file.mimetype`
- Salvar bytes diretamente no model

**Passo 4: Criar Rota para Servir Imagens**
- Criar endpoint `/capa_livro/<id>`
- Retornar bytes com `send_file(BytesIO(dados), mimetype=tipo)`

**Passo 5: Atualizar Templates**
- Trocar `{% if livro.capa_url %}` por `{% if livro.capa_dados %}`
- Mudar `src` de `/static/uploads/...` para `{{ url_for('capa_livro', id=livro.id) }}`

A IA alertou sobre necessidade de recarregar dados de imagens existentes.

**Análise Crítica:**
A migração foi necessária para atender requisito do trabalho ("salvar imagens no banco"). **Inicialmente implementei upload local (Opção 1)** porque era o método mais direto. Funcionou bem, mas identifiquei que arquivos com mesmo nome seriam sobrescritos. Resolvi adicionando timestamp ao nome.

**Posteriormente, migrei para banco de dados (Opção 2)** porque:

1. **Requisito do trabalho:** Especificava "armazenamento de imagens no banco"
2. **Simplicidade de backup:** Um `pg_dump` do PostgreSQL contém tudo
3. **Portabilidade:** Não depende de estrutura de pastas
4. **Escopo pequeno:** Performance não é crítica para biblioteca com centenas de livros

**Modificações Realizadas:**

1. **Model (`models.py`):**
```python
# ANTES
capa_url = db.Column(db.String(500), nullable=True)

# DEPOIS
capa_dados = db.Column(db.LargeBinary, nullable=True)
capa_tipo = db.Column(db.String(50), nullable=True)
```

2. **Controller (`create_livro`):**
```python
# ANTES
filename = secure_filename(file.filename)
timestamp = str(int(time.time()))
name, ext = os.path.splitext(filename)
capa_filename = f"{name}_{timestamp}{ext}"
file.save(os.path.join(app.config['UPLOAD_FOLDER'], capa_filename))
new_livro = Livro(..., capa_url=capa_filename)

# DEPOIS
capa_dados = file.read()
capa_tipo = file.mimetype
new_livro = Livro(..., capa_dados=capa_dados, capa_tipo=capa_tipo)
```

3. **Nova Rota:**
```python
@app.route('/capa_livro/<int:id>')
def capa_livro(id):
    livro = Livro.query.get_or_404(id)
    if livro.capa_dados and livro.capa_tipo:
        return send_file(io.BytesIO(livro.capa_dados), mimetype=livro.capa_tipo)
    else:
        abort(404)
```

4. **Templates:**
```html
<!-- ANTES -->
{% if livro.capa_url %}
    <img src="{{ url_for('static', filename='uploads/capas/' + livro.capa_url) }}">
{% endif %}

<!-- DEPOIS -->
{% if livro.capa_dados %}
    <img src="{{ url_for('capa_livro', id=livro.id) }}">
{% endif %}
```

**Ponto de Atenção:** Livros com capas existentes precisaram ser re-cadastrados pois a migration mudou estrutura da coluna. Em produção real, criaria script de migração de dados.

**Aplicação no Projeto:**
O mesmo padrão foi aplicado em:
- `app/templates/livros/livros.html` (listagem)
- `app/templates/livros/update_livro.html` (edição)
- `app/templates/emprestimos/emprestimos.html` (capas em empréstimos)

Todos os templates agora usam `livro.capa_dados` para verificar existência e `url_for('capa_livro', id=livro.id)` para exibir.

---

## PROMPT 9: Geração de PDF com Tabelas de Dados em Flask

**Pergunta:**
> "Como gerar um arquivo PDF com uma tabela de dados usando Python Flask?"

**Resposta da IA:**
A IA apresentou duas opções principais para geração de PDF em Flask:

**Opção 1: ReportLab**
- Biblioteca Python pura para criação programática de PDFs
- Requer construir o PDF "do zero" com código Python
- Oferece controle total sobre posicionamento e elementos
- Curva de aprendizado mais íngreme
- Exemplo básico mostrado com `SimpleDocTemplate`, `Table` e `TableStyle`

**Opção 2: xhtml2pdf (pisa)**
- Converte HTML/CSS existente em PDF
- Permite usar templates Jinja2 familiares
- Aproveita conhecimento de HTML/CSS já existente
- Mais intuitivo para desenvolvedores web
- Funciona bem com Bootstrap (parcialmente)

A IA explicou que xhtml2pdf renderiza templates HTML com dados usando `render_template()`, converte para PDF com `pisa.CreatePDF()`, e retorna como resposta HTTP.

**Análise Crítica:**
Avaliei ambas as opções cuidadosamente. ReportLab oferece mais controle, mas exigiria aprender uma API completamente nova e escrever muito código imperativo para criar cada elemento da tabela. Como já tenho templates HTML bem estruturados no projeto, **optei por xhtml2pdf** porque:

1. **Reutilização de conhecimento:** Já sei HTML/CSS, não preciso aprender nova API
2. **Consistência visual:** Posso manter o visual similar às páginas web
3. **Manutenibilidade:** Designers podem modificar templates sem saber Python
4. **Velocidade de desenvolvimento:** Muito mais rápido para prototipar
5. **Separação de responsabilidades:** HTML para estrutura, Python para lógica

A desvantagem do xhtml2pdf (suporte limitado a CSS3 moderno) não é crítica para relatórios simples em tabela. Criei uma função genérica `generate_pdf()` que funciona para qualquer entidade, garantindo UTF-8 para caracteres acentuados e usando BytesIO para evitar arquivos temporários.

**Aplicação no Projeto:**
Criado arquivo `app/utils/pdf_utils.py`:
```python
from flask import render_template, make_response
from xhtml2pdf import pisa
from io import BytesIO

def generate_pdf(template_name, context, filename='relatorio.pdf'):
    html = render_template(template_name, **context)
    pdf_buffer = BytesIO()
    
    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=pdf_buffer
    )
    
    if pisa_status.err:
        return None
    
    pdf_buffer.seek(0)
    response = make_response(pdf_buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    return response
```

Uso nos controllers (exemplo em `livro_controller.py`):
```python
from app.utils.pdf_utils import generate_pdf
from datetime import datetime

@app.route('/livros/pdf')
def livros_pdf():
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
```

O mesmo padrão foi aplicado em `usuario_controller.py` e `emprestimo_controller.py` com rotas `/usuarios/pdf` e `/emprestimos/pdf`.

---

## PROMPT 10: Estilização de Templates HTML para Geração de PDF

**Pergunta:**
> "Como criar templates HTML otimizados para conversão em PDF usando xhtml2pdf, garantindo boa formatação, tabelas legíveis e paginação adequada?"

**Resposta da IA:**
A IA apresentou diferentes estratégias de estilização para PDF:

**Opção 1: CSS Inline nos Elementos**
- Estilos diretamente nas tags: `<td style="color: red">`
- Garantia máxima de compatibilidade
- Código repetitivo e difícil de manter

**Opção 2: CSS em Tag `<style>` no HTML**
- Estilos centralizados no cabeçalho do template
- Reutilização de classes
- xhtml2pdf lê confivelmente
- Balanço entre compatibilidade e manutenibilidade

**Opção 3: CSS Externo Referenciado**
- Arquivo `.css` separado
- Melhor organização
- xhtml2pdf pode ter problemas para carregar

A IA recomendou Opção 2 e sugeriu: fontes pequenas (8-10px), `table-layout: fixed`, larguras percentuais, `word-wrap: break-word` para texto longo, e zebrado com `nth-child(even)`.

**Análise Crítica:**
**Escolhi Opção 2 (CSS em `<style>`)** porque:

1. **Compatibilidade garantida:** xhtml2pdf lê CSS inline no HTML
2. **Manutenibilidade:** Classes reutilizáveis sem repetição
3. **Auto-contido:** Template PDF não depende de arquivos externos

**Desafios e Soluções Encontradas:**

| Problema | Solução Aplicada |
|----------|------------------|
| Tabelas muito largas | `table-layout: fixed` + larguras % por coluna |
| Texto longo quebrando layout | `word-wrap: break-word` em todas as células |
| Fontes grandes demais | Reduzir de 12-14px para 8-9px |
| Difícil distinguir linhas | Zebrado com `nth-child(even)` |
| PDFs sem contexto | Adicionar cabeçalho com data/hora e total de registros |

**Evolução Iterativa:**
- **Tentativa 1:** Fontes 12px → Tabela não cabia na página
- **Tentativa 2:** Reduzir para 9px → Melhorou mas ISBNs longos quebravam
- **Tentativa 3:** Adicionar `word-wrap` → Resolveu overflow
- **Versão Final:** Fontes 8-9px + word-wrap + zebrado + cabeçalho profissional

Criei templates separados (`livros_pdf.html`, `usuarios_pdf.html`, `emprestimos_pdf.html`) com estrutura similar mas adaptados aos dados de cada entidade. Todos seguem o padrão: cabeçalho com título e data, box com total de registros, tabela formatada, rodapé com copyright.

**Aplicação no Projeto:**
Criados três templates PDF com estrutura semelhante. Exemplo de `livros_pdf.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Relatório de Livros</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 3px solid #333;
        }
        
        .info {
            background-color: #f0f0f0;
            padding: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
        }
        
        th {
            background-color: #333;
            color: white;
            padding: 8px 5px;
            font-size: 9px;
            word-wrap: break-word;
        }
        
        td {
            padding: 6px 5px;
            border-bottom: 1px solid #ddd;
            font-size: 8px;
            word-wrap: break-word;
        }
        
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Relatório de Livros</h1>
        <p>{{ data_geracao }}</p>
    </div>
    
    <div class="info">Total de Livros: {{ livros|length }}</div>
    
    <table>
        <thead>
            <tr>
                <th style="width: 28%;">Título</th>
                <th style="width: 20%;">Autor</th>
                <th style="width: 16%;">ISBN</th>
                <!-- ... -->
            </tr>
        </thead>
        <tbody>
            {% for livro in livros %}
            <tr>
                <td>{{ livro.titulo }}</td>
                <td>{{ livro.autor }}</td>
                <!-- ... -->
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
```

Botões adicionados nos templates de listagem (exemplo em `livros.html`):
```html
<div class="d-flex gap-2 mb-3">
    <a href="{{ url_for('create_livro') }}" class="btn btn-primary">
        <i class="bi bi-plus-circle-fill"></i> Novo Livro
    </a>
    {% if livros %}
    <a href="{{ url_for('livros_pdf') }}" class="btn btn-danger" target="_blank">
        <i class="bi bi-file-pdf-fill"></i> Exportar PDF
    </a>
    {% endif %}
</div>
```

O atributo `target="_blank"` faz o PDF abrir em nova aba, melhorando a experiência do usuário.

---

## Conclusão

O uso de Inteligência Artificial durante o desenvolvimento do projeto foi fundamental para acelerar o aprendizado e resolver problemas técnicos. Porém, foi essencial manter uma postura crítica, testando todas as sugestões, identificando limitações e adaptando as soluções ao contexto específico do projeto. A IA serviu como ferramenta de apoio, mas a compreensão e as decisões finais foram responsabilidade dos desenvolvedores.
