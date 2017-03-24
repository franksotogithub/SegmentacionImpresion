# coding=utf-8
import json

from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse

# from reportlab.pdfgen.canvas import Canvas
# !/usr/bin/env python

from reportlab.pdfgen import canvas
from django.db.models import Q
#from reporte.reportes_models import *
from reportes_models import *
from reportlab.graphics.barcode import code39,code128
from reportlab.lib.pagesizes import A4, cm, inch
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import utils
from reportlab.platypus.flowables import PageBreak, Spacer
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Image, Paragraph, Table, TableStyle
from io import BytesIO

from  reportlab.lib.styles import ParagraphStyle as PS
from django.http import HttpResponse
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
import os
import os.path
import win32print
import win32api

width, height = A4

def get_image(path, width=1 * cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

def coord(x, y, unit=1):
    x, y = x * unit, height - y * unit
    return x, y




def generarLegajo(request, ubigeo):
    print "Se va Gwnerar el pdf del Ubigeo: " + str(ubigeo)
    MARGIN_SIZE = 17 * mm
    PAGE_SIZE = A4

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=" + ubigeo + "001" + ".pdf"
    styles = getSampleStyleSheet()
    stylesTitle = getSampleStyleSheet()
    stylesCabe = getSampleStyleSheet()

    styleTitle = stylesTitle["Normal"]
    styleTitle.alignment = TA_CENTER
    styleBH = styles["Normal"]
    styleBH.alignment = TA_LEFT
    styleCa = stylesCabe["Normal"]
    styleCa.alignment = TA_CENTER

    buff = BytesIO()

    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=65,
                            leftMargin=65,
                            topMargin=0.5 *cm,
                            bottomMargin=0.5 *cm,
                            )

    h_sub_tile = PS(
        name='Heading1',
        fontSize=10,
        leading=14,
        alignment=TA_CENTER
    )

    h_sub_tile_2 = PS(
        name='Heading1',
        fontSize=11,
        leading=14,
        alignment=TA_CENTER
    )

    h_center = PS(
        name='Heading1',
        fontSize=7,
        leading=8,
        alignment=TA_CENTER
    )

    h1 = PS(
        name='Heading1',
        fontSize=7,
        leading=8
    )

    h11 = PS(
        name='Heading1',
        fontSize=7,
        leading=8,
        alignment=TA_CENTER
    )

    h2 = PS(
        name='Normal',
        fontSize=6,
        leading=16
    )

    h3 = PS(
        name='Normal',
        fontSize=7,
        leading=14,
        alignment=TA_CENTER)

    h4 = PS(
        name='Normal',
        fontSize=6,
        leading=16
    )

    h5 = PS(
        name='Normal',
        fontSize=8,
        leading=16,
        alignment=TA_CENTER
    )


    h_resumen = PS(
        name='Normal',
        fontSize=7,
        leading=8,
        alignment=TA_CENTER


    )
    h_obser = PS(
        name='Normal',
        fontSize=8,
        leading=16
    )

    h_bar = PS(
        name='Normal',
        fontSize=7,
        leading=14,
        alignment=TA_CENTER
    )

    Elementos = []

    ccdd = ubigeo[0:2]
    ccpp = ubigeo[2:4]
    ccdi = ubigeo[4:6]
    print "ubigeo: " + str(ubigeo)
    print "ccdd: " + str(ccdd)
    print "ccpp" + str(ccpp)
    print "ccdi" + str(ccdi)

    lista = Vw_reporte_legajo.objects.filter(ccdd=ccdd, ccpp=ccpp, ccdi=ccdi)
    lista2=Distrito.objects.filter(ubigeo=ubigeo)

    dist_legajo=lista[0]
    dist=lista2[0]
    dist.flag_legajo_u=1
    dist.save()



    if os.path.exists("\\\srv-fileserver\\CPV2017\\legajos\\{}".format(ubigeo)) == False:
        os.mkdir("\\\srv-fileserver\\CPV2017\\legajos\\{}".format(ubigeo))


    destino = "\\\srv-fileserver\\CPV2017\\legajos\\{}\\{}.pdf".format( ubigeo, ubigeo)


    doc2 = SimpleDocTemplate(destino, pagesize=A4,
                             rightMargin=70,
                             leftMargin=70,
                             topMargin=0.5 * cm,
                             bottomMargin=0.5 * cm, )

    fichero_imagen_inei = 'Reporte/Img/inei.png'
    imagen_logo_inei = Image(os.path.realpath(fichero_imagen_inei), width=50, height=40)

    P2 = Paragraph('', styleBH)
    fichero_imagen = 'Reporte/Img/escudo.png'
    imagen_logo_escudo = Image(os.path.realpath(fichero_imagen), width=50, height=50)




    titulo = Paragraph(u'CENSOS NACIONALES 2017: XII DE POBLACIÓN, VII DE VIVIENDA<br/>Y III DE COMUNIDADES INDÍGENAS',h_sub_tile)
    subtitulo=Paragraph(u'CARGO DE ENTREGA DE LEGAJOS URBANO',h_sub_tile)
    barcode = code128.Code128(u'{}'.format(ubigeo), barHeight=1 * cm, barWidth=1.2)

    data_titulo = [
        [imagen_logo_escudo,titulo,imagen_logo_inei],
        ['', subtitulo, ''],
        [barcode,'' '']
    ]

    titulo = Table(data_titulo, colWidths=[2.5 * cm, 14 * cm, 2.5 * cm],)
    titulo.setStyle(TableStyle([

    ]))
    titulo.setStyle(TableStyle([

        ('SPAN', (0, 2), (2, 2)),
        ('ALIGN', (0, 0), (2, 2), 'CENTER'),


    ]))

    data = [


       [Paragraph(u'<strong>UBICACIÓN GEOGRÁFICA</strong>', h11), '', ''],
       [Paragraph('<strong>DEPARTAMENTO</strong>', h1),Paragraph(str(dist_legajo.ccdd), h_center),Paragraph(str(dist_legajo.departamento), h1)],
       [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(dist_legajo.ccpp, h_center),Paragraph(dist_legajo.provincia, h1) ],
       [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph(dist_legajo.ccdi, h_center), Paragraph(dist_legajo.distrito, h1)],
       [Paragraph(u'<strong>FECHA DE ENTREGA</strong>', h1), '',''],
    ]

    cabecera = Table(data, colWidths=[3.7 * cm, 1 * cm, 5.5 * cm],rowHeights=[ 0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4* cm,0.4*cm])
    cabecera.setStyle(TableStyle([

        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (1, 4), (2, 4)),
        ('GRID', (0, 0), (2, 4), 1, colors.black),
        ('BACKGROUND', (0, 0), (2, 0), colors.Color(219.0/255,229.0/255,241.0/255)),
        ('BACKGROUND', (0, 0), (0, 4), colors.Color(219.0/255,229.0/255,241.0/255)),
    ]))


    total=int(dist_legajo.cant_aeu_u)+int(dist_legajo.cant_secc_u)+ int(dist_legajo.cant_zonas_u)+1
    data_res = [
        [Paragraph(u'<strong>RESUMEN DE LEGAJOS POR DISTRITO</strong>',h11),''],
        [ Paragraph('<strong>A.E.U.</strong>', h1), Paragraph('{}'.format(dist_legajo.cant_aeu_u),h_resumen)],
        [ Paragraph('<strong>SECCIONES</strong>', h1),Paragraph('{}'.format(dist_legajo.cant_secc_u),h_resumen) ],
        [ Paragraph('<strong>ZONAS</strong>', h1), Paragraph('{}'.format(dist_legajo.cant_zonas_u) ,h_resumen)],
        [ Paragraph('<strong>DISTRITAL</strong>', h1), Paragraph('1',h_resumen)],
        [ Paragraph('<strong>TOTAL</strong>', h1),Paragraph('{}'.format(total),h_resumen) ],
    ]

    resumen = Table(data_res, colWidths=[4.5 * cm, 3 * cm] ,rowHeights= 6*[0.4 * cm])
    resumen.setStyle(TableStyle([

       ('GRID', (0, 0), (1, 5), 1, colors.black),
       ('SPAN', (0, 0), (1, 0)),
       ('BACKGROUND', (0, 0), (1, 0), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
       ('BACKGROUND', (0, 0), (0, 5), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),

    ]))
    Elementos.append(titulo)
    Elementos.append(Spacer(0, 6 * mm))
    Elementos.append(cabecera)
    Elementos.append(Spacer(0, 6 * mm))
    Elementos.append(resumen)
    Elementos2=Elementos[:]
    doc.build(Elementos)
    doc2.build(Elementos2)

    imprimirLegajo(ubigeo)
    response.write(buff.getvalue())
    buff.close()
    return response

def imprimirLegajo(ubigeo):
    archivo = "\\\srv-fileserver\\CPV2017\\legajos\\{}\\{}.pdf".format(ubigeo,ubigeo)
    tempprinter = "\\\\172.18.1.35\\192.168.230.20"
    currentprinter = win32print.GetDefaultPrinter()
    win32print.SetDefaultPrinter(tempprinter)
    win32api.ShellExecute(0, "print", archivo, None, ".", 0)
    win32print.SetDefaultPrinter(currentprinter)


