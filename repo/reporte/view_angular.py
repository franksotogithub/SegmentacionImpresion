from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
#
from reportes_models import *
from django.core import serializers
from django.http import JsonResponse
from seguridad.helpers import json_serial
from django.http import HttpResponse
from django.db.models import Count, Q
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import json
import os.path
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date
import threading
import time


# .filter(Q(nobre=jose) | Q(otro=otro))
def departamentos(request):
    # data_departamentos = list(Departamento.objects.values('ccdd', 'departamento').annotate(data=Count('ccdd')))
    data_departamentos = list(Tb_Marco_Ubigeos_Segmentados.objects.values('ccdd', 'departamento').distinct())
    return HttpResponse(json.dumps(data_departamentos), content_type='application/json')


def provincias(request, depa):
    filtroPro = Tb_Marco_Ubigeos_Segmentados.objects.filter(ccdd=depa).values('ccpp', 'provincia').distinct()
    data = list(filtroPro)
    return HttpResponse(json.dumps(data), content_type='application/json')


def distritos(request, depa, prov, tipo):
    if tipo == "0":
        filtroDist = Distrito.objects.filter(ccdd=depa, ccpp=prov).values('ccdi', 'distrito').annotate(
            data=Count('ccpp', 'ccdi'))
        data = list(filtroDist)
        return HttpResponse(json.dumps(data), content_type='application/json')
    elif tipo == "1":
        filtroDist = Distrito.objects.filter(ccdd=depa, ccpp=prov, id_estrato=1).values('ccdi', 'distrito').annotate(
            data=Count('ccpp', 'ccdi'))
        data = list(filtroDist)
        return HttpResponse(json.dumps(data), content_type='application/json')
    elif tipo == "2":
        filtroDist = Distrito.objects.filter(ccdd=depa, ccpp=prov, id_estrato=2).values('ccdi', 'distrito').annotate(
            data=Count('ccpp', 'ccdi'))
        data = list(filtroDist)
        return HttpResponse(json.dumps(data), content_type='application/json')
    elif tipo == None or tipo == '' or tipo == '':
        filtroDist = Distrito.objects.filter(ccdd=depa, ccpp=prov).values('ccdi', 'distrito').annotate(
            data=Count('ccpp', 'ccdi'))
        data = list(filtroDist)
        return HttpResponse(json.dumps(data), content_type='application/json')


def aeus(request, nivel, ubigeo, zona):
    if nivel == u"1":

        listado = Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona).order_by('aeu_final')
        json_tmp = [{'nombre': '{}{}{}{}'.format(x.ubigeo, x.zona, str(x.seccion).zfill(3), str(x.aeu_final).zfill(3)),
                     'cant_pag': x.cant_pag, 'est_imp': int(x.est_imp), 'tipo': 1} for x in listado]

    elif nivel == u"2":  # Cuando se filtre a nivel de seccion
        json_tmp = [];
        secc = Tab_Secciones.objects.filter(ubigeo=ubigeo, zona=zona).order_by('seccion')
        for scu in secc:
            scu_tmp = {'nombre': '{}{}{}'.format(scu.ubigeo, scu.zona, str(scu.seccion).zfill(3)),
                       'cant_pag': scu.cant_pag, 'est_imp': int(scu.est_imp_secc), 'tipo': 2}
            json_tmp.append(scu_tmp)
            for aue in Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona, seccion=scu.seccion).order_by('aeu_final'):
                aeu_tmp = {'nombre': '{}{}{}{}'.format(aue.ubigeo, aue.zona, str(aue.seccion).zfill(3),
                                                       str(aue.aeu_final).zfill(3)), 'cant_pag': aue.cant_pag,
                           'est_imp': int(aue.est_imp), 'tipo': 1}
                json_tmp.append(aeu_tmp)


    elif nivel == u"3":
        json_tmp = [];
        zonas = Tab_Zonas.objects.filter(ubigeo=ubigeo, zona=zona).order_by('zona')
        for zns in zonas:
            scu_tmp = {'nombre': '{}{}'.format(zns.ubigeo, zns.zona), 'cant_pag': zns.cant_pag,
                       'est_imp': int(zns.est_imp_zona), 'tipo': 3}
            json_tmp.append(scu_tmp)
            for scu in Tab_Secciones.objects.filter(ubigeo=ubigeo, zona=zona).order_by('seccion'):
                aeu_tmp = {'nombre': '{}{}{}'.format(scu.ubigeo, scu.zona, str(scu.seccion).zfill(3)),
                           'cant_pag': scu.cant_pag, 'est_imp': int(scu.est_imp_secc), 'tipo': 2}
                json_tmp.append(aeu_tmp)

    return HttpResponse(json.dumps(json_tmp), content_type='application/json')


def dataImpresionRural(request, nivel, ubigeo):
    if nivel == u'1':
        empadronadores = segm_r_emp.objects.filter(ubigeo=ubigeo).order_by('emp')
        json_tmp = [
            {'nombre': '{}{}'.format(x.idruta, x.emp), 'cant_pag': x.cant_pag, 'est_imp': int(x.est_imp), 'tipo': 1} for
            x in empadronadores]

    elif nivel == u'2':
        json_tmp = []
        secciones = segm_r_scr.objects.filter(ubigeo=ubigeo).order_by('scr')
        for scr in secciones:
            jsom_scr = {'nombre': scr.idscr, 'cant_pag': scr.cant_pag, 'est_imp': int(scr.est_imp), 'tipo': 2}
            json_tmp.append(jsom_scr)
            for emp in segm_r_emp.objects.filter(idscr=scr.idscr).order_by('emp'):
                json_emp = {'nombre': '{}{}'.format(emp.idruta, emp.emp), 'cant_pag': emp.cant_pag,
                            'est_imp': int(emp.est_imp), 'tipo': 1}
                json_tmp.append(json_emp)


    elif nivel == u'3':
        json_tmp = []
        distrito = Distrito.objects.filter(ubigeo=ubigeo)[0]
        jsom_dist = {'nombre': distrito.ubigeo, 'cant_pag': distrito.cant_pag_r, 'est_imp': int(distrito.est_imp_r),
                     'tipo': 3}
        json_tmp.append(jsom_dist)
        for scr in segm_r_scr.objects.filter(ubigeo=ubigeo).order_by('scr'):
            json_scr = {'nombre': scr.idscr, 'cant_pag': scr.cant_pag,
                        'est_imp': int(scr.est_imp), 'tipo': 2}
            json_tmp.append(json_scr)

            #  json_tmp = []
            # distrito = Distrito.objects.filter(ubigeo=ubigeo)[0]
            # secciones = segm_r_scr.objects.filter(ubigeo=ubigeo).order_by('scr')
            # json_dist = {'nombre': distrito.ubigeo, 'cant_pag': distrito.cant_pag_r, 'est_imp': int(distrito.est_imp_r), 'tipo': 3}
            # json_tmp.append(json_dist)
            # json_scr = [{'nombre': scr.idscr, 'cant_pag': scr.#, 'est_imp': scr.est_imp, 'tipo': 2} for scr in secciones]
            # json_tmp.append(json_scr)

    return HttpResponse(json.dumps(json_tmp), content_type='application/json')


def aeus_leg(request, nivel, ubigeo, zona):
    print "nivel: " + nivel
    print "ubigeo: " + ubigeo
    print "zona: " + zona
    # print data
    if nivel == u"1":

        data = Tab_Aeus.objects.filter(Q(ubigeo=ubigeo) & Q(zona=zona), Q(est_imp=1) |  Q(est_imp=2)).order_by('aeu_final')
        json_tmp = [
            {'aeu': '{}{}{}{}'.format(x.ubigeo, x.zona, str(x.seccion).zfill(3), str(x.aeu_final).zfill(3)) + ".pdf",
             'estado_conf': int(x.est_con_aeu), 'estado': int(x.est_imp), 'cant_pag': x.number_of_pages, 'tipo': 1,
             'codigo': '{}{}{}{}'.format(x.ubigeo, x.zona, str(x.seccion).zfill(3), str(x.aeu_final).zfill(3))} for x in
            data]


    elif nivel == u"2":  # Cuando se filtre a nivel de seccion
        json_tmp = [];
        secc = Tab_Secciones.objects.filter(Q(ubigeo=ubigeo) & Q(zona=zona),
                                            Q(est_imp_secc=1) | Q(est_imp_secc=2)).order_by('seccion')
        for scu in secc:
            scu_tmp = {'aeu': '{}{}{}'.format(scu.ubigeo, scu.zona, str(scu.seccion).zfill(3)) + ".pdf",
                       'estado_conf': int(scu.est_con_secc),
                       'cant_pag': scu.cant_pag, 'estado': int(scu.est_imp_secc), 'tipo': 2,
                       'codigo': '{}{}{}'.format(scu.ubigeo, scu.zona, str(scu.seccion).zfill(3))}
            json_tmp.append(scu_tmp)
            for aeu in Tab_Aeus.objects.filter(Q(ubigeo=ubigeo) & Q(zona=zona) & Q(seccion=scu.seccion),
                                               Q(est_imp_secc=1) | Q(est_imp_secc=2)).order_by('aeu_final'):
                aeu_tmp = {'aeu': '{}{}{}{}'.format(aeu.ubigeo, aeu.zona, str(aeu.seccion).zfill(3),
                                                    str(aeu.aeu_final).zfill(3)) + ".pdf",
                           'estado': int(aeu.est_imp_secc), 'estado_conf': int(aeu.est_con_aeu),
                           'cant_pag': aeu.cant_pag, 'tipo': 1,
                           'codigo': '{}{}{}{}'.format(aeu.ubigeo, aeu.zona, str(aeu.seccion).zfill(3),
                                                       str(aeu.aeu_final).zfill(3))}
                json_tmp.append(aeu_tmp)

    elif nivel == u"3":
        json_tmp = [];
        zonas = Tab_Zonas.objects.filter(Q(ubigeo=ubigeo) & Q(zona=zona),
                                         Q(est_imp_zona=1) | Q(est_imp_zona=2)).order_by('zona')
        for zns in zonas:
            scu_tmp = {'aeu': '{}{}'.format(zns.ubigeo, zns.zona) + ".pdf", 'cant_pag': zns.cant_pag,
                       'estado_conf': int(zns.est_con_zona),
                       'estado': int(zns.est_imp_zona), 'tipo': 3, 'codigo': '{}{}'.format(zns.ubigeo, zns.zona)}
            json_tmp.append(scu_tmp)
            for scu in Tab_Secciones.objects.filter(Q(ubigeo=ubigeo) & Q(zona=zona),
                                                    Q(est_imp_zona=1) | Q(est_imp_zona=2)).order_by('seccion'):
                aeu_tmp = {'aeu': '{}{}{}'.format(scu.ubigeo, scu.zona, str(scu.seccion).zfill(3)) + ".pdf",
                           'cant_pag': scu.cant_pag, 'estado_conf': int(scu.est_con_zona),
                           'estado': int(scu.est_imp_zona), 'tipo': 2,
                           'codigo': '{}{}{}'.format(scu.ubigeo, scu.zona, str(scu.seccion).zfill(3))}
                json_tmp.append(aeu_tmp)

    return HttpResponse(json.dumps(json_tmp), content_type='application/json')


def legajoRural(request, nivel, ubigeo):
    print "nivel: " + nivel
    print "ubigeo: " + ubigeo

    lista = []
    # print data
    if nivel == '1' or nivel == 1:

        #
        empadronadores = segm_r_emp.objects.filter(Q(ubigeo=ubigeo), Q(est_imp=1) | Q(est_imp=2)).order_by('emp')

        json_tmp = [
            {'nombre': '{}{}'.format(x.idruta, x.emp) + ".pdf", 'cant_pag': x.cant_pag, 'est_imp': int(x.est_imp),
             'est_check': x.flag_legajo, 'tipo': 1, 'codigo': '{}{}'.format(x.idruta, x.emp)} for
            x in empadronadores]

    elif nivel == '2' or nivel == 2:
        json_tmp = []
        secciones = segm_r_scr.objects.filter(ubigeo=ubigeo).order_by('scr')
        for scr in secciones:
            jsom_scr = {'nombre': scr.idscr + ".pdf", 'cant_pag': scr.cant_pag, 'est_imp': int(scr.est_imp),
                        'est_check': scr.flag_legajo, 'tipo': 2, 'codigo': scr.idscr}
            json_tmp.append(jsom_scr)
            for emp in segm_r_emp.objects.filter(idscr=scr.idscr).order_by('emp'):
                json_emp = {'nombre': '{}{}'.format(emp.idruta, emp.emp) + ".pdf", 'cant_pag': emp.cant_pag,
                            'est_imp': int(emp.est_imp), 'est_check': emp.flag_legajo, 'tipo': 1,
                            'codigo': '{}{}'.format(emp.idruta, emp.emp)}
                json_tmp.append(json_emp)

    elif nivel == '3' or nivel == 3:
        json_tmp = []
        distrito = Distrito.objects.filter(ubigeo=ubigeo)[0]

        jsom_dist = {'nombre': distrito.ubigeo + ".pdf", 'cant_pag': distrito.cant_pag_r,
                     'est_imp': int(distrito.est_imp_r), 'est_check': distrito.flag_legajo_r, 'tipo': 3,
                     'codigo': distrito.ubigeo}
        json_tmp.append(jsom_dist)
        for scr in segm_r_scr.objects.filter(ubigeo=ubigeo).order_by('scr'):
            json_scr = {'nombre': scr.idscr + ".pdf", 'cant_pag': scr.cant_pag, 'est_imp': int(scr.est_imp),
                        'est_check': scr.flag_legajo, 'tipo': 2, 'codigo': scr.idscr}
            json_tmp.append(json_scr)

    return HttpResponse(json.dumps(json_tmp), content_type='application/json')


@csrf_exempt
def guardar_pag(request):
    nombres_ubig = list(os.listdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\"))

    for ubigeo in nombres_ubig:

        nombres_zonas = [x for x in os.listdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\{}".format(ubigeo)) if
                         len(x) == 5]

        # print nombres_zonas
        print "Entro al ubigeo: " + ubigeo
        # time.sleep(3)
        for zona in nombres_zonas:

            nombres_totales = list(
                [x for x in os.listdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\{}\\{}".format(ubigeo, zona))])

            for nombre in nombres_totales:

                if len(nombre) == 21:

                    ubigeos = str(nombre[0:6])
                    zona = str(nombre[6:11])
                    aeu = str(nombre[14:17])

                    try:
                        participants = Tab_Aeus.objects.get(ubigeo=ubigeo, zona=zona, aeu_final=aeu)

                    except ObjectDoesNotExist:
                        participants = None

                    if participants != None:
                        pdf_file = PdfFileReader(open(
                            "//srv-fileserver/CPV2017/segm_tab/urbano/" + str(ubigeos) + "/" + str(zona) + "/" + str(
                                nombre), 'rb'))

                        number_of_pages = pdf_file.getNumPages()

                        participants.cant_pag = int(number_of_pages)
                        participants.save()
                        print "Se guardo las paginas del Ubigeo" + str(ubigeo) + " y con el AEU: " + str(aeu)

                elif len(nombre) == 18:

                    ubigeos = str(nombre[0:6])
                    zona = str(nombre[6:11])
                    secc = int(nombre[11:14])
                    print "este es el nombre de tu seccion " + nombre
                    try:
                        participants = Tab_Secciones.objects.get(ubigeo=ubigeo, zona=zona, seccion=secc)

                    except ObjectDoesNotExist:
                        participants = None

                    if participants != None:
                        pdf_file = PdfFileReader(open(
                            "//srv-fileserver/CPV2017/segm_tab/urbano/" + str(ubigeos) + "/" + str(zona) + "/" + str(
                                nombre), 'rb'))

                        number_of_pages = pdf_file.getNumPages()

                        participants.cant_pag = number_of_pages
                        participants.save()
                        print "Se guardo las paginas del Ubigeo " + str(ubigeo) + " y con seccion: " + str(secc)

    return JsonResponse({'msg': True})


@csrf_exempt
def actualizar_confir(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # print ("======================nombre===========================", type(data['nombre']))

        if data['opc_niv'] == '1' or data['opc_niv'] == 1:
            for i in data['nombre']:
                print "Entreo para aeusssssssssssssss"
                aeu = int(i['aeu'][14:17])
                print "AEU: " + str(aeu)
                participants = Tab_Aeus.objects.get(ubigeo=data['ubigeo'], zona=data['zona'], aeu_final=aeu)
                participants.est_con_aeu = 1
                participants.save()

        elif data['opc_niv'] == '2' or data['opc_niv'] == 2:
            for i in data['nombre']:
                print "Entreo para seccionesssssssssss"

                if len(i['aeu']) == 21:
                    aeu = int(i['aeu'][14:17])
                    participants = Tab_Aeus.objects.get(ubigeo=data['ubigeo'], zona=data['zona'], aeu_final=aeu)
                    participants.est_con_secc = 1
                    participants.save()
                elif len(i['aeu']) == 18:
                    secc = int(i['aeu'][11:14])
                    participants = Tab_Secciones.objects.get(ubigeo=data['ubigeo'], zona=data['zona'], seccion=secc)
                    participants.est_con_secc = 1
                    participants.save()
        elif data['opc_niv'] == '3' or data['opc_niv'] == 3:
            for i in data['nombre']:
                print "Entreo para zonassssss"

                if len(i['aeu']) == 18:
                    secc = int(i['aeu'][11:14])
                    participants = Tab_Secciones.objects.get(ubigeo=data['ubigeo'], zona=data['zona'], seccion=secc)
                    participants.est_con_zona = 1
                    participants.save()
                elif len(i['aeu']) == 15:
                    participants = Tab_Zonas.objects.get(ubigeo=data['ubigeo'], zona=data['zona'])
                    participants.est_con_zona = 1
                    participants.save()
        return JsonResponse({'msg': True})


@csrf_exempt
def actualizar_confir_rural(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # print ("======================nombre===========================", type(data['nombre']))

        if data['opc_niv'] == '1' or data['opc_niv'] == 1:
            for pdf in data['nombre']:
                nombrePDF = pdf['nombre']
                print "Entreo para empadronador"

                participants = segm_r_emp.objects.get(idruta=nombrePDF[0:10], emp=nombrePDF[10:12])
                participants.flag_legajo = "1"
                participants.save()

        elif data['opc_niv'] == '2' or data['opc_niv'] == 2:
            for pdf in data['nombre']:
                print pdf, "::::::::::::::::::::::::"
                print len(pdf['nombre']), "kkkkkkkkkkkkkkkkkkkkkkkkkk"

                if len(pdf['nombre']) == 12:

                    participants = segm_r_scr.objects.get(idscr=nombrePDF[0:8])
                    participants.flag_legajo = "1"
                    participants.save()
                elif len(pdf['nombre']) == 16:
                    nombrePDF = pdf['nombre']
                    #  print nombrePDF[0:10] ,  nombrePDF[10:12] ,"<<-------------"
                    participants = segm_r_emp.objects.get(idruta=nombrePDF[0:10], emp=nombrePDF[10:12])
                    participants.flag_legajo = "1"
                    participants.save()

        elif data['opc_niv'] == '3' or data['opc_niv'] == 3:
            for pdf in data['nombre']:
                if len(pdf['nombre']) == 10:
                    nombrePDF = pdf['nombre']
                    participants = Distrito.objects.get(ubigeo=nombrePDF[0:6])
                    participants.est_con_zona = 1
                    participants.save()
                elif len(pdf['nombre']) == 12:
                    nombrePDF = pdf['nombre']
                    participants = segm_r_scr.objects.get(idscr=nombrePDF[0:8])
                    participants.est_con_zona = 1
                    participants.save()

        return JsonResponse({'msg': True})


def calidad(request, ubigeo, zona):
    # data = [x for x in os.listdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\{}\\{}".format(ubigeo, zona))
    # if len(x) == 18]

    ccdd = ubigeo[0:2]
    ccpp = ubigeo[2:4]
    ccdi = ubigeo[4:6]
    lista = []

    data_secc = Tab_Secciones.objects.filter(ubigeo=ubigeo, zona=zona).values('seccion')

    depart = Departamento.objects.filter(ccdd=ccdd).values('departamento')[:1][0]
    provincia = Provincia.objects.filter(ccpp=ccpp, ccdd=ccdd).values('provincia')[:1][0]
    distrito = Distrito.objects.filter(Q(ccdd=ccdd), Q(ccpp=ccpp), Q(ccdi=ccdi)).values('distrito')[:1][0]

    dep = depart['departamento']
    prov = provincia['provincia']
    dist = distrito['distrito']
    zon = zona[0:3]
    '''
    print "Esto es de departamentoooooooo: "+ str(depart)
    return HttpResponse(json.dumps(lista), content_type='application/json')
    '''
    for aeu in data_secc:
        lista.append({'DEPARTAMENTO': dep, 'PROVINCIA': prov, 'DISTRITO': dist, 'ZONA': zon, 'NUM_SEC': aeu["seccion"]})

    return JsonResponse(lista, safe=False)


def calidad_errores(request, ubigeo, zona, seccion):
    lista = []
    data_aeus = Tb_Calidad_Aeu.objects.filter(ubigeo=ubigeo, zona=zona, seccion=seccion).order_by('aeu_final')

    for aeu in data_aeus:
        print ("aeu", aeu.aeu_final)
        lista.append({'aeu': aeu.aeu_final,
                      'nom_reg': aeu.nom_reg,
                      'fec_reg': aeu.fec_reg,
                      'cont_urb_error_01': aeu.cont_urb_error_01,
                      'cont_urb_error_02': aeu.cont_urb_error_02,
                      'cont_urb_error_03': aeu.cont_urb_error_03,
                      'cont_urb_error_04': aeu.cont_urb_error_04,
                      'cont_urb_error_05': aeu.cont_urb_error_05,
                      'cont_urb_error_06': aeu.cont_urb_error_06,
                      'cont_urb_error_07': aeu.cont_urb_error_07,
                      'cont_urb_error_08': aeu.cont_urb_error_08,
                      'cont_urb_error_09': aeu.cont_urb_error_09,
                      'cont_urb_error_10': aeu.cont_urb_error_10,
                      'cont_urb_error_11': aeu.cont_urb_error_11,
                      'cont_urb_error_12': aeu.cont_urb_error_12})

    return JsonResponse(lista, safe=False)


@csrf_exempt
def calidad_guardar_errors(request):
    if request.method == "POST":
        data = json.loads(request.body)

        print data
        for i in data['indicadores']:
            #     #aeu = int(i['nombre'][14:17])
            print i['aeu']
            participants = Tb_Calidad_Aeu.objects.get(ubigeo=data['ubigeo'], zona=data['zona'], aeu_final=i['aeu'])
            #
            participants.nom_reg = i['nom_reg']
            participants.fec_reg = i['fec_reg']
            participants.cont_urb_error_01 = i['cont_urb_error_01']
            participants.cont_urb_error_02 = i['cont_urb_error_02']
            participants.cont_urb_error_03 = i['cont_urb_error_03']
            participants.cont_urb_error_04 = i['cont_urb_error_04']
            participants.cont_urb_error_05 = i['cont_urb_error_05']
            participants.cont_urb_error_06 = i['cont_urb_error_06']
            participants.cont_urb_error_07 = i['cont_urb_error_07']
            participants.cont_urb_error_08 = i['cont_urb_error_08']
            participants.cont_urb_error_09 = i['cont_urb_error_09']
            participants.cont_urb_error_10 = i['cont_urb_error_10']
            participants.cont_urb_error_11 = i['cont_urb_error_11']
            participants.cont_urb_error_12 = i['cont_urb_error_12']
            #
            participants.save()

    return JsonResponse({'msg': True})


# @csrf_exempt
# def calidad_Indicadores_errors_urb(request):
#    if request.method == "POST":
#        data = json.loads(request.body)
#
#        print data
#        for i in data['indicadoresError']:
#        #     #aeu = int(i['nombre'][14:17])
#             print i['aeu']
#             participants = Calidad_Error_urb.objects.get(ubigeo=data['ubigeo'], zona=data['zona'], seccion=data['seccion'],aeu=data['aeu'])
#        #
#             participants.nom_reg = i['nom_reg']
#             participants.fec_reg = i['fec_reg']
#             participants.ind1 = i['IND1']
#             participants.ind2 = i['IND2']
#             participants.ind3 = i['IND3']
#             participants.ind4 = i['IND4']
#             participants.ind5 = i['IND5']
#             participants.ind6 = i['IND6']
#             participants.ind7 = i['IND7']
#             participants.ind8 = i['IND8']
#
#        #
#             participants.save()
#
#    return JsonResponse({'msg': True})
#


def zonas(request, ubigeo):
    data_zona = list(Tab_Aeus.objects.filter(ubigeo=ubigeo).values('zona').order_by('zona').distinct())

    return HttpResponse(json.dumps(data_zona), content_type='application/json')


def seccion(request, ubigeo, zona):
    data_secciones = list(Tab_Secciones.objects.filter(ubigeo=ubigeo, zona=zona).values('seccion').order_by('seccion'))

    return HttpResponse(json.dumps(data_secciones), content_type='application/json')


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
            # ubicacion_pdf_leer = "//srv-fileserver/CPV2017/list_segm_tab/listas.pdf"
            pdf_file = PdfFileReader(open(
                "//srv-fileserver/CPV2017/list_segm_tab/" + str(ubigeo) + "/" + str(zona) + "/" + str(ubigeo) + str(
                    zona) + str(secc) + str(aeu) + ".pdf", 'rb'))

            number_of_pages = pdf_file.getNumPages()
            lista_paginas.append({'cant_pag': number_of_pages})
            # lista_paginas.append({'nombre_de_tu_key': number_of_pages})
            # {NOMBRE: LI[0],}

    for i in range(len(data)):
        total = str(data[i + 1]) + "," + str(lista_paginas[i + 1])

    return HttpResponse(json.dumps(total), content_type='application/json')


def aeus_Seccion(request, ubigeo, zona):
    lista = []
    nombres_tot = [x for x in os.listdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\{}\\{}".format(ubigeo, zona)) if
                   len(x) > 15]

    for nombre in nombres_tot:
        lista.append({'nombre': nombre})

    print lista

    return HttpResponse(json.dumps(lista), content_type='application/json')


def seccion_Zonas(request, ubigeo, zona):
    datos_seccion = list(Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona).values('zona', 'seccion').annotate(
        data=Count('zona', 'seccion')))

    return HttpResponse(json.dumps(datos_seccion), content_type='application/json')


def zonas_Distritos(request, ubigeo):
    datos_seccion = list(
        Tab_Aeus.objects.filter(ubigeo=ubigeo).values('ubigeo', 'zona').annotate(data=Count('ubigeo', 'zona')))

    return HttpResponse(json.dumps(datos_seccion), content_type='application/json')


def cargarTabla(request, depa, prov, dist):
    lista = []

    if depa == 0 or depa == '0':

        data_dep = Departamento.objects.all().values('departamento')

        # cant_cab =
        # cant_tot = Tab_Aeus.objects.filter (Q(ubigeo = depa) )

        data_calidad = Tab_Aeus.objects.filter()

        # CONT_URB_ERROR_01
        for aeu in data_dep:
            lista.append({'departamento': aeu["departamento"]})

        return JsonResponse(lista, safe=False)

    elif prov == 0 or prov == '0':

        print "depa: " + str(depa)
        print "prov: " + str(prov)
        print "dist: " + str(dist)

        data_prov = Provincia.objects.filter(ccdd=depa).values('provincia')

        print "datos de la prov: " + str(data_prov)
        for aeu in data_prov:
            lista.append({'provincia': aeu["provincia"],
                          'cont_urb_error_01': aeu["cont_urb_error_01"],
                          'cont_urb_error_02': aeu["cont_urb_error_02"],
                          'cont_urb_error_03': aeu["cont_urb_error_03"],
                          'cont_urb_error_04': aeu["cont_urb_error_04"],
                          'cont_urb_error_05': aeu["cont_urb_error_05"],
                          'cont_urb_error_06': aeu["cont_urb_error_06"],
                          'cont_urb_error_07': aeu["cont_urb_error_07"],
                          'cont_urb_error_08': aeu["cont_urb_error_08"],
                          'cont_urb_error_09': aeu["cont_urb_error_09"],
                          'cont_urb_error_10': aeu["cont_urb_error_10"],
                          'cont_urb_error_11': aeu["cont_urb_error_11"],
                          'cont_urb_error_12': aeu["cont_urb_error_12"]})

        return JsonResponse(lista, safe=False)

    elif dist == 0 or dist == '0':

        data_dis = Distrito.objects.filter(ccdd=depa, ccpp=prov).values('distrito')

        print "datos del distrito: " + str(data_dis)
        for aeu in data_dis:
            lista.append({'distrito': aeu["distrito"],
                          'cont_urb_error_01': aeu["cont_urb_error_01"],
                          'cont_urb_error_02': aeu["cont_urb_error_02"],
                          'cont_urb_error_03': aeu["cont_urb_error_03"],
                          'cont_urb_error_04': aeu["cont_urb_error_04"],
                          'cont_urb_error_05': aeu["cont_urb_error_05"],
                          'cont_urb_error_06': aeu["cont_urb_error_06"],
                          'cont_urb_error_07': aeu["cont_urb_error_07"],
                          'cont_urb_error_08': aeu["cont_urb_error_08"],
                          'cont_urb_error_09': aeu["cont_urb_error_09"],
                          'cont_urb_error_10': aeu["cont_urb_error_10"],
                          'cont_urb_error_11': aeu["cont_urb_error_11"],
                          'cont_urb_error_12': aeu["cont_urb_error_12"]
                          })

        return JsonResponse(lista, safe=False)

    elif depa != 0 or depa != '0' and prov != 0 or prov != '0' and dist != 0 or dist != '0':

        data_zonas = Tab_Zonas.objects.filter(ubigeo=str(depa) + str(prov) + str(dist)).values('zona')

        print "datos de la zona: " + str(data_zonas)
        for aeu in data_zonas:
            lista.append({'zona': aeu["zona"],
                          'cont_urb_error_01': aeu["cont_urb_error_01"],
                          'cont_urb_error_02': aeu["cont_urb_error_02"],
                          'cont_urb_error_03': aeu["cont_urb_error_03"],
                          'cont_urb_error_04': aeu["cont_urb_error_04"],
                          'cont_urb_error_05': aeu["cont_urb_error_05"],
                          'cont_urb_error_06': aeu["cont_urb_error_06"],
                          'cont_urb_error_07': aeu["cont_urb_error_07"],
                          'cont_urb_error_08': aeu["cont_urb_error_08"],
                          'cont_urb_error_09': aeu["cont_urb_error_09"],
                          'cont_urb_error_10': aeu["cont_urb_error_10"],
                          'cont_urb_error_11': aeu["cont_urb_error_11"],
                          'cont_urb_error_12': aeu["cont_urb_error_12"]
                          })

        return JsonResponse(lista, safe=False)


def dataCro(request, ccdd, ccpp, estrato, ccdi, zona, seccion):
    from django.db import connection
    cursor = connection.cursor()
    # sql ="exec [dbo].[REPORTE_INDICADORES] %s,%s,%s ", (str(ccdd),str(ccpp),str(ccdi))
    cursor.execute("exec [dbo].[REPORTE_INDICADORES_CALIDAD_2] %s, %s , %s, %s, %s, %s",
                   (ccdd, ccpp, estrato, ccdi, zona, seccion))

    print "Aqui tu cursor"

    columns = [column[0] for column in cursor.description]

    menu = []

    for row in cursor.fetchall():
        print row
        menu.append(dict(zip(columns, row)))

    print menu

    return JsonResponse(menu, safe=False)


def data_cobertura(request, ccdd, ccpp, ccdi, tipo_r):
    from django.db import connection
    cursor = connection.cursor()
    print ccdd, ccpp, ccdi

    # sql ="exec [dbo].[REPORTE_INDICADORES] %s,%s,%s ", (str(ccdd),str(ccpp),str(ccdi))
    cursor.execute("exec [dbo].[REPORTES_SEGMENTACION] %s, %s , %s, %s",
                   (ccdd, ccpp, ccdi, tipo_r))
    # print cursor.fetchall()
    print "Aqui tu cursor"

    columns = [column[0] for column in cursor.description]

    menu = []

    for row in cursor.fetchall():
        print row
        menu.append(dict(zip(columns, row)))

    print menu

    return JsonResponse(menu, safe=False)


def data_prueba(request):
    ubigeo = '150116'

    zona = '00100'

    lista_paginas = []
    lista_aeu = []
    # nombres_tot = [x for x in os.listdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\{}\\{}".format(ubigeo, zona))
    #                if len(x) == 21 ]

    # print nombres_tot

    # data = list(Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona).values('cant_pag', 'est_imp'))

    # for nombre in nombres_tot:
    #     if len(nombre) == 21:  # Para AEUS
    #         lista_aeu.append(int(nombre[14:17]))
    # #print lista_aeu
    #
    # # for nombre in nombres_tot:
    # #     print "Nombre: " + str(nombre)
    # #     if len(nombre) == 21:  # Para AEUS
    # #         # pdf_file = PdfFileReader(open("//srv-fileserver/CPV2017/segm_tab/urbano/" + str(ubigeo) + "/" + str(zona) + "/" + str(nombre),'rb'))
    # #         # number_of_pages = pdf_file.getNumPages()
    # #         aeusin = int(nombre[14:17])
    #
    # #
    # lista_new = []
    # #print cond
    # cond = [[name.cant_pag, name.est_imp] for name in Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona, aeu_final__in=lista_aeu)]
    #
    # a = zip(nombres_tot, lista_aeu, cond)
    # print a
    # # i = 0
    # for dato in a:
    #     lista_new.append({'nombre': dato[0], 'cant_pag': dato[2][0], 'est_imp': dato[2][1]})
    # #
    #     print i
    #     #if len(name) == 21:
    #     #if name[0:5] == cond[i].ubigeo:
    #     lista_new.append({ 'nombre':name ,'cant_pag': cond[i].cant_pag})
    #    i = i + 1
    #
    # print lista_new
    # lista_paginas.append({'nombre': nombre, 'cant_pag': cond[0].cant_pag, 'est_imp': cond[0].est_imp_secc, 'tipo': 1})

    # for nombre in nombres_tot:

    lista_new = []
    lista_aeu = []
    nombres_tot = [x for x in os.listdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\{}\\{}".format(ubigeo, zona))
                   if len(x) == 18 or len(x) == 21]
    lista_seccion = []

    liston = []

    for nombre in nombres_tot:
        if len(nombre) == 21:  # Para AEUS
            lista_aeu.append(int(nombre[14:17]))
        if len(nombre) == 18:  # Para Seccion
            lista_seccion.append(int(nombre[11:14]))

    cond_aeu = [[name.cant_pag, name.est_imp_secc] for name in
                Tab_Aeus.objects.filter(ubigeo=ubigeo, zona=zona, aeu_final__in=lista_aeu)]

    cond_secc = [[name.cant_pag, name.est_imp_secc] for name in
                 Tab_Secciones.objects.filter(ubigeo=ubigeo, zona=zona, seccion__in=lista_seccion)]

    a = zip(nombres_tot, cond_secc)
    var = cond_aeu + cond_secc
    print var
    # for dato in a:
    #     lista_new.append({'nombre': dato[0], 'cant_pag': dato[1][0], 'est_imp': dato[1][1]})
    # print cond_secc

    # print lista_seccion

    return HttpResponse(json.dumps(lista_new), content_type='application/json')


def listado_Urbano(request, ubigeo, zona, aeu):
    # variable que guarda lo que se obtiene en la funcion dataCont
    # dataAux = dataCont(area, tipo, ccdd, ccpp, ccdi, zona)
    cursor = connection.cursor()

    cursor.execute("exec LISTADO_URBANO '{}','{}','{}'".format(str(ubigeo), str(zona), str(aeu)))

    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        # Se agrega un elemento
        data.append(dict(zip(columns, row)))
    # se retorna la data (dataAux) como un HttpResponse - json
    return HttpResponse(json.dumps(data), content_type='application/json')


def calidadErrorUrb(request, ubigeo, zona, aeu):
    data = Calidad_Error_urb.objects.filter(ubigeo=ubigeo, zona=zona, aeu=aeu)

    json_tmp = [{'UBIGEO': x.ubigeo, 'ZONA': x.zona, 'AEU': int(x.aeu),
                 'IND1': x.ind1, 'IND2': x.ind2, 'IND3': x.ind3, 'IND4': x.ind4, 'IND5': x.ind5, 'IND6': x.ind6,
                 'IND7': x.ind7} for x in data]

    return HttpResponse(json.dumps(json_tmp), content_type='application/json')


@csrf_exempt
def guardarCalidadErrorUrb(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for i in data['indicadoresErrorUrb']:
            info = Calidad_Error_urb.objects.get(ubigeo=data['ubigeo'], zona=data['zona'], aeu=data['aeu'])
            print info.ubigeo, info.zona, info.aeu, info.ind1, "<----------------"

            info.ind1 = i['IND1']
            info.ind2 = i['IND2']
            info.ind3 = i['IND3']
            info.ind4 = i['IND4']
            info.ind5 = i['IND5']
            info.ind6 = i['IND6']
            info.ind7 = i['IND7']

            ##indica que se registro loss indicadores
            info.check = 1
            info.save()

        info1 = Calidad_Error_urb.objects.filter(ubigeo=data['ubigeo'], zona=data['zona'])
        flag_zona = Tab_Zonas.objects.get(ubigeo=data['ubigeo'], zona=data['zona'])
        cont = 0
        zonaRechazo = 0
        for e in info1:
            if (e.check == 1):
                cont += 1;
            else:
                pass

        if len(info1) == cont:
            print "SE COMPLETARON LOS CHECKS, se Evaluaran los Indicadores"
            aeuRechazada = 0;
            for i in info1:
                sumTotal = i.ind1 + i.ind2 + i.ind3 + i.ind4 + i.ind5 + i.ind6 + i.ind7;
                print sumTotal, "<------->", i
                if sumTotal >= 1:
                    aeuRechazada += 1;
            if len(info1) >= 2 and len(info1) <= 7:
                if aeuRechazada >= 1:
                    print "SE RECHAZA LA ZONA: MUESTRA:2"
                    flag_zona.flag = 1;
                    flag_zona.save()
                else:
                    print "NO SE RECHAZA LA ZONA : MUESTRA:2"
                    flag_zona.flag = 0;
                    flag_zona.save()

            if len(info1) >= 8 and len(info1) <= 12:
                if aeuRechazada >= 2:
                    print "SE RECHAZA LA ZONA MUESTRA: 8"
                    flag_zona.flag = 1;
                    flag_zona.save()
                else:
                    print "NO SE RECHAZA LA ZONA MUESTRA : 8"
                    flag_zona.flag = 0;
                    flag_zona.save()

            if len(info1) >= 13 and len(info1) <= 19:
                if aeuRechazada >= 3:
                    print "SE RECHAZA LA ZONA MUESTRA: 13"
                    flag_zona.flag = 1;
                    flag_zona.save()
                else:
                    print "NO SE RECHAZA LA ZONA MUESTRA :13"
                    flag_zona.flag = 0;
                    flag_zona.save()

            if len(info1) >= 20 and len(info1) <= 31:
                if aeuRechazada >= 4:
                    print "SE RECHAZA LA ZONA MUESTRA: 20"
                    flag_zona.flag = 1;
                    flag_zona.save()
                else:
                    print "NO SE RECHAZA LA ZONA  MUESTRA: 20"
                    flag_zona.flag = 0;
                    flag_zona.save()

            if len(info1) >= 32:
                if aeuRechazada >= 6:
                    print "SE RECHAZA LA ZONA MUESTRA: 32"
                    flag_zona.flag = 1;
                    flag_zona.save()
                else:
                    print "NO SE RECHAZA LA ZONA MUESTRA: 32"
                    flag_zona.flag = 0;
                    flag_zona.save()


        else:
            print "AUN NO SE COMPLETARON LOS CHECKS, NO se Evaluaran los Indicadores"


            print cont, "<------- SUMA"
            print len(info1), "<------------TOTAL AEUS"


    return JsonResponse({'msg': True})


def calidadErrorRural(request, ubigeo, emp):
    data = Calidad_Error_rural.objects.filter(ubigeo=ubigeo, emp=emp)
    json_tmp = [{'UBIGEO': x.ubigeo, 'EMP': x.emp,
                 'IND1': x.ind1, 'IND2': x.ind2, 'IND3': x.ind3, 'IND4': x.ind4} for x in data]

    return HttpResponse(json.dumps(json_tmp), content_type='application/json')


@csrf_exempt
def guardarCalidadErrorRural(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for i in data['indicadoresErrorRural']:
            info = Calidad_Error_rural.objects.get(ubigeo=data['ubigeo'], emp=data['emp'])
            info.ind1 = i['IND1']
            info.ind2 = i['IND2']
            info.ind3 = i['IND3']
            info.ind4 = i['IND4']
            info.save()
    return JsonResponse({'msg': True})


### vERIFICA SI RECHASA UNA ZONA
def verficaRechazoZonaUrb(request, ubigeo, zona):
    info = Calidad_Error_urb.objects.get(ubigeo=ubigeo, zona=zona)
    for i in info:

        n_errores = i.ind1 + i.ind2 + i.ind3 + i.ind4 + i.ind5 + i.ind6 + i.ind7 + i.ind8;
        if n_errores >= 1:
            unid_defec = unid_defec + 1

        elif n_errores == 0:
            unid_defec = unid_defec + 0

    print n_errores
    print unid_defec

    return JsonResponse({'msg': True})


def listado_segm_rural(request, nivel, dep, prov):
    cursor = connection.cursor()
    cursor.execute("exec ASIGNAR_SEGMTACION {},'{}','{}'".format(nivel, str(dep), str(prov)))
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        # Se agrega un elemento
        data.append(dict(zip(columns, row)))
    # se retorna la data (dataAux) como un HttpResponse - json
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def guardar_Asig_segm(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for i in data['registros']:
            asig = SegmentacionJefe.objects.get(ccdd=data['CCDD'], ccpp=data['CCPP'], ccdi=i['CCDI'])

            if asig.equipo ==  i['EQUIPO']:
                pass
            else:
                 asig.equipo = i['EQUIPO']
                 if asig.equipo != 0:
                     asig.estado = 1
                     asig.segmentista =0
                 else:
                     asig.estado = 0
            asig.save()
    return JsonResponse({'msg': True})


@csrf_exempt
def guardar_Asig_Equi(request):
    if request.method == "POST":
        data = json.loads(request.body)

        for i in data['registros']:
            asig = SegmentacionJefe.objects.get(ccdd=data['CCDD'], ccpp=data['CCPP'], ccdi=i['CCDI'])
            usu = Usuario_Segm.objects.get(user_equipo=i['EQUIPO'], user_segm=i['SEGMENTISTA'])

            if asig.segmentista == usu.segmentista :
                pass
            else:

                 asig.segmentista = usu.segmentista
                 print "<<-------------ENTROOO AQUIIII", asig.segmentista
                 if asig.segmentista == '0':
                      print "<<-------------ENTROOO AQUIIII" , asig.ubigeo
                      asig.estado = 1
                 elif asig.segmentista != 0:
                      asig.estado = 2
                 asig.save()


    return JsonResponse({'msg': True})


@csrf_exempt
def guardar_validacion(request, ubigeo, val):
    asig = SegmentacionJefe.objects.get(ubigeo=ubigeo)

    asig.estado = val
    asig.save()

    print ubigeo, asig.estado, val, '<<<-------------------------'
    return JsonResponse({'msg': True})


#####################MODULO MONITOREO CALIDAD INPUT


def listado_monit_calid(request, nivel, dep, prov):
    cursor = connection.cursor()
    cursor.execute("exec MONITOREO_CALIDAD {},'{}','{}'".format(nivel, str(dep), str(prov)))
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        # Se agrega un elemento
        data.append(dict(zip(columns, row)))
    # se retorna la data (dataAux) como un HttpResponse - json
    return HttpResponse(json.dumps(data), content_type='application/json')


def listado_monit_calid_rural(request, nivel, dep, prov):
    cursor = connection.cursor()
    cursor.execute("exec MONITOREO_CALIDAD_RURAL {},'{}','{}'".format(nivel, str(dep), str(prov)))
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        # Se agrega un elemento
        data.append(dict(zip(columns, row)))
    # se retorna la data (dataAux) como un HttpResponse - json
    return HttpResponse(json.dumps(data), content_type='application/json')




@csrf_exempt
def guardar_validacion_input(request, ubigeo, val):
    asig = Calidad_input.objects.get(ubigeo=ubigeo)
    print (time.strftime("%m/%d/%y"))

    asig.estado = val
    if asig.estado == '1':
        print "ENTROOOOO"
        asig.fechaEnvio = (time.strftime("%Y-%m-%d"))

    elif asig.estado == '2':
        asig.fechaValid = (time.strftime("%Y-%m-%d"))

    asig.save()

    print ubigeo, asig.estado, val,asig.fechaValid,asig.fechaEnvio,    '<<<-------------------------'
    return JsonResponse({'msg': True})


@csrf_exempt
def guardar_validacion_input_rural(request, ubigeo, val):
    asig_r = Calidad_input_rural.objects.get(ubigeo=ubigeo)
    print (time.strftime("%m/%d/%y"))
    asig_r.estado = val
    if asig_r.estado == '1':
        print "ENTROOOOO"
        asig_r.fechaEnvio = (time.strftime("%Y-%m-%d"))

    elif asig.estado == '2':
        asig_r.fechaValid = (time.strftime("%Y-%m-%d"))

    asig_r.save()

    print ubigeo, asig_r.estado, val,asig_r.fechaValid,asig_r.fechaEnvio,    '<<<-------------------------'
    return JsonResponse({'msg': True})






###### muestreo control-calidad

def listado_calid_muestreo(request, nivel, dep, prov):
    cursor = connection.cursor()
    cursor.execute("exec LISTA_CALIDAD_MUESTREO {},'{}','{}'".format(nivel, str(dep), str(prov)))
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        # Se agrega un elemento
        data.append(dict(zip(columns, row)))
    # se retorna la data (dataAux) como un HttpResponse - json
    return HttpResponse(json.dumps(data), content_type='application/json')



def listado_calid_legajos(request, nivel, dep, prov, dist, zona):
    cursor = connection.cursor()
    cursor.execute("exec LISTA_CALIDAD_LEGAJOS {},'{}','{}','{}','{}'".format(nivel, str(dep),str(prov),str(dist),str(zona)))
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        # Se agrega un elemento
        data.append(dict(zip(columns, row)))
    # se retorna la data (dataAux) como un HttpResponse - json
    return HttpResponse(json.dumps(data), content_type='application/json')


