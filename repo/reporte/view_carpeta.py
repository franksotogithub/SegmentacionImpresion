import os
import shutil

#
# def Crear_Carpetas_Croquis_AEU(ubigeos):
#     ZONAS = r"D:\ShapesPruebasSegmentacionUrbanaTabular\AEU\EnumerarAEUViviendas\TB_ZONA_CENSAL.shp"
#
#     where_list = ubigeos
#     if os.path.exists("D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/CroquisUrbanoAEU") == False:
#         os.mkdir("D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/CroquisUrbanoAEU")
#
#     where_expression = UBIGEO.ExpresionUbigeos(ubigeos)
#
#     ###############creando carpetas de ubigeos
#     for row in ubigeos:
#         print row
#         if os.path.exists("D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/CroquisUrbanoAEU/" + str(row)) == False:
#             os.mkdir("D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/CroquisUrbanoAEU/" + str(row))
#
#
#             #################creando carpetas de zonas#####################
#     with arcpy.da.SearchCursor(ZONAS, ['UBIGEO', 'ZONA'], where_expression) as cursor:
#
#         for row in cursor:
#             if os.path.exists("D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/CroquisUrbanoAEU/" + str(
#                     row[0]) + "/" + str(row[1])) == False:
#                 os.mkdir(
#                     "D:/ShapesPruebasSegmentacionUrbanaTabular/AEU/CroquisUrbanoAEU/" + str(row[0]) + "/" + str(row[1]))
#     del cursor

import os

from django.http import HttpResponse

from reportes_models import *

def crearCarpeta(request):
    secuencia = 1
    lista_distritos = []
    lista_distritos.append("030602")
    lista_distritos.append("022001")
    lista_distritos.append("021509")
    lista_distritos.append("050601")

    tam_dis = 4
    listin = []

    for ubigeo in range(tam_dis):

        if os.path.exists("\\\srv-fileserver\\CPV2017\\list_segm_tab\\" + str(lista_distritos[ubigeo])) == False:
            os.mkdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\" + str(lista_distritos[ubigeo])  )

        total_zonas = int(str(Tab_Aeus.objects.filter(ubigeo=lista_distritos[ubigeo]).values_list('zona', flat=True).distinct().count()))

        for zona_t in range(total_zonas):
            zoner = str(zona_t + 1).zfill(3) + "00"
            listin.append(str(lista_distritos[ubigeo])+": "+zoner+"<br/>")
            if os.path.exists("\\\srv-fileserver\\CPV2017\\list_segm_tab\\"+str(lista_distritos[ubigeo])+"\\"+zoner) == False :
                os.mkdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\" + str(lista_distritos[ubigeo])+"\\"+zoner)

    return HttpResponse(listin)

def crearCarpetaAes(request):
    secuencia = 1
    lista_distritos = []
    lista_distritos.append("030602")
    lista_distritos.append("022001")
    lista_distritos.append("021509")
    lista_distritos.append("050601")

    tam_dis = 4
    listin = []

    for ubigeo in range(tam_dis):

        if os.path.exists("C:/Users/acarrillo/Desktop/Projects/Reportes/repo/Secciones/" + str(lista_distritos[ubigeo])) == False:
            os.mkdir("C:/Users/acarrillo/Desktop/Projects/Reportes/repo/Secciones/" + str(lista_distritos[ubigeo])  )

        total_zonas = int(str(Tab_Aeus.objects.filter(ubigeo=lista_distritos[ubigeo]).values_list('zona', flat=True).distinct().count()))

        for zona_t in range(total_zonas):
            zoner = str(zona_t + 1).zfill(3) + "00"
            listin.append(str(lista_distritos[ubigeo])+": "+zoner+"<br/>")
            if os.path.exists("C:/Users/acarrillo/Desktop/Projects/Reportes/repo/Secciones/"+str(lista_distritos[ubigeo])+"/"+zoner) == False :
                os.mkdir("C:/Users/acarrillo/Desktop/Projects/Reportes/repo/Secciones/" + str(lista_distritos[ubigeo])+"/"+zoner)

    return HttpResponse(listin)



