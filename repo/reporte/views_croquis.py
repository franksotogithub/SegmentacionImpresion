# coding=utf-8


# from reportlab.pdfgen.canvas import Canvas
#!/usr/bin/env python

from reportlab.pdfgen import canvas
from django.db.models import Q
from reporte.reportes_models import *

from reportlab.lib.pagesizes import A4, cm, inch
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import utils
from reportlab.platypus.flowables import PageBreak, Spacer
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Image, Paragraph, Table, TableStyle
from io import BytesIO

from  reportlab.lib.styles import ParagraphStyle as PS
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table
import os
import os.path
width, height = A4

def get_image(path, width=1 * cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

def coord(x, y, unit=1):
    x, y = x * unit, height - y * unit
    return x, y

def generar_croq(ubigeo,aeut):
    print "croquis"
    MARGIN_SIZE = 17 * mm
    PAGE_SIZE = A4
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename="+ubigeo+"001"+str(aeut.aeu_final)+".pdf"
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

    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=70,
                            leftMargin=70,
                            topMargin=60,
                            bottomMargin=18,
                            )
    h1 = PS(
        name='Heading1',
        fontSize=9,
        leading=16)
    h2 = PS(
        name='Normal',
        fontSize=7,
        leading=16)

    h3 = PS(
        name='Normal',
        fontSize=6,
        leading=16,
        alignment = TA_CENTER)

    h4 = PS(
        name='Normal',
        fontSize=6,
        leading=16)

    story = []

    distrito = Distrito.objects.get(ubigeo = ubigeo)  # ubigeo

    # if aeut!=None and aeut!='':
    cond = Aeus.objects.filter(ubigeo = distrito.ubigeo, zona = '00100')
    # elif ubigeo!=None and ubigeo!='':
    #     cond = Aeus.objects.filter(ubigeo=distrito.ubigeo, zona = '00100', aeu_final = aeut)
    #
    # if aeut!=None and aeut!='':
    total = str(Aeus.objects.filter(ubigeo = distrito.ubigeo, zona = '00100').count())
    # elif ubigeo!= None and ubigeo!='':
    #     total = str(Aeus.objects.filter(ubigeo=distrito.ubigeo, zona = '00100', aeu_final = aeut).count())
    x = 0
    rango_equivalencia = [[1, 'A'],[2, 'B'],[3, 'C'],[4, 'D'],[5, 'E'],[6, 'F'],[7, 'G'],[8, 'H'],[9, 'I'],
                          [10, 'J'],[11, 'K'],[12, 'L'],[13, 'M'],[14, 'N'],[15, 'O'],[16, 'P'],[17, 'Q']
                          ]

    for aeu in cond:
        x=x+1
        y = x

        if aeu.seccion < 10:
            secc = Paragraph("00" + str(aeu.seccion), h1)
        elif aeu.seccion > 9 or aeu.seccion < 100:
            secc = Paragraph("0" + str(aeu.seccion), h1)
        else:
            secc = Paragraph(str(aeu.seccion), h1)

        if aeu.aeu_final < 10:
            aeus = Paragraph("00" + str(aeu.aeu_final), h1)
        elif aeu.aeu_final > 9 or aeu.aeu_final < 100:
            aeus = Paragraph("0" + str(aeu.aeu_final), h1)
        else:
            aeus = Paragraph(str(aeu.aeu_final), h1)

        zona_temp = aeu.zona[0:3]
        zona_int = int(aeu.zona[3:])
        zona_int_eq = ""
        for el in rango_equivalencia:
            if (el[0] == zona_int):
                zona_int_eq = el[1]

        zona_temp = zona_temp + str(zona_int_eq)

        data_croq = [
            ['', '', '', '','', Paragraph('<strong>Doc. CPV</strong>',h4)],
            [Paragraph('<strong>A. UBICACION GEOGRAFICA</strong>', h1), '', '', '',Paragraph('<strong>B. UBICACION CENSAL</strong>', h1), ''],
            [Paragraph('<strong>DEPARTAMENTO</strong>', h1),
             Paragraph(str(distrito.ccdd.ccdd), h1),
             Paragraph(str(distrito.ccdd.departamento), h1), '',
             Paragraph('<strong>ZONA Nº</strong>', h1),
             Paragraph(zona_temp, h1)],
            [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(distrito.ccpp, h1), Paragraph(distrito.cod_prov.provincia, h1), '',Paragraph(str('<strong>SECCION Nº</strong>'), h1), secc],
            [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph(distrito.ccdi, h1), Paragraph(distrito.distrito, h1), '',Paragraph('<strong>A.E.U. Nº</strong>', h1), aeus],
            [Paragraph('<strong>CENTRO POBLADO</strong>', h1), Paragraph(aeu.llave_ccpp.nomccpp, h1), '', '', '', ''],
            [Paragraph('<strong>CATEGORIA CENTRO POBLADO</strong>', h1), Paragraph('CIUDAD', h1), '', '',Paragraph('<strong>C. TOTAL DE VIVIENDAS DEL A.E.U.</strong>', h1), Paragraph(str(int(aeu.sum_viv_ae)), h1)],
        ]

        tables_croq = Table(data_croq, colWidths=[6 * cm, 1 * cm, 3.5 * cm, 0.1 * cm, 6 * cm, 1.5 * cm])
        #t_aeu = Table(all_aeu, colWidths=[6 * cm, 1 * cm, 3.5 * cm, 0.1 * cm, 6 * cm, 1.5 * cm])

        tables_croq.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (5, 0), colors.black),
            ('ALIGN', (4, 0), (5, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 1), (2, 6), 1, colors.black),
            ('GRID', (4, 1), (5, 4), 1, colors.black),
            ('GRID', (-2, -1), (-1, -1), 1, colors.black),
            ('SPAN', (0, 1), (2, 1)),
            ('SPAN', (4, 1), (5, 1)),
            ('SPAN', (1, 5), (2, 5)),
            ('SPAN', (1, 6), (2, 6)),
            ('BACKGROUND', (4, 1), (5, 5), colors.white),
            ('BACKGROUND', (0, 1), (-1, 1), colors.lightskyblue),
            ('BACKGROUND', (0, 1), (0, 6), colors.lightskyblue),
            ('BACKGROUND', (4, 1), (4, 4), colors.lightskyblue),
            ('BACKGROUND', (4, 6), (4, 6), colors.lightskyblue)
        ]))
        t1_c = Paragraph(
            "<strong>INSTITUO NACIONAL DE ESTADISTICA E INFORMATICA</strong>",
            styleTitle)
        t2_c = Paragraph(
            "<strong>CENSOS NACIONALES 2017: XII DE POBLACION, VII DE VIVIENDA</strong>",
            styleTitle)
        # story.append(Spacer(0, 001 * mm))
        t3_c = Paragraph("<strong>Y III DE COMUNIDADES INDIGENAS</strong>", styleTitle)
        fichero_imagen_inei = 'Reporte/Img/inei.png'
        imagen_logo_inei = Image(os.path.realpath(fichero_imagen_inei), width=50, height=50)

        P2 = Paragraph('', styleBH)
        fichero_imagen = 'Reporte/Img/escudo.png'
        imagen_logo = Image(os.path.realpath(fichero_imagen), width=50, height=50)

        t = Table(
            data=[
                ['', t1_c, ''],
                [[imagen_logo, P2], t2_c, [imagen_logo_inei, P2]],
                ['', t3_c, '']
            ],
            colWidths=[2 * cm, 13 * cm, 2 * cm],
            style=[
                ('GRID', (1, 1), (-2, -2), 1, colors.white),

                ('GRID', (0, 0), (-1, -1), 0.5, colors.white),

            ]
        )
        story.append(t)
        story.append(Spacer(0, 3 * mm))
        story.append(Paragraph("<strong>CROQUIS DEL ÁREA DE EMPADRONAMIENTO URBANO</strong>", styleTitle))
        story.append(Spacer(0, 1 * mm))
        story.append(tables_croq)
        story.append(Spacer(0, 2 * mm))

        viv_urb = ViviendaUrbana.objects.filter(Q(ubigeo=distrito.ubigeo), Q(zona= aeu.zona), Q(aeu_final= aeu.aeu_final)).order_by('or_viv_aeu')

        P2 = Paragraph('', styleBH)
        fichero_imagen = 'Reporte/Croquis/Zona'+ubigeo+'00100'+'/Imagen'+ubigeo+'00100'+str(aeut.aeu_final)+'.jpg'
        imagen_croquis = Image(os.path.realpath(fichero_imagen), width=16 * cm, height=14.5 * cm)

        data_img = [
            [Paragraph(e, h3) for e in ["<strong>Imagen de Croquis</strong>"]],
         ]
        cr = Table(
            data=[
                [imagen_croquis]
            ],
            colWidths=[18 * cm],
            style=[
                ('GRID', (1, 1), (-2, -2), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]
        )

        story.append(cr)

        Z1_croq = Paragraph("<strong>OBSERVACIONES: ...................................................................."
                       "..........................................................................................."
                       "..........................................................................................."
                       "..........................................................................................."
                       "..........................................................................................."
                       "..........................................................................................."
                       "..........................................................................................."
                       "..........................................................................................."
                       ".........................................</strong>", h2)

        table_obs_croq = Table(
            data=[
                [Z1_croq]
            ],
            colWidths=[18.3 * cm],
            style=[
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]
        )

        p_croq = Paragraph(str(y)+" - "+total, h2)
        extra = Paragraph("-", h2)

        p_page = Table(
            data=[
                [extra, p_croq]
            ],
            colWidths=[17 * cm, 2.3 * cm],
            style=[
                ('GRID', (0, 0), (-1, -1), 1, colors.white),
                ('ALIGN', (0, 0), (1, 0), 'RIGHT'),
            ]
        )
        story.append(Spacer(0, 1 * mm))
        story.append(Spacer(0, 2 * mm))
        story.append(table_obs_croq)
        story.append(Spacer(0, 2 * mm))
        story.append(p_page)

        story.append(PageBreak())

    doc.build(story)
    obj=buff.getvalue()
    buff.close()
    return obj

