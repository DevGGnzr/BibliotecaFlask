# Documentação - Implementação de Exportação de PDF

## Data: 26 de novembro de 2025

## Contexto do Trabalho

Este documento registra a conversa sobre a implementação da funcionalidade de exportação de PDF no sistema de Biblioteca Flask.

## Estrutura Atual do Projeto

O projeto possui a seguinte estrutura:

```
BIBLIOTECA-FLASK/
├── app/
│   ├── controllers/
│   │   ├── livro_controller.py
│   │   ├── usuario_controller.py
│   │   └── emprestimo_controller.py
│   ├── models/
│   │   └── models.py
│   ├── templates/
│   │   ├── livros/
│   │   ├── usuarios/
│   │   └── emprestimos/
│   └── utils/
│       └── pdf_utils.py
├── requirements.txt
└── run.py
```

## Estado Atual

### Arquivos Analisados

1. **pdf_utils.py** - Já existe um arquivo básico para geração de PDF com a biblioteca `xhtml2pdf`
2. **Controllers** - Implementados para Livros, Usuários e Empréstimos
3. **Models** - Três entidades principais: Livro, Usuario e Emprestimo

### Funcionalidade Existente de PDF

O arquivo `app/utils/pdf_utils.py` já contém uma função básica:

```python
from flask import render_template, make_response
from xhtml2pdf import pisa

def generate_pdf(template_name, context):
    """
    Renderiza um template HTML com o contexto fornecido e converte para PDF.
    """
    html = render_template(template_name, **context)
    pdf= pisa.CreatePDF(html)
    if not pdf.err:
        response= make_response(pdf.dest)
        response.headers['Content-Type']= 'application/pdf'
        response.headers['Content-Disposition']= f'inline; filename=document.pdf'
        return response
    return None
```

## Requisitos Identificados

### Dependências Necessárias

A biblioteca `xhtml2pdf` precisa ser adicionada ao `requirements.txt` (atualmente não está listada).

### Implementação Planejada

Para uma implementação completa de exportação de PDF, seria necessário:

1. **Atualizar requirements.txt**
   - Adicionar `xhtml2pdf` às dependências

2. **Melhorar pdf_utils.py**
   - Corrigir a função de geração de PDF
   - Adicionar suporte para nomes de arquivo personalizados
   - Melhorar o tratamento de erros

3. **Criar Templates HTML para PDF**
   - Template para lista de livros
   - Template para lista de usuários
   - Template para lista de empréstimos
   - Templates devem ser otimizados para impressão

4. **Adicionar Rotas de Exportação**
   - `/livros/pdf` - Exportar lista de livros
   - `/usuarios/pdf` - Exportar lista de usuários
   - `/emprestimos/pdf` - Exportar lista de empréstimos

5. **Adicionar Botões nas Interfaces**
   - Botões "Exportar PDF" nas páginas de listagem
   - Ícones apropriados para melhor UX

## Entidades do Sistema

### Livro
- ID
- Título
- Autor
- ISBN
- Ano de Publicação
- Categoria
- Capa (imagem em binary)

### Usuário
- ID
- Nome
- Email

### Empréstimo
- ID
- Número do Empréstimo
- Usuário (relacionamento)
- Livros (relacionamento muitos-para-muitos)

## Próximos Passos Sugeridos

1. Instalar a biblioteca `xhtml2pdf`
2. Criar templates HTML específicos para PDF com CSS para formatação
3. Implementar as rotas de exportação nos controllers
4. Adicionar botões de exportação na interface
5. Testar a geração de PDF com diferentes volumes de dados

## Observações Técnicas

- O projeto usa Flask com SQLAlchemy
- Banco de dados PostgreSQL
- Sistema de templates Jinja2
- A função atual de PDF já está parcialmente implementada, mas precisa de melhorias
- É importante considerar a formatação e paginação para grandes volumes de dados

## Referências

- Biblioteca xhtml2pdf: Para conversão de HTML para PDF
- Flask-SQLAlchemy: ORM utilizado no projeto
- Jinja2: Sistema de templates do Flask
