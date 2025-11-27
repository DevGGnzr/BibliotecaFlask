# PROMPT 7: Armazenamento de Imagens no Banco de Dados

**Pergunta:**
> "Como armazenar imagens diretamente no banco de dados usando Flask e SQLAlchemy, evitando salvar arquivos no disco?"

**Resposta da IA:**
A IA explicou que é possível usar o tipo `db.LargeBinary` para armazenar o conteúdo binário da imagem e um campo extra para o tipo MIME. No controller, basta ler o arquivo enviado (`file.read()`) e salvar nos campos do modelo. Para exibir, crie uma rota que retorna o binário usando `send_file` e `io.BytesIO`, e no template use a URL dessa rota como `src` da tag `<img>`.

**Análise Crítica:**
A solução funcionou perfeitamente e simplificou o gerenciamento de arquivos, pois tudo fica centralizado no banco. Para o escopo acadêmico, a abordagem é adequada e facilita backup/restauração. Em sistemas grandes, pode impactar performance, mas para o projeto é ideal.

**Aplicação no Projeto:**
No modelo `Livro`:
```python
capa_dados = db.Column(db.LargeBinary, nullable=True)
capa_tipo = db.Column(db.String(50), nullable=True)
```
No controller:
```python
if 'capa' in request.files:
    file = request.files['capa']
    livro.capa_dados = file.read()
    livro.capa_tipo = file.mimetype
```
Rota para servir imagem:
```python
@app.route('/capa_livro/<int:id>')
def capa_livro(id):
    livro = Livro.query.get_or_404(id)
    if livro.capa_dados and livro.capa_tipo:
        return send_file(io.BytesIO(livro.capa_dados), mimetype=livro.capa_tipo)
    else:
        abort(404)
```
No template:
```html
<img src="{{ url_for('capa_livro', id=livro.id) }}" alt="{{ livro.titulo }}">
```

---

# PROMPT 8: Exibição de Imagens Salvas no Banco

**Pergunta:**
> "Como exibir imagens salvas no banco de dados em um template Flask, usando uma rota para servir o binário?"

**Resposta da IA:**
A IA sugeriu criar uma rota Flask que retorna o binário da imagem usando `send_file` e `io.BytesIO`, com o tipo MIME correto. No template, basta usar a URL dessa rota como `src` da tag `<img>`. Explicou que isso permite exibir imagens diretamente do banco sem depender de arquivos no disco.

**Análise Crítica:**
A abordagem é simples e eficiente para projetos pequenos. Permite que as imagens sejam exibidas em qualquer página do sistema, sem risco de conflito de nomes ou problemas de permissão de arquivos. O único cuidado é garantir que o campo binário e o tipo MIME estejam preenchidos corretamente.

**Aplicação no Projeto:**
No controller:
```python
@app.route('/capa_livro/<int:id>')
def capa_livro(id):
    livro = Livro.query.get_or_404(id)
    if livro.capa_dados and livro.capa_tipo:
        return send_file(io.BytesIO(livro.capa_dados), mimetype=livro.capa_tipo)
    else:
        abort(404)
```
No template:
```html
<img src="{{ url_for('capa_livro', id=livro.id) }}" alt="{{ livro.titulo }}">
```
