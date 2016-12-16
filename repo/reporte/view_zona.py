# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse

# from reportlab.pdfgen.canvas import Canvas
# !/usr/bin/env python

from reportlab.pdfgen import canvas
from django.db.models import Q
from reportes_models import *
from reportes_models import *

from reportlab.lib.pagesizes import A4, cm, inch
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import utils
from reportlab.platypus.flowables import PageBreak, Spacer
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Image, Paragraph, Table, TableStyle
from io import BytesIO

from reportlab.lib.styles import ParagraphStyle as PS
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


def generar_seccion(request, ubigeo, zonaq):
    print "Se va a generar el PDF de Ubigeo:" + str(ubigeo) +" y Zona: "+str(zonaq)
    MARGIN_SIZE = 17 * mm
    PAGE_SIZE = A4

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=" + str(ubigeo) + str(zonaq) + ".pdf"
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
                            topMargin=0.5 *cm,
                            bottomMargin=0.5 *cm,
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
    # rutas = Rutas.objects.get(ubigeo=ubigeo)

    distrito = Distrito.objects.get(ubigeo=ubigeo)

    #cond = Aeus.objects.filter(ubigeo=distrito.ubigeo, zona='00100')
    cond = Vw_Rep_Cab_Zona_Esp.objects.filter(ubigeo=ubigeo, zona=zonaq)

    #total_secc = str(Aeus.objects.filter(ubigeo='020601', zona='00100').values_list('seccion', flat=True).distinct().count())
    total_secc = str(v_ReporteSecciones.objects.filter(ubigeo=ubigeo, zona=zonaq).values_list('seccion', flat=True).distinct().count())

    #total_aeus = str(Aeus.objects.filter(ubigeo=distrito.ubigeo, zona='00100').count())
    total_aeus = str(v_ReporteSecciones.objects.filter(ubigeo=ubigeo, zona=zonaq).count())

    resumen = v_ReporteResumenDistrito.objects.get(ubigeo=ubigeo, zona=zonaq)

    primero = v_ReporteSecciones.objects.filter(ubigeo=distrito.ubigeo, zona=zonaq).order_by('aeu_final').first()
    ultimo = v_ReporteSecciones.objects.filter(ubigeo=distrito.ubigeo, zona=zonaq).order_by('aeu_final').last()

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

    string = str(ubigeo) + str(zonaq)
    st = code39.Extended39(string)

    bar_string = Paragraph(string, h_bar)
        
    pi = Paragraph("", h2)
    st_b = st
        
    table_bar = Table(
            data=[
                [pi, st_b],
                ['', bar_string]
            ],
            colWidths=[15 * cm, 4 * cm],
            style=[
                ('ALIGN', (0, 0), (-1, -1),'CENTER')
            ]
    )

    total=0
    x = 0

    for aeu in cond:
        # string = "02060100100"
        # st = code39.Extended39(string)
        # story.append(st)

        #secc = str(aeu.seccion).zfill(3)
        #aeus = str(aeu.aeu_final).zfill(3)

        # prim = str(primero.aeu_final).zfill(3)
        # ult = str(ultimo.aeu_final).zfill(3)

        prim_secc = str(primero.seccion).zfill(3)
        ulti_secc = str(ultimo.seccion).zfill(3)

        lista_distritos = []
        lista_distritos.append(ubigeo)
        listin = []
        tam_dis = 1
        lista_zonas = []
        for ubigein in range(tam_dis):

            if os.path.exists("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein])) == False:
                os.mkdir("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein]))

            total_zonas = int(str(Tab_Aeus.objects.filter(ubigeo=lista_distritos[ubigein]).values_list('zona',flat=True).distinct().count()))
            total_zonales = Esp_Aeus.objects.filter(ubigeo=lista_distritos[ubigein]).values_list('zona', flat=True)
            cuchi = list(set(total_zonales))
            lista_zonas.append(total_zonas)

            for zona_t in range(total_zonas):
                #zoner = str(zona_t + 1).zfill(3) + "00"
                listin.append(str(lista_distritos[ubigein]) + ": " + cuchi[zona_t] + "<br/>")
                if os.path.exists("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein]) + "\\" + cuchi[zona_t]) == False:
                    os.mkdir("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein]) + "\\" + cuchi[zona_t])



        # destino = "Zonas/" + str(ubigeo) + zonaq + ".pdf"


        # destino = "Zonas/" + str(ubigeo) + zonaq + ".pdf"
        #
        # doc2 = SimpleDocTemplate(destino, pagesize=A4,
        #                          rightMargin=70,
        #                          leftMargin=70,
        #                          topMargin=0.5 * cm,
        #                          bottomMargin=0.5 * cm, )

        tota_viv = tota_viv + int(aeu.cant_viv)

        zona_temp = aeu.zona[0:3]
        zona_int = int(aeu.zona[3:])
        zona_int_eq = ""

    destino = "\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(ubigeo) + "\\" + zonaq + "\\" + str(ubigeo) + zonaq + ".pdf"
    doc2 = SimpleDocTemplate(destino, pagesize=A4,
                             rightMargin=70,
                             leftMargin=70,
                             topMargin=0.5 * cm,
                             bottomMargin=0.5 * cm, )

    for el in rango_equivalencia:
        if (el[0] == zona_int):
            zona_int_eq = el[1]

    # zona_temp = zona_temp + str(zona_int_eq)
    #
    # aeu_tot = str(total_aeus).zfill(3)
    # secc_tot = str(total_secc).zfill(3)
    #
    # nombreccpp=Ccpp.objects.filter(ubigeo=ubigeo,codccpp=aeu.codccpp).values('nomccpp')
    data = [
        ['', '', '', '', '', Paragraph('<strong>Doc. CPV</strong>', h4)],
        [Paragraph('<strong>A. UBICACION GEOGRAFICA</strong>', h11), '', '', '',Paragraph('<strong>B. UBICACION CENSAL</strong>', h11), ''],
        [Paragraph('<strong>DEPARTAMENTO</strong>', h1),Paragraph(str(aeu.ccdd), h_center),
            Paragraph(str(aeu.departamento), h1), '',
            Paragraph('<strong>ZONA Nº</strong>', h1),Paragraph(aeu.zona_convert, h_center)],
        [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(aeu.ccpp, h_center),
            Paragraph(aeu.provincia, h1), '', Paragraph(str('<strong>SECCION Nº</strong>'), h1), Paragraph('DEL '+str(aeu.seccion_inicial)+' AL '+str(aeu.seccion_final), h_center)],
        [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph(aeu.ccdi, h_center), Paragraph(aeu.distrito, h1),
            '', Paragraph('<strong>A.E.U. Nº</strong>', h1), Paragraph("DEL "+ str(aeu.aeu_inicial) +" AL " +str(aeu.aeu_final), h_center)],
        [Paragraph('<strong>CENTRO POBLADO</strong>', h1), Paragraph(aeu.nomccpp, h1), '', '', '', ''],
        [Paragraph('<strong>CATEGORIA DEL CENTRO POBLADO</strong>', h1), Paragraph('CIUDAD', h1), '', '',
            Paragraph('<strong>TOTAL DE VIVIENDAS DE LA ZONA</strong>', h1),Paragraph(str(aeu.cant_viv), h1)],
    ]

    tables = Table(data, colWidths=[3.7 * cm, 1 * cm, 7.1 * cm, 0.3 * cm, 4 * cm, 2.7 * cm],rowHeights=[0.4 * cm, 0.4  * cm, 0.4  * cm, 0.4  * cm, 0.4  * cm, 0.4  * cm, 0.7  * cm])

    tables.setStyle(TableStyle([
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
        ('BACKGROUND', (0, 1), (-1, 1), colors.Color(219.0/255,229.0/255,241.0/255)),
        ('BACKGROUND', (0, 1), (0, 6), colors.Color(219.0/255,229.0/255,241.0/255)),
        ('BACKGROUND', (4, 1), (4, 4), colors.Color(219.0/255,229.0/255,241.0/255)),
        ('BACKGROUND', (4, 6), (4, 6), colors.Color(219.0/255,229.0/255,241.0/255))
    ]))

    t2 = Paragraph("CENSOS NACIONALES 2017: XII DE POBLACIÓN, VII DE VIVIENDA",h_sub_tile)

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
    story.append(table_bar)
    story.append(t)
    story.append(Spacer(0, 5 * mm))
    story.append(Paragraph("<strong>LISTADO DE LA ZONA CENSAL POR SECCIONES Y AREAS DE EMPADRONAMIENTO URBANO</strong>", styleTitle))
    story.append(Spacer(0, 5 * mm))
    story.append(tables)
    story.append(Spacer(0, 3 * mm))

    obs_data = [
        [Paragraph(e, h3) for e in ["<strong>D. INFORMACIÓN DE LA ZONA CENSAL</strong>",
                                    "",
                                    "",
                                    ]],
        [Paragraph(e, h3) for e in ["<strong>SECCION Nª</strong>",
                                    "<strong>A.E.U. Nº</strong>",
                                    "<strong>MANZANA Nº</strong>",
                                    "<strong>Nº DE VIVIENDAS POR A.E.U.</strong>"
                                    ]],
    ]
    c = Table(obs_data, colWidths=[4.9* cm, 4.5* cm, 4.5 * cm, 4.9 * cm])

    c.setStyle(TableStyle(
        [
            ('GRID', (1, 1), (-2, -2), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('BACKGROUND', (0, 0), (-1, 1), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('SPAN', (0, 0), (3, 0)),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(219.0/255,229.0/255,241.0/255)),
        ]
    ))
    story.append(c)
    #aeusi = Aeus.objects.filter(Q(ubigeo=distrito.ubigeo),Q(zona='00100'))
    aeusi = v_ReporteSecciones.objects.filter(Q(ubigeo=ubigeo),Q(zona=zonaq)).order_by('seccion','aeu_final')[0:33]

    aeusi_second = v_ReporteSecciones.objects.filter(Q(ubigeo=ubigeo), Q(zona=zonaq)).order_by('seccion','aeu_final')[33:]

    cant_secciones = int(v_ReporteSecciones.objects.filter(Q(ubigeo=ubigeo),Q(zona=zonaq)).count())
    total_page = 1


    total_secciones = 0
    total_mznsr = 0
    total_aeusr = 0

    for aeusis in aeusi:
        total_secciones = total_secciones + 1
        total_mznsr = total_mznsr + 1
        total_aeusr = total_aeusr + 1


    for aeusis in aeusi:
        x = x + 1
        y = x
        secc = str(aeusis.seccion).zfill(3)
        aeus = str(aeusis.aeu_final).zfill(3)
        # str(vivienda.p28) if vivienda.p28 == 0 else ""
        mzn = str(aeusis.manzanas.zfill(3) if not aeusis.manzanas == None else "")
        table2 = [(
                    str(secc).decode('latin-1'),
                    str(aeus).decode('latin-1'),
                    str(mzn).decode('latin-1'),
                    str(int(aeusis.cant_viv)).decode('latin-1')
                    )
                    ]
        s = Table(table2,
                    colWidths=[4.9 * cm, 4.5 * cm, 4.5 * cm, 4.9 * cm],
                    rowHeights=[0.5 *cm])

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


    if cant_secciones>33:
        story.append(c)
        # Aca va el segundo for
        for aeusis_second in aeusi_second:
            x = x + 1
            y = x
            secc = str(aeusis_second.seccion).zfill(3)
            aeus = str(aeusis_second.aeu_final).zfill(3)
            mzn = str(aeusis_second.manzanas).zfill(3)
            table2 = [(
                        str(secc).decode('latin-1'),
                        str(aeus).decode('latin-1'),
                        str(mzn).decode('latin-1'),
                        str(int(aeusis_second.cant_viv)).decode('latin-1')
                        )
                        ]
            s = Table(table2,
                        colWidths=[4.9 * cm, 4.5 * cm, 4.5 * cm, 4.9 * cm],
                        rowHeights=[0.5 *cm])

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

        ['', Paragraph('<strong>C. RESUMEN DE LA ZONA</strong>', h11), '', ''],
        ['', Paragraph('<strong>TOTAL DE SECCIONES</strong>', h1), Paragraph(str(resumen.cant_secciones), h_res), ''],
        ['', Paragraph('<strong>TOTAL DE MANZANAS.</strong>', h1), Paragraph(str(resumen.cant_mzs), h_res), ''],
        ['', Paragraph('<strong>TOTAL DE AEUS</strong>', h1), Paragraph(str(resumen.cant_aeus), h_res), ''],
    ]

    tables_res = Table(data_res, colWidths=[3 * cm, 6 * cm, 2.5 * cm, 3 * cm],
                       rowHeights=[0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4 * cm])

    tables_res.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (2, 0), colors.black),
        # ('ALIGN', (4, 0), (5, 0), 'RIGHT'),
        # ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (1, 0), (2, 3), 1, colors.black),
        # ('ALIGN', (2, 1), (2, 5), 'LEFT'),
        # ('GRID', (2, 1), (2, 3), 1, colors.black),
        # ('GRID', (-2, -1), (-1, -1), 1, colors.black),
        ('SPAN', (1, 0), (2, 0)),
        # ('SPAN', (1, 4), (2, 4)),
        # ('SPAN', (1, 5), (2, 5)),
        # ('SPAN', (1, 6), (2, 6)),
        # ('BACKGROUND', (4, 1), (5, 5), colors.white),
        ('BACKGROUND', (1, 0), (2, 0), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
    ]))

    story.append(Spacer(0, 2 * cm))

    story.append(tables_res)

    if (PageBreak()):
        total_page = total_page + 1
        # story.append(Paragraph("<strong>Hice salto</strong>", styleTitle))

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

    story.append(Spacer(0, 5 * cm))
    # story.append(table_obs)
    story.append(Spacer(0, 1 * mm))
    story.append(p_page)

    story.append(PageBreak())

    doc2.build(story)
    doc.build(story)
    response.write(buff.getvalue())
    buff.close()
    return response

def generar_lote_zona(request):

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
    #
    # lista_distrito.append('060903')
    # lista_distrito.append('080205')
    # lista_distrito.append('080307')

    # lista_distrito.append('080301')
    # lista_distrito.append('080302')
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
    # #
    # lista_distrito.append('130202')
    # lista_distrito.append('130701')
    # lista_distrito.append('130705')
    # lista_distrito.append('131203')
    # lista_distrito.append('140107')
    #
    # lista_distrito.append('150508')
    # lista_distrito.append('150604')
    # lista_distrito.append('150705')
    lista_distrito.append('150116')

    #lista_distrito.append('170102')
#
    #lista_distrito.append('180106')
#
    #lista_distrito.append('180208')
    #lista_distrito.append('180210')
#
    #lista_distrito.append('190111')
#
    #lista_distrito.append('190303')
    #lista_distrito.append('210407')
#
    #lista_distrito.append('230106')
    #lista_distrito.append('230109')
    #lista_distrito.append('240103')
    #lista_distrito.append('240105')
    #lista_distrito.append('240106')

    lista_zonas = []
    for ubigeos in lista_distrito:

        #total_zonas = Esp_Aeus.objects.filter(ubigeo=ubigeos).values_list('zona', flat=True)
        total_zonales = Esp_Aeus.objects.filter(ubigeo=ubigeos).values_list('zona', flat=True)
        cuchi_zonas = list(set(total_zonales))
        lista_zonas.append(total_zonales)
        lista = []
        for zona_t in cuchi_zonas:
            #zona_conv = str(zona_t + 1).zfill(3) + "00"
            lista.append(str(ubigeos)+": "+str(zona_t))
            generar_seccion(request, ubigeos, zona_t)

    return HttpResponse(lista_distrito)

