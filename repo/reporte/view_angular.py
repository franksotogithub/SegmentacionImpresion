from django.http import HttpResponse
from reportes_models import *
from django.core import serializers
from django.http import JsonResponse
from seguridad.helpers import json_serial
from django.http import HttpResponse
from django.db.models import Count

from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import json

def departamentos(request):

    data_departamentos = list(Departamento.objects.values('ccdd', 'departamento').annotate(data=Count('ccdd')))
    return HttpResponse(json.dumps(data_departamentos), content_type='application/json')

def provincias(request, depa):
    filtroPro = Provincia.objects.filter(ccdd=depa).values('ccpp', 'provincia').annotate(data=Count('ccdd','ccpp'))
    data = list(filtroPro)
    return HttpResponse(json.dumps(data), content_type='application/json')

def distritos(request, depa, prov):
    filtroDist = Distrito.objects.filter(ccdd=depa, ccpp=prov).values('ccdi', 'distrito').annotate(data=Count('ccpp','ccdi'))
    data = list(filtroDist)
    return HttpResponse(json.dumps(data), content_type='application/json')

def zonas(request, depa, prov):
    filtroDist = Distrito.objects.filter(ccdd=depa, ccpp=prov).values('ccdi', 'distrito').annotate(data=Count('ccpp','ccdi'))
    data = list(filtroDist)
    return HttpResponse(json.dumps(data), content_type='application/json')

def aeus(request,ubigeo, zona):

    ubig = list([x for x in os.listdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\{}\\{}".format(ubigeo, zona)) if len(x) == 21])
    print ubig

    lista_paginas = []

    total_aes_zona = int(str(Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona).count()))

    data = list(Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona).values('aeu_final').order_by('aeu_final'))
    #data_est = Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona)

    for aeu in range(total_aes_zona):
        aeu_conv = str(aeu).zfill(3)
        cond = Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona, aeu_final=aeu)

        for aeusi in cond:
            # data_con = str(data[aeu - 1]).zfill(3)
            secc = str(aeusi.seccion).zfill(3)
            # ubicacion_pdf_leer = "//srv-fileserver/CPV2017/list_segm_tab/listas.pdf"
            pdf_file = PdfFileReader(open("//srv-fileserver/CPV2017/segm_tab/urbano/" + str(ubigeo) + "/" + str(zona) + "/" + str(ubigeo) + str(zona) + str(secc) + str(aeu_conv) + ".pdf", 'rb'))
            number_of_pages = pdf_file.getNumPages()

            lista_paginas.append({'cant_pag': number_of_pages, 'aeu_final':ubig[aeusi.aeu_final-1], 'est_imp': int(aeusi.est_imp)})
            # lista_paginas.append({'nombre_de_tu_key': number_of_pages})
            # {NOMBRE: LI[0],}
    return HttpResponse(json.dumps(lista_paginas), content_type='application/json')

def aeus_leg(request, ubigeo, zona):

    #ubig = list([x for x in os.listdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\{}\\{}".format(ubigeo, zona)) if len(x) == 21])


    lista_paginas = []

    lista = []

    data = Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona, est_imp=1).order_by('aeu_final')

    #print data

    for aeu in data:
        aeu_fin = str(aeu.aeu_final).zfill(3)
        secc_fin = str(aeu.seccion).zfill(3)
        #
        pdf_file = PdfFileReader(open("//srv-fileserver/CPV2017/segm_tab/urbano/" + str(ubigeo) + "/" + str(zona) + "/" + str(ubigeo)+str(zona)+str(secc_fin)+aeu_fin+".pdf", 'rb'))
        #
        number_of_pages = pdf_file.getNumPages()

        lista.append({'aeu':aeu.aeu_final, 'estado': int(aeu.est_imp), 'cant_pag': number_of_pages})

    print lista

    # for nom in ubig:
    #
    #     aeu = int(nom[14:17])
    #
    #     pdf_file = PdfFileReader(open("//srv-fileserver/CPV2017/segm_tab/urbano/" + str(ubigeo) + "/" + str(zona) + "/" + str(nom), 'rb'))
    #
    #     number_of_pages = pdf_file.getNumPages()
    #
    #     lista_paginas.append({'cant_pag': number_of_pages, 'aeu_final': aeu})


    return HttpResponse(json.dumps(lista), content_type='application/json')



def zonas(request,ubigeo):

    data_zona = list(Tab_Aeus.objects.filter(ubigeo=ubigeo).values('zona').distinct())
    #nuevo = [x[1] for x in data_zona]
    #s = list(set( val for dic in data_zona for val in dic.values()))
    return HttpResponse(json.dumps(data_zona), content_type='application/json')


def seccion(request,ubigeo, zona):

    to_pdf_secc = Tab_Secciones.objects.filter(ubigeo = ubigeo, zona = zona)

    return HttpResponse(json.dumps(to_pdf_secc), content_type='aplication/json')

def distrito(request, ubigeo):

    to_pdf_distrito = v_ReporteSecciones.objects.filter(ubigeo=ubigeo)

    return HttpResponse(json.dumps(to_pdf_distrito), content_type='aplication/json')

def cant_aeus(request, ubigeo, zona):

    data_cant = int(Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona).values('aeu_final').count())
    return HttpResponse(json.dumps(data_cant), content_type='application/json')

def cargar_tabla(request, ubigeo, zona):

    data_cant = Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona).values('aeu_final')
    return HttpResponse(json.dumps(data_cant), content_type='application/json')

def prueba(request, ubigeo, zona):

    lista_paginas = []
    total = []
    total_aes_zona = int(str(Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona).count()))

    data = list(Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona).values_list('aeu_final', flat=True))
    for aeu in range(total_aes_zona):
        aeu_conv = str(aeu).zfill(3)
        cond = Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona, aeu_final=aeu)

        for aeusi in cond:

            secc = str(aeusi.seccion).zfill(3)
            #ubicacion_pdf_leer = "//srv-fileserver/CPV2017/list_segm_tab/listas.pdf"
            pdf_file = PdfFileReader(open("//srv-fileserver/CPV2017/list_segm_tab/"+str(ubigeo)+"/"+str(zona)+"/"+str(ubigeo)+str(zona)+str(secc)+str(aeu)+".pdf", 'rb'))

            number_of_pages = pdf_file.getNumPages()
            lista_paginas.append({'cant_pag':number_of_pages})
            # lista_paginas.append({'nombre_de_tu_key': number_of_pages})
            #{NOMBRE: LI[0],}


    for i in range (len(data)):
         total = str(data[i+1])+","+str(lista_paginas[i+1])

    return HttpResponse(json.dumps(total), content_type='application/json')

def aeus_Seccion(request, ubigeo, zona):

    listin = []
    lista_pdf = []
    data_cant = Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona).values('aeu_final')

    datos_seccion = Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona).values_list('seccion', flat=True)

    # ubigeo_c = ubigeo[0:6]
    # zona_c =  zona[0:5]

    # nombres_tot = [x for x in os.listdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\{}\\{}".format(ubigeo, zona)) if len(x)>15]
    #
    # for i in nombres_tot:
    #     print i
    #
    secciones = list(set(datos_seccion))

    for i in range(len(secciones)):
        buscar_aeu = list(Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona, seccion=i+1).values('aeu_final', 'seccion').annotate(data=Count('aeu_final', 'seccion')))
        #lista_aeus = Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona, seccion=i + 1).values('seccion')

        listin.append(buscar_aeu)

    resultado = listin.append({'seccion': buscar_aeu})

    return HttpResponse(json.dumps(listin), content_type='application/json')

def seccion_Zonas(request, ubigeo, zona):

    datos_seccion = list(Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona).values('zona', 'seccion').annotate(data=Count('zona', 'seccion')))

    return HttpResponse(json.dumps(datos_seccion), content_type='application/json')

def zonas_Distritos(request, ubigeo):

    datos_seccion = list(Tab_Aeus.objects.filter(ubigeo=ubigeo).values('ubigeo', 'zona').annotate(data=Count('ubigeo', 'zona')))

    return HttpResponse(json.dumps(datos_seccion), content_type='application/json')

# def login(request):
#     user = False
#     if (request.method == 'GET'):
#
#         username = request.GET.get('username', False)
#         contrasena = request.GET.get('clave', False)
#         user = list(MaeUsuario.objects.filter(usuario=username, clave=contrasena).values())
#
#         if user:
#             sesion = get_session(user[0]['id_usuario'])
#             user[0]['detalle'] = sesion
#             user[0]['routes'] = get_routes(user[0]['id_usuario'])
#         else:
#             user = False
#
#     return HttpResponse(json.dumps(user, default=json_serial), content_type='application/json')