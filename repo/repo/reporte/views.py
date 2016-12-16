from django.shortcuts import render
from django.http import HttpResponse

# from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen import canvas
from reporte.reportes_models import MaeProyecto
from reporte.reportes_models import Distrito
from reporte.reportes_models import Departamento
from reporte.reportes_models import Provincia
from models import Pruebaaa
from django.template import loader
from reportlab.lib.pagesizes import A4, cm, inch
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import utils
from reportlab.platypus.flowables import PageBreak, Spacer
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Image, Paragraph, Table, TableStyle
from io import BytesIO
# from styles import DOCUMENT_STYLE
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
width, height = A4

import chardet
# styles = getSampleStyleSheet()
# styleN = styles["BodyText"]
# styleN.alignment = TA_LEFT
# styleBH = styles["Normal"]
# styleBH.alignment = TA_CENTER

# MARGIN_SIZE = 25 * mm
# PAGE_SIZE = A4


# Create your views here.
# def obtener_data(request):
#     mnz = Pruebaaa.objects.filter(ubigeo='21806').order_by('id')
#     template = loader.get_template('index.html')
#     context = {
#         'mnz': mnz,
#     }
#     return HttpResponse(template.render(context, request))

def get_image(path, width=1 * cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

def coord(x, y, unit=1):
    x, y = x * unit, height - y * unit
    return x, y

def generar_pdf(request):
    MARGIN_SIZE = 17 * mm
    PAGE_SIZE = A4
    #from django.db import connection
    print "Genero el PDF"
    response = HttpResponse(content_type='application/pdf')
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
    # pdf_name = "clientes.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    c = canvas.Canvas(buff, pagesize=A4)
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
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
        name='centered',
        fontSize=7,
        leading=14,
        alignment = TA_CENTER)

    clientes = []
    story = []

    # allclientes = Pruebaaa.objects.filter(ubigeo='21806').order_by('id')
    # allclientes = [(p.zona, p.id, p.aeu) for p in Pruebaaa.objects.all()]
    # permisos = list(ViewPermisosMenuChild.objects.filter(id_usuario=id).values('cod_permiso', 'nom_permiso', 'des_rol', 'id_menu'))


    filtro = list(MaeProyecto.objects.filter(ubigeo='020601', frente_ord = '1', id_reg_or='23').values('or_viv_aeu', 'manzana', 'frente_ord', 'p20','p21','p22_a', 'p23','p24','p25','p26','p27_a','p32'))
    #allclientes = [(p.zona, p.id, p.aeu) for p in Pruebaaa.objects.filter(ubigeo='21806')]
    alltodo = [(str(a['or_viv_aeu']).decode('utf-8'),
                str(a['manzana']).decode('utf-8'),
                str(a['frente_ord']).decode('utf-8'),
                str(a['p20']).decode('utf-8'),
                str(a['p21']).decode('utf-8'),
                str(a['p22_a']).decode('utf-8'),
                str(a['p23']).decode('utf-8'),
                str(a['p24']).decode('utf-8'),
                str(a['p25']).decode('utf-8'),
                str(a['p26']).decode('utf-8'),
                str(a['p27_a']).decode('utf-8'),
                str(a['p32']).decode('utf-8'))
               for a in filtro]

    # Paragraph('a['p32']', styleTitle)
    # for i, e in enumerate(allclientes):
    # p.drawString(x + (18 * diff_x), y - diff_y, str(data_models.pub_date))
    # story.append(Paragraph(str(e.ubigeo), styleBH))
    # for a in allclientes:
    #    story.append(a.id)
    # Texts
    # descrpcion = Paragraph('long paragraph long paragraphlong paragraphlong paragraphlong paragraphlong paragraph',
    #                        DOCUMENT_STYLE["normal"])
    # partida = Paragraph('1', DOCUMENT_STYLE["normal"])
    # candidad = Paragraph('120', DOCUMENT_STYLE["normal"])
    # precio_unitario = Paragraph('$52.00', DOCUMENT_STYLE["normal"])
    # precio_total = Paragraph('$6240.00', DOCUMENT_STYLE["normal"])

    # data= [[hdescrpcion, hcandidad,hcandidad, hprecio_unitario, hprecio_total],
    #       [partida, candidad, descrpcion, precio_unitario, precio_total]]
    data = [
            [Paragraph('<strong>A. UBICACION GEOGRAFICA</strong>', h1), '', '', '', Paragraph('<strong>B. UBICACION CENSAL</strong>', h1), ''],
            [Paragraph('<strong>DEPARTAMENTO</strong>', h1), Paragraph('15', h1), Paragraph('LIMA', h1), '', Paragraph('<strong>ZONA N</strong>', h1), Paragraph('001', h1)],
            [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph('01', h1),Paragraph('LIMA', h1), '', Paragraph('<strong>SECCION N</strong>', h1), Paragraph('010', h1)],
            [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph('15', h1),Paragraph('LA VICTORIA', h1), '', Paragraph('<strong>A.E.U. N</strong>', h1),Paragraph('008', h1)],
            [Paragraph('<strong>CENTRO POBLADO</strong>', h1), Paragraph('LA VICTORIA', h1),'', '', '', ''],
            [Paragraph('<strong>CATEGORIA CENTRO POBLADO</strong>', h1), Paragraph('CIUDAD', h1), '', '', Paragraph('<strong>C. TOTAL DE VIVIENDAS DEL A.E.U.</strong>', h1),Paragraph('16', h1)],
    ]

    obs_data = [
        [Paragraph(e, h2) for e in["<strong>VIV. N</strong>", "<strong>MZ N</strong>", "<strong>FRENTE N</strong>", "<strong>DIRECCION DE LA VIVIENDA</strong>", "", "", "", "", "", "", "","<strong>Apellidos y Nombres del JEFE DEL HOGAR</strong>"]],
        [Paragraph(e, h2) for e in["", "", "", "<strong>Tipo de Via</strong>", "<strong>Nombre de Via</strong>", "<strong>N de Puerta</strong>", "<strong>Block</strong>", "<strong>Man-zana N</strong>", "<strong>Lote N</strong>", "<strong>Piso N</strong>","<strong>Interior N</strong>", ""]],
        #[Paragraph('<strong>VIV. N</strong>', styleTitle), Paragraph('<strong>MANZANA N</strong>', styleTitle), Paragraph('<strong>FRENTE N</strong>', styleTitle), Paragraph('<strong>DIRECCION DE LA VIVIENDA</strong>', styleTitle), '', '', '', '', '', '', '', Paragraph('<strong>Apellidos y Nombres del JEFE DEL HOGAR</strong>', styleTitle)],
        #['', '', '', Paragraph('<strong>Tipo de Via</strong>',styleTitle), Paragraph('<strong>Nombre de Via</strong>', styleTitle), Paragraph('<strong>N de Puerta</strong>', styleTitle), Paragraph('<strong>Block</strong>', styleTitle), Paragraph('<strong>Manzana N</strong>', styleTitle), Paragraph('<strong>Lote N</strong>', styleTitle),Paragraph( '<strong>Piso N</strong>', styleTitle),Paragraph('<strong>Interior N</strong>',styleTitle),''],
    ]
    obs = [
        [Paragraph('OBSERVACIONES', styleBH), ''],
        ['', '', ],
        ['', '', ],
        ['', '', ],
    ]
    headings = ('Nombre', 'zona', 'repo','Nombre', 'zona', 'repo','Nombre', 'zona', 'repo','Nombre', 'zona')
    #t = Table([headings] + allclientes)
    d = Table (obs_data + alltodo, colWidths=[0.9 * cm, 0.9 * cm, 1.5 * cm,1.4 * cm,None,1.2 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.3 * cm ,4.6 * cm])

    # t.setStyle(TableStyle(
    #     [
    #         ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
    #         ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
    #         ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
    #     ]
    # ))
    d.setStyle(TableStyle(
        [
            # ('GRID', (0, 0), (10, -1), 1, colors.black),
            # ('GRID', (4, 0), (5, 3), 1, colors.black)
            ('GRID', (1, 1), (-2, -2), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightskyblue),
            ('BACKGROUND', (0, 0), (-1, 1), colors.lightskyblue),
            ('SPAN', (3, 0), (10, 0)),
            ('SPAN', (0, 0), (0, 1)),
            ('SPAN', (1, 0), (1, 1)),
            ('SPAN', (2, 0), (2, 1)),
            ('SPAN', (11, 0), (11, 1)),
            # ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black)
            # ('BACKGROUND', (0, 0), (-1, 0), colors.lightskyblue)
        ]
    ))

    # d.setStyle(TableStyle(
    #     [
    #         ('GRID', (0, 0), (10, -1), 1, colors.black),
    #         ('GRID', (4, 0), (5, 3), 1, colors.black),
    #         ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black)
    #         #('BACKGROUND', (0, 0), (-1, 0), colors.lightskyblue)
    #     ]
    # ))

    table = Table(data, colWidths=[6 * cm, 1 * cm, 3.5 * cm, 0.1 * cm, 6 * cm, 1.5 * cm])

    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (2, 5), 1, colors.black),
        ('GRID', (4, 0), (5, 3), 1, colors.black),
        ('GRID', (-2, -1), (-1, -1), 1, colors.black),
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (4, 0), (5, 0)),
        ('SPAN', (1, 4), (2, 4)),
        ('SPAN', (1, 5), (2, 5)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightskyblue),
        ('BACKGROUND', (0, 0), (0, 5), colors.lightskyblue),
        ('BACKGROUND', (4, 0), (4, 5), colors.lightskyblue)
        # ('TEXTFONT',(0,0), (-1,-1), 'Roboto-Regular'),
        # ('FONTSIZE',(0,0), (-1,-1), 1),
    ]))

    otable = Table(obs_data, colWidths=[1 * cm, 1 * cm, 1.6 * cm, 1.4 * cm, None, 1.4 * cm, 1 * cm, 1.2 * cm, 1.2 * cm, 1.1 * cm, 1.5 * cm, 4 * cm])


    otable.setStyle(TableStyle([
                       ('TEXTCOLOR', (0, 0), (-1, -1), colors.blue),
                       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                       ('GRID', (0, 0), (-1, -1), 1, colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.lightskyblue),
                       ('BACKGROUND', (0, 0), (-1, 1), colors.lightskyblue),
                       # ('FONTSIZE', (0, 0), (-1, -1), 7),
                       # ('FONTNAME', (0, 0), (-1, -1), 7),
                       ('SPAN', (0, 0), (0, 1)),
                       ('SPAN', (1, 0), (1, 1)),
                       ('SPAN', (2, 0), (2, 1)),
                       ('SPAN', (3, 0), (10, 0)),
                       ('SPAN', (11, 0), (11, 1))
        #('SPAN', (0, 0), (0, 1)),
        #('SPAN', (1, 0), (1, 1)),
        #('SPAN', (2, 0), (2, 1)),
        #('SPAN', (3, 0), (10, 0)),
        #('SPAN', (11, 0), (11, 1)),
    ]))

    t1 = Paragraph("<strong>INSTITUO NACIONAL DE ESTADISTICA E INFORMATICA CENSOS NACIONALES 2017: XII DE POBLACION, VII DE VIVIENDA</strong>",styleTitle)
    # story.append(Spacer(0, 001 * mm))
    t2 = Paragraph("<strong>Y III DE COMUNIDADES INDIGENAS</strong>", styleTitle)

    fichero_imagen_inei = 'Reporte/Img/inei.png'
    imagen_logo_inei = Image(os.path.realpath(fichero_imagen_inei), width=50, height=50)
    P2 = Paragraph('', styleBH)
    fichero_imagen = 'Reporte/Img/escudo.png'
    imagen_logo = Image(os.path.realpath(fichero_imagen),width=50, height=50)

    t = Table(
        data=[
            ['', '', ''],
            [[imagen_logo, P2], t1, [imagen_logo_inei, P2]],
            ['', t2, '']
        ],
        colWidths=[2 * cm, 12 * cm, 2*cm],
        style=[
            ('GRID', (1, 1), (-2, -2), 1, colors.white),

            #('BOX', (0, 0), (1, -1), 2, colors.black),
            #('LINEABOVE', (1, 2), (-2, 2), 1, colors.blue),
            #('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
            #('BACKGROUND', (0, 0), (0, 1), colors.pink),
            #('BACKGROUND', (1, 1), (1, 2), colors.lavender),
            #('BACKGROUND', (2, 2), (2, 3), colors.orange),
            #('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            #('VALIGN', (3, 0), (3, 0), 'BOTTOM'),
            #('BACKGROUND', (3, 0), (3, 0), colors.limegreen),
            #('BACKGROUND', (3, 1), (3, 1), colors.khaki),
            #('ALIGN', (3, 1), (3, 1), 'CENTER'),
            #('BACKGROUND', (3, 2), (3, 2), colors.beige),
            #('ALIGN', (3, 2), (3, 2), 'LEFT'),
        ]
    )


    t1 = Paragraph("<strong>VIV.N</strong>", h2)
    t2 = Paragraph("<strong>MZ N</strong>", h2)
    t3 = Paragraph("<strong>FRENTE N</strong>", h2)
    t4 = Paragraph("<strong>Tipo de Via</strong>", h2)
    t5 = Paragraph("<strong>Nombre de Via</strong>", h2)
    t6 = Paragraph("<strong>N de Puerta</strong>", h2)
    t7 = Paragraph("<strong>Block</strong>", h2)
    t8 = Paragraph("<strong>Man-zana N</strong>", h2)
    t9 = Paragraph("<strong>Lote N</strong>", h2)
    t10 = Paragraph("<strong>Piso N</strong>", h2)
    t11 = Paragraph("<strong>Interior N</strong>", h2)
    t12 = Paragraph("<strong>Apellidos y Nombres del JEFE DEL HOGAR</strong>", h2)
    t13 = Paragraph("<strong>DIRECCION DE LA VIVIENDA</strong>", h2)
    z = Table(
        data=[
            [t1, t2, t3, t13, '', '', '', '', '', '', '', t12],
            ['', '', '',t4,t5,t6,t7,t8,t9,t10,t11,'']
        ],
        colWidths=[0.9 * cm, 0.9 * cm, 1.5 * cm,1.4 * cm,None,1.2 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.3 * cm ,3.4 * cm],
        style=[
            ('GRID', (1, 1), (-2, -2), 1, colors.black),
            # ('BOX', (0, 0), (1, -1), 2, colors.black),
            # ('LINEABOVE', (1, 2), (-2, 2), 1, colors.blue),
            # ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
            # ('BACKGROUND', (0, 0), (0, 1), colors.pink),
            # ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
            # ('BACKGROUND', (2, 2), (2, 3), colors.orange),
            # ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            # ('VALIGN', (3, 0), (3, 0), 'BOTTOM'),
            # ('BACKGROUND', (3, 0), (3, 0), colors.limegreen),
            # ('BACKGROUND', (3, 1), (3, 1), colors.khaki),
            # ('ALIGN', (3, 1), (3, 1), 'CENTER'),
            # ('BACKGROUND', (3, 2), (3, 2), colors.beige),
            # ('ALIGN', (3, 2), (3, 2), 'LEFT'),
            ('SPAN', (0, 0), (0, 1)),
            ('SPAN', (1, 0), (1, 1)),
            ('SPAN', (2, 0), (2, 1)),
            ('SPAN', (11, 0), (11, 1)),
            ('SPAN', (3, 0), (10, 0))
        ]
    )

    # imagen_logo.drawOn(canvas,20,20)
    # imagen_logo.drawWidth(10)
    # imagen_logo.drawWidth(5)

    # drawImage(archivo, x, y, width=None, height=None)
    # c.drawImage(fichero_imagen, 2, 2, width=100, height=100)
    # # table.wrapOn(c, A4, A4)
    # # table.drawOn(c, 20, 650)
    # c.showPage()
    # c.save()

    story.append(t)
    # story.append(z)
    # story.append(imagen_logo_inei)
    story.append(Spacer(0,05 * mm))
    story.append(Paragraph("<strong>LISTADO DE VIVIENDAS DEL AREA DE EMPADRONAMIENTO URBANO (A.E.U.)</strong>", styleTitle))
    story.append(Spacer(0,5 * mm))
    story.append(table)
    story.append(dist)
    story.append(Spacer(0,5 * mm))
    # story.append(otable)
    # story.append(Spacer(0,01 * mm))
    story.append(d)
    doc.build(story)
    response.write(buff.getvalue())
    buff.close()
    return response
    # story.append(get_image('Img/mapa.png', width=16 * cm))

    # story.append(Spacer(0, 5 * mm))
    # story.append(Table(obs, colWidths=[None, None], style=TableStyle([
    #     ('SPAN', (0, 1), (1, 1)),
    #     ('SPAN', (0, 2), (1, 2)),
    #     ('SPAN', (0, 3), (1, 3)),
    #     ('GRID', (0, 0), (-1, -1), 1, colors.black),
    # ])))

    #story.append(PageBreak())

    # story.append(Paragraph("CENSOS NACIONALES 2017: XII DE POBLACIoN, VII DE VIVIENDA Y III DE COMUNIDADES INDiGENAS",
    #                        styleBH))
    # story.append(Spacer(0, 5 * mm))
    # story.append(Paragraph("LISTADO DE VIVIENDAS DEL aREA DE EMPADRONAMIENTO URBANO (A.E.U.)", styleBH))
    # story.append(Spacer(0, 5 * mm))
    # story.append(table)
    # story.append(Spacer(0, 5 * mm))
    # story.append(otable)
    # story.append(Spacer(0, 1 * mm))
    # story.append(t)
    # story.append(d)
    # story.append(Spacer(0, 5 * mm))
    # story.append(Table(obs, colWidths=[None, None], style=TableStyle([
    #     ('SPAN', (0, 1), (1, 1)),
    #     ('SPAN', (0, 2), (1, 2)),
    #     ('SPAN', (0, 3), (1, 3)),
    #     ('GRID', (0, 0), (-1, -1), 1, colors.black),
    # ])))

    # pdf_doc = BaseDocTemplate("demo.pdf", pagesize=PAGE_SIZE,
    #                           leftMargin=MARGIN_SIZE, rightMargin=MARGIN_SIZE,
    #                           topMargin=MARGIN_SIZE, bottomMargin=MARGIN_SIZE)
    #
    # main_frame = Frame(MARGIN_SIZE, MARGIN_SIZE,
    #                    PAGE_SIZE[0] - 2 * MARGIN_SIZE, PAGE_SIZE[1] - 2 * MARGIN_SIZE,
    #                    leftPadding=0, rightPadding=0, bottomPadding=0,
    #                    topPadding=0, id='main_frame')
    #
    # main_template = PageTemplate(id='main_template', frames=[main_frame])

    #response = HttpResponse(content_type='application/pdf')
    #pdf_doc.addPageTemplates([main_template])

    # doc.build(story)
    # response.write(buff.getvalue())
    # buff.close()
    # return response

    # pdf_doc.build(story)
    #
    # response.write(buff.getvalue())
    # buff.close()
    # return response
    ##################################################
    # clientes.append(t)
    # doc.build(clientes)
    # response.write(buff.getvalue())
    # buff.close()
    # return response
    ##################################################
