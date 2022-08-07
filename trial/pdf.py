from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
# import xhtml2pdf
from xhtml2pdf import pisa
import pdfkit
# from num2words import num2words

# def render_to_pdf(template_src):
#     print('hi1')
#     template = get_template(template_src)
#     # html  = template.render(context)
#     html=template.render()
#     print(html,"hi")
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         print(pdf,'hi2')
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

# def render_to_pdf(template_src):
#     # print('hi1')
#     template = get_template(template_src)
#     # html  = template.render(context)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     html=template.render()
#     # print(html,"hi")
#     # result = BytesIO()
#     print("1")
#     pisa_status  = pisa.CreatePDF(html, dest=response)
#     print(pisa_status)
#     print("2")
#     if not pisa_status.err:
#         # print(pdf,'hi2')
#         return response
#     return None

# def render_to_pdf(template_src):
#     # print('hi1')
#     config = pdfkit.configuration(wkhtmltopdf = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
#     a=pdfkit.from_file('temp.html', 'output.pdf', configuration = config)
#     if a:
#         return ()
