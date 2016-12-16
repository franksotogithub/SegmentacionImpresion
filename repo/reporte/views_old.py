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
    print "generar_pdf"
    MARGIN_SIZE = 17 * mm
    PAGE_SIZE = A4
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=" + ubigeo + "001" + str(aeut) + ".pdf"
    # response['Content-Disposition'] = "attachment; filename="+ubigeo+"001"+".pdf"
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

    distrito = Distrito.objects.get(ubigeo=ubigeo)  # ubigeo

    # vivi = ViviendaUrbana.objects.get(ubigeo=distrito.ubigeo, zona='00100', aeu_final=aeut)

    cond = Esp_Aeus.objects.filter(ubigeo=ubigeo, zona=zonal, aeu_final=aeut)

    # cond_viv = Aeus.objects.filter(ubigeo=distrito.ubigeo, zona='00100', aeu_final=aeut)

    # total = Aeus.objects.filter(ubigeo=distrito.ubigeo, zona='00100', aeu_final=aeut).count()

    # viv_u = ViviendaU.objects.filter(ubigeo=ubigeo)

    rango_equivalencia = [[1, 'A'], [2, 'B'], [3, 'C'], [4, 'D'], [5, 'E'], [6, 'F'], [7, 'G'], [8, 'H'], [9, 'I'],
                          [10, 'J'], [11, 'K'], [12, 'L'], [13, 'M'], [14, 'N'], [15, 'O'], [16, 'P'], [17, 'Q'], [18, 'R'],
                          [19, 'S'], [20, 'T'], [21, 'U'], [22, 'V'], [23, 'W'], [24, 'X'], [25, 'Y'], [26, 'Z']
                          ]

    Z1 = Paragraph("<strong>OBSERVACIONES: .............................................................................."
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

    Z2 = Paragraph("<strong>EMPADRONADOR</strong>", h5)

    Z3 = Paragraph("<strong>Todas las viviendas que estén dentro de los límites de tu A.E.U. deben ser empadronadas. Debes tener<br/>cuidado de no omitir ninguna vivienda</strong>",h5)

    table_empa_cuerp = Table(
        data=[
            [Z2],
            [Z3]
        ],
        colWidths=[18.8 * cm],
        rowHeights=[0.7 * cm, 1.5 * cm],
        style=[
            ('GRID', (0, 0), (0, 0), 1, colors.black),
            ('GRID', (0, 1), (0, 1), 1, colors.black),
            ('ALIGN', (0, 0), (0, 0), 'CENTER')
        ]
    )

    x = 0

    for aeu in cond:
        x = x + 1
        y = x
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
        for ubigein in range(tam_dis):

            if os.path.exists("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein])) == False:
                os.mkdir("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein]))

            total_zonas = int(str(Tab_Aeus.objects.filter(ubigeo=lista_distritos[ubigein]).values_list('zona',flat=True).distinct().count()))

            for zona_t in range(total_zonas):
                zoner = str(zona_t + 1).zfill(3) + "00"
                listin.append(str(lista_distritos[ubigein]) + ": " + zoner + "<br/>")
                if os.path.exists("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein]) + "\\" + zoner) == False:
                    os.mkdir("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein]) + "\\" + zoner)

        destino = "\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(ubigeo) + "\\" + zonal + "\\" + str(ubigeo) + zonal + str(secc) + str(aeu_conv) + ".pdf"

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

        bar_string = Paragraph(string, h_bar)

        pi = Paragraph("-", h2)
        st_b = st

        table_bar = Table(
            data = [
                [pi, st_b],
                ['', bar_string]
            ],
            colWidths= [13 * cm, 5 * cm],
            style=[
                ('ALIGN', (0, 0), (-1, -1),'CENTER')
            ]
        )

        story.append(table_bar)

        zona_temp = aeu.zona[0:3]
        zona_int = int(aeu.zona[3:])
        zona_int_eq = ""


        for el in rango_equivalencia:
            if (el[0] == zona_int):
                zona_int_eq = el[1]

        zona_temp = zona_temp + str(zona_int_eq)

        data = [
            ['', '', '', '', '', Paragraph('<strong>Doc. CPV</strong>', h4)],
            [Paragraph('<strong>A. UBICACION GEOGRAFICA</strong>', h11), '', '', '',
             Paragraph('<strong>B. UBICACION CENSAL</strong>', h11), ''],
            [Paragraph('<strong>DEPARTAMENTO</strong>', h1),Paragraph(str(distrito.ccdd.ccdd), h_center),
             Paragraph(str(distrito.ccdd.departamento), h1), '',
             Paragraph('<strong>ZONA Nº</strong>', h1),Paragraph(zona_temp, h_center)],
            [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(distrito.ccpp, h_center),
             Paragraph(str(distrito.cod_prov.provincia).decode('latin-1'), h1), '', Paragraph(str('<strong>SECCION Nº</strong>'), h1), Paragraph(secc, h_center)],
            [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph(distrito.ccdi, h_center), Paragraph(str(distrito.distrito).decode('latin-1'), h1),
             '', Paragraph('<strong>A.E.U. Nº</strong>', h1), Paragraph(aeus, h_center)],
            [Paragraph('<strong>CENTRO POBLADO</strong>', h1), Paragraph(str(aeu.llave_ccpp.nomccpp).decode('latin-1'), h1), '', '', '', ''],
            [Paragraph('<strong>CATEGORIA DEL CENTRO POBLADO</strong>', h1), Paragraph('CIUDAD', h1), '', '',
             Paragraph('<strong>TOTAL DE VIVIENDAS<br/>DEL A.E.U.</strong>', h1),Paragraph(str(int(aeu.cant_viv)), h_center)],
        ]

        tables = Table(data, colWidths=[3.7 * cm, 1 * cm, 7.1 * cm, 0.3 * cm, 4.7 * cm, 2 * cm],
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
            ('SPAN', (1, 5), (2, 5)),
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
                # ['', t1, ''],
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
                # ('VALIGN', (3, 0), (3, 0), 'BOTTOM'),
                # ('BACKGROUND', (3, 0), (3, 0), colors.limegreen),
                # ('BACKGROUND', (3, 1), (3, 1), colors.khaki),
                # ('ALIGN', (3, 1), (3, 1), 'CENTER'),
                # ('BACKGROUND', (3, 2), (3, 2), colors.beige),
                # ('ALIGN', (3, 2), (3, 2), 'LEFT'),
            ]
        )

        obs_data = [
            [Paragraph(e, h3) for e in ["<strong>Viv Nº</strong>",
                                        "<strong>Mz Nº</strong>",
                                        "<strong>Fren<br/>-<br/>te<br/>Nº</strong>",
                                        "<strong>DIRECCION DE LA VIVIENDA</strong>",
                                        "", "", "", "", "", "", "","",
                                        "<strong>Nombres y Apellidos del JEFE DEL HOGAR</strong>"]],
            [Paragraph(e, h3) for e in ["", "", "",
                                        "<strong>Tipo de Via</strong>",
                                        "<strong>Nombre de Via</strong>",
                                        "<strong>Nº de Puerta</strong>",
                                        "<strong>Block</strong>",
                                        "<strong>Man-<br/>zana Nº</strong>",
                                        "<strong>Lote Nº</strong>",
                                        "<strong>Piso Nº</strong>",
                                        "<strong>Inter. Nº</strong>",
                                        "<strong>Km.<br/> Nº</strong>",
                                        ""]],
         ]
        c = Table(obs_data,
                  colWidths=[0.8 * cm, 0.9 * cm, 0.8 * cm, 1.2 * cm, 2.5 * cm, 1.2 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm,
                             1.1 * cm, 0.5 * cm, 5.8 * cm])

        c.setStyle(TableStyle(
            [
                ('GRID', (1, 1), (-2, -2), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(219.0/255,229.0/255,241.0/255)),
                ('BACKGROUND', (0, 0), (-1, 1), colors.Color(219.0/255,229.0/255,241.0/255)),
                ('SPAN', (3, 0), (11, 0)),
                ('SPAN', (0, 0), (0, 1)),
                ('SPAN', (1, 0), (1, 1)),
                ('SPAN', (2, 0), (2, 1)),
                ('SPAN', (12, 0), (12, 1)),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(219.0/255,229.0/255,241.0/255)),
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
        equi_pta = [[1, 'PF de:'], [2, 'PG de:'], [3, 'PB de:'], [4, 'PC de:'], [5, 'Frente, pared corrida'], [6, 'Frente sin construir'], [7, 'Otro'], [8, 'Sin Edificación']]
        # Bloque Croquis

        data_croq = [
            ['', '', '', '', '', Paragraph('<strong>Doc. CPV</strong>', h4)],
            [Paragraph('<strong>A. UBICACION GEOGRAFICA</strong>', h1), '', '', '',
             Paragraph('<strong>B. UBICACION CENSAL</strong>', h1), ''],
            [Paragraph('<strong>DEPARTAMENTO</strong>', h1),Paragraph(str(distrito.ccdd.ccdd), h1),
             Paragraph(str(distrito.ccdd.departamento), h1), '',
             Paragraph('<strong>ZONA Nº</strong>', h1),Paragraph(zona_temp, h1)],
            [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(distrito.ccpp, h1),
             Paragraph(str(distrito.cod_prov.provincia).decode('latin-1'), h1), '', Paragraph(str('<strong>SECCION Nº</strong>'), h1), secc],
            [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph(distrito.ccdi, h1), Paragraph(str(distrito.distrito).decode('latin-1'), h1),
             '', Paragraph('<strong>A.E.U. Nº</strong>', h1), aeus],
            [Paragraph('<strong>CENTRO POBLADO</strong>', h1), Paragraph(str(aeu.llave_ccpp.nomccpp).decode('latin-1'), h1), '', '', '', ''],
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

        t = Table(
            data=[
                [[imagen_logo, P2], t1, [imagen_logo_inei, P2]],
                ['', t1_croq, '']
            ],
            colWidths=[2 * cm, 14 * cm, 2 * cm],
            style=[
                ('GRID', (1, 1), (-2, -2), 1, colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ]
        )

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

        viv_urb = ViviendaUrbana.objects.filter(Q(ubigeo=distrito.ubigeo), Q(zona=aeu.zona),
                                                Q(aeu_final=aeu.aeu_final)).order_by('or_viv_aeu')

        fichero_imagen = 'Reporte/Croquis/Zona' + ubigeo + '00100' + '/Croquis' + ubigeo + '00100' + str(
            aeut) + '.png'
        imagen_croquis = Image(os.path.realpath(fichero_imagen), width=18.8 * cm, height=18 * cm)

        data_img = [
            [Paragraph(e, h3) for e in ["<strong>Imagen de Croquis</strong>"]],
        ]
        croq = Table(
            data=[
                [imagen_croquis]
            ],
            colWidths=[18.8 * cm],
            rowHeights=[18.8 * cm],
            style=[
                ('GRID', (1, 1), (-2, -2), 1, colors.black),
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]
        )

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

        viviendas = v_ReporteViviendas.objects.filter(Q(ubigeo=ubigeo), Q(zona=zonal), Q(aeu_final=aeut)
                                                  # Q(ubigeo='020601'), Q(zona='001'), Q(aeu_final='001')
                                                  ).order_by('ubigeo', 'zona', 'manzana', 'id_reg_or')[0:32]

        toti_viv = int(v_ReporteViviendas.objects.filter(Q(ubigeo=ubigeo), Q(zona=aeu.zona), Q(aeu_final=aeu.aeu_final)
        ).order_by('ubigeo', 'zona', 'manzana', 'id_reg_or', 'uso_local').count())
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
                    jefe_hogar = str(pta_f) + "" + str(vivienda.p29_p)
                elif vivienda.p29_a in (5, 6):
                    jefe_hogar = str(pta_f)
                elif vivienda.p29_a == 7:
                    jefe_hogar = str(vivienda.p29_o)
                elif vivienda.p29_a == 8:
                    jefe_hogar = str(vivienda.p29_8_o)
            elif vivienda.p29 == 2 or vivienda.p29 == 4:
                jefe_hogar = str(vivienda.p35)
            else:
                print "No idea u.u"

            # Bloque Listado
            table2 = [(str(vivienda.or_viv_aeu if not vivienda.or_viv_aeu == 0 or vivienda.or_viv_aeu == '0'  else '' ).decode('latin-1'),
                       str(vivienda.manzana).decode('latin-1'),
                       str(vivienda.frente_ord).decode('latin-1'),
                       str(vivienda.p20.p20_nombre).decode('latin-1') if vivienda.p20 else "",
                       str(vivienda.p21).decode('latin-1'),
                       str(str(vivienda.p22_a) + str(vivienda.p22_b)).decode('latin-1'),
                       str(str(vivienda.p23) if vivienda.p23 == 0 else "").decode('latin-1'),
                       str(vivienda.p24).decode('latin-1'),
                       str(vivienda.p25).decode('latin-1'),
                       str(vivienda.p26).decode('latin-1'),
                       str(str(vivienda.p27_a if not vivienda.p27_a == None else '') + str(vivienda.p27_b if not vivienda.p27_b == None else '')).decode('latin-1'),
                       # 1 if a > b else -1
                       str(str(vivienda.p28) if vivienda.p28 == 0 else "").decode('latin-1'),
                       str(jefe_hogar if not jefe_hogar == None else '').decode('latin-1'))
                      ]
            u = Table(table2,
                      colWidths=[0.8 * cm, 0.9 * cm, 0.8 * cm, 1.2 * cm, 2.5 * cm, 1.2 * cm, 1 * cm, 1 * cm, 1 * cm,
                                 1 * cm, 1.1 * cm, 0.5 * cm, 5.8 * cm],
                      rowHeights=[0.5 *cm])


            u.setStyle(TableStyle(
                [
                    ('GRID', (1, 1), (-2, -2), 1, colors.black),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (12, 0), 7),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]
            ))
            story.append(u)

        # viviendas_second = ViviendaUrbana.objects.filter(
        #     Q(ubigeo=distrito.ubigeo), Q(zona=aeu.zona), Q(aeu_final=aeu.aeu_final)
        #     # Q(ubigeo='020601'), Q(zona='001'), Q(aeu_final='001')
        # ).order_by('ubigeo', 'zona', 'manzana', 'id_reg_or', 'uso_local')[33:]
        viviendas_second = v_ReporteViviendas.objects.filter(Q(ubigeo=ubigeo), Q(zona=zonal), Q(aeu_final=aeut)
                                                                 # Q(ubigeo='020601'), Q(zona='001'), Q(aeu_final='001')
                                                                 ).order_by('ubigeo', 'zona', 'manzana', 'id_reg_or')[32:]
        #
        if toti_viv>33:
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
                        jefe_hogar = str(pta_f) + "" + str(vivienda.p29_p)
                    elif vivienda.p29_a in (5, 6):
                        jefe_hogar = str(pta_f)
                    elif vivienda.p29_a == 7:
                        jefe_hogar = str(vivienda.p29_o)
                    elif vivienda.p29_a == 8:
                        jefe_hogar = str(vivienda.p29_8_o)
                elif vivienda.p29 == 2 or vivienda.p29 == 4:
                    jefe_hogar = str(vivienda.p35)
                else:
                    print "No idea u.u"

                if vivienda.p22_b==None:
                    p22_b=''
                else:
                    p22_b = vivienda.p22_b


                if vivienda.p24==None:
                    p24=''
                else:
                    p24 = vivienda.p24

                if vivienda.p25==None:
                    p25=''
                else:
                    p25 = vivienda.p25

                if vivienda.p26==None:
                    p26=''
                else:
                    p26 = vivienda.p26
                # Bloque Listado
                table2 = [(str(
                    vivienda.or_viv_aeu if not vivienda.or_viv_aeu == 0 or vivienda.or_viv_aeu == '0'  else '').decode(
                    'latin-1'),
                           str(vivienda.manzana).decode('latin-1'),
                           str(vivienda.frente_ord).decode('latin-1'),
                           str(vivienda.p20.p20_nombre).decode('latin-1') if vivienda.p20 else "",
                           str(vivienda.p21).decode('latin-1'),
                           str(str(vivienda.p22_a) + str(p22_b)).decode('latin-1'),
                           str(str(vivienda.p23) if vivienda.p23 == 0 else "").decode('latin-1'),
                           str(p24).decode('latin-1'),
                           str(p25).decode('latin-1'),
                           str(p26).decode('latin-1'),
                           str(str(vivienda.p27_a) + str(vivienda.p27_b)).decode('latin-1'),
                           # 1 if a > b else -1
                           str(str(vivienda.p28) if vivienda.p28 == 0 else "").decode('latin-1'),
                           str(jefe_hogar if not jefe_hogar == None else '').decode('latin-1'))
                          ]
                u_second = Table(table2,
                          colWidths=[0.8 * cm, 0.9 * cm, 0.8 * cm, 1.2 * cm, 2.5 * cm, 1.2 * cm, 1 * cm, 1 * cm, 1 * cm,
                                     1 * cm, 1.1 * cm, 0.5 * cm, 5.8 * cm],
                          rowHeights=[0.5 * cm])

                u_second.setStyle(TableStyle(
                    [
                        ('GRID', (1, 1), (-2, -2), 1, colors.black),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 0), (12, 0), 7),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]
                ))
                story.append(u_second)

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


    # total = int(str(ViviendaUrbana.objects.filter(ubigeo=distrito.ubigeo, zona='00100').values_list('id_reg_or', flat=True).distinct().count()))
    lista_distrito = []

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
    #lista_distrito.append('080205')
    #lista_distrito.append('080206')
    #lista_distrito.append('080207')
    # lista_distrito.append('080402')
    # lista_distrito.append('080407')
    # lista_distrito.append('090203')
    # lista_distrito.append('090208')
    # lista_distrito.append('090301')
    # lista_distrito.append('110107')
    # lista_distrito.append('110204')
    # lista_distrito.append('120201')
    # lista_distrito.append('120501')
    # # lista_distrito.append('120708')
    # lista_distrito.append('130202')
    # lista_distrito.append('131203')
    # lista_distrito.append('130701')
    # # lista_distrito.append('130705')
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
    #
    # lista_distrito.append('210407')
    # lista_distrito.append('230106')
    # lista_distrito.append('230109')
    # lista_distrito.append('240103')
    # lista_distrito.append('240105')
    # lista_distrito.append('240106')



    lista =[]
    tam_dist = 3
    for ubigeos in range(len(lista_distrito)):
        total_zonas = int(str(Esp_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos]).values_list('zona', flat=True).distinct().count()))
        for zona_t in range(total_zonas):
            zoner = str(zona_t+1).zfill(3)+"00"
            total_aes_zona = int(str(Esp_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos], zona= zoner).count()))
            for aeu in range(total_aes_zona):
                # list.append(aeu+1)
                 lista.append(str(zona_t + 1)+": " + str(aeu + 1) + "<br/>")
                 # str(zona_t + 1)+": " + str(aeu + 1) + "<br/>"
                 generar_pdf(request,lista_distrito[ubigeos],zoner, str(aeu+1))
    return HttpResponse(lista)
    # return HttpResponse(list)

