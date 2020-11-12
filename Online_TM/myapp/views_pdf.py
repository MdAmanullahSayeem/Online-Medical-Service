# pdf output using just xhtml2pdf (preferable)

from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from .models import Prescription

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# Opens up page as PDF
class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        pk=request.session['pk']
        data = Prescription.objects.get(pk=pk)
        pdf = render_to_pdf('pdf/test.html', {'data':data})
        return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        pk = request.session['pk']
        data = Prescription.objects.get(pk=pk)
        pdf = render_to_pdf('pdf/test.html', {'data':data})
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response


def index(request):
    context = {}
    return render(request, 'pdf/index.html', context)

# pdf output using easy_pdf


from easy_pdf.views import PDFTemplateResponseMixin
from django.views.generic import DetailView
from .models import Account

class HelloPDFView(PDFTemplateResponseMixin, DetailView):
    template_name = 'unicode.html'
    model = Account
    context_object_name = 'obj'

