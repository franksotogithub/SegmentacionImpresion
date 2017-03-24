# import subprocess
# lpr = subprocess.Popen("C:/Users/acarrillo/Desktop/pap.pdf", stdin=subprocess.PIPE)
# lpr.stdin.write(your_data_here)

import os

import win32gui

import win32ui
from django.http import HttpResponse
import os, sys
import win32print
import win32api

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from reportes_models import *
from reportes_models import *
import cgi
import tempfile
import tempfile
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

import win32com.client
import os.path
import threading
import time
import json


#
# def imprimir(request):
#
#     lista = []
#     #
#     # lista.append(1)
#     #
#     # os.startfile("C:/Users/acarrillo/Desktop/pap.pdf", "print")
#
#
#     filename = tempfile.mktemp(".txt")
#     open(filename, "w").write("This is a test")
#     win32api.ShellExecute(
#         0,
#         "print",
#         filename,
#         #
#         # If this is None, the default printer will
#         # be used anyway.
#         #
#         '/d:"%s"' % win32print.GetDefaultPrinter(),
#         ".",
#         0
#     )
#
#     win32api.ShellExecute(0, "print", pdf_file_name, None, ".", 0)
#
#     HttpResponse(lista)

# def imprimir(request):
#
#     lista = []
#     #
#     # lista.append(1)
#     #
#     # os.startfile("C:/Users/acarrillo/Desktop/pap.pdf", "print")
#
#
#
#     printer_name = win32print.GetDefaultPrinter()
#     #
#     # raw_data could equally be raw PCL/PS read from
#     #  some print-to-file operation
#     #
#     if sys.version_info >= (3,):
#         raw_data = bytes("This is a test", "utf-8")
#     else:
#         raw_data = "This is a test"
#
#     hPrinter = win32print.OpenPrinter(printer_name)
#
#     try:
#         hJob = win32print.StartDocPrinter(hPrinter, 1, ("test of raw data", None, "RAW"))
#         try:
#             win32print.StartPagePrinter(hPrinter)
#             win32print.WritePrinter(hPrinter, raw_data)
#             win32print.EndPagePrinter(hPrinter)
#         finally:
#             win32print.EndDocPrinter(hPrinter)
#     finally:
#         win32print.ClosePrinter(hPrinter)
#
#     return HttpResponse(lista)


# def imprimir(request):
#
#     lista = []
#
#     filename = tempfile.mktemp ("C:/Users/acarrillo/Desktop/pap.pdf")
#     open(filename, "w").write ("This is a test")
#     win32api.ShellExecute(
#       0,
#       "printto",
#       filename,
#       '"%s"' % win32print.GetDefaultPrinter (),
#       ".",
#       0
#     )
#
#     return HttpResponse(lista)



def imprimi_zona(request):
    lista = []
    ubigeo = '050617'
    zona = '00200'
    nombres_tot = [x for x in os.listdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\{}\\{}".format(ubigeo, zona)) if
                   len(x) == 18 or len(x) == 15]

    for nombre in nombres_tot:
        sacar_impresion(request, ubigeo, zona, nombre)
        print nombre
        time.sleep(3)

    return HttpResponse(lista)


@csrf_exempt
def imprimir_seccion_unica(request):

        if request.method == "POST":
            data = json.loads(request.body)

            if data['opc_niv'] == '1':
                for i in data['nombre']:
                    aeu = int(i['nombre'][14:17])
                    participants = Tab_Aeus.objects.get(ubigeo=data['ubigeo'], zona=data['zona'], aeu_final=aeu)


                    print "estado del la impresion {}".format(  participants.est_imp)

                    if participants.est_imp == '0':
                        participants.est_imp = '1'
                        participants.save()

                    if participants.est_imp == '1':
                        participants.est_imp = '2'
                        participants.save()

                    sacar_impresion(request, data['ubigeo'], data['zona'], i['nombre'], data['opc'])
                    time.sleep(6)

                return JsonResponse({'msg': True})

            elif data['opc_niv'] == '2':

                for i in data['nombre']:

                     if len(i['nombre'])==21:#Para Aeus
                        aeu = int(i['nombre'][14:17])
                        participants = Tab_Aeus.objects.get(ubigeo=data['ubigeo'], zona=data['zona'], aeu_final=aeu)

                        if participants.est_imp_secc == '1' or participants.est_imp_secc == 1:
                            #print participants
                            participants.est_imp_secc = 2
                            participants.save()
                            #sacar_impresion(request, data['ubigeo'], data['zona'], i['nombre'], data['opc'])
                            time.sleep(6)
                        if participants.est_imp_secc == '0' or participants.est_imp_secc == 0:
                            participants.est_imp_secc = 1
                            participants.save()
                            time.sleep(6)


                     elif len(i['nombre'])==18: #Para Seccion
                        secc = int(i['nombre'][11:14])
                        participants_secc = Tab_Secciones.objects.get(ubigeo=data['ubigeo'], zona=data['zona'], seccion=secc)

                        if participants_secc.est_imp_secc == 1 or participants_secc.est_imp_secc == '1':
                            participants_secc.est_imp_secc = 2
                            participants_secc.save()
                            time.sleep(6)
                        if  participants_secc.est_imp_secc == 0 or participants_secc.est_imp_secc == '0':
                            participants_secc.est_imp_secc = 1
                            participants_secc.save()
                            time.sleep(6)
                     sacar_impresion(request, data['ubigeo'], data['zona'], i['nombre'], data['opc'])
                        #time.sleep(5)

                return JsonResponse({'msg': True})

            elif data['opc_niv'] == '3':
                # object.save(force_insert=True)
                print 'Entro para guardar a nivel Zonal'
                print 'ubigeo: ' + str(data['ubigeo'])
                print 'zona: ' + str(data['zona'])
                print 'impresora: ' + str(data['opc'])

                for i in data['nombre']:

                     if len(i['nombre'])==18: #Seccion
                        secc = int(i['nombre'][11:14])
                        participants = Tab_Secciones.objects.get(ubigeo=data['ubigeo'], zona=data['zona'], seccion=secc)

                        if participants.est_imp_zona == '1' or participants.est_imp_zona == 1:
                            participants.est_imp_zona = 2
                            participants.save()
                            time.sleep(5)
                        if participants.est_imp_zona == '0' or participants.est_imp_zona == 0:
                            participants.est_imp_zona = 1
                            participants.save()
                            time.sleep(5)

                     elif len(i['nombre']) == 15:  #Zona

                        participants_secc = Tab_Zonas.objects.get(ubigeo=data['ubigeo'], zona=data['zona'])

                        if participants_secc.est_imp_zona == '1' or participants_secc.est_imp_zona == 1:
                            participants_secc.est_imp_zona = 2
                            participants_secc.save()
                            time.sleep(5)
                        if participants_secc.est_imp_zona == '0' or participants_secc.est_imp_zona == 0:
                            participants_secc.est_imp_zona = 1
                            participants_secc.save()
                            time.sleep(5)

                     sacar_impresion(request, data['ubigeo'], data['zona'], i['nombre'], data['opc'])

                return JsonResponse({'msg': True})


@csrf_exempt
def procesoImpresionRural(request):

    if request.method == "POST":
        data = json.loads(request.body)
        if data['opc_niv'] == '1':
            for pdf in data['nombre']:
                nombrePDF = pdf['nombre']
                registro = segm_r_emp.objects.get(idruta=nombrePDF[0:10], emp=nombrePDF[10:12])
                if registro.est_imp == '0':
                    registro.est_imp = '1'
                    registro.save()

                elif registro.est_imp == '1':
                    registro.est_imp = '2'
                    registro.save()

                impresion_rural(request, data['ubigeo'], nombrePDF, data['opc'])
                time.sleep(6)
                del nombrePDF

        elif data['opc_niv'] == '2':
            for pdf in data['nombre']:
                if len(pdf['nombre']) == 8:
                    nombrePDF = pdf['nombre']
                    registrosscr = segm_r_scr.objects.get(idscr=nombrePDF)
                    print registrosscr.est_imp, type(registrosscr.est_imp), "<<<------------"
                    if registrosscr.est_imp == '0':
                        registrosscr.est_imp = '1'
                        registrosscr.save()

                    elif registrosscr.est_imp == '1':
                        registrosscr.est_imp = '2'
                        registrosscr.save()

                elif len(pdf['nombre']) == 12:
                    nombrePDF = pdf['nombre']
                    registroemp = segm_r_emp.objects.get(idruta=nombrePDF[0:10], emp=nombrePDF[10:12])

                    if registroemp.est_imp == '0':
                        registroemp.est_imp = '1'
                        registroemp.save()

                    elif registroemp.est_imp == '1':
                        registroemp.est_imp = '2'
                        registroemp.save()

                impresion_rural(request, data['ubigeo'], nombrePDF, data['opc'])
                time.sleep(6)
                del nombrePDF

        elif data['opc_niv'] == '3':
            for pdf in data['nombre']:
                if len(pdf['nombre']) == 6:
                    nombrePDF = pdf['nombre']
                    registrosdist = Distrito.objects.get(ubigeo=nombrePDF)

                    if registrosdist.est_imp_r == '0':
                        registrosdist.est_imp_r = '1'
                        registrosdist.save()

                    elif registrosdist.est_imp_r == '1':
                        registrosdist.est_imp_r = '2'
                        registrosdist.save()

                elif len(pdf['nombre']) == 8:
                    nombrePDF = pdf['nombre']
                    registrosscr = segm_r_scr.objects.get(idscr=nombrePDF)

                    if registrosscr.est_imp == '0':
                        registrosscr.est_imp = '1'
                        registrosscr.save()

                    elif registrosscr.est_imp == '1':
                        registrosscr.est_imp = '2'
                        registrosscr.save()

                impresion_rural(request, data['ubigeo'], nombrePDF, data['opc'])
                time.sleep(6)
                del nombrePDF

    return JsonResponse({'msg': True})







def imprimir(request):
    lista = []
    lista_distrito = []

    lista_distrito.append('020601')

    lista = []
    lista_zonas = []

    # for ubigeos in lista_distrito:
    #     #tempprinter = "\\\\server01\\printer01"
    #     # tempprinter = "\\\\172.18.1.35\\192.168.230.68"
    #     # total_zonas = int(str(Esp_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos]).values_list('zona', flat=True).distinct().count()))
    #     total_zonales = Esp_Aeus.objects.filter(ubigeo=ubigeos, zona='00100').values_list('zona', flat=True)
    #     zona_dif = list(set(total_zonales))

    # lista_zonas.append(total_zonas)
    ubigeo = '050302'
    zona = '00100'
    nombres_tot = [x for x in os.listdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\{}\\{}".format(ubigeo, zona)) if
                   len(x) > 15]

    for nombre in nombres_tot:
        #sacar_impresion(request, ubigeo, zona, nombre)
        #print nombre
        time.sleep(3)


    return HttpResponse(lista)

# def sacar_impresion(request,ubigeo, zonaq, seccq, aeut):
def sacar_impresion(request, ubig, zon, name, opc):
    lista = []
    if opc == 1:
        "Entro a la impresora blanca"
        tempprinter = "\\\\172.18.1.35\\192.168.230.16"
    else:
        print "Entro a la impresora negra"
        tempprinter = "\\\\172.18.1.35\\192.168.230.20"

    print tempprinter
    currentprinter = win32print.GetDefaultPrinter()


    source_file_name = "\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubig) + "\\" + str(zon) + "\\" + str(name)

    win32api.ShellExecute(0, "print", source_file_name, None, ".", 0)
    win32print.SetDefaultPrinter(currentprinter)

    return HttpResponse(lista)


def impresion_rural(request, ubigeo, pdf, impresora):
    if impresora == 1:
        # IMPRESORA CARTO


        tempprinter = "\\\\172.18.1.35\\HPM880-CARTO"
        #tempprinter = "\\\\172.18.1.35\\192.168.230.16"
    else:
        # IMPRESORA UDRA

        tempprinter = "\\\\172.18.1.35\\HP9050-UDRA"
        #tempprinter = "\\\\172.18.1.35\\192.168.230.20"

    currentprinter = win32print.GetDefaultPrinter()

    PathPDF = "\\\\192.168.201.115\\cpv2017\\croquis-listado\\rural\\{}\\{}.pdf".format(ubigeo, pdf)

    win32print.SetDefaultPrinter(tempprinter)

    win32api.ShellExecute(0, "print", PathPDF, None, ".", 0)
    win32print.SetDefaultPrinter(currentprinter)
    return HttpResponse([])




def ImpresorasConectadas(request):
    impresoras = [{'nombre': x[2]} for x in win32print.EnumPrinters(win32print.PRINTER_ENUM_CONNECTIONS)]
    return HttpResponse(json.dumps(impresoras), content_type='application/json')


def mergePDF(pdfs):
    temp = tempfile.NamedTemporaryFile(delete=False)
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write('{}.pdf'.format(temp.name))
    return tf.name


def EnviarImpresion(namepdf, impresoraselect):
    impresoras = [x[2] for x in win32print.EnumPrinters(win32print.PRINTER_ENUM_CONNECTIONS)]
    win32print.SetDefaultPrinter(impresoras[int(impresoraselect)])
    os.startfile(namepdf, "print")
    return JsonResponse({'msg': True})










@csrf_exempt
def procesoImpresionEtiquetaRural(request, ubigeo, nivel):

        print "nivel: " + nivel
        print "ubigeo: " + ubigeo

        if nivel == '1' or nivel == 1:

            empadronadores = segm_r_emp.objects.filter(ubigeo=ubigeo).order_by('emp')


            for eti in empadronadores:
                etiqueta = eti.idruta + eti.emp+".pdf"
                print "Se Imprimio la Etiqueta<<<------------------"
                print etiqueta
                #impresion_etiqueta_rural(request, ubigeo, etiqueta, 2)
                #time.sleep(6)
                #del etiqueta

        elif nivel == '2' or nivel == 2:
            tmp = []
            secciones = segm_r_scr.objects.filter(ubigeo=ubigeo).order_by('scr')
            for scr in secciones:
                etiqueta = scr.idscr + ".pdf"
                tmp.append(etiqueta)
                for emp in segm_r_emp.objects.filter(idscr=scr.idscr).order_by('emp'):
                    etiqueta = emp.idruta + emp.emp + ".pdf"
                    tmp.append(etiqueta)

            print tmp
            for lisEtiqueta in tmp:
                print "Se Imprimio la Etiqueta<<<------------------"
                print lisEtiqueta

                #impresion_etiqueta_rural(request, ubigeo, lisEtiqueta, 2)
                #time.sleep(6)
                #del lisEtiqueta

        elif nivel == '3' or nivel == 3:
            tmp = []
            distrito = Distrito.objects.filter(ubigeo=ubigeo)[0]
            etiqueta = distrito.ubigeo+".pdf"
            tmp.append(etiqueta)
            for scr in segm_r_scr.objects.filter(ubigeo=ubigeo).order_by('scr'):
                etiqueta = scr.idscr + ".pdf"
                tmp.append(etiqueta)
            for lisEtiqueta in tmp:
                print lisEtiqueta
                print "Se Imprimio la Etiqueta<<<------------------"
                #impresion_etiqueta_rural(request, ubigeo, lisEtiqueta, 2)
                #time.sleep(6)
                #del lisEtiqueta

        return JsonResponse({'msg': True})


def impresion_etiqueta_rural(request, ubigeo, pdf, impresora):
    if impresora == 1:
        # IMPRESORA BLANCA
        tempprinter = "\\\\172.18.1.35\\192.168.230.16"
    else:
        # IMPRESORA NEGRA


        tempprinter = "\\\\172.18.1.35\\192.168.230.20"

    currentprinter = win32print.GetDefaultPrinter()

    PathPDF = "\\\\192.168.201.115\\cpv2017\\etiquetas\\rural\\{}\\{}".format(ubigeo, pdf)

    win32print.SetDefaultPrinter(tempprinter)

    win32api.ShellExecute(0, "print", PathPDF, None, ".", 0)
    win32print.SetDefaultPrinter(currentprinter)
    return HttpResponse([])



        # # tempprinter = "\\\\server01\\printer01"
    # # tempprinter = "\\\\172.18.1.35\\192.168.230.68"
    # tempprinter = "\\\\172.18.1.35\\192.168.230.16"
    # currentprinter = win32print.GetDefaultPrinter()
    # source_file_name = "C:/Users/acarrillo/Desktop/pap.pdf"
    # win32print.SetDefaultPrinter(tempprinter)
    # win32api.ShellExecute(0, "print", source_file_name, None, ".", 0)
    # win32print.SetDefaultPrinter(currentprinter)
