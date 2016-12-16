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
import barcode

width, height = A4

def get_image(path, width=1 * cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


def coord(x, y, unit=1):
    x, y = x * unit, height - y * unit
    return x, y


def generar_pdf(request, ubigeo,zonal, aeut):
    print "Se va a generar el PDF de Ubigeo: " + str(ubigeo) + " de zona: "+ str(zonal) + " con aeu: "+ str(aeut)
    MARGIN_SIZE = 17 * mm
    PAGE_SIZE = A4
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=" + ubigeo + "001" + str(aeut) + ".pdf"

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
    # destino = "Lista/" + str(ubigeo)+"00100"+ str(aeut)+ ".pdf"
    #
    # doc2 = SimpleDocTemplate(destino, pagesize=A4,
    #                          rightMargin=70,
    #                          leftMargin=70,
    #                          topMargin=0.5 *cm,
    #                          bottomMargin=0.5 *cm, )
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

    story = []

    #distrito = Distrito.objects.get(ubigeo=ubigeo)  # ubigeo

    # vivi = ViviendaUrbana.objects.get(ubigeo=distrito.ubigeo, zona='00100', aeu_final=aeut)

    # cond = Esp_Aeus.objects.filter(ubigeo=ubigeo, zona=zonal, aeu_final=aeut)  # v_ReporteCabViviendas

    cond = v_ReporteCabViviendas.objects.filter(ubigeo=ubigeo, zona=zonal, aeu_final=aeut)

    rango_equivalencia = [[1, 'A'], [2, 'B'], [3, 'C'], [4, 'D'], [5, 'E'], [6, 'F'], [7, 'G'], [8, 'H'], [9, 'I'],
                          [10, 'J'], [11, 'K'], [12, 'L'], [13, 'M'], [14, 'N'], [15, 'O'], [16, 'P'], [17, 'Q'], [18, 'R'],
                          [19, 'S'], [20, 'T'], [21, 'U'], [22, 'V'], [23, 'W'], [24, 'X'], [25, 'Y'], [26, 'Z']
                          ]

    # Z1 = Paragraph("<strong>OBSERVACIONES: .............................................................................."
    #                "....................................................................................................."
    #                "....................................................................................................."
    #                "....................................................................................................."
    #                "....................................................................................................."
    #                "....................................................................................................."
    #                "................................................................................</strong>", h_obser)

    # table_obs = Table(
    #     data=[
    #         [Z1]
    #     ],
    #     colWidths=[18.8 * cm],
    #     rowHeights=[2 * cm],
    #     style=[
    #         ('GRID', (0, 0), (-1, -1), 1, colors.black)
    #     ]
    # )

    Z2 = Paragraph("<strong>EMPADRONADOR</strong>", h5)

    Z3 = Paragraph("<strong>Todas las viviendas que estén dentro de los límites de tu A.E.U. deben ser empadronadas. Debes tener<br/>cuidado de no omitir ninguna vivienda</strong>",h5)

    # table_empa_cuerp = Table(
    #     data=[
    #         [Z2],
    #         [Z3]
    #     ],
    #     colWidths=[18.8 * cm],
    #     rowHeights=[0.7 * cm, 1.5 * cm],
    #     style=[
    #         ('GRID', (0, 0), (0, 0), 1, colors.black),
    #         ('GRID', (0, 1), (0, 1), 1, colors.black),
    #         ('ALIGN', (0, 0), (0, 0), 'CENTER')
    #     ]
    # )

    x = 0

    for aeu in cond:
        x = x + 1

        lista_distritos = []
        lista_distritos.append(ubigeo)

        listin = []
        secc = str(aeu.seccion).zfill(3)
        aeus = str(aeu.aeu_final).zfill(3)
        aeu_conv = str(aeut).zfill(3)
        tam_dis = 1
        # destino = "Lista/" + str(ubigeo) + zonal + str(secc)+str(aeut) + ".pdf"
        #
        # doc2 = SimpleDocTemplate(destino, pagesize=A4,
        #                          rightMargin=70,
        #                          leftMargin=70,
        #                          topMargin=0.5 * cm,
        #                          bottomMargin=0.5 * cm, )

        lista_zonas = []
        for ubigein in range(tam_dis):

            if os.path.exists("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein])) == False:
                os.mkdir("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein]))

            total_zonas = int(str(Esp_Aeus.objects.filter(ubigeo=lista_distritos[ubigein]).values_list('zona',flat=True).distinct().count()))
            total_zonales = Esp_Aeus.objects.filter(ubigeo=lista_distritos[ubigein]).values_list('zona', flat=True)
            cuchi = list(set(total_zonales))
            lista_zonas.append(total_zonas)

            for zona_t in range(total_zonas):

                listin.append(str(lista_distritos[ubigein]) + ": " + zonal + "<br/>")
                if os.path.exists("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein]) + "\\" + cuchi[zona_t]) == False:
                    os.mkdir("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein]) + "\\" + cuchi[zona_t])
        destino="\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(ubigeo) + "\\" + zonal + "\\" + str(ubigeo) + zonal + str(aeu.seccion_convert) + str(aeu.aeu_convert) + ".pdf"

        doc2 = SimpleDocTemplate(destino, pagesize=A4,
                                 rightMargin=70,
                                 leftMargin=70,
                                 topMargin=0.5 * cm,
                                 bottomMargin=0.5 * cm, )

        p = Paragraph(str(1) + " - " + str(1), h2)
        extra = Paragraph("-", h2)

        p_page = Table(
            data=[
                [extra, p]
            ],
            colWidths=[17 * cm, 2.3 * cm],
            style=[
                ('GRID', (0, 0), (-1, -1), 1, colors.white),
                ('ALIGN', (0, 0), (1, 0), 'RIGHT'),
            ]
        )

        string = str(ubigeo)+zonal+str(secc)+str(aeut)
        st = code39.Extended39(string)

        pi = Paragraph("-", h2)
        st_b = st
        #bar_string = Paragraph(string, h_bar)

        # table_bar = Table(
        #     data = [
        #         [pi, st_b],
        #         ['', bar_string]
        #     ],
        #     colWidths=[13 * cm, 5 * cm],
        #     style=[
        #         ('ALIGN', (0, 0), (-1, -1),'CENTER')
        #     ]
        # )

        #story.append(table_bar)

        #zona_temp = aeu.zona[0:3]
        #zona_int = int(aeu.zona[3:])
        #zona_int_eq = ""

        #for el in rango_equivalencia:
        #    if (el[0] == zona_int):
        #        zona_int_eq = el[1]

        #zona_temp = str(zona_temp) + str(zona_int_eq)

        data = [
            ['', '', '', '', '', Paragraph('<strong>Doc. CPV</strong>', h4)],
            [Paragraph('<strong>A. UBICACION GEOGRAFICA</strong>', h11), '', '', '',
             Paragraph('<strong>B. UBICACION CENSAL</strong>', h11), ''],
            [Paragraph('<strong>DEPARTAMENTO</strong>', h1),Paragraph(str(aeu.ccdd), h_center),
             Paragraph(str(aeu.departamento), h1), '',
             Paragraph('<strong>ZONA Nº</strong>', h1),Paragraph(str(aeu.zona_convert), h_center)],
            [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(aeu.ccpp, h_center),
             Paragraph(aeu.provincia, h1), '', Paragraph(str('<strong>SECCION Nº</strong>'), h1), Paragraph(aeu.seccion_convert, h_center)],
            [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph(aeu.ccdi, h_center), Paragraph(aeu.distrito, h1),
             '', Paragraph('<strong>A.E.U. Nº</strong>', h1), Paragraph(aeu.aeu_convert, h_center)],
            [Paragraph('<strong>CENTRO POBLADO</strong>', h1), Paragraph(aeu.codccpp, h1), Paragraph(aeu.nomccpp, h1), '', '', ''],
            [Paragraph('<strong>CATEGORIA DEL CENTRO POBLADO</strong>', h1), Paragraph('CIUDAD', h1), '', '',
             Paragraph('<strong>C. TOTAL DE VIVIENDAS<br/>DEL A.E.U.</strong>', h1),Paragraph(str(int(aeu.cant_viv)), h_center)],
        ]

        tables = Table(data, colWidths=[3.7 * cm, 1 * cm, 8.1 * cm, 0.3 * cm, 4.7 * cm, 2 * cm],
                       rowHeights=[0.4 * cm, 0.4  * cm, 0.4  * cm, 0.4  * cm, 0.4  * cm, 0.4  * cm, 0.7  * cm])

        tables.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (5, 0), colors.black),
            ('ALIGN', (4, 0), (5, 0), 'RIGHT'),
            ('ALIGN', (1, 2), (1, 4), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('GRID', (0, 1), (2, 6), 1, colors.black),
            ('GRID', (4, 1), (5, 4), 1, colors.black),
            ('GRID', (-2, -1), (-1, -1), 1, colors.black),
            ('SPAN', (0, 1), (2, 1)),
            ('SPAN', (4, 1), (5, 1)),
            ('SPAN', (2, 5), (3, 5)),
            ('SPAN', (1, 6), (2, 6)),
            ('BACKGROUND', (0, 1), (0, 6), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('BACKGROUND', (0, 1), (2, 1), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('BACKGROUND', (4, 1), (5, 1), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('BACKGROUND', (4, 1), (4, 4), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('BACKGROUND', (4, 6), (4, 6), colors.Color(219.0/255,229.0/255,241.0/255))
        ]))

        t1 = Paragraph("CENSOS NACIONALES 2017: XII DE POBLACIÓN, VII DE VIVIENDA<br/>Y III DE COMUNIDADES INDÍGENAS",h_sub_tile)
        t1_sub = Paragraph("<strong>LISTADO DE VIVIENDAS DEL AREA DE EMPADRONAMIENTO URBANO</strong>", h_sub_tile_2)

        fichero_imagen_inei = 'Reporte/Img/inei.png'
        imagen_logo_inei = Image(os.path.realpath(fichero_imagen_inei), width=50, height=50)

        P2 = Paragraph('', styleBH)
        fichero_imagen = 'Reporte/Img/escudo.png'
        imagen_logo = Image(os.path.realpath(fichero_imagen), width=50, height=50)

        t1_croq = Paragraph("<strong>CROQUIS DEL ÁREA DE EMPADRONAMIENTO URBANO</strong>", h_sub_tile_2)
        t = Table(
            data=[

                [[imagen_logo, P2], t1, [imagen_logo_inei, P2]],
                ['', t1_croq, '']
            ],
            colWidths=[2 * cm, 14 * cm, 2 * cm],
            style=[
                ('GRID', (1, 1), (-2, -2), 1, colors.white),
                # ('SPAN', (0, 1), (2, 1)),
                # ('BOX', (0, 0), (1, -1), 2, colors.black),
                # ('LINEABOVE', (1, 2), (-2, 2), 1, colors.blue),
                # ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                # ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                # ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                # ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                # ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.white),

            ]
        )

        obs_data = [
            [Paragraph(e, h3) for e in ["<strong>Viv Nº</strong>",
                                        "<strong>Mz. Nº</strong>",
                                        "<strong>Or. Reg.</strong>",
                                        "<strong>Frent. Nº</strong>",
                                        "<strong>DIRECCIÓN DE LA VIVIENDA</strong>",
                                        "", "", "", "", "", "", "", "",
                                        "<strong>Nombres y Apellidos del JEFE DE HOGAR</strong>"]],
            [Paragraph(e, h3) for e in ["", "", "", "",
                                        "<strong>Tipo de Via</strong>",
                                        "<strong>Nombre de Via</strong>",
                                        "<strong>Nº de Puerta</strong>",
                                        "<strong>Block N°</strong>",
                                        "<strong>Man-<br/>zana Nº</strong>",
                                        "<strong>Lote Nº</strong>",
                                        "<strong>Piso Nº</strong>",
                                        "<strong>Inter. Nº</strong>",
                                        "<strong>Km. Nº</strong>",
                                        ""]],
            [Paragraph(e, h3) for e in ["<strong>(1)</strong>",
                                        "<strong>(2)</strong>",
                                        "<strong>(3)</strong>",
                                        "<strong>(4)</strong>",
                                        "<strong>(5)</strong>",
                                        "<strong>(6)</strong>",
                                        "<strong>(7)</strong>",
                                        "<strong>(8)</strong>",
                                        "<strong>(9)</strong>",
                                        "<strong>(10)</strong>",
                                        "<strong>(11)</strong>",
                                        "<strong>(12)</strong>",
                                        "<strong>(13)</strong>",
                                        "<strong>(14)</strong>"]],
         ]
        c = Table(obs_data,
                  colWidths=[0.8 * cm, 0.9 * cm, 1 * cm, 1.2 * cm, 1.2 * cm, 2.5 * cm, 1.2 * cm, 1.1 * cm, 1 * cm, 1 * cm, 1 * cm,
                             1.1 * cm, 0.9 * cm, 4.9 * cm])

        c.setStyle(TableStyle(
            [
                ('GRID', (1, 1), (-2, -2), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                #('VALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('BACKGROUND', (0, 0), (-1, -1), colors.Color(219.0/255,229.0/255,241.0/255)),
                ('BACKGROUND', (0, 0), (-1, -1), colors.Color(219.0/255,229.0/255,241.0/255)),
                ('SPAN', (4, 0), (12, 0)),
                ('SPAN', (0, 0), (0, 1)),
                ('SPAN', (1, 0), (1, 1)),
                ('SPAN', (2, 0), (2, 1)),
                ('SPAN', (3, 0), (3, 1)),
                ('SPAN', (13, 0), (13, 1)),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, -1), colors.Color(219.0/255,229.0/255,241.0/255)),
            ]
        ))

        # viviendas = ViviendaUrbana.objects.filter(ubigeo=distrito.ubigeo, zona=aeu.zona, aeu_final=aeu.aeu_final).order_by('manzana','id_reg_or')

        # viviendas = ViviendaUrbana.objects.filter(
        #     Q(ubigeo=distrito.ubigeo), Q(zona=aeu.zona), Q(aeu_final=aeu.aeu_final)
        #     # Q(ubigeo='020601'), Q(zona='001'), Q(aeu_final='001')
        # ).order_by('ubigeo', 'zona', 'manzana', 'id_reg_or', 'uso_local')

        # vivi = ViviendaUrbana.objects.get(ubigeo=distrito.ubigeo, zona=aeu.zona,).values('id_reg_or', flat=True).distinct().order_by('manzana')
        # for viv in ViviendaUrbana.objects.values('or_viv_aeu').filter(
        #        Q(ubigeo=distrito.ubigeo), Q(zona= aeu.zona), Q(aeu_final= aeu.aeu_final)
        # ).distinct().order_by('or_viv_aeu'):
        i=0
        # Bloque Croquis

        data_croq = [
            ['', '', '', '', '', Paragraph('<strong>Doc. CPV</strong>', h4)],
            [Paragraph('<strong>A. UBICACION GEOGRAFICA</strong>', h1), '', '', '',
             Paragraph('<strong>B. UBICACION CENSAL</strong>', h1), ''],
            [Paragraph('<strong>DEPARTAMENTO</strong>', h1),Paragraph(str(aeu.ccdd), h1),
             Paragraph(str(aeu.departamento), h1), '',
             Paragraph('<strong>ZONA Nº</strong>', h1),Paragraph(str(aeu.zona_convert), h1)],
            [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(str(aeu.ccpp), h1),
             Paragraph(str(aeu.provincia), h1), '', Paragraph(str('<strong>SECCION Nº</strong>'), h1), str(aeu.seccion_convert)],
            [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph(str(aeu.ccdi), h1), Paragraph(str(aeu.distrito), h1),
             '', Paragraph('<strong>A.E.U. Nº</strong>', h1), str(aeu.aeu_convert)],
            [Paragraph('<strong>CENTRO POBLADO</strong>', h1), Paragraph(aeu.nomccpp, h1), '', '', '', ''],
            [Paragraph('<strong>CATEGORIA DEL<br/>CENTRO POBLADO</strong>', h1), Paragraph('CIUDAD', h1), '', '',
             Paragraph('<strong>TOTAL DE VIVIENDAS DEL A.E.U.</strong>', h1),Paragraph(str(int(aeu.cant_viv)), h1)],
        ]

        tables_croq = Table(data_croq, colWidths=[3.7 * cm, 1 * cm, 8.3 * cm, 0.3 * cm, 4.7 * cm, 1 * cm])

        tables_croq.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (5, 0), colors.black),
            ('ALIGN', (4, 0), (5, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 2), (1, 4), 'CENTER'),
            ('GRID', (0, 1), (2, 6), 1, colors.black),
            ('GRID', (4, 1), (5, 4), 1, colors.black),
            ('GRID', (-2, -1), (-1, -1), 1, colors.black),
            ('SPAN', (0, 1), (2, 1)),
            ('SPAN', (4, 1), (5, 1)),
            ('SPAN', (1, 5), (2, 5)),
            ('SPAN', (1, 6), (2, 6)),
            ('BACKGROUND', (4, 1), (5, 5), colors.white),
            ('BACKGROUND', (0, 1), (-1, 1), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('BACKGROUND', (0, 1), (0, 6), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('BACKGROUND', (4, 1), (4, 4), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('BACKGROUND', (4, 6), (4, 6), colors.Color(219.0/255,229.0/255,241.0/255))
        ]))

        fichero_imagen_inei = 'Reporte/Img/inei.png'
        imagen_logo_inei = Image(os.path.realpath(fichero_imagen_inei), width=50, height=40)

        P2 = Paragraph('', styleBH)
        fichero_imagen = 'Reporte/Img/escudo.png'
        imagen_logo = Image(os.path.realpath(fichero_imagen), width=50, height=50)

        # t = Table(
        #     data=[
        #         [[imagen_logo, P2], t1, [imagen_logo_inei, P2]],
        #         ['', t1_croq, '']
        #     ],
        #     colWidths=[2 * cm, 14 * cm, 2 * cm],
        #     style=[
        #         ('GRID', (1, 1), (-2, -2), 1, colors.white),
        #         ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
        #     ]
        # )

        t_croq = Table(
            data=[
                [[imagen_logo, P2], t1, [imagen_logo_inei, P2]],
                ['',t1_sub, '']
            ],
            colWidths=[2 * cm, 14 * cm, 2 * cm],
            style=[
                ('GRID', (1, 1), (-2, -2), 1, colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ]
        )

        # story.append(t)
        # story.append(Spacer(0, 1 * mm))
        # story.append(tables)
        # story.append(Spacer(0, 1 * mm))

        viv_urb = ViviendaUrbana.objects.filter(Q(ubigeo=ubigeo), Q(zona=zonal),
                                                Q(aeu_final=aeut)).order_by('or_viv_aeu')

        fichero_imagen = 'Reporte/Croquis/Zona' + ubigeo + '00100' + '/Croquis' + ubigeo + '00100' + str(aeut) + '.png'
        imagen_croquis = Image(os.path.realpath(fichero_imagen), width=18.8 * cm, height=18 * cm)

        # data_img = [
        #     [Paragraph(e, h3) for e in ["<strong>Imagen de Croquis</strong>"]],
        # ]
        # croq = Table(
        #     data=[
        #         [imagen_croquis]
        #     ],
        #     colWidths=[18.8 * cm],
        #     rowHeights=[18.8 * cm],
        #     style=[
        #         ('GRID', (1, 1), (-2, -2), 1, colors.black),
        #         ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        #         ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        #     ]
        # )

        # story.append(croq)
        # story.append(Spacer(0, 1 * mm))
        # story.append(table_obs)
        # story.append(PageBreak())

        # story.append(table_bar)
        story.append(t_croq)
        story.append(Spacer(0, 2 * mm))
        story.append(tables)
        story.append(Spacer(0, 3 * mm))
        story.append(c)

        # viviendas = ViviendaUrbana.objects.filter(Q(ubigeo=distrito.ubigeo), Q(zona=aeu.zona), Q(aeu_final=aeu.aeu_final)
        #     # Q(ubigeo='020601'), Q(zona='001'), Q(aeu_final='001')
        # ).order_by('ubigeo', 'zona', 'manzana', 'id_reg_or', 'uso_local')[0:32]

        viviendas = v_ReporteViviendas.objects.filter(Q(ubigeo=ubigeo), Q(zona=zonal), Q(aeu_final=aeut)).order_by('manzana', 'id_reg_or')[0:18]

        toti_viv = int(v_ReporteViviendas.objects.filter(Q(ubigeo=ubigeo), Q(zona=zonal), Q(aeu_final=aeut)
        ).order_by('manzana', 'id_reg_or').count())

        equi_pta = [[1, 'PF de:'], [2, 'PG de:'], [3, 'PB de:'], [4, 'PC de:'], [5, 'Frente, pared corrida'],
                    [6, 'Frente sin construir'], [7, 'Otro'], [8, 'Sin Edificación']]



        for vivienda in viviendas:
            i=i+1

            pep = vivienda.p29_a

            for el in equi_pta:
                if (el[0] == pep):
                    pta_f = el[1]

            jefe_hogar = ""
            if vivienda.p29 == 1 or vivienda.p29 == 3:
                jefe_hogar = vivienda.p32
            # elif vivienda.id_viv.p29 == 2 or vivienda.id_viv.p29 == 5:
            elif vivienda.p29 == 5:
                if vivienda.p29_a in (1, 2, 3, 4):
                    jefe_hogar = pta_f + " " + vivienda.p29_p
                elif vivienda.p29_a in (5, 6):
                    jefe_hogar = pta_f
                elif vivienda.p29_a == 7:
                    jefe_hogar = vivienda.p29_o
                elif vivienda.p29_a == 8:
                    jefe_hogar = vivienda.p29_8_o
            elif vivienda.p29 == 2 or vivienda.p29 == 4:
                jefe_hogar = vivienda.p35
            else:
                print "Ni idea u.u"

            jefe_h = jefe_hogar

            if jefe_h != None and jefe_h == type('a') and len(jefe_h) > 26:
                print "Entroooooo 111"
                jefe_jug = jefe_h.rsplit(' ', 2)
                jefe_home = jefe_jug[0] + '\n' + jefe_jug[1]
            else:
                jefe_home = jefe_h
            # len_viviendap21 = len(vivienda.p21) - 1
            #
            # if ' ' not in vivienda.p21:
            #     p21 = vivienda.p21
            # else:
            #     firstblank_viviendap21 = (vivienda.p21).index(' ')
            #     p21 = vivienda.p21[:firstblank_viviendap21] + '\n' + vivienda.p21[len_viviendap21 - firstblank_viviendap21:]



            p22_a = vivienda.p22_a
            if p22_a == None:
                p22_a = ' '
            else:
                p22_a = vivienda.p22_a


            p22_b = vivienda.p22_b
            if p22_b == None:
                p22_b = ' '
            else:
                p22_b = vivienda.p22_b

            p24 = vivienda.p24
            if p24 == None:
                p24 = ' '
            else:
                p24 = vivienda.p24

            p25 = vivienda.p25
            if p25 == None:
                p25 = ' '
            else:
                p25 = vivienda.p25

            p26 = vivienda.p26
            if p26 == None:
                p26 = ' '
            else:
                p26 = vivienda.p26

            # p21 = vivienda.p21
            # p21 = list(p21)
            #
            # if len(p21) > 12:
            #     for i in range(-1, len(p21)):
            #         pos = "i: " + p21[-i]
            #         print pos
            #         if p21[-i] == " ":
            #             # new_data = string.replace(data," ", "\n")
            #             p21[-i] = '\n'
            #             # data = data.replace(" ", "\n")
            #             break
            #     # if data.find(' ')>=0:
            #     #     print 'Existe caracter'
            #     # else:
            #     #     print 'No existe nada'
            #     p21 = ''.join(p21)
            #     print ''.join(p21)
            #     # print info

            if vivienda.id_reg_or == 0:
                id_reg_or=''
            else:
                id_reg_or = vivienda.id_reg_or

            # if len(vivienda.p21)>11:
            #     len_viviendap21 = len(vivienda.p21) - 1
            #
            #     if ' ' not in vivienda.p21:
            #         p21 = vivienda.p21
            #     else:
            #
            #         firstblank_viviendap21 = (vivienda.p21).index(' ')
            #         p21 = vivienda.p21[:firstblank_viviendap21] + '\n' + vivienda.p21[len_viviendap21 - firstblank_viviendap21:]
            # else:
            #     p21 = vivienda.p21

            if len(vivienda.p21)>11:
                jug_p21 = (vivienda.p21).rsplit(' ',1)
                #firstblank_viviendap21 = (vivienda.p21).index(' ')
                p21 =jug_p21[0] + '\n' + jug_p21[1]
            else:
                p21 = vivienda.p21

            # Bloque Listado
            table2 = [(vivienda.or_viv_aeu if not vivienda.or_viv_aeu == 0 or vivienda.or_viv_aeu == '0'  else '' ,
                       vivienda.manzana,
                       id_reg_or,
                       vivienda.frente_ord,
                       vivienda.p20_nombre if vivienda.p20 else "",
                       p21,
                       p22_a + p22_b,
                       vivienda.p23 if vivienda.p23 == 0 else "",
                       p24,
                       p25,
                       p26,
                       vivienda.p27_a if not vivienda.p27_a == None else '' + vivienda.p27_b if not vivienda.p27_b == None else '',
                       # 1 if a > b else -1
                       vivienda.p28 if vivienda.p28 == 0 else "",
                       jefe_home if not jefe_home == None else '')
                      ]
            u = Table(table2,
                      colWidths=[0.8 * cm, 0.9 * cm, 1 * cm, 1.2 * cm, 1.2 * cm, 2.5 * cm, 1.2 * cm, 1.1 * cm, 1 * cm, 1 * cm,
                                 1 * cm, 1.1 * cm, 0.9 * cm, 4.9 * cm],
                      rowHeights=[1 *cm])

            u.setStyle(TableStyle(
                [
                    ('GRID', (1, 1), (-2, -2), 1, colors.black),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (13, 0), 7),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]
            ))
            story.append(u)

        # viviendas_second = ViviendaUrbana.objects.filter(
        #     Q(ubigeo=distrito.ubigeo), Q(zona=aeu.zona), Q(aeu_final=aeu.aeu_final)
        #     # Q(ubigeo='020601'), Q(zona='001'), Q(aeu_final='001')
        # ).order_by('ubigeo', 'zona', 'manzana', 'id_reg_or', 'uso_local')[33:]
        viviendas_second = v_ReporteViviendas.objects.filter(Q(ubigeo=ubigeo), Q(zona=zonal), Q(aeu_final=aeut)
                                                                 ).order_by('manzana', 'id_reg_or')[18:42]

        if toti_viv>19:
            story.append(c)
            for vivienda in viviendas_second:
                i = i + 1

                pep = vivienda.p29_a

                for el in equi_pta:
                    if (el[0] == pep):
                        pta_f = el[1]

                jefe_hogar = ""
                if vivienda.p29 == 1 or vivienda.p29 == 3:
                    jefe_hogar = vivienda.p32
                # elif vivienda.id_viv.p29 == 2 or vivienda.id_viv.p29 == 5:
                elif vivienda.p29 == 5:
                    if vivienda.p29_a in (1, 2, 3, 4):
                        jefe_hogar = pta_f + "" + vivienda.p29_p
                    elif vivienda.p29_a in (5, 6):
                        jefe_hogar = pta_f
                    elif vivienda.p29_a == 7:
                        jefe_hogar = vivienda.p29_o
                    elif vivienda.p29_a == 8:
                        jefe_hogar = vivienda.p29_8_o
                elif vivienda.p29 == 2 or vivienda.p29 == 4:
                    jefe_hogar = vivienda.p35
                else:
                    print "No idea u.u"

                jefe_h = jefe_hogar

                if jefe_h != None and jefe_h == type('a') and len(jefe_h) > 26:
                    print "Entroooooo 111"
                    jefe_jug = jefe_h.rsplit(' ', 2)
                    jefe_home = jefe_jug[0] + '\n' + jefe_jug[1]
                else:
                    jefe_home = jefe_h


                # if jefe_hogar != None:
                #     if len(jefe_hogar) > 27:
                #         len_jefehogar = len(jefe_hogar) - 1
                #
                #         if ' ' not in jefe_hogar:
                #             jefe_home = jefe_hogar
                #         else:
                #             firstblank_jefe_hogar = (jefe_hogar).index(' ')
                #             jefe_home = jefe_hogar[:firstblank_jefe_hogar] + '\n' + jefe_hogar[
                #                                                                     len_jefehogar - firstblank_jefe_hogar:]
                #     else:
                #         jefe_home = jefe_hogar

                # if jefe_hogar != None:
                #     jefe_hogar = list(jefe_hogar)
                #     if len(jefe_hogar) > 27:
                #         for i in range(-1, len(jefe_hogar)):
                #             pos = "i: " + jefe_hogar[-i]
                #             # print pos
                #             if jefe_hogar[-i] == " ":
                #                 # new_data = string.replace(data," ", "\n")
                #                 jefe_hogar[-i] = '\n'
                #                 # data = data.replace(" ", "\n")
                #                 break
                #
                #         jefe_hogar = ''.join(jefe_hogar)
                #
                #     else:
                #         jefe_hogar = ''.join(jefe_hogar)
                # else:
                #     jefe_hogar = ' '

                p22_a = vivienda.p22_a
                if p22_a == None:
                    p22_a = ' '
                else:
                    p22_a = vivienda.p22_a

                p22_b = vivienda.p22_b
                if p22_b==None:
                    p22_b=''
                else:
                    p22_b = vivienda.p22_b


                p24 = vivienda.p24
                if p24==None:
                    p24=''
                else:
                    p24 = vivienda.p24

                p25 = vivienda.p25
                if p25 == None:
                    p25 = ' '
                else:
                    p25 = vivienda.p25

                p26 = vivienda.p26
                if p26 == None:
                    p26 = ' '
                else:
                    p26 = vivienda.p26

                # if len(str(vivienda.p21).decode('latin-1')) > 11:
                #     data = str(vivienda.p21).decode('latin-1')
                #     p21 = (data[:11] + '..') if len(data) > 11 else data
                # else:
                #     p21 = str(vivienda.p21).decode('latin-1')

                # info = (data[:10] + '..') if len(data) > 10 else data

                # cadena.find('ha')

                x = 0
                # p21 = vivienda.p21
                # if p21 != None:
                #     p21 = list(p21)
                #     x = 0
                #     if len(p21) > 12:
                #
                #         for i in range(-1, len(p21)):
                #             pos = "i: " + p21[-i]
                #             # print pos
                #             if p21[-i] == " ":
                #                 # new_data = string.replace(data," ", "\n")
                #                 p21[-i] = '\n'
                #                 # data = data.replace(" ", "\n")
                #                 break
                #
                #         p21 = ''.join(p21)
                #         # print ''.join(p21)
                #         # print info
                #     else:
                #         p21 = vivienda.p21
                #         # print ''.join(data)
                # else:
                #     p21 = ' '
                if len(vivienda.p21) > 11:
                    jug_p21 = (vivienda.p21).rsplit(' ', 1)

                    # firstblank_viviendap21 = (vivienda.p21).index(' ')
                    p21 = jug_p21[0] + '\n' + jug_p21[1]
                else:
                    p21 = vivienda.p21

                p27_a = vivienda.p27_a
                if p27_a == None:
                    p27_a = ''
                else:
                    p27_a = vivienda.p27_a

                p27_b = vivienda.p27_b
                if p27_b == None:
                    p27_b = ''
                else:
                    p27_b = vivienda.p27_b

                if vivienda.or_viv_aeu == 0:
                    id_reg_or = ''
                else:
                    id_reg_or = vivienda.id_reg_or

                # Bloque Listado
                table2 = [(vivienda.or_viv_aeu if not vivienda.or_viv_aeu == 0 or vivienda.or_viv_aeu == '0'  else '',
                           vivienda.manzana,

                           id_reg_or,
                           vivienda.frente_ord,
                           vivienda.p20_nombre if vivienda.p20 else "",
                           p21,
                           p22_a + p22_b,
                           vivienda.p23 if vivienda.p23 == 0 else "",
                           p24,
                           p25,
                           p26,
                           p27_a+p27_b,

                           vivienda.p28 if vivienda.p28 == 0 else "",
                           jefe_home if not jefe_home == None else '')
                          ]
                u_second = Table(table2,
                          colWidths=[0.8 * cm, 0.9 * cm, 1 * cm, 1.2 * cm, 1.2 * cm, 2.5 * cm, 1.2 * cm, 1.1 * cm, 1 * cm, 1 * cm,
                                     1 * cm, 1.1 * cm, 0.9 * cm, 4.9 * cm],
                          rowHeights=[1 * cm])

                u_second.setStyle(TableStyle(
                    [
                        ('GRID', (1, 1), (-2, -2), 1, colors.black),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 0), (13, 0), 7),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]
                ))
                story.append(u_second)

        obs_data_three = [
            [Paragraph(e, h3) for e in ["<strong>Viv Nº</strong>",
                                        "<strong>Mz Nº</strong>",
                                        "<strong>Or Reg</strong>",
                                        "<strong>Frent. Nº</strong>",
                                        "<strong>DIRECCION DE LA VIVIENDA</strong>",
                                        "", "", "", "", "", "", "", "",
                                        "<strong>Nombres y Apellidos del JEFE DEL HOGAR</strong>"]],
            [Paragraph(e, h3) for e in ["", "", "", "",
                                        "<strong>Tipo de Via</strong>",
                                        "<strong>Nombre de Via</strong>",
                                        "<strong>Nº de Puerta</strong>",
                                        "<strong>Block</strong>",
                                        "<strong>Man-<br/>zana Nº</strong>",
                                        "<strong>Lote Nº</strong>",
                                        "<strong>Piso Nº</strong>",
                                        "<strong>Inter. Nº</strong>",
                                        "<strong>Km. Nº</strong>",
                                        ""]],
            [Paragraph(e, h3) for e in ["<strong>(1)</strong>",
                                        "<strong>(2)</strong>",
                                        "<strong>(3)</strong>",
                                        "<strong>(4)</strong>",
                                        "<strong>(5)</strong>",
                                        "<strong>(6)</strong>",
                                        "<strong>(7)</strong>",
                                        "<strong>(8)</strong>",
                                        "<strong>(9)</strong>",
                                        "<strong>(10)</strong>",
                                        "<strong>(11)</strong>",
                                        "<strong>(12)</strong>",
                                        "<strong>(13)</strong>",
                                        "<strong>(14)</strong>"]],
        ]
        d = Table(obs_data_three,
                  colWidths=[0.8 * cm, 0.9 * cm, 1 * cm, 1.2 * cm, 1.2 * cm, 2.5 * cm, 1.2 * cm, 1.1 * cm, 1 * cm, 1 * cm,
                             1 * cm,
                             1.1 * cm, 0.9 * cm, 4.9 * cm])

        d.setStyle(TableStyle(
            [
                ('GRID', (1, 1), (-2, -2), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                # ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),

                ('SPAN', (4, 0), (12, 0)),
                ('SPAN', (0, 0), (0, 1)),
                ('SPAN', (1, 0), (1, 1)),
                ('SPAN', (2, 0), (2, 1)),
                ('SPAN', (3, 0), (3, 1)),
                ('SPAN', (13, 0), (13, 1)),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('BACKGROUND', (0, 0), (13, 2), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            ]
        ))

        viviendas_three = v_ReporteViviendas.objects.filter(Q(ubigeo=ubigeo), Q(zona=zonal), Q(aeu_final=aeut)
                                                            ).order_by('zona', 'manzana', 'id_reg_or')[42:]

        if toti_viv > 43:
            story.append(d)
            for vivienda in viviendas_three:
                i = i + 1
                pep = vivienda.p29_a
                for el in equi_pta:
                    if (el[0] == pep):
                        pta_f = el[1]
                jefe_hogar = ""
                if vivienda.p29 == 1 or vivienda.p29 == 3:
                    jefe_hogar = vivienda.p32
                elif vivienda.p29 == 5:
                    if vivienda.p29_a in (1, 2, 3, 4):
                        jefe_hogar = pta_f + "" + vivienda.p29_p
                    elif vivienda.p29_a in (5, 6):
                        jefe_hogar = pta_f
                    elif vivienda.p29_a == 7:
                        jefe_hogar = vivienda.p29_o
                    elif vivienda.p29_a == 8:
                        jefe_hogar = vivienda.p29_8_o
                elif vivienda.p29 == 2 or vivienda.p29 == 4:
                    jefe_hogar = vivienda.p35
                else:
                    print "Ni idea u.u"
                # if jefe_hogar != None:
                #     jefe_hogar = list(jefe_hogar)
                #     if len(jefe_hogar) > 27:
                #         for i in range(-1, len(jefe_hogar)):
                #             pos = "i: " + jefe_hogar[-i]
                #             print pos
                #             if jefe_hogar[-i] == " ":
                #                 # new_data = string.replace(data," ", "\n")
                #                 jefe_hogar[-i] = '\n'
                #                 break
                #         jefe_hogar = ''.join(jefe_hogar)
                #         # print ''.join(jefe_hogar)
                #         # print info
                #     else:
                #         jefe_hogar = ''.join(jefe_hogar)
                # else:
                #     jefe_hogar = ' '

                jefe_h = jefe_hogar

                if jefe_h!=None  and jefe_h==type('a') and len(jefe_h)>26:
                    print "Entroooooo 2222"
                    jefe_jug = jefe_h.rsplit(' ', 2)
                    jefe_home = jefe_jug[0] + '\n' + jefe_jug[1]
                else:
                    jefe_home = jefe_h


                p22_a = vivienda.p22_a
                if p22_a==None:
                    p22_a = ' '
                else:
                    p22_a = vivienda.p22_a

                p22_b = vivienda.p22_b
                if p22_b == None:
                    p22_b = ''
                else:
                    p22_b = vivienda.p22_b

                p24 = vivienda.p24
                if p24 == None:
                    p24 = ''
                else:
                    p24 = vivienda.p24

                p25 = vivienda.p25
                if p25 == None:
                    p25 = ' '
                else:
                    p25 = vivienda.p25

                p26 = vivienda.p26
                if p26 == None:
                    p26 = ' '
                else:
                    p26 = vivienda.p26

                if len(vivienda.p21) > 11:
                    jug_p21 = (vivienda.p21).rsplit(' ', 1)

                    # firstblank_viviendap21 = (vivienda.p21).index(' ')
                    p21 = jug_p21[0] + '\n' + jug_p21[1]
                else:
                    p21 = vivienda.p21
                #p21 = vivienda.p21

                x = 0

                # Bloque Listado
                # table2 = [(str(vivienda.or_viv_aeu if not vivienda.or_viv_aeu == 0 or vivienda.or_viv_aeu == '0'  else '').decode('latin-1'),
                #            str(vivienda.manzana).decode('latin-1'),
                #            str(vivienda.frente_ord).decode('latin-1'),
                #            str(vivienda.p20.p20_nombre).decode('latin-1') if vivienda.p20 else "",
                #            p21,
                #            str(p22_a + p22_b).decode('latin-1'),
                #            str(str(vivienda.p23) if vivienda.p23 == 0 else "").decode('latin-1'),
                #            str(p24).decode('latin-1'),
                #            p25,
                #            p26,
                #            str(str(vivienda.p27_a) + str(vivienda.p27_b)).decode('latin-1'),
                #            # 1 if a > b else -1
                #            str(str(vivienda.p28) if vivienda.p28 == 0 else "").decode('latin-1'),
                #            str(jefe_hogar if not jefe_hogar == None else '').decode('latin-1'))
                # ]

                p27_a= vivienda.p27_a
                if p27_a == None:
                    p27_a = ''
                else:
                    p27_a = vivienda.p27_a

                p27_b = vivienda.p27_b
                if p27_b == None:
                    p27_b = ''
                else:
                    p27_b = vivienda.p27_b

                if vivienda.or_viv_aeu == 0:
                    id_reg_or = ''
                else:
                    id_reg_or = vivienda.id_reg_or

                table2 = [(vivienda.or_viv_aeu if not vivienda.or_viv_aeu == 0 or vivienda.or_viv_aeu == '0'  else '',
                           vivienda.manzana,
                           id_reg_or,
                           vivienda.frente_ord,
                           vivienda.p20_nombre if vivienda.p20 else "",
                           p21,
                           p22_a + p22_b,
                           vivienda.p23 if vivienda.p23 == 0 else "",
                           p24,
                           p25,
                           p26,
                           p27_a + p27_b,
                           # 1 if a > b else -1
                           vivienda.p28 if vivienda.p28 == 0 else "",
                           jefe_home if not jefe_home == None else '')
                ]
                u_three = Table(table2,
                                 colWidths=[0.8 * cm, 0.9 * cm, 1 * cm, 1.2 * cm, 1.2 * cm, 2.5 * cm, 1.2 * cm,1.1 * cm, 1 * cm, 1 * cm,
                                            1 * cm, 1.1 * cm, 0.9 * cm, 4.9 * cm],
                                 rowHeights=[1 * cm])
                u_three.setStyle(TableStyle(
                    [
                        ('GRID', (1, 1), (-2, -2), 1, colors.black),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 0), (13, 0), 7),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]
                ))
                story.append(u_three)
        # if(PageBreak()):
        #     story.append(Spacer(0, 22 * cm))
        #     story.append(table_obs)
        #     story.append(Spacer(0, 1 * mm))
        #     story.append(table_empa_cuerp)
        # else:
        # story.append(Spacer(0, 1 * cm))
        # story.append(table_obs)
        # story.append(Spacer(0, 1 * mm))
        # story.append(table_empa_cuerp)

        # Z_obs = Paragraph("<strong>OBSERVACIONES: ...................................................................."
        #                    "..........................................................................................."
        #                    "..........................................................................................."
        #                    "..........................................................................................."
        #                    "..........................................................................................."
        #                    "..........................................................................................."
        #                    "..........................................................................................."
        #                    "..........................................................................................."
        #                    ".............................1</strong>", h_obser)
        #
        # table_obser = Table(
        #         data=[
        #             [Z_obs]
        #         ],
        #         colWidths=[18.3 * cm],
        #         style=[
        #             ('GRID', (0, 0), (-1, -1), 1, colors.black)
        #         ]
        # )
        # if (PageBreak()):
        # story.append(Spacer(0, 1.3 * cm))

        # story.append(Spacer(0, 1 * mm))
        # story.append(table_empa_cuerp)
        # story.append(Spacer(0, 1 * mm))
        # story.append(p_page)
        # else:
        #     story.append(Spacer(0, 21 * cm))
        #     story.append(table_obs)
        #     story.append(Spacer(0, 1 * mm))
        #     story.append(table_empa_cuerp)
        #     story.append(Spacer(0, 1 * mm))
        #     story.append(p_page)

    doc2.build(story)
    doc.build(story)
    response.write(buff.getvalue())
    buff.close()
    return response

def generar_lote(request):

    lista_distrito = []

    # lista_distrito.append('020801')
    # lista_distrito.append('020601')
    # lista_distrito.append('021509')
    # lista_distrito.append('021806')
    # lista_distrito.append('022001')
    # lista_distrito.append('030212')
    # lista_distrito.append('030602')
    # lista_distrito.append('050507')
    # lista_distrito.append('050601')
    # lista_distrito.append('050617')
    # lista_distrito.append('060903')
    # lista_distrito.append('080301')
    # lista_distrito.append('080205')
    # lista_distrito.append('080206')
    # lista_distrito.append('080207')
    # lista_distrito.append('080402')
    # lista_distrito.append('080407')
    # lista_distrito.append('090203')
    # lista_distrito.append('090208')
    # lista_distrito.append('090301')
    # lista_distrito.append('110107')
    # lista_distrito.append('110204')
    # lista_distrito.append('120201')
    # lista_distrito.append('120501')
    # lista_distrito.append('120708')
    # lista_distrito.append('130202')
    # lista_distrito.append('131203')
    # lista_distrito.append('130701')
    # lista_distrito.append('130705')
    # lista_distrito.append('131203')
    # lista_distrito.append('140107')
    lista_distrito.append('150116')
    # lista_distrito.append('150508')
    # lista_distrito.append('150604')
    # lista_distrito.append('150705')
    # lista_distrito.append('170102')
    # lista_distrito.append('180106')
    #
    # lista_distrito.append('180208')
    # lista_distrito.append('180210')
    # lista_distrito.append('190111')

    # lista_distrito.append('180210')
    # lista_distrito.append('210407')
    # lista_distrito.append('230106')
    # lista_distrito.append('230109')
    # lista_distrito.append('240103')
    # lista_distrito.append('240105')
    # lista_distrito.append('240106')
    lista = []

    for ubigeos in lista_distrito:

        total_zonas = Esp_Aeus.objects.filter(ubigeo=ubigeos).values_list('zona', flat=True)
        zona_dif = list(set(total_zonas))

        for zona_t in zona_dif:
            total_secc_zona = Esp_Aeus.objects.filter(ubigeo=ubigeos, zona=zona_t).values_list('aeu_final', flat=True)
            dif_ae = list(set(total_secc_zona))
            for aeu in dif_ae:

                lista.append(str(zona_t) + ": " + str(aeu) + "<br/>")
                # str(zona_t + 1)+": " + str(aeu + 1) + "<br/>"
                # print "Ubigeo: "+str(ubigeos)+ " de zona: "+ str(zona_t) +" y "+ str(aeu)
                generar_pdf(request, ubigeos, zona_t, aeu )
    return HttpResponse(lista)


