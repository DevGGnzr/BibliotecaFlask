# Documentação dos Relacionamentos - Sistema de Biblioteca

## Diagrama Entidade-Relacionamento (ER)

```
┌─────────────────┐
│    USUARIO      │
├─────────────────┤
│ id (PK)         │
│ nome            │
│ email (UNIQUE)  │
└────────┬────────┘
         │
         │ 1
         │
         │ N
         │
┌────────▼────────┐          ┌──────────────────────┐          ┌─────────────────┐
│  EMPRESTIMO     │          │  EMPRESTIMO_LIVRO    │          │     LIVRO       │
├─────────────────┤          │  (Tabela Associativa)│          ├─────────────────┤
│ id (PK)         │   1    N ├──────────────────────┤  N    1  │ id (PK)         │
│ numero_emprest..│◄─────────┤ emprestimo_id (FK,PK)├─────────►│ titulo          │
│ usuario_id (FK) │          │ livro_id (FK,PK)     │          │ autor           │
│ data_emprestimo │          └──────────────────────┘          │ isbn (UNIQUE)   │
│ data_devolucao  │                                            │ ano_publicacao  │
└─────────────────┘                                            │ categoria       │
                                                               │ ano_publicacao  │
                                                               │ categoria       │
                                                               │ capa_dados      │
                                                               │ capa_tipo       │
                                                               └─────────────────┘

Legenda:
PK = Primary Key (Chave Primária)
FK = Foreign Key (Chave Estrangeira)
◄─────► = Relacionamento
1 = Um
N = Muitos
```

## Entidades do Sistema

### 1. USUARIO (Usuários)
**Descrição:** Representa os usuários da biblioteca que podem fazer empréstimos de livros.

**Atributos:**
- `id` (INTEGER, PK): Identificador único do usuário (autoincremento)
- `nome` (VARCHAR(150), NOT NULL): Nome completo do usuário
- `email` (VARCHAR(100), UNIQUE, NOT NULL): Email único do usuário

**Constraints:**
- Primary Key: `id`
- Unique: `email` (cada usuário deve ter um email único)

---

### 2. LIVRO (Livros)
**Descrição:** Representa os livros disponíveis no acervo da biblioteca.

**Atributos:**
- `id` (INTEGER, PK): Identificador único do livro (autoincremento)
- `titulo` (VARCHAR(200), NOT NULL): Título do livro
- `autor` (VARCHAR(150), NOT NULL): Nome do autor
- `isbn` (VARCHAR(20), UNIQUE, NOT NULL): Código ISBN único do livro
- `ano_publicacao` (INTEGER, NOT NULL): Ano de publicação
- `categoria` (VARCHAR(100), NOT NULL): Categoria/gênero do livro
- `capa_dados` (BYTEA, NULL): Dados binários da imagem da capa armazenados no banco
- `capa_tipo` (VARCHAR(50), NULL): Tipo MIME da imagem (ex: image/jpeg, image/png)

**Constraints:**
- Primary Key: `id`
- Unique: `isbn` (cada livro tem um ISBN único)

---

### 3. EMPRESTIMO (Empréstimos)
**Descrição:** Representa um empréstimo feito por um usuário. Um empréstimo pode incluir múltiplos livros.

**Atributos:**
- `id` (INTEGER, PK): Identificador único do empréstimo (autoincremento)
- `numero_emprestimo` (VARCHAR(50), UNIQUE, NOT NULL): Número de controle do empréstimo
- `usuario_id` (INTEGER, FK, NOT NULL): Referência ao usuário que fez o empréstimo
- `data_emprestimo` (TIMESTAMP, NOT NULL, DEFAULT=now): Data e hora em que o empréstimo foi criado
- `data_devolucao` (DATE, NOT NULL): Data prevista para devolução dos livros

**Constraints:**
- Primary Key: `id`
- Foreign Key: `usuario_id` REFERENCES `usuarios(id)`
- Unique: `numero_emprestimo`
- Check: `data_devolucao` não pode ser anterior à data atual (validação no controller)

---

### 4. EMPRESTIMO_LIVRO (Tabela Associativa)
**Descrição:** Tabela de junção que implementa o relacionamento muitos-para-muitos entre empréstimos e livros.

**Atributos:**
- `emprestimo_id` (INTEGER, FK, PK): Referência ao empréstimo
- `livro_id` (INTEGER, FK, PK): Referência ao livro

**Constraints:**
- Composite Primary Key: (`emprestimo_id`, `livro_id`)
- Foreign Key: `emprestimo_id` REFERENCES `emprestimos(id)`
- Foreign Key: `livro_id` REFERENCES `livros(id)`

---

## Relacionamentos

### Relacionamento 1: USUARIO ──< EMPRESTIMO (1-para-N)
**Tipo:** Um-para-Muitos (1:N)

**Descrição:**
- Um USUARIO pode ter vários EMPRESTIMOS
- Cada EMPRESTIMO pertence a apenas um USUARIO

**Implementação:**
- Chave Estrangeira `usuario_id` na tabela `emprestimos` referencia `usuarios(id)`
- Campo obrigatório (NOT NULL)

**Justificativa:**
Esta chave estrangeira é essencial para rastrear qual usuário é responsável por cada empréstimo. Ela garante a integridade referencial, impedindo a criação de empréstimos sem um usuário válido e controlando que empréstimos não possam referenciar usuários inexistentes.

**Comportamento de Exclusão:**
- **Restrição implementada:** Não é possível excluir um usuário que possui empréstimos ativos
- **Validação no código:** Antes de excluir um usuário, o sistema verifica se existem empréstimos vinculados
- **Mensagem de erro:** "Não é possível excluir o usuário '{nome}' pois ele possui X empréstimo(s) vinculado(s)!"

---

### Relacionamento 2: EMPRESTIMO ──< EMPRESTIMO_LIVRO >── LIVRO (N-para-N)
**Tipo:** Muitos-para-Muitos (N:N)

**Descrição:**
- Um EMPRESTIMO pode incluir vários LIVROS
- Um LIVRO pode estar em vários EMPRESTIMOS (ao longo do tempo)

**Implementação:**
- Tabela associativa `emprestimo_livro` com chave composta
- Duas chaves estrangeiras:
  - `emprestimo_id` → `emprestimos(id)`
  - `livro_id` → `livros(id)`

**Justificativa:**
O relacionamento N:N é necessário porque:
1. Um empréstimo pode conter múltiplos livros (usuário pode pegar vários livros de uma vez)
2. Um mesmo livro pode ser emprestado múltiplas vezes (em empréstimos diferentes ao longo do tempo)
3. A tabela associativa permite rastrear exatamente quais livros fazem parte de cada empréstimo

**Comportamento de Exclusão:**
- **EMPRESTIMO:** Ao excluir um empréstimo, os registros correspondentes na tabela `emprestimo_livro` são automaticamente removidos (cascade)
- **LIVRO:** Não é possível excluir um livro que está vinculado a algum empréstimo ativo
- **Validação no código:** Sistema verifica se o livro possui empréstimos antes de permitir exclusão
- **Mensagem de erro:** "Não é possível excluir o livro '{titulo}' pois ele está vinculado a X empréstimo(s)!"

---

## Integridade Referencial

### Regras de Negócio Implementadas

1. **Criação de Empréstimo:**
   - Deve ter um usuário válido (obrigatório)
   - Deve ter pelo menos um livro selecionado
   - Número do empréstimo deve ser único

2. **Exclusão de Usuário:**
   - ❌ BLOQUEADA se existirem empréstimos vinculados
   - ✅ PERMITIDA se não houver empréstimos

3. **Exclusão de Livro:**
   - ❌ BLOQUEADA se o livro estiver em algum empréstimo
   - ✅ PERMITIDA se não houver vinculações

4. **Exclusão de Empréstimo:**
   - ✅ SEMPRE PERMITIDA
   - Remove automaticamente os vínculos na tabela `emprestimo_livro`
   - Não afeta usuários nem livros

### Validações de Dados

**USUARIO:**
- Email deve ser único e ter formato válido
- Nome obrigatório

**LIVRO:**
- ISBN deve ser único e conter 10 ou 13 dígitos
- Ano de publicação deve estar entre 1000 e 2100
- Todos os campos são obrigatórios

**EMPRESTIMO:**
- Número do empréstimo deve ser único
- Deve referenciar um usuário existente
- Deve ter ao menos um livro associado
- Data de empréstimo é registrada automaticamente no momento da criação
- Data de devolução é obrigatória e não pode ser anterior à data atual

---

## Exemplo de Uso do Sistema

### Cenário Típico:

1. **Cadastrar Usuário:**
   ```
   Nome: João Silva
   Email: joao@email.com
   ```

2. **Cadastrar Livros:**
   ```
   Livro 1: "1984" - George Orwell (ISBN: 978-0451524935)
   Livro 2: "O Hobbit" - J.R.R. Tolkien (ISBN: 978-0547928227)
   ```

3. **Criar Empréstimo:**
   ```
   Número: EMP-001
   Usuário: João Silva
   Livros: "1984" + "O Hobbit"
   Data de Devolução: 10/12/2025
   ```

4. **Resultado no Banco:**
   ```
   Tabela USUARIOS:
   id=1, nome="João Silva", email="joao@email.com"
   
   Tabela LIVROS:
   id=1, titulo="1984", isbn="978-0451524935"
   id=2, titulo="O Hobbit", isbn="978-0547928227"
   
   Tabela EMPRESTIMOS:
   id=1, numero_emprestimo="EMP-001", usuario_id=1,
   data_emprestimo="2025-11-27 10:30:00", data_devolucao="2025-12-10"
   
   Tabela EMPRESTIMO_LIVRO:
   emprestimo_id=1, livro_id=1
   emprestimo_id=1, livro_id=2
   ```

---

## Tecnologias Utilizadas

- **Flask-SQLAlchemy:** ORM para mapeamento objeto-relacional
- **PostgreSQL:** Banco de dados relacional
- **Flask-Migrate (Alembic):** Sistema de migrações de banco de dados

## Conclusão

Este modelo de dados implementa corretamente os requisitos de relacionamentos:
- ✅ Mínimo de 3 entidades (Usuario, Livro, Emprestimo)
- ✅ Relacionamento 1:N (Usuario → Emprestimo)
- ✅ Relacionamento N:N (Emprestimo ↔ Livro)
- ✅ Chaves estrangeiras documentadas e justificadas
- ✅ Comportamento de exclusão definido e implementado
- ✅ Integridade referencial garantida
