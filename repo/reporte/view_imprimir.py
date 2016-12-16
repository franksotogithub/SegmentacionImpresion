# import subprocess
# lpr = subprocess.Popen("C:/Users/acarrillo/Desktop/pap.pdf", stdin=subprocess.PIPE)
# lpr.stdin.write(your_data_here)

import os
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


#
# def imprimir(request):
#
#     lista = []
#
#     source_file_name = "C:/Users/acarrillo/Desktop/test.txt"
#     pdf_file_name = tempfile.mktemp(".pdf")
#
#     styles = getSampleStyleSheet()
#     h1 = styles["h1"]
#     normal = styles["Normal"]
#
#     doc = SimpleDocTemplate(pdf_file_name)
#     #
#     # reportlab expects to see XML-compliant
#     #  data; need to escape ampersands &c.
#     #
#     text = cgi.escape(open(source_file_name).read().decode('latin-1')).splitlines()
#
#     #
#     # Take the first line of the document as a
#     #  header; the rest are treated as body text.
#     #
#     story = [Paragraph(text[0], h1)]
#     for line in text[1:]:
#         story.append(Paragraph(line, normal))
#         story.append(Spacer(1, 0.2 * inch))
#
#     doc.build(story)
#     win32api.ShellExecute(0, "print", pdf_file_name, None, ".", 0)
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


        #object.save(force_insert=True)

        print 'ubigeo: '+ str(data['ubigeo'])
        print 'zona: ' + str(data['zona'])
        print 'impresora' + str(data['opc'])
        for i in data['nombre']:

            hola = '{} {} {}'.format(data['ubigeo'], data['zona'], i['aeu_final'])

            aeu = int(i['aeu_final'][14:17])
            print "AEU: "+str(aeu)
            participants = Tab_Aeus.objects.get(ubigeo=data['ubigeo'], zona=data['zona'], aeu_final=aeu)
            print participants
            participants.est_imp = '1'

            participants.save()

            sacar_impresion(request, data['ubigeo'], data['zona'], i['aeu_final'], data['opc'])
            #print i['aeu_final']
            print hola
            time.sleep(3)

        # lista = []
        # lista_zonas = []

        # ubigeo = '150116'
        # zona = '00100'
        # seccion = '013'
        # nombres_tot = [x for x in os.listdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\{}\\{}".format(ubigeo, zona))if len(x) > 15 and x[11:14] ==seccion]

        # nombres = os.listdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\{}\\{}\\{}".format(ubigeo, zona, name))

        # for nombre in nombres:
        #     #sacar_impresion(request, ubigeo, zona, nombre)
        #     # print nombre
        #     time.sleep(3)
        # for nombre in nombres_tot:
        #     # sacar_impresion(request, ubigeo, zona, nombre)
        #     print nombre
        #     time.sleep(3)

        return JsonResponse({'msg': True})


def imprimir(request):
    lista = []
    lista_distrito = []

    # lista_distrito.append('020801')
    lista_distrito.append('020601')
    # lista_distrito.append('021509')
    # lista_distrito.append('021806')
    # lista_distrito.append('022001')
    # lista_distrito.append('030212')


    lista = []
    lista_zonas = []

    # for ubigeos in lista_distrito:
    #     #tempprinter = "\\\\server01\\printer01"
    #     # tempprinter = "\\\\172.18.1.35\\192.168.230.68"
    #     # total_zonas = int(str(Esp_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos]).values_list('zona', flat=True).distinct().count()))
    #     total_zonales = Esp_Aeus.objects.filter(ubigeo=ubigeos, zona='00100').values_list('zona', flat=True)
    #     zona_dif = list(set(total_zonales))

    # lista_zonas.append(total_zonas)
    ubigeo = '150116'
    zona = '00100'
    nombres_tot = [x for x in os.listdir("\\\srv-fileserver\\CPV2017\\list_segm_tab\\{}\\{}".format(ubigeo, zona)) if
                   len(x) > 15]

    for nombre in nombres_tot:
        sacar_impresion(request, ubigeo, zona, nombre)
        print nombre
        time.sleep(3)

        # for zona_t in zona_dif:
        #     # zoner = str(zona_t+1).zfill(3)+"00"
        #     # total_aes_zona = int(str(Esp_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos], zona=zona_t).count()))
        #     # total_secc_zona= Esp_Aeus.objects.filter(ubigeo=ubigeos, zona=zona_t).values_list('seccion', flat=True)
        #     total_secc_zona = Esp_Aeus.objects.filter(ubigeo=ubigeos, zona=zona_t, seccion='1').values_list('seccion', flat=True).order_by('seccion')
        #     seccion_dif = list(set(total_secc_zona))
        #
        #     print "SeccioneS: ->"
        #
        #     for secci in seccion_dif:
        #
        #         total_secc_zona = Esp_Aeus.objects.filter(ubigeo=ubigeos, zona=zona_t, seccion=secci).values_list('aeu_final', flat=True).order_by('aeu_final')
        #         aeu_dif = list(set(total_secc_zona))
        #         # list.append(aeu+1)
        #         for aeu in aeu_dif:
        #             lista.append("Ubigeo: "+str(ubigeos)+" Zona: "+zona_t + " Seccion: "+str(secci)+" y AEU: "+str(aeu) + "<br/>")
        #             # str(zona_t + 1)+": " + str(aeu + 1) + "<br/>"
        #             sacar_impresion(request, str(ubigeos), zona_t, str(secci), str(aeu))
        #             time.sleep(3)

    return HttpResponse(lista)

# def sacar_impresion(request,ubigeo, zonaq, seccq, aeut):
def sacar_impresion(request, ubig, zon, name, opc):
    lista = []
    # lista.append("Ubigeo: "+str(ubigeo)+" Zona: " +str(zonaq) +" Seccion:  "+ str(seccq)+" y  AEU: "+str(aeut) +"<br/>")


    # cond = Esp_Aeus.objects.filter(ubigeo=ubigeo, zona=zonaq, aeu_final=aeut)

    print "Esta la impresora elegida de opcion: "+ str(opc)
    tempprinter = " "
    if opc == 1:
        "Entro a la impresora blanca"
        tempprinter = "\\\\172.18.1.35\\192.168.230.16"
    else:
        print "Entro a la impresora negra"
        tempprinter = "\\\\172.18.1.35\\192.168.230.20"

    print tempprinter
    currentprinter = win32print.GetDefaultPrinter()


    # print "Aqui esta el nombre: " + str(ubig) + name
    source_file_name = "\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubig) + "\\" + str(zon) + "\\" + str(name)
    print source_file_name
    # \\\srv - fileserver\\CPV2017\\list_segm_esp\\" + str(ubigeo) + "\\" + zonal + "\\" + str(ubigeo) + zonal + str(secc) + str(aeu_conv) + ".pdf"

    win32print.SetDefaultPrinter(tempprinter)

    win32api.ShellExecute(0, "print", source_file_name, None, ".", 0)
    win32print.SetDefaultPrinter(currentprinter)


    return HttpResponse(lista)



    # # tempprinter = "\\\\server01\\printer01"
    # # tempprinter = "\\\\172.18.1.35\\192.168.230.68"
    # tempprinter = "\\\\172.18.1.35\\192.168.230.16"
    # currentprinter = win32print.GetDefaultPrinter()
    # source_file_name = "C:/Users/acarrillo/Desktop/pap.pdf"
    # win32print.SetDefaultPrinter(tempprinter)
    # win32api.ShellExecute(0, "print", source_file_name, None, ".", 0)
    # win32print.SetDefaultPrinter(currentprinter)
