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


def generar_pdf(request, ubigeo, zonal, aeut):
    print "Se va a generar el PDF de Ubigeo: "+ str(ubigeo)+ " de zona: " + str(zonal) + " y AE: "+str(aeut)
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



    # cond_viv = Aeus.objects.filter(ubigeo=distrito.ubigeo, zona='00100', aeu_final=aeut)

    # total = Aeus.objects.filter(ubigeo=distrito.ubigeo, zona='00100', aeu_final=aeut).count()

    # viv_u = ViviendaU.objects.filter(ubigeo=ubigeo)

    rango_equivalencia = [[1, 'A'], [2, 'B'], [3, 'C'], [4, 'D'], [5, 'E'], [6, 'F'], [7, 'G'], [8, 'H'], [9, 'I'],
                          [10, 'J'], [11, 'K'], [12, 'L'], [13, 'M'], [14, 'N'], [15, 'O'], [16, 'P'], [17, 'Q'], [18, 'R'],
                          [19, 'S'], [20, 'T'], [21, 'U'], [22, 'V'], [23, 'W'], [24, 'X'], [25, 'Y'], [26, 'Z']
                          ]


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
    cond =v_ReporteCabViviendasTab.objects.filter(ubigeo=ubigeo, zona=zonal, aeu_final=aeut)
    x = 0

    lista_zonas = []
    for aeu in cond:
        x = x + 1
        y = x

        secc = str(aeu.seccion).zfill(3)
        aeus = str(aeu.aeu_final).zfill(3)
        aeut_conv = str(aeu.aeu_final).zfill(3)

        lista_distritos = []
        lista_distritos.append(ubigeo)
        listin = []
        tam_dis = 1
        for ubigein in range(tam_dis):

            if os.path.exists("\\\srv-fileserver\\CPV2017\\list_segm_tab\\" + str(lista_distritos[ubigein])) == False:
                os.mkdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\" + str(lista_distritos[ubigein]))

            total_zonas = int(str(Esp_Aeus.objects.filter(ubigeo=lista_distritos[ubigein]).values_list('zona',flat=True).distinct().count()))
            total_zonales = Esp_Aeus.objects.filter(ubigeo=lista_distritos[ubigein]).values_list('zona', flat=True)
            cuchi = list(set(total_zonales))
            lista_zonas.append(total_zonas)

            for zona_t in range(total_zonas):
                #zoner = str(zona_t + 1).zfill(3) + "00"
                listin.append(str(lista_distritos[ubigein]) + ": " + cuchi[zona_t] + "<br/>")
                if os.path.exists("\\\srv-fileserver\\CPV2017\\list_segm_tab\\" + str(lista_distritos[ubigein]) + "\\" + cuchi[zona_t]) == False:
                    os.mkdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\" + str(lista_distritos[ubigein]) + "\\" + cuchi[zona_t])
                    # destino = "\\\srv-fileserver\\CPV2017\\list_segm_tab\\" + str(lista_distritos[ubigein]) + "\\" + zoner+ "\\" + str(ubigeo) + zonal + str(secc)+str(aeut) + ".pdf"
                    #
                    #
                    #
                    # doc2 = SimpleDocTemplate(destino, pagesize=A4,
                    #                                        rightMargin=70,
                    #                                        leftMargin=70,
                    #                                        topMargin=0.5 * cm,
                    #                                        bottomMargin=0.5 * cm, )

        destino = "\\\srv-fileserver\\CPV2017\\list_segm_tab\\" + str(ubigeo) + "\\" + zonal+ "\\" + str(ubigeo) + zonal + str(secc) + str(aeut_conv) + ".pdf"
        doc2 = SimpleDocTemplate(destino, pagesize=A4,
                                          rightMargin=70,
                                          leftMargin=70,
                                          topMargin=0.5 * cm,
                                          bottomMargin=0.5 * cm,)
        # destino =  "\\\srv-fileserver\\CPV2017\\list_segm_tab\\" + str(ubigeo) + zonal + str(secc)+str(aeut) + ".pdf"
        #
        # doc2 = SimpleDocTemplate(destino, pagesize=A4,
        #                          rightMargin=70,
        #                          leftMargin=70,
        #                          topMargin=0.5 * cm,
        #                          bottomMargin=0.5 * cm, )

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
        #story.append(table_bar)
        # zona_temp = aeu.zona[0:3]
        # zona_int = int(aeu.zona[3:])
        # zona_int_eq = ""
        # for el in rango_equivalencia:
        #     if (el[0] == zona_int):
        #         zona_int_eq = el[1]
        # zona_temp = zona_temp + str(zona_int_eq)
        data = [
            ['', '', '', '', '', Paragraph('<strong>Doc. CPV</strong>', h4)],
            [Paragraph('<strong>A. UBICACIÓN GEOGRÁFICA</strong>', h11), '', '', '',
             Paragraph('<strong>B. UBICACIÓN CENSAL</strong>', h11), ''],
            [Paragraph('<strong>DEPARTAMENTO</strong>', h1),Paragraph(str(aeu.ccdd), h_center),
             Paragraph(str(aeu.departamento), h1), '',
             Paragraph('<strong>ZONA Nº</strong>', h1),Paragraph(aeu.zona_convert, h_center)],
            [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(aeu.ccpp, h_center),
             Paragraph(str(aeu.provincia).decode('latin-1'), h1), '', Paragraph(str('<strong>SECCIÓN Nº</strong>'), h1), Paragraph(str(aeu.seccion_convert), h_center)],
            [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph(aeu.ccdi, h_center), Paragraph(aeu.distrito, h1),
             '', Paragraph('<strong>A.E.U. Nº</strong>', h1), Paragraph(aeus, h_center)],
            [Paragraph('<strong>CENTRO POBLADO</strong>', h1), Paragraph(aeu.nomccpp, h1), '', '', '', ''],
            [Paragraph('<strong>CATEGORÍA DEL CENTRO POBLADO</strong>', h1), Paragraph('CIUDAD', h1), '', '',
             Paragraph('<strong>TOTAL DE VIVIENDAS<br/>DEL A.E.U.</strong>', h1),Paragraph(str(aeu.cant_viv), h_center)],
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

        obs_data = [
            [Paragraph(e, h3) for e in ["<strong>Viv Nº</strong>",
                                        "<strong>Mz Nº</strong>",
                                        "<strong>Ord Reg</strong>",
                                        "<strong>Frent Nº</strong>",
                                        "<strong>DIRECCIÓN DE LA VIVIENDA</strong>",
                                        "", "", "", "", "", "", "", "",
                                        "<strong>Nombres y Apellidos del JEFE DEL HOGAR</strong>"]],
            [Paragraph(e, h3) for e in ["", "", "", "",
                                        "<strong>Tipo de Vía</strong>",
                                        "<strong>Nombre de Vía</strong>",
                                        "<strong>Nº de Puerta</strong>",
                                        "<strong>Block</strong>",
                                        "<strong>Mz Nº</strong>",
                                        "<strong>Lote Nº</strong>",
                                        "<strong>Piso Nº</strong>",
                                        "<strong>Int. Nº</strong>",
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
                  colWidths=[0.8 * cm, 0.8 * cm, 1 * cm, 1.1 * cm, 1.8 * cm, 2.6 * cm, 1.2 * cm, 1.1 * cm, 0.8 * cm, 1 * cm,
                             1 * cm, 0.9 * cm, 0.9 * cm, 4.7 * cm])
        c.setStyle(TableStyle(
            [
                ('GRID', (1, 1), (-2, -2), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                # ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
                ('BACKGROUND', (0, 0), (-1, 1), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
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
            [Paragraph('<strong>A. UBICACIÓN GEOGRÁFICA</strong>', h1), '', '', '',
             Paragraph('<strong>B. UBICACIÓN CENSAL</strong>', h1), ''],
            [Paragraph('<strong>DEPARTAMENTO</strong>', h1),Paragraph(str(aeu.ccdd), h1),
             Paragraph(str(aeu.departamento), h1), '',
             Paragraph('<strong>ZONA Nº</strong>', h1),Paragraph(aeu.zona_convert, h1)],
            [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(aeu.ccpp, h1),
             Paragraph(str(aeu.provincia).decode('latin-1'), h1), '', Paragraph(str('<strong>SECCIÓN Nº</strong>'), h1), aeu.seccion_convert],
            [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph(aeu.ccdi, h1), Paragraph(aeu.distrito, h1),
             '', Paragraph('<strong>A.E.U. Nº</strong>', h1), aeu.aeu_final],
            [Paragraph('<strong>CENTRO POBLADO</strong>', h1), Paragraph(aeu.nomccpp, h1), '', '', '', ''],
            [Paragraph('<strong>CATEGORÍA DEL<br/>CENTRO POBLADO</strong>', h1), Paragraph('CIUDAD', h1), '', '',
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
        fichero_imagen = 'Reporte/Croquis/Zona' + ubigeo + '00100' + '/Croquis' + ubigeo + '00100' + str(aeut) + '.png'

        story.append(t_croq)
        story.append(Spacer(0, 2 * mm))
        story.append(tables)
        story.append(Spacer(0, 3 * mm))
        story.append(c)

        viviendas = v_ReporteViviendas_Tab.objects.filter(Q(ubigeo=ubigeo), Q(zona=zonal), Q(aeu_final=aeut)).order_by('manzana', 'id_reg_or')[0:18]

        toti_viv = int(v_ReporteViviendas_Tab.objects.filter(Q(ubigeo=ubigeo), Q(zona=zonal), Q(aeu_final=aeut)).count())
        for vivienda in viviendas:
            i=i+1
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
                print "No idea u.u"

            jefe_h = u'{}'.format(jefe_hogar)

            if jefe_h != None and jefe_h.count(' ') > 2 and len(jefe_h) > 26  and len(jefe_h) < 28:
                print "Mayor a 26 caracteres"
                jefe_jug = jefe_h.rsplit(' ', 1)
                jefe_home = jefe_jug[0] + '\n' + jefe_jug[1]
            # elif jefe_h != None and jefe_h!= type(1) and  jefe_h ==type('a') and jefe_h.count(' ') < 1:
            #     print "Entro segunda condicion"
            #
            #     jefe_home = jefe_hogar
            # elif jefe_h != None and jefe_h!= type(1) and  jefe_h ==type('a') and jefe_h.count(' ') == 0:
            #     print "Entro tercera condicion"
            #     # jefe_jug = jefe_h.rsplit(' ', 1)
            #     jefe_home = jefe_hogar
            if jefe_h != None and jefe_h.count(' ') > 2 and len(jefe_h) > 28:
                print "Mayor a 26 caracteres"
                jefe_jug = jefe_h.rsplit(' ', 2)
                jefe_home = jefe_jug[0] + '\n' + jefe_jug[1]+ ' '+ jefe_jug[2]
            elif jefe_h==type(1) or jefe_h==type('a'):
                print "Mayor a 26 caracteres enteero"

                jefe_home = jefe_hogar
            else:
                print "Entro cuarta"
                jefe_home = jefe_hogar
            # Bloque Listado
            if(vivienda.p22_a==None):
                p22_a = ''
            else:
                p22_a = vivienda.p22_a
            if(vivienda.p22_b==None):
                p22_b = ''
            else:
                p22_b = vivienda.p22_b
            if(vivienda.p24==None):
                p24 = ''
            else:
                p24 = vivienda.p24
            if (vivienda.p25 == None):
                p25 = ''
            else:
                p25 = vivienda.p25
            if (vivienda.p26 == None):
                p26 = ''
            else:
                p26 = vivienda.p26

            if vivienda.or_viv_aeu == 0:
                id_reg_or = ''
            else:
                id_reg_or = vivienda.id_reg_or

            p21 = vivienda.p21

            if len(p21) > 13 and p21.count(' ')==1:
                print "mas de 111111"
                jug_p21 = p21.rsplit(' ', 1)

                # firstblank_viviendap21 = (vivienda.p21).index(' ')
                p21 = jug_p21[0] + '\n' + jug_p21[1]
            elif len(p21)>13 and p21.count(' ')==2:
                jug_p21 = p21.rsplit(' ',2)
                p21 = jug_p21[0] + '\n' + jug_p21[1] + ' ' +jug_p21[2]
            elif len(p21)>13 and p21.count(' ')==3:
                jug_p21 = p21.rsplit(' ',3)
                p21 = jug_p21[0] + '\n' + jug_p21[1] + ' ' +jug_p21[2] +' ' +jug_p21[3]
            elif len(p21)>13 and p21.count(' ')==4:
                jug_p21 = p21.rsplit(' ',4)
                p21 = jug_p21[0] + '\n' + jug_p21[1] + ' ' +jug_p21[2] +' ' +jug_p21[3]+' ' +jug_p21[4]
            else:
                print "mas de 166666666666"
                p21 = vivienda.p21
                #p21 = jug_p21[0] + '\n' + jug_p21[1]

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
                      colWidths=[0.8 * cm, 0.8 * cm, 1 * cm, 1.1 * cm, 1.8 * cm, 2.6 * cm, 1.2 * cm, 1.1 * cm, 0.8 * cm, 1 * cm,
                             1 * cm, 0.9 * cm, 0.9 * cm, 4.7 * cm],
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
            #u.wrapOn(c, width, height)
            story.append(u)

        if toti_viv>18:
            story.append(c)
            # inicio = range(16, toti_viv, 24)
            # fin = range(40, toti_viv, 24)
            # ini = 18
            # rango = 24
            # dato = 18
            #
            # while dato<toti_viv:
            #     dato = dato + rango
            #
            #
            #
            # inicio = list(range(ini,dato-(rango-1),rango))
            # final = list(range(ini+rango, dato+1, rango))
            #
            # final[-1]= toti_viv
            #
            # largo = zip(inicio, final)
            largo = rangos_registros(toti_viv)

            for i in largo:



                viviendas_second = v_ReporteViviendas_Tab.objects.filter(Q(ubigeo=ubigeo), Q(zona=zonal),Q(aeu_final=aeut)).order_by('manzana',
                                                                                                     'id_reg_or')[i[0]:i[1]]


                for vivienda in viviendas_second:
                    #i = i + 1

                    pep2 = vivienda.p29_a

                    for el in equi_pta:
                        if (el[0] == pep2):
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
                        print "No idea u.u"



                    jefe_h = u'{}'.format(jefe_hogar)

                    if jefe_h != None and jefe_h.count(' ') > 2 and len(jefe_h) > 26 and len(jefe_h) < 28:
                        print "Mayor a 26 caracteres"
                        jefe_jug = jefe_h.rsplit(' ', 1)
                        jefe_home = jefe_jug[0] + '\n' + jefe_jug[1]
                    # elif jefe_h != None and jefe_h!= type(1) and  jefe_h ==type('a') and jefe_h.count(' ') < 1:
                    #     print "Entro segunda condicion"
                    #
                    #     jefe_home = jefe_hogar
                    # elif jefe_h != None and jefe_h!= type(1) and  jefe_h ==type('a') and jefe_h.count(' ') == 0:
                    #     print "Entro tercera condicion"
                    #     # jefe_jug = jefe_h.rsplit(' ', 1)
                    #     jefe_home = jefe_hogar
                    if jefe_h != None and jefe_h.count(' ') > 2 and len(jefe_h) > 28:
                        print "Mayor a 26 caracteres"
                        jefe_jug = jefe_h.rsplit(' ', 2)
                        jefe_home = jefe_jug[0] + '\n' + jefe_jug[1] + ' ' + jefe_jug[2]
                    elif jefe_h == type(1) or jefe_h == type('a'):
                        print "Mayor a 26 caracteres enteero"

                        jefe_home = jefe_hogar
                    else:
                        print "Entro cuarta"
                        jefe_home = jefe_hogar

                    # Bloque Listado
                    if (vivienda.p22_a == None):
                        p22_a = ''
                    else:
                        p22_a = vivienda.p22_a
                    if (vivienda.p22_b == None):
                        p22_b = ''
                    else:
                        p22_b = vivienda.p22_b
                    if (vivienda.p24 == None):
                        p24 = ''
                    else:
                        p24 = vivienda.p24
                    if (vivienda.p25 == None):
                        p25 = ''
                    else:
                        p25 = vivienda.p25
                    if (vivienda.p26 == None):
                        p26 = ''
                    else:
                        p26 = vivienda.p26

                    if vivienda.or_viv_aeu == 0:
                        id_reg_or = ''
                    else:
                        id_reg_or = vivienda.id_reg_or

                    p21 = vivienda.p21

                    if len(p21) > 13 and p21.count(' ') == 1:
                        print "mas de 111111"
                        jug_p21 = p21.rsplit(' ', 1)

                        # firstblank_viviendap21 = (vivienda.p21).index(' ')
                        p21 = jug_p21[0] + '\n' + jug_p21[1]
                    elif len(p21) > 13 and p21.count(' ') == 2:
                        jug_p21 = p21.rsplit(' ', 2)
                        p21 = jug_p21[0] + '\n' + jug_p21[1] + ' ' + jug_p21[2]
                    elif len(p21) > 13 and p21.count(' ') == 3:
                        jug_p21 = p21.rsplit(' ', 3)
                        p21 = jug_p21[0] + '\n' + jug_p21[1] + ' ' + jug_p21[2] + ' ' + jug_p21[3]
                    else:
                        print "mas de 166666666666"
                        p21 = vivienda.p21
                        # p21 = jug_p21[0] + '\n' + jug_p21[1]

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
                           vivienda.p28 if vivienda.p28 == 0 else "",
                           jefe_home if not jefe_home == None else '')
                          ]
                    u_second = Table(table2,
                              colWidths=[0.8 * cm, 0.8 * cm, 1 * cm, 1.1 * cm, 1.8 * cm, 2.6 * cm, 1.2 * cm, 1.1 * cm, 0.8 * cm, 1 * cm,
                                 1 * cm, 0.9 * cm, 0.9 * cm, 4.7 * cm],
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
                story.append(PageBreak())
                story.append(c)
            del story[-1]
            del story[-1]

            # obs_data_two = [
            #     [Paragraph(e, h3) for e in ["<strong>Viv Nº</strong>",
            #                                 "<strong>Mz Nº</strong>",
            #                                 "<strong>Or Reg</strong>",
            #                                 "<strong>Frent Nº</strong>",
            #                                 "<strong>DIRECCIÓN DE LA VIVIENDA</strong>",
            #                                 "", "", "", "", "", "", "", "",
            #                                 "<strong>Nombres y Apellidos del JEFE DEL HOGAR</strong>"]],
            #     [Paragraph(e, h3) for e in ["", "", "", "",
            #                                 "<strong>Tipo de Vía</strong>",
            #                                 "<strong>Nombre de VÍa</strong>",
            #                                 "<strong>Nº de Puerta</strong>",
            #                                 "<strong>Block</strong>",
            #                                 "<strong>Mz Nº</strong>",
            #                                 "<strong>Lote Nº</strong>",
            #                                 "<strong>Piso Nº</strong>",
            #                                 "<strong>Int. Nº</strong>",
            #                                 "<strong>Km. Nº</strong>",
            #                                 ""]],
            #     [Paragraph(e, h3) for e in ["<strong>(1)</strong>",
            #                                 "<strong>(2)</strong>",
            #                                 "<strong>(3)</strong>",
            #                                 "<strong>(4)</strong>",
            #                                 "<strong>(5)</strong>",
            #                                 "<strong>(6)</strong>",
            #                                 "<strong>(7)</strong>",
            #                                 "<strong>(8)</strong>",
            #                                 "<strong>(9)</strong>",
            #                                 "<strong>(10)</strong>",
            #                                 "<strong>(11)</strong>",
            #                                 "<strong>(12)</strong>",
            #                                 "<strong>(13)</strong>",
            #                                 "<strong>(14)</strong>"]],
            # ]
            # c_2 = Table(obs_data_two,
            #           colWidths=[0.8 * cm, 0.8 * cm, 1 * cm, 1.1 * cm, 1.8 * cm, 2.6 * cm, 1.2 * cm, 1.1 * cm, 0.8 * cm, 1 * cm,
            #                  1 * cm, 0.9 * cm, 0.9 * cm, 4.7 * cm])
            # c_2.setStyle(TableStyle(
            #     [
            #         ('GRID', (1, 1), (-2, -2), 1, colors.black),
            #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
            #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
            #         # ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
            #         ('FONTSIZE', (0, 0), (-1, -1), 7),
            #         ('BACKGROUND', (0, 0), (-1, 0), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            #         ('BACKGROUND', (0, 0), (-1, 1), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            #         ('SPAN', (4, 0), (12, 0)),
            #         ('SPAN', (0, 0), (0, 1)),
            #         ('SPAN', (1, 0), (1, 1)),
            #         ('SPAN', (2, 0), (2, 1)),
            #         ('SPAN', (3, 0), (3, 1)),
            #         ('SPAN', (13, 0), (13, 1)),
            #         ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            #         ('BACKGROUND', (0, 0), (13, 2), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            #     ]
            # ))

            # viviendas_three = v_ReporteViviendas_Tab.objects.filter(Q(ubigeo=ubigeo), Q(zona=zonal),Q(aeu_final=aeut)).order_by('manzana',
            #                                                                                      'id_reg_or')[41:]
            #
            # if toti_viv > 41:
            #     story.append(c_2)
            #
            #     inicio = range(32, toti_viv, 52)
            #     fin = range(85, toti_viv, 52)
            #     nhojas = len(zip(inicio, fin))
            #     for vivienda in viviendas_three:
            #         i = i + 1
            #
            #         pep2 = vivienda.p29_a
            #
            #         for el in equi_pta:
            #             if (el[0] == pep2):
            #                 pta_f = el[1]
            #
            #         jefe_hogar = ""
            #         if vivienda.p29 == 1 or vivienda.p29 == 3:
            #             jefe_hogar = vivienda.p32
            #         elif vivienda.p29 == 5:
            #             if vivienda.p29_a in (1, 2, 3, 4):
            #                 jefe_hogar = pta_f + "" + vivienda.p29_p
            #             elif vivienda.p29_a in (5, 6):
            #                 jefe_hogar = pta_f
            #             elif vivienda.p29_a == 7:
            #                 jefe_hogar = vivienda.p29_o
            #             elif vivienda.p29_a == 8:
            #                 jefe_hogar = vivienda.p29_8_o
            #         elif vivienda.p29 == 2 or vivienda.p29 == 4:
            #             jefe_hogar = vivienda.p35
            #         else:
            #             print "No idea u.u"
            #
            #         jefe_h = jefe_hogar
            #
            #         if jefe_h != None and jefe_h == type('a') and  jefe_h ==type('a') and len(jefe_h) > 25 and jefe_h.count(' ') >= 3:
            #             print "Entroooooo  nombre 2222"
            #             jefe_jug = jefe_h.rsplit(' ', 2)
            #             jefe_home = jefe_jug[0] + '\n' + jefe_jug[1]
            #         elif jefe_h != None and jefe_h != type(1) and  jefe_h ==type('a') and jefe_h.count(' ') < 3:
            #             print "Entro nombre normal"
            #
            #             jefe_home = jefe_hogar
            #         elif jefe_h != None and jefe_h!= type(1) and  jefe_h ==type('a') and jefe_h.count(' ') == 0:
            #             print "Entro nombre normal"
            #             # jefe_jug = jefe_h.rsplit(' ', 1)
            #             jefe_home = jefe_hogar
            #         else:
            #             jefe_home = jefe_hogar
            #         # Bloque Listado
            #         if (vivienda.p22_a == None):
            #             p22_a = ''
            #         else:
            #             p22_a = vivienda.p22_a
            #         if (vivienda.p22_b == None):
            #             p22_b = ''
            #         else:
            #             p22_b = vivienda.p22_b
            #         if (vivienda.p24 == None):
            #             p24 = ''
            #         else:
            #             p24 = vivienda.p24
            #         if (vivienda.p25 == None):
            #             p25 = ''
            #         else:
            #             p25 = vivienda.p25
            #         if (vivienda.p26 == None):
            #             p26 = ''
            #         else:
            #             p26 = vivienda.p26
            #
            #         if vivienda.or_viv_aeu == 0:
            #             id_reg_or = ''
            #         else:
            #             id_reg_or = vivienda.id_reg_or
            #
            #         p21 = vivienda.p21
            #
            #         if len(p21) > 11 and p21.count(' ') > 2:
            #             print "mas de 111111"
            #             jug_p21 = p21.rsplit(' ', 2)
            #
            #             # firstblank_viviendap21 = (vivienda.p21).index(' ')
            #             p21 = jug_p21[0] + '\n' + jug_p21[1]
            #         else:
            #             print "mas de 166666666666"
            #             jug_p21 = p21.rsplit(' ', 1)
            #             p21 = jug_p21[0] + '\n' + jug_p21[1]
            #         table2 = [
            #             (vivienda.or_viv_aeu if not vivienda.or_viv_aeu == 0 or vivienda.or_viv_aeu == '0'  else '',
            #              vivienda.manzana,
            #              id_reg_or,
            #              vivienda.frente_ord,
            #              vivienda.p20_nombre if vivienda.p20 else "",
            #              p21,
            #              p22_a + p22_b,
            #              vivienda.p23 if vivienda.p23 == 0 else "",
            #              p24,
            #              p25,
            #              p26,
            #              vivienda.p27_a if not vivienda.p27_a == None else '' + vivienda.p27_b if not vivienda.p27_b == None else '',
            #              vivienda.p28 if vivienda.p28 == 0 else "",
            #              jefe_home if not jefe_home == None else '')
            #             ]
            #         u_three= Table(table2,
            #                          colWidths=[0.8 * cm, 0.8 * cm, 1 * cm, 1.1 * cm, 1.8 * cm, 2.6 * cm, 1.2 * cm, 1.1 * cm, 0.8 * cm, 1 * cm,
            #                  1 * cm, 0.9 * cm, 0.9 * cm, 4.7 * cm],
            #                          rowHeights=[1 * cm])
            #
            #         u_three.setStyle(TableStyle(
            #             [
            #                 ('GRID', (1, 1), (-2, -2), 1, colors.black),
            #                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
            #                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
            #                 ('FONTSIZE', (0, 0), (13, 0), 7),
            #                 ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            #             ]
            #         ))
            #         story.append(u_three)
        # if(PageBreak()):
        #     story.append(Spacer(0, 22 * cm))
        #     story.append(table_obs)
        #     story.append(Spacer(0, 1 * mm))
        #     story.append(table_empa_cuerp)
        # else:
        story.append(Spacer(0, 1 * cm))
        #story.append(table_obs)
        story.append(Spacer(0, 1 * mm))
        story.append(table_empa_cuerp)
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
        story.append(Spacer(0, 1 * mm))
        #story.append(p_page)
        # else:
        #     story.append(Spacer(0, 21 * cm))
        #     story.append(table_obs)
        #     story.append(Spacer(0, 1 * mm))
        #     sory.append(table_empa_cuerp)
        #     story.append(Spacer(0, 1 * mm))
        #     story.append(p_page)

    doc2.build(story)
    doc.build(story)
    response.write(buff.getvalue())
    buff.close()
    return response


def rangos_registros(registros):
    ini = 18
    rango = 25
    dato = 18
    while dato < registros:
        dato = dato + rango

    inicio = list(range(ini, dato - (rango - 1), rango))
    final = list(range(ini + rango, dato + 1, rango))

    final[-1] = registros

    largo = zip(inicio, final)

    return largo

def generar_lote(request):

    lista_distrito = []

    # lista_distrito.append('020601')
    # lista_distrito.append('090301')
    # lista_distrito.append('090208')
    # lista_distrito.append('050619')
    # lista_distrito.append('050617')
    # lista_distrito.append('140107')
    # lista_distrito.append('030602')
    # lista_distrito.append('021509')
    # lista_distrito.append('021509')
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
    # lista_distrito.append('080302')
    # lista_distrito.append('080402')
    # lista_distrito.append('080407')
    # lista_distrito.append('090203')
    # lista_distrito.append('090208')
    # lista_distrito.append('090301')
    #lista_distrito.append('110107')
    # lista_distrito.append('110204')
    # lista_distrito.append('120201')
    #lista_distrito.append('120501')
    # # lista_distrito.append('120708')
    # lista_distrito.append('130202')
    # lista_distrito.append('130701')
    # # lista_distrito.append('130705')
    # lista_distrito.append('131203')
    # lista_distrito.append('140107')
    # lista_distrito.append('150125')
    # lista_distrito.append('150508')
    # lista_distrito.append('150604')
    lista_distrito.append('150108')
    # lista_distrito.append('150705')
    # lista_distrito.append('170102')
    # lista_distrito.append('180106')
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

    lista_zonas = []
    lista =[]

    for ubigeos in lista_distrito:
        # total_zonas = int(str(Tab_Aeus.objects.filter(ubigeo=ubigeos).values_list('zona', flat=True).distinct().count()))
        # total_zonales = Esp_Aeus.objects.filter(ubigeo=ubigeos).values_list('zona', flat=True)
        # cuchi = list(set(total_zonales))
        # lista_zonas.append(total_zonas)

        total_zonales = Tab_Aeus.objects.filter(ubigeo=ubigeos, zona = '00100').values_list('zona', flat=True)
        zona_dif = list(set(total_zonales))
        for zona_t in zona_dif:

            total_aes_zona = Tab_Aeus.objects.filter(ubigeo=ubigeos, zona=zona_t).values_list('aeu_final', flat=True).order_by('aeu_final')[75:]
            for aeu in total_aes_zona:
                # list.append(aeu+1)
                 lista.append(str(zona_t)+": " + str(aeu + 1) + "<br/>")
                 # str(zona_t + 1)+": " + str(aeu + 1) + "<br/>"
                 generar_pdf(request,ubigeos, zona_t, aeu)

    return HttpResponse(lista)

