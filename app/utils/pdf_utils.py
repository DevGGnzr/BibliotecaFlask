from flask import render_template, make_response
from xhtml2pdf import pisa
from io import BytesIO

def generate_pdf(template_name, context, filename='relatorio.pdf'):
    """
    Renderiza um template HTML com o contexto fornecido e converte para PDF.
    
    Args:
        template_name: Nome do template HTML a ser renderizado
        context: Dicionário com os dados para o template
        filename: Nome do arquivo PDF gerado (padrão: relatorio.pdf)
    
    Returns:
        Response do Flask com o PDF ou None em caso de erro
    """
    html = render_template(template_name, **context)
    
    # Criar buffer para armazenar o PDF
    pdf_buffer = BytesIO()
    
    # Gerar PDF
    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=pdf_buffer
    )
    
    # Verificar se houve erro
    if pisa_status.err:
        return None
    
    # Preparar resposta
    pdf_buffer.seek(0)
    response = make_response(pdf_buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename={filename}'
    
    return response