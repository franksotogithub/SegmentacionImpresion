from PyPDF2 import PdfFileMerger, PdfFileReader
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate

from pyPdf import PdfFileWriter, PdfFileReader
from .views import generar_pdf
from .views_croquis import generar_croq
from .reportes_models import *
from urllib2 import Request, urlopen
from StringIO import StringIO
from unipath import Path


def union_pdf(request, ubig):
    print "en unuoin"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=" + ubig + "001" + ".pdf"
    pdf_name = "clientes.pdf"
    styles = getSampleStyleSheet()
    stylesTitle = getSampleStyleSheet()
    stylesCabe = getSampleStyleSheet()

    styleTitle = stylesTitle["Normal"]
    styleTitle.alignment = TA_CENTER

    styleBH = styles["Normal"]
    styleBH.alignment = TA_LEFT

    styleCa = stylesCabe["Normal"]
    styleCa.alignment = TA_CENTER

    distrito = Distrito.objects.get(ubigeo=ubig)  # ubigeo

    total = int(str(Aeus.objects.filter(ubigeo=distrito.ubigeo, zona='00100').count()))
    story = []
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=" + ubig + "001" + ".pdf"
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=70,
                            leftMargin=70,
                            topMargin=60,
                            bottomMargin=18,
                            )
    i = 0
    print "for"
    for aeu in Aeus.objects.filter(ubigeo=distrito.ubigeo, zona='00100'):
        i += 1
        if i > 3:
            break
        a = generar_pdf(ubig, aeu)
        print "ubigeo:"
        b = generar_croq(ubig, aeu)
        print "aeu:"
        story.append(b)
        story.append(a)

    doc.build(story)
    response.write(buff.getvalue())
    buff.close()

    return response


def merge_pdf(request):
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = "attachment; filename=001"+ ".pdf"
    # merger = PdfFileMerger()
    # filenames = ['02060100100.pdf', '02060100100001.pdf']
    # for filename in filenames:
    #     remoteFile = urlopen(Request(filename)).read()
    #     memoryFile = StringIO(remoteFile)
    #     pdfFile = PdfFileReader(memoryFile)
    #     merger.append(PdfFileReader(file(pdfFile, 'rb')))
    #
    # merger.write(open('result.pdf', 'wb'))

    # Creamos una funcion que automatice la union de los archivos pdf
    def append_pdf(input, output):
        [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

    # Instanciamos la escritura de archivos PDF de la libreria pypdf
    output = PdfFileWriter()

    ## Aniadimos los reportes, estos podemos cargarlos desde archivos temporales


    append_pdf(PdfFileReader(file("Zonas/02060100100.pdf", "rb")), output)
    append_pdf(PdfFileReader(file("Croquis2/02060100100001.pdf", "rb")), output)

    # Escribimos la Salida Final del Reporte
    a = output.write(file("UnionFinalPDF.pdf", "wb"))

    return a