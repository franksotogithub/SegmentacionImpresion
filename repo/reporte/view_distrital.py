# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse

# from reportlab.pdfgen.canvas import Canvas
# !/usr/bin/env python

from reportlab.pdfgen import canvas
from django.db.models import Q
#from reporte.reportes_models import *
from reportes_models import *

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

from reportlab.graphics.barcode import code39

width, height = A4

def get_image(path, width=1 * cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


def coord(x, y, unit=1):
    x, y = x * unit, height - y * unit
    return x, y


def generar_distrito(request, ubigeo):
    print "generar_pdf"
    MARGIN_SIZE = 17 * mm
    PAGE_SIZE = A4

    # zona_conv = str(zonaq).zfill(3) + "00"
    # secc_conv = str(seccionq).zfill(3) + "00"


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=" + ubigeo +  ".pdf"
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
    # destino = "Secciones/" + str(ubigeo) + str(zona_conv)+".pdf"
    # doc2 = SimpleDocTemplate(destino, pagesize=A4,
    #                          rightMargin=70,
    #                          leftMargin=70,
    #                          topMargin=0.5 *cm,
    #                          bottomMargin=0.5 *cm, )

    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=65,
                            leftMargin=65,
                            topMargin=0.5 * cm,
                            bottomMargin=0.5 * cm,
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
        leading=16)

    h3 = PS(
        name='Normal',
        fontSize=7,
        leading=16,
        alignment=TA_CENTER)

    h4 = PS(
        name='Normal',
        fontSize=6,
        leading=16)

    h5 = PS(
        name='Normal',
        fontSize=8,
        leading=16,
        alignment=TA_CENTER)

    h_obser = PS(
        name='Normal',
        fontSize=8,
        leading=16
    )

    h_sub_tile = PS(
        name='Heading1',
        fontSize=10,
        leading=14,
        alignment=TA_CENTER
    )

    h_bar = PS(
        name='Normal',
        fontSize=7,
        leading=14,
        alignment=TA_CENTER
    )

    h_res = PS(
        name='Normal',
        fontSize=7,
        leading=7,
        alignment=TA_RIGHT
    )

    story = []

    # Acà van consultas para los 'for'
    distrito = Distrito.objects.get(ubigeo=ubigeo)

    cond = v_ReporteSecciones.objects.filter(ubigeo=ubigeo)

    total_secc = str(v_ReporteSecciones.objects.filter(ubigeo=ubigeo).values_list('seccion', flat=True).distinct().count())

    total_aeus = str(v_ReporteSecciones.objects.filter(ubigeo=ubigeo).count())

    rango_equivalencia = [[1, 'A'], [2, 'B'], [3, 'C'], [4, 'D'], [5, 'E'], [6, 'F'], [7, 'G'], [8, 'H'], [9, 'I'],
                          [10, 'J'], [11, 'K'], [12, 'L'], [13, 'M'], [14, 'N'], [15, 'O'], [16, 'P'], [17, 'Q'],
                          [18, 'R'],
                          [19, 'S'], [20, 'T'], [21, 'U'], [22, 'V'], [23, 'W'], [24, 'X'], [25, 'Y'], [26, 'Z']
                          ]

    Z1 = Paragraph(
        "<strong>OBSERVACIONES: .............................................................................."
        "....................................................................................................."
        "....................................................................................................."
        "....................................................................................................."
        "....................................................................................................."
        "....................................................................................................."
        "................................................................................</strong>", h_obser)

    table_obs = Table(
        data=[
            [Z1]
        ],
        colWidths=[18.8 * cm],
        rowHeights=[2 * cm],
        style=[
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]
    )

    tota_viv = 0

    # string = str(ubigeo) + "001010"
    # st = code39.Extended39(string)
    #
    # bar_string = Paragraph(string, h_bar)
    #
    # pi = Paragraph("", h2)
    # st_b = st
    #
    # table_bar = Table(
    #     data=[
    #         [pi, st_b],
    #         ['', bar_string]
    #     ],
    #     colWidths=[15 * cm, 4 * cm],
    #     style=[
    #         ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    #     ]
    # )


    total = 0
    x = 0

    aeusi = v_ReporteResumenDistrito.objects.filter(Q(ubigeo=ubigeo))

    total_zona = int(v_ReporteResumenDistrito.objects.filter(Q(ubigeo=ubigeo)).count())

    for aeu in cond:
        # string = "02060100100"
        # st = code39.Extended39(string)
        # story.append(st)

        secc = str(aeu.seccion).zfill(3)
        aeus = str(aeu.aeu_final).zfill(3)

        destino = "Distritos/" + str(ubigeo) + ".pdf"

        doc2 = SimpleDocTemplate(destino, pagesize=A4,
                                 rightMargin=70,
                                 leftMargin=70,
                                 topMargin=0.5 * cm,
                                 bottomMargin=0.5 * cm, )

        tota_viv = tota_viv + int(aeu.cant_viv)

        # string = str(ubigeo) + "001010"
        # st = code39.Extended39(string)
        #
        # pi = Paragraph("-", h2)
        # st_b = st

        # table_bar = Table(
        #    data=[
        #        [pi, st_b]
        #    ],
        #    colWidths=[14 * cm, 5 * cm]
        # )

        # story.append(table_bar)
    # zona_temp = 0

    aeu_tot = str(total_aeus).zfill(3)
    secc_tot = str(total_secc).zfill(3)

    nombreccpp = Ccpp.objects.filter(codccpp=aeu.codccpp).values('nomccpp')
    data = [
        # ['', '', '', '', '', Paragraph('<strong>Doc. CPV</strong>', h4)],
        [Paragraph('<strong>A. UBICACIÓN GEOGRÁFICA</strong>', h11), '', '','','',''],
        [Paragraph('<strong>DEPARTAMENTO</strong>', h1), Paragraph(str(distrito.ccdd.ccdd), h_center), Paragraph(str(distrito.ccdd.departamento), h1),'','','' ],
        [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(distrito.ccpp, h_center), Paragraph(distrito.cod_prov.provincia, h1),'','',''],
        [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph(distrito.ccdi, h_center), Paragraph(str(distrito.distrito).decode('latin-1'), h1),'','',''],
        # [Paragraph('<strong>CENTRO POBLADO</strong>', h1), Paragraph(nombreccpp[0]['nomccpp'], h1), ''],
        # [Paragraph('<strong>CATEGORIA DEL CENTRO POBLADO</strong>', h1), Paragraph('CIUDAD', h1), ''],
    ]

    tables = Table(data, colWidths=[3 * cm, 2 * cm, 7 * cm, 4.8 * cm, 0.5 * cm, 1.5 * cm, 2.3 * cm, 2 * cm],
                   rowHeights=[ 0.6 * cm, 0.6 * cm, 0.6 * cm, 0.6 * cm])

    tables.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (2, 0), colors.black),
        # ('ALIGN', (4, 0), (5, 0), 'RIGHT'),
        # ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (2, 3), 1, colors.black),
        # ('GRID', (2, 1), (2, 3), 1, colors.black),
        # ('GRID', (-2, -1), (-1, -1), 1, colors.black),
        ('SPAN', (0, 0), (2, 0)),
        # ('SPAN', (1, 4), (2, 4)),
        # ('SPAN', (1, 5), (2, 5)),
        # ('SPAN', (1, 6), (2, 6)),
        # ('BACKGROUND', (4, 1), (5, 5), colors.white),
        ('BACKGROUND', (0, 1), (0, 3), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
        ('BACKGROUND', (0, 0), (2, 0), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
        # ('BACKGROUND', (4, 1), (4, 4), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
        # ('BACKGROUND', (4, 6), (4, 6), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255))
    ]))

    t2 = Paragraph( "CENSOS NACIONALES 2017: XII DE POBLACIÓN, VII DE VIVIENDA",h_sub_tile)

    t3 = Paragraph("Y III DE COMUNIDADES INDÍGENAS", h_sub_tile)

    fichero_imagen_inei = 'Reporte/Img/inei.png'
    imagen_logo_inei = Image(os.path.realpath(fichero_imagen_inei), width=50, height=40)

    P2 = Paragraph('', styleBH)
    fichero_imagen = 'Reporte/Img/escudo.png'
    imagen_logo = Image(os.path.realpath(fichero_imagen), width=50, height=50)

    t = Table(
        data=[

            [[imagen_logo, P2], t2, [imagen_logo_inei, P2]],
            ['', t3, '']
        ],
        colWidths=[2 * cm, 14 * cm, 2 * cm],
        style=[
            ('GRID', (1, 1), (-2, -2), 1, colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
        ]
    )

    # story.append(table_bar)
    story.append(t)
    story.append(Spacer(0, 5 * mm))
    story.append(Paragraph("<strong>LISTADO DISTRITAL DE ZONAS CENSALES, SECCIONES Y AREAS DE EMPADRONAMIENTO URBANO</strong>",styleTitle))
    story.append(Spacer(0, 5 * mm))
    story.append(tables)
    story.append(Spacer(0, 3 * mm))

    # aeusi = v_ReporteResumenDistrito.objects.filter(Q(ubigeo=ubigeo))
    total_zon = 0
    total_secc = 0
    tatal_aeus = 0
    total_mzns = 0
    total_vivis = 0
    total_prom_aeu = 0
    total_prom_mnz = 0

    for aeusis in aeusi:
        total_zon = total_zon + 1
        total_secc = total_secc + int(aeusis.cant_secciones)
        tatal_aeus = tatal_aeus + int(aeusis.cant_aeus)
        total_mzns = total_mzns + int(str(aeusis.cant_mzs))
        total_vivis = total_vivis + int(str(aeusis.cant_viv))
        total_prom_aeu = total_prom_aeu + float(str(aeusis.prom_viv_aeu))
        total_prom_mnz = total_prom_mnz + float(str(aeusis.prom_mzs_aeu))


    t_prom_aeu = str(total_prom_aeu/total_zona)[0:4]
    t_prom_zona = str(total_prom_mnz/total_zona)[0:3]

    obs_data = [
        [Paragraph(e, h3) for e in ["<strong>B.  INFORMACIÓN DEL DISTRITO</strong>",
                                    "",
                                    "",
                                    ]],
        [Paragraph(e, h3) for e in ["<strong>ZONA Nº</strong>",
                                    "<strong>NOMBRE DEL CENTRO POBLADO</strong>",
                                    "<strong>CATEGORÍA DEL CENTRO POBLADO</strong>",

                                    "<strong>Nº DE SECCIONES CENSALES</strong>",
                                    "<strong>Nº DE AEU</strong>",
                                    # PROM DE VIV X AEU
                                    "<strong>Nº DE MANZANAS</strong>",
                                    # PROM DE MZ.X AEU
                                    "<strong>Nº DE VIVIENDAS</strong>"
                                    ]]
        # ,
        # [Paragraph(e, h3) for e in ["<strong>Total</strong>",
        #                             str(''),
        #                             str(''),
        #                             str(total_secc),
        #                             str(tatal_aeus),
        #                             str(total_mzns),
        #                             str(total_vivis)
        #                             ]]
    ]
    c = Table(obs_data, colWidths=[2.2 * cm, 3.7 * cm, 4.1 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm])

    c.setStyle(TableStyle(
        [
            ('GRID', (1, 1), (-2, -2), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            # ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            ('BACKGROUND', (0, 0), (-1, 2), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            ('SPAN', (0, 0), (6, 0)),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
        ]
    ))
    story.append(c)

    # aeusi = v_ReporteResumenDistrito.objects.filter(Q(ubigeo=distrito.ubigeo))

    # for aeusin in aeusi:
    #
    #     zona_temp = aeusin.zona[0:3]
    #     zona_int = int(aeusin.zona[3:])
    #     zona_int_eq = ""
    #
    # for el in rango_equivalencia:
    #     if (el[0] == zona_int):
    #         zona_int_eq = el[1]

    # zona_temp = zona_temp + str(zona_int_eq)

    zona_tot = 0
    total_page = 1

    for aeusis in aeusi:
        x = x + 1
        y = x


        # secc = str(aeusis.seccion).zfill(3)
        # aeus = str(aeusis.aeu_final).zfill(3)
        # mzn = str(aeusis.manzanas).zfill(3)

        # for el in rango_equivalencia:
        #     if (el[0] == zona_int):
        #         zona_int_eq = el[1]
        #
        # zona_temp = zona_temp + str(zona_int_eq)
        zona_temp = aeusis.zona[0:3]
        zona_int = int(aeusis.zona[3:])
        zona_int_eq = ""

        for el in rango_equivalencia:
            if (el[0] == zona_int):
                zona_int_eq = el[1]

        zona_temp_du = zona_temp + str(zona_int_eq)

        table2 = [(
            str(zona_temp_du).decode('latin-1'),
            str(aeusis.nomccpp).decode('latin-1'),
            str('CIUDAD').decode('latin-1'),

            str(aeusis.cant_secciones).decode('latin-1'),
            str(aeusis.cant_aeus).decode('latin-1'),
            str(aeusis.cant_mzs).decode('latin-1'),
            str(aeusis.cant_viv).decode('latin-1')
        )
        ]
        s = Table(table2,colWidths=[ 2.2 * cm, 3.7 * cm, 4.1 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm])

        s.setStyle(TableStyle(
            [
                ('GRID', (1, 1), (-2, -2), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ]
        ))
        story.append(s)

    data_res = [

        ['', Paragraph('<strong>C. RESUMEN DEL DISTRITO</strong>', h11), '', ''],
        ['', Paragraph('<strong>TOTAL DE ZONAS</strong>', h1),Paragraph(str(total_zon), h_res), ''],
        ['', Paragraph('<strong>TOTAL DE SECCIONES</strong>', h1), Paragraph(str(total_secc), h_res), ''],
        ['', Paragraph('<strong>TOTAL DE A.E.U.</strong>', h1),Paragraph(str(tatal_aeus), h_res), ''],
        ['', Paragraph('<strong>TOTAL DE MANZANAS</strong>', h1), Paragraph(str(total_mzns), h_res), ''],
        ['',Paragraph('<strong>TOTAL DE VIVIENDAS DEL DISTRITO</strong>', h1),Paragraph(str(total_vivis), h_res),''],
    ]

    tables_res = Table(data_res, colWidths=[3 * cm, 6 * cm, 2.5 * cm, 3 * cm],
                   rowHeights=[0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4 * cm])

    tables_res.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (2, 0), colors.black),
        # ('ALIGN', (4, 0), (5, 0), 'RIGHT'),
        # ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (1, 0), (2, 5), 1, colors.black),
        ('ALIGN', (2, 1), (2, 5), 'LEFT'),
        # ('GRID', (2, 1), (2, 3), 1, colors.black),
        # ('GRID', (-2, -1), (-1, -1), 1, colors.black),
        ('SPAN', (1, 0), (2, 0)),
        # ('SPAN', (1, 4), (2, 4)),
        # ('SPAN', (1, 5), (2, 5)),
        # ('SPAN', (1, 6), (2, 6)),
        # ('BACKGROUND', (4, 1), (5, 5), colors.white),
        ('BACKGROUND', (1, 0), (2, 0), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
        # ('BACKGROUND', (0, 0), (2, 0), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
        # ('BACKGROUND', (4, 1), (4, 4), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
        # ('BACKGROUND', (4, 6), (4, 6), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255))
    ]))

    story.append(Spacer(0, 2.5 * cm))

    story.append(tables_res)

    if (PageBreak()):
        total_page = total_page + 1
        # story.append(Paragraph("<strong>Hice salto</strong>", styleTitle))
        # story.append(c)
        # story.append(Spacer(0, 15 * cm))

    p = Paragraph(str(1) + " - " + str(1), h2)
    extra = Paragraph("-", h2)

    p_page = Table(
        data=[
            [extra, p]
        ],
        colWidths=[19 * cm, 2.3 * cm],
        style=[
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ('ALIGN', (0, 0), (1, 0), 'RIGHT'),
        ]
    )

    story.append(Spacer(0, 7.5 * cm))
    # story.append(table_obs)
    story.append(Spacer(0, 1 * mm))
    story.append(p_page)
    #
    # story.append(PageBreak())
    doc2.build(story)
    doc.build(story)
    response.write(buff.getvalue())
    buff.close()
    return response

def generar_distrito_lote(request):

    lista_distrito = []

    lista_distrito.append('090301')
    lista_distrito.append('090208')
    lista_distrito.append('050619')
    lista_distrito.append('050617')
    lista_distrito.append('050601')
    lista_distrito.append('030602')
    lista_distrito.append('022001')
    lista_distrito.append('021509')
    # distrito = Distrito.objects.get(ubigeo=ubig)
    # total = int(Aeus.objects.filter(ubigeo=distrito.ubigeo).values_list('zona', flat=True).distinct().count())
    # total = int(Aeus.objects.filter(ubigeo=distrito.ubigeo, zona=zonag ).values_list('seccion', flat=True).distinct().count())
    # total = int(str(v_ReporteSecciones.objects.filter(ubigeo=ubig).values_list('zona', flat=True).distinct().count()))
    totales = 10
    lista = []
    c = 0
    tam_distrito = 7
    for ubigeos in range(tam_distrito):
        total = int(str(v_ReporteSecciones.objects.filter(ubigeo=lista_distrito[ubigeos]).values_list('zona', flat=True).distinct().count()))
        generar_distrito(request, lista_distrito[ubigeos])
        for zonita in range(total):
            # c=zonita+1
            lista.append(zonita+1)
            # generar_urbana(request,ubig)
            # lista.append(zona+1)
    return HttpResponse(lista)
    return True