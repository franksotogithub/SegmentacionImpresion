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


def generar_pdf(request, ubigeo, scr_inic):
    print "generar_pdf"
    MARGIN_SIZE = 17 * mm
    PAGE_SIZE = A4
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=" + ubigeo + "001" + ".pdf"
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
        alignment=TA_CENTER
    )
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

    caso = Seg_R_Secc_Ccpp.objects.filter(ubigeo=ubigeo, scr_ini=scr_inic)[0:1]
    #Q(ubigeo=ubigeo), Q(zona=zonal)
    for aeu_v in caso:
        idaer = aeu_v.idaer
        idscr = aeu_v.idscr

        scr_ini = aeu_v.scr_ini

        print idaer
        print idscr

        secc_ini = idscr[6:8]

        secc_fin = idscr[8:10]

        x = x + 1
        y = x
        lista_distritos = []
        lista_distritos.append(ubigeo)

        for ubigein in range(len(lista_distritos)):

            if os.path.exists("\\\srv-fileserver\\CPV2017\\list_seg_esp_rur\\" + str(lista_distritos[ubigein])) == False:
                os.mkdir("\\\srv-fileserver\\CPV2017\\list_seg_esp_rur\\" + str(lista_distritos[ubigein]))

        pdf = "{}-{}-{}.pdf".format(ubigeo, idscr[6:8], idscr[8:10])

        print pdf

        destino = "\\\srv-fileserver\\CPV2017\\list_seg_esp_rur\\" + str(ubigeo) + "\\" + str(pdf)

        print destino

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
        #
        # string = str(ubigeo)+str(secc)+str(aeut)
        # st = code39.Extended39(string)
        #
        # bar_string = Paragraph(string, h_bar)

        pi = Paragraph("-", h2)
        # st_b = st

        # table_bar = Table(
        #     data = [
        #         [pi, st_b],
        #         ['', bar_string]
        #     ],
        #     colWidths= [13 * cm, 5 * cm],
        #     style=[
        #         ('ALIGN', (0, 0), (-1, -1),'CENTER')
        #     ]
        # )

        # story.append(table_bar)

        viviendas_totales = Vw_Seg_Esp_R_Secdist_Secc.objects.filter(idscr=idscr).order_by('idaer','codccpp')

        total_viv = 0
        for viviendon in viviendas_totales:
            total_viv = total_viv + viviendon.viv_ccpp

        data = [
            ['', '', '', '', Paragraph('<strong>Doc. CPV</strong>', h4),''],
            [Paragraph('<strong>A. UBICACION GEOGRAFICA</strong>', h11), '', '', '',Paragraph('<strong>B. UBICACION CENSAL</strong>', h11), ''],
            [Paragraph('<strong>DEPARTAMENTO</strong>', h1),Paragraph(str(distrito.ccdd.ccdd), h_center),Paragraph(str(distrito.ccdd.departamento), h1), '',Paragraph('<strong>SECCIÓN Nº</strong>', h1),Paragraph('Del '+secc_ini+' Al '+secc_fin, h1)],
            [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(distrito.ccpp, h_center),Paragraph(distrito.cod_prov.provincia, h1), '', '',''],
            [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph(distrito.ccdi, h_center), Paragraph(distrito.distrito, h1),'', Paragraph('<strong>C. TOTAL DE VIVIENDAS DE LA SECCIÓN.</strong>', h1),Paragraph(str(total_viv), h1)],
            #Paragraph('<strong>C. TOTAL DE VIVIENDAS DEL AER.</strong>', h1)
        ]

        tables = Table(data, colWidths=[3.7 * cm, 1 * cm, 7.1 * cm, 0.3 * cm, 4.7 * cm, 2 * cm])
                       # ,
                       # rowHeights=[0.4 * cm, 0.4  * cm, 0.4  * cm, 0.4  * cm, 0.4  * cm, 0.4  * cm, 0.7  * cm])

        tables.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (5, 0), colors.black),
            #('ALIGN', (4, 0), (5, 0), 'RIGHT'),
            #('ALIGN', (1, 2), (1, 4), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            #('GRID', (0, 1), (2, 6), 1, colors.black),
            #('GRID', (4, 1), (5, 4), 1, colors.black),
            ('GRID', (0, 1), (2, 4), 1, colors.black),
            ('GRID', (4, 4), (5, 5), 1, colors.black),
            ('GRID', (4, 1), (5, 2), 1, colors.black),
            ('SPAN', (0, 1), (2, 1)),
            ('SPAN', (4, 1), (5, 1)),
            #('SPAN', (4, 1), (5, 1)),
            #('SPAN', (1, 5), (2, 5)),
            #('SPAN', (1, 6), (2, 6)),
            #('BACKGROUND', (0, 1), (0, 6), colors.Color(219.0/255,229.0/255,241.0/255)),

            ('BACKGROUND', (0, 1), (2, 1), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            ('BACKGROUND', (0, 2), (0, 4), colors.Color(219.0/255,229.0/255,241.0/255)),
            #('BACKGROUND', (4, 2), (4, 3), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            ('BACKGROUND', (4, 1), (4, 2), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            ('BACKGROUND', (4, 4), (4, 4), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('BACKGROUND', (4, 1), (5, 1), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            #('BACKGROUND', (4, 1), (5, 1), colors.Color(219.0/255,229.0/255,241.0/255))
            #('BACKGROUND', (4, 6), (4, 6), colors.Color(219.0/255,229.0/255,241.0/255))
        ]))

        t1 = Paragraph("CENSOS NACIONALES 2017: XII DE POBLACIÓN, VII DE VIVIENDA<br/>Y III DE COMUNIDADES INDÍGENAS",h_sub_tile)
        t1_sub = Paragraph("<strong>LISTADO DE ÁREAS DE EMPADRONAMIENTO DE LA SECCIÓN CENSAL RURAL</strong>", h_sub_tile_2)

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
            [Paragraph(e, h3) for e in ["<strong>D. INFORMACIÓN DE CENTROS POBLADOS Y VIVIENDAS</strong>",
                                        "",
                                        "",
                                        "",
                                        "",
                                        ""]],
            [Paragraph(e, h3) for e in ["<strong>AER Nº</strong>",
                                        "",
                                        "<strong>CENTRO POBLADO</strong>",
                                        "",
                                        "",
                                        "<strong>N° DE VIVIENDAS</strong>"]],
            [Paragraph(e, h3) for e in ["INICIAL",
                                        "<strong>FINAL</strong>",
                                        "<strong>CÓDIGO</strong>",
                                        "<strong>NOMBRE</strong>",
                                        "<strong>CATEGORÍA</strong>",
                                        ""]],
         ]
        c = Table(obs_data,
                  colWidths=[1.3 * cm, 1.3 * cm, 1.7 * cm, 6.5 * cm, 4.9 * cm, 3.2 * cm])

        c.setStyle(TableStyle(
            [
                ('GRID', (1, 1), (-2, -2), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(219.0/255,229.0/255,241.0/255)),
                ('BACKGROUND', (0, 0), (-1, -1), colors.Color(219.0/255,229.0/255,241.0/255)),
                ('SPAN', (0, 0), (5, 0)),
                ('SPAN', (0, 1), (1, 1)),
                ('SPAN', (2, 1), (4, 1)),
                ('SPAN', (5, 1), (5, 2)),
                #('SPAN', (12, 0), (12, 1)),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(219.0/255,229.0/255,241.0/255)),
            ]
        ))

        i=0

        data_croq = [
            ['', '', '', '', Paragraph('<strong>Doc. CPV</strong>', h4), ''],
            [Paragraph('<strong>A. UBICACION GEOGRAFICA</strong>', h11), '', '', '',
             Paragraph('<strong>B. UBICACION CENSAL</strong>', h11), ''],
            [Paragraph('<strong>DEPARTAMENTO</strong>', h1), Paragraph(str(distrito.ccdd.ccdd), h_center),
             Paragraph(str(distrito.ccdd.departamento), h1), '', Paragraph('<strong>SECCIÓN Nº</strong>', h1), ''],
            [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(distrito.ccpp, h_center),
             Paragraph(str(distrito.cod_prov.provincia).decode('latin-1'), h1), '',
             Paragraph(str('<strong>A.E.R. Nº</strong>'), h1), ''],
            [Paragraph('<strong>DISTRITO</strong>', h1), '', '', '', '', ''],
            ['', '', '', '', Paragraph('<strong>C. TOTAL DE VIVIENDAS DEL AER.</strong>', h1), ''],
        ]

        tables_croq = Table(data_croq, colWidths=[2 * cm, 2 * cm, 2 * cm, 5.5 * cm, 2.3 * cm, 4.6 * cm])

        tables_croq.setStyle(TableStyle([
            #('TEXTCOLOR', (0, 0), (5, 0), colors.black),
            #('ALIGN', (4, 0), (5, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 2), (1, 4), 'CENTER'),
            ('GRID', (0, 0), (2, 3), 1, colors.black),
            ('GRID', (4, 5), (1, 3), 1, colors.black),

            ('SPAN', (0, 1), (2, 1)),
            ('SPAN', (0, 1), (2, 1)),
            #('SPAN', (1, 5), (2, 5)),
            #('SPAN', (1, 6), (2, 6)),
            #('BACKGROUND', (4, 1), (5, 5), colors.white),
            ('BACKGROUND', (0, 1), (-1, 1), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('BACKGROUND', (0, 1), (0, 6), colors.Color(219.0/255,229.0/255,241.0/255)),

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

        # story.append(Spacer(0, 1 * mm))
        # story.append(table_obs)
        # story.append(PageBreak())

        # story.append(table_bar)
        story.append(t_croq)
        story.append(Spacer(0, 2 * mm))
        story.append(tables)
        story.append(Spacer(0, 3 * mm))
        story.append(c)

        viviendas = Vw_Seg_Esp_R_Secdist_Secc.objects.filter(idscr=idscr).order_by('idaer','codccpp')

        #toti_viv = int(Vw_Seg_Esp_R_Secdist_Secc.objects.filter(idscr=idscr).count())


        for vivienda in viviendas:
            if vivienda.categoria_o == None:
                categoria_o = ''
            else:
                categoria_o = vivienda.categoria_o
            i = i + 1
            # Bloque Listado



            table2 = [(
                vivienda.aer_ini,
                vivienda.aer_fin,
                vivienda.codccpp,
                vivienda.nomccpp,
                categoria_o,
                vivienda.viv_ccpp
            )
            ]
            u = Table(table2,
                      colWidths=[1.3 * cm, 1.3 * cm, 1.7 * cm, 6.5 * cm, 4.9 * cm, 3.2 * cm],
                      rowHeights=[0.5 * cm])
            u.setStyle(TableStyle(
                [
                    ('GRID', (1, 1), (-2, -2), 1, colors.black),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (5, 0), 7),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (5, 0), (5, 0), 'CENTER'),
                    ('ALIGN', (5, 0), (5, 0), 'CENTER'),
                ]
            ))
            story.append(u)

    doc2.build(story)
    doc.build(story)
    response.write(buff.getvalue())
    buff.close()
    return response

def generar_lote(request):

    lista_distrito = []
    ubigeosa = os.listdir("\\\srv-fileserver\\CPV2017\\croquis_segm_esp\\rural")

    # lista_distrito.append('020601')
    # lista_distrito.append('021509')
    # lista_distrito.append('021806')
    # lista_distrito.append('022001')
    # lista_distrito.append('030212')
    lista_distrito.append('030602')
    # lista_distrito.append('050507')
    lista_distrito.append('050601')
    # lista_distrito.append('050617')
    # lista_distrito.append('060903')
    # lista_distrito.append('080301')
    # lista_distrito.append('080205')
    # lista_distrito.append('080206')
    # lista_distrito.append('080207')
    # lista_distrito.append('080402')
    # lista_distrito.append('080407')
    # lista_distrito.append('090203')
    #lista_distrito.append('090411')
    # lista_distrito.append('090208')
    # lista_distrito.append('090301')
    lista_distrito.append('110104')
    lista_distrito.append('110105')
    lista_distrito.append('110109')
    lista_distrito.append('110114')
    lista_distrito.append('110302')
    lista_distrito.append('110303')
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
    # lista_distrito.append('150508')
    # lista_distrito.append('150604')
    # lista_distrito.append('150705')
    # lista_distrito.append('170102')
    # lista_distrito.append('180106')
    # lista_distrito.append('180208')
    # lista_distrito.append('180210')
    # lista_distrito.append('190111')
    # lista_distrito.append('180210')
    # lista_distrito.append('210407')
    lista_distrito.append('230103')
    lista_distrito.append('230105')
    lista_distrito.append('230301')
    # lista_distrito.append('240103')
    # lista_distrito.append('240105')
    # lista_distrito.append('240106')
    lista =[]

    for ubigeos in ubigeosa:
        total_secciones = int(str(Seg_R_Secc_Ccpp.objects.filter(ubigeo=ubigeos).values_list('scr_ini', flat=True).distinct().count()))
        ubigeo_aer = Seg_R_Secc_Ccpp.objects.filter(ubigeo=ubigeos).values_list('scr_ini', flat=True)
        # models.Shop.objects.order_by().values('city').distinct()
        uchi = list(set(ubigeo_aer))
        for pos in range(total_secciones):
            # list.append(aeu+1)
            lista.append(str(pos + 1)+ ": "+uchi[pos]+"<br/>")
            # str(zona_t + 1)+": " + str(aeu + 1) + "<br/>"
            generar_pdf(request, ubigeos, uchi[pos])
    return HttpResponse(lista)


