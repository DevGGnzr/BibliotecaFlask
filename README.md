# Sistema de Biblioteca - Flask (Padrão MVC)

Sistema completo de gerenciamento de biblioteca desenvolvido com Flask, SQLAlchemy, PostgreSQL e Bootstrap 5, seguindo o padrão arquitetural **Model-View-Controller (MVC)**.

## Descrição do Projeto

Este é um sistema web para gerenciamento de biblioteca que permite cadastrar livros, usuários e controlar empréstimos. O projeto foi desenvolvido seguindo os requisitos acadêmicos de modelagem de banco de dados com relacionamentos e implementação de CRUD completo, **refatorado para seguir o padrão MVC**.

### Características Principais

- **Arquitetura MVC:** Separação clara entre Model, View e Controller
- **3 Entidades:** Livros, Usuários e Empréstimos
- **Relacionamento 1:N:** Um usuário pode ter múltiplos empréstimos
- **Relacionamento N:N:** Um empréstimo pode ter múltiplos livros e vice-versa
- **CRUD Completo:** Criar, Ler, Atualizar e Deletar para todas as entidades
- **Validações:** Campos obrigatórios, formatos de e-mail e ISBN
- **Integridade Referencial:** Proteção contra exclusão de registros vinculados
- **Interface:** Bootstrap 5 com ícones e responsividade
- **Template Base:** Reutilização de código com herança de templates
- **Mensagens Flash:** Feedback visual de sucesso e erro
- **PostgreSQL:** Banco de dados relacional robusto
- **Migrações:** Controle de versão do banco com Alembic

## Estrutura do Projeto (Padrão MVC)

```
BIBLIOTECA-FLASK/
├── run.py                      # ⭐ Ponto de entrada da aplicação
├── config.py                   # ⭐ Configurações centralizadas
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
├── RELACIONAMENTOS.md          # Documentação detalhada do modelo ER
├── .env                        # Variáveis de ambiente
├── .env.example                # Exemplo de variáveis de ambiente
├── .gitignore                  # Arquivos ignorados pelo Git
│
├── app/                        # ⭐ Pacote principal da aplicação
│   ├── __init__.py             # ⭐ Inicialização da aplicação Flask
│   │
│   ├── controllers/            # ⭐ CONTROLLERS (Lógica e Rotas)
│   │   ├── __init__.py
│   │   ├── livro_controller.py        # Rotas e lógica de livros
│   │   ├── usuario_controller.py      # Rotas e lógica de usuários
│   │   └── emprestimo_controller.py   # Rotas e lógica de empréstimos
│   │
│   ├── models/                 # ⭐ MODELS (Banco de Dados)
│   │   ├── __init__.py
│   │   └── models.py           # Modelos SQLAlchemy (Livro, Usuario, Emprestimo)
│   │
│   ├── templates/              # ⭐ VIEWS (Interface Visual)
│   │   ├── base.html           # ⭐ Template base (navbar, footer, flash messages)
│   │   ├── index.html          # Página inicial
│   │   │
│   │   ├── livros/             # ⭐ Templates organizados por módulo
│   │   │   ├── livros.html
│   │   │   ├── create_livro.html
│   │   │   └── update_livro.html
│   │   │
│   │   ├── usuarios/
│   │   │   ├── usuarios.html
│   │   │   ├── create_usuario.html
│   │   │   └── update_usuario.html
│   │   │
│   │   └── emprestimos/
│   │       ├── emprestimos.html
│   │       ├── create_emprestimo.html
│   │       └── update_emprestimo.html
│   │
│   └── static/                 # Arquivos estáticos
│       └── uploads/
│           └── capas/          # Upload de capas de livros
│
└── migrations/                 # Migrações do banco de dados
    ├── alembic.ini
    ├── env.py
    └── versions/
```

### Padrão MVC Implementado

#### 📦 **MODEL** (app/models/)
- **Responsabilidade:** Gerenciar dados e banco de dados
- **Arquivos:** `models.py`
- **Classes:** `Livro`, `Usuario`, `Emprestimo`

#### 🎮 **CONTROLLER** (app/controllers/)
- **Responsabilidade:** Lógica de negócio e rotas
- **Arquivos:**
  - `livro_controller.py` - Gerencia todas as rotas de livros
  - `usuario_controller.py` - Gerencia todas as rotas de usuários
  - `emprestimo_controller.py` - Gerencia todas as rotas de empréstimos e página inicial

#### 🎨 **VIEW** (app/templates/)
- **Responsabilidade:** Interface visual e apresentação
- **Template Base:** `base.html` com navbar, flash messages e footer
- **Templates Organizados:** Subpastas por módulo (livros/, usuarios/, emprestimos/)

## Diagrama ER

Para uma visão detalhada do modelo de dados, consulte o arquivo [RELACIONAMENTOS.md](RELACIONAMENTOS.md).

## Instalação e Configuração

### Pré-requisitos

- Python 3.10+
- PostgreSQL 12+
- pip (gerenciador de pacotes Python)

### Passo 1: Instalar Dependências

```powershell
pip install -r requirements.txt
```

### Passo 2: Configurar PostgreSQL

1. Instale o PostgreSQL se ainda não tiver
2. Crie um banco de dados:

```sql
CREATE DATABASE biblioteca_db;
```

3. Crie um usuário (opcional, mas recomendado):

```sql
CREATE USER biblioteca_user WITH PASSWORD 'senha_segura';
GRANT ALL PRIVILEGES ON DATABASE biblioteca_db TO biblioteca_user;
```

### Passo 3: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://biblioteca_user:senha_segura@localhost:5432/biblioteca_db
SECRET_KEY=sua-chave-secreta-aqui-gere-uma-aleatoria
```

**Dica:** Para gerar uma chave secreta aleatória:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

**Nota:** O campo `SECRET_KEY` é opcional. Se não for definido no `.env`, o sistema usará automaticamente o valor padrão `'dev-secret-key-change-in-production'` configurado no `app.py`. Isso é suficiente para desenvolvimento e testes.

### Passo 4: Inicializar e Criar o Banco de Dados

```bash
# Inicializar o Flask-Migrate (cria a pasta migrations)
flask db init

# Criar a migration inicial
flask db migrate -m "criacao inicial"

# Aplicar as migrations ao banco
flask db upgrade
```

### Passo 5: Executar o Projeto

```bash
python run.py
```

O sistema estará disponível em: **http://localhost:5000**

## Funcionalidades Principais

### 1. Gerenciamento de Livros

- **Listar Livros:** Visualize todos os livros cadastrados com miniaturas de capas
- **Adicionar Livro:** Cadastre novos livros com título, autor, ISBN, ano, categoria e capa (upload de imagem)
- **Editar Livro:** Atualize informações de livros existentes e altere a capa
- **Excluir Livro:** Remove livros (apenas se não estiverem em empréstimos ativos)
- **Upload de Capas:** Faça upload de imagens das capas dos livros (PNG, JPG, JPEG - máx. 5MB)

**Validações:**
- ISBN único (10 ou 13 dígitos)
- Ano de publicação válido (1000-2100)
- Formato de imagem válido (PNG, JPG, JPEG)
- Tamanho máximo de arquivo: 5MB
- Todos os campos obrigatórios

### 2. Gerenciamento de Usuários

- **Listar Usuários:** Visualize todos os usuários cadastrados
- **Adicionar Usuário:** Cadastre novos usuários com nome e email
- **Editar Usuário:** Atualize informações de usuários
- **Excluir Usuário:** Remove usuários (apenas se não tiverem empréstimos ativos)

**Validações:**
- Email único e formato válido
- Nome obrigatório

### 3. Gerenciamento de Empréstimos

- **Listar Empréstimos:** Visualize todos os empréstimos com usuários e livros
- **Criar Empréstimo:** Registre novos empréstimos selecionando usuário e livros
- **Editar Empréstimo:** Atualize empréstimos existentes
- **Excluir Empréstimo:** Remove empréstimos

**Validações:**
- Número de empréstimo único
- Usuário obrigatório
- Pelo menos um livro selecionado

### 4. Proteção de Integridade Referencial

O sistema impede:
- ❌ Excluir usuários com empréstimos ativos
- ❌ Excluir livros vinculados a empréstimos
- ❌ Criar registros com dados inválidos
- ❌ Duplicar emails de usuários
- ❌ Duplicar ISBNs de livros

## Tecnologias Utilizadas

### Backend
- **Flask 3.1.2** - Framework web Python
- **Flask-SQLAlchemy 3.1.1** - ORM (Object-Relational Mapping)
- **Flask-Migrate 4.1.0** - Gerenciador de migrações com Alembic
- **PostgreSQL** - Banco de dados relacional
- **psycopg2-binary 2.9.11** - Adaptador PostgreSQL para Python
- **python-dotenv 1.1.1** - Gerenciamento de variáveis de ambiente

### Frontend
- **Bootstrap 5.3.0** - Framework CSS responsivo
- **Bootstrap Icons 1.11.0** - Ícones
- **HTML5 + Jinja2** - Templates dinâmicos

## Modelo de Dados

### Entidades

#### 1. Livro
```python
- id (PK, autoincrement)
- titulo (string, obrigatório)
- autor (string, obrigatório)
- isbn (string, único, obrigatório)
- ano_publicacao (integer, obrigatório)
- categoria (string, obrigatório)
- capa_url (string, opcional) # Nome do arquivo da capa
```

#### 2. Usuario
```python
- id (PK, autoincrement)
- nome (string, obrigatório)
- email (string, único, obrigatório)
```

#### 3. Emprestimo
```python
- id (PK, autoincrement)
- numero_emprestimo (string, único, obrigatório)
- usuario_id (FK → usuarios.id, obrigatório)
- livros (relacionamento N:N via emprestimo_livro)
```

#### 4. Emprestimo_Livro (Tabela Associativa)
```python
- emprestimo_id (FK → emprestimos.id, PK)
- livro_id (FK → livros.id, PK)
```


## Segurança e Boas Práticas

- ✅ Variáveis de ambiente para dados sensíveis (`.env`)
- ✅ Validação de entrada no servidor
- ✅ Proteção contra injeção SQL (via SQLAlchemy ORM)
- ✅ Mensagens de erro amigáveis sem expor informações sensíveis
- ✅ Confirmação antes de exclusões
- ✅ Flash messages para feedback do usuário
- ✅ Upload seguro de arquivos com validação de tipo e tamanho
- ✅ Nomes de arquivo seguros (secure_filename)
- ✅ Limite de tamanho de upload (5MB)

## Documentação Adicional

- **RELACIONAMENTOS.md:** Documentação detalhada do modelo ER com diagramas

## Desenvolvimento

**Autores:** Gilberto, Victoria   
**Instituição:** IFRS - Campus Veranópolis  
**Disciplina:** Desenvolvimento Web II  
**Professor:** Jorge Arthur Schneider Aranda  
**Data:** Outubro 2025

## Licença

Este projeto foi desenvolvido para fins educacionais.

## Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências estão instaladas
2. Confirme que o PostgreSQL está rodando
3. Verifique o arquivo `.env` com as credenciais corretas
4. Consulte a documentação em RELACIONAMENTOS.md

