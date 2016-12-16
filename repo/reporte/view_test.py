import os.path

# f = Path('../Zonas/Anthony.pdf')
# if f.exists():
#     print "Existe!!!!!"


from PyPDF2 import PdfFileMerger, PdfFileReader
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate

from pyPdf import PdfFileWriter, PdfFileReader
# from .views import generar_pdf
# from .views_croquis import generar_croq
# from .reportes_models import *
from urllib2 import Request, urlopen
from StringIO import StringIO
from unipath import Path

#from reporte.reportes_models import *

from reportes_models import *

def append_pdf(input, output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

    # zona_conv = str(zona_t + 1).zfill(3) + "00"
    # lista.append(zona_t + 1)

#A = Path('../Zonas/' + str('020601') + '00100' + '.pdf')
#B = Path('../Croquis2/' + str('020601') + '00100'+ '.pdf')
#
#
#if Path(A, B):
#    print "Existen los dos archivos"
#    output = PdfFileWriter()
#
#    ## Aniadimos los reportes, estos podemos cargarlos desde archivos temporales
#    append_pdf(PdfFileReader(file("../Croquis2/" + '020601' + '00100' + ".pdf", "rb")), output)
#    append_pdf(PdfFileReader(file("../Zonas/" + '020601' + '00100' + ".pdf", "rb")), output)
#
#
#    # Escribimos la Salida Final del Reporte
#    a = output.write(file("CR/" + str('020601') + '00100' + ".pdf", "wb"))
#    print 'exito'
#else:
#    print "no hay igualdas"
# Nivel de zonas
def unir_zonas(request):
    # A = Path('../Zonas/'+str(ubig)+'.pdf')
    # B = Path('../Croquis2/'+str(ubig)+'.pdf')
    msg = ''

    totales = 10
    lista = []
    c = 0

    lista_distrito = []

    #lista_distrito.append('090301')
    #lista_distrito.append('090208')
    # lista_distrito.append('050619')
    #lista_distrito.append('050617')
    lista_distrito.append('050601')
    #lista_distrito.append('030602')
    #lista_distrito.append('022001')
    #lista_distrito.append('021509')



    tam_dist = 1
    for ubigeos in range(tam_dist):
        total_zonas = int(str(Esp_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos]).values_list('zona', flat=True).distinct().count()))
        for zona_t in range(total_zonas):
            zona_conv = str(zona_t + 1).zfill(3) + "00"
            lista.append(zona_t + 1)

            A = Path('../Zonas/'+str(lista_distrito[ubigeos])+zona_conv +'.pdf')
            B = Path('../Croquis2/'+str(lista_distrito[ubigeos])+zona_conv+'.pdf')


            if Path(A, B):
                print "Existen los dos archivos"
                output = PdfFileWriter()
                ## Aniadimos los reportes, estos podemos cargarlos desde archivos temporales
                append_pdf(PdfFileReader(file("Croquis2/" + str(lista_distrito[ubigeos]) + zona_conv + ".pdf", "rb")), output)
                append_pdf(PdfFileReader(file("Zonas/"+str(lista_distrito[ubigeos])+zona_conv +".pdf", "rb")), output)

                # Escribimos la Salida Final del Reporte
                a = output.write(file("CR/"+str(lista_distrito[ubigeos])+zona_conv +".pdf", "wb"))
                msg='exito'
            else:
                msg= "no hay igualdas"

    return HttpResponse(lista)

def unir_secciones(request):
    # A = Path('../Zonas/'+str(ubig)+'.pdf')
    # B = Path('../Croquis2/'+str(ubig)+'.pdf')
    msg = ''

    totales = 10
    lista = []
    c = 0

    lista_distrito = []

    # lista_distrito.append('090301')
    # lista_distrito.append('090208')
    # # lista_distrito.append('050619')
    # lista_distrito.append('050617')
    #lista_distrito.append('021509')
    lista_distrito.append('050601')
    # lista_distrito.append('030602')
    # lista_distrito.append('050601')

    #021509
    #050601 00100 001 001
    #050601 00100 002 1
    tam_dist = 1
    for ubigeos in range(tam_dist):
        total_zonas = int(str(Esp_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos]).values_list('zona', flat=True).distinct().count()))
        for zona_t in range(total_zonas):
            zoner = str(zona_t + 1).zfill(3) + "00"
            total_seccion_zona = int(str(Esp_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos], zona=zoner).values_list('seccion',flat=True).distinct().count()))
            for seccion in range(total_seccion_zona):
                    lista.append(zona_t + 1)
                    cond = Esp_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos], zona=zoner, aeu_final=seccion+1)
                    secc_conv = str(seccion+1).zfill(3)



                    A = Path('../Secciones/' + str(lista_distrito[ubigeos]) + zoner + str(secc_conv)+'.pdf')
                    B = Path('../Croquis2/' + str(lista_distrito[ubigeos]) + zoner + str(secc_conv )+'.pdf')

                    if Path(A, B):
                        print "Existen los dos archivos"
                        output = PdfFileWriter()
                        ## Aniadimos los reportes, estos podemos cargarlos desde archivos temporales
                        append_pdf(PdfFileReader(file("Croquis2/" + str(lista_distrito[ubigeos]) + zoner + str(secc_conv)+".pdf", "rb")),output)
                        append_pdf(PdfFileReader(file("Secciones/" + str(lista_distrito[ubigeos]) + zoner + str(secc_conv)+".pdf", "rb")), output)

                        # Escribimos la Salida Final del Reporte
                        a = output.write(file("CR/" + str(lista_distrito[ubigeos]) + zoner + str(secc_conv)+".pdf", "wb"))
                        msg = 'exito'
                    else:
                        msg = "no hay igualdas"

    return HttpResponse(lista)


def unir_aes(request):
    # A = Path('../Zonas/'+str(ubig)+'.pdf')
    # B = Path('../Croquis2/'+str(ubig)+'.pdf')
    msg = ''

    totales = 10
    lista = []
    c = 0

    lista_distrito = []

    # lista_distrito.append('090301')
    # lista_distrito.append('090208')
    # # lista_distrito.append('050619')
    # lista_distrito.append('050617')
    lista_distrito.append('021509')
    lista_distrito.append('030602')
    lista_distrito.append('022001')
    lista_distrito.append('021509')


    for ubigeos in lista_distrito:
        total_zonas_ubigeo = int(str(Esp_Aeus.objects.filter(ubigeo=ubigeos).values_list('zona', flat=True).distinct().count()))
        for zona_t in range(total_zonas_ubigeo):
            zona_conv = str(zona_t + 1).zfill(3) + "00"
            total_aes_zona = int(str(Esp_Aeus.objects.filter(ubigeo=ubigeos, zona=zona_conv).values_list('aeu_final', flat=True).distinct().count()))
            for aeu in range(total_aes_zona):
                lista.append(zona_t + 1)
                cond = Esp_Aeus.objects.filter(ubigeo=ubigeos, zona=zona_conv, aeu_final=aeu+1)
                for aeutes in cond:

                    secc_conv = str(aeutes.seccion).zfill(3)
                    A = Path('../Lista/' + str(ubigeos) + zona_conv + str(secc_conv)+str(aeutes.aeu_final)+'.pdf')
                    B = Path('../Croquis2/' + str(ubigeos) + zona_conv + str(secc_conv )+str(aeutes.aeu_final)+'.pdf')

                    if Path(A, B):
                        print "Existen los dos archivos"
                        output = PdfFileWriter()
                        ## Aniadimos los reportes, estos podemos cargarlos desde archivos temporales
                        append_pdf(PdfFileReader(file("Croquis2/" + str(ubigeos) + zona_conv + str(secc_conv)+str(aeutes.aeu_final)+".pdf", "rb")),output)
                        append_pdf(PdfFileReader(file("Lista/" + str(ubigeos) + zona_conv + str(secc_conv)+str(aeutes.aeu_final)+".pdf", "rb")), output)

                        # Escribimos la Salida Final del Reporte
                        a = output.write(file("CR/" + str(ubigeos) + zona_conv + str(secc_conv)+str(aeutes.aeu_final)+".pdf", "wb"))
                        msg = 'exito'
                    else:
                        msg = "no hay igualdas"

    return HttpResponse(lista)

def unir_aes_tab(request):
    # A = Path('../Zonas/'+str(ubig)+'.pdf')
    # B = Path('../Croquis2/'+str(ubig)+'.pdf')
    msg = ''
    lista = []
    lista_totales = []
    lista_distrito = []

    #lista_distrito.append('020601')
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
    # lista_distrito.append('080205')
    # lista_distrito.append('080206')

    # lista_distrito.append('080207')
    # lista_distrito.append('080402')
    # lista_distrito.append('080407')
    # lista_distrito.append('090203')
    # lista_distrito.append('090208')

    # lista_distrito.append('090301')
    ##lista_distrito.append('110107')
    # lista_distrito.append('110204')
    ##lista_distrito.append('120201')
    #
    # lista_distrito.append('120501')
    # lista_distrito.append('120708')
    # lista_distrito.append('130202')
    # lista_distrito.append('131203')
    ##lista_distrito.append('130701')
    ##lista_distrito.append('130705')
    # lista_distrito.append('131203')
    # lista_distrito.append('140107')
    #
    # lista_distrito.append('150508')
    # lista_distrito.append('150604')
    lista_distrito.append('150116')
    # lista_distrito.append('150705')
    # lista_distrito.append('170102')
    # lista_distrito.append('180106')
    # lista_distrito.append('180208')
    #
    # lista_distrito.append('180210')
    # lista_distrito.append('190111')
    # lista_distrito.append('180210')

    # lista_distrito.append('210407')
    # lista_distrito.append('230106')
    # lista_distrito.append('230109')
    # lista_distrito.append('240103')
    # lista_distrito.append('240105')
    # lista_distrito.append('240106')


    # lista_distritos = []
    # lista_distrito.append('150116')
    listin = []

    for ubigein in lista_distrito:

        if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein)) == False:
            os.mkdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein))

        total_zonas = Tab_Aeus.objects.filter(ubigeo=str(ubigein)).values_list('zona', flat=True)

        for zona_totales in total_zonas:

            listin.append(str(ubigein) + ": " + str(zona_totales) + "<br/>")
            if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein) + "\\" + str(zona_totales)) == False:
                os.mkdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein) + "\\" + str(zona_totales))


    for ubigeos in lista_distrito:
        total_zonas_ubigeo = Tab_Aeus.objects.filter(ubigeo=ubigeos, zona = '00100').values_list('zona',flat=True)
        cuchi_zona = list(set(total_zonas_ubigeo))
        for zona_t in cuchi_zona:

            total_aes_zona = Tab_Aeus.objects.filter(ubigeo=ubigeos, zona=zona_t).values_list('aeu_final',flat=True)
            cuchi_aeu = list(set(total_aes_zona))
            for aeu in cuchi_aeu:
                lista.append(zona_t)
                cond = Tab_Aeus.objects.filter(ubigeo=ubigeos, zona=zona_t, aeu_final=aeu)
                for aeutes in cond:
                    secc_conv = str(aeutes.seccion).zfill(3)
                    aeu_conv = str(aeutes.aeu_final).zfill(3)
                    A = Path("\\\srv-fileserver\\CPV2017\\list_segm_tab\\"+str(ubigeos)+"\\" +str(zona_t)+"\\" + str(ubigeos) + str(zona_t)+ str(secc_conv) + aeu_conv + '.pdf')

                    B = Path("\\\srv-fileserver\\CPV2017\\croquis_segm_tab\\urbano\\"+str(ubigeos)+"\\"+str(zona_t) +"\\" + str(ubigeos) + str(zona_t) + str(secc_conv) + aeu_conv + '.pdf')

                    if Path(A, B):
                        print "Se va a generar el PDF con Ubigeo: "+ str(ubigeos)+ " con la zona: "+ str(zona_t)+ "y con el AE: "+ str(aeu)
                        output = PdfFileWriter()

                        ## Aniadimos los reportes, estos podemos cargarlos desde archivos temporales
                        #append_pdf(PdfFileReader(file("srv-fileserver/CPV2017/croquis_segm_tab/urbano/"+lista_distrito[ubigeos]+"/"+zona_conv+"/"+ str(lista_distrito[ubigeos]) + zona_conv + str(secc_conv) + str(aeutes.aeu_final) + ".pdf", "rb")), output)
                        append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/croquis_segm_tab/urbano/"+str(ubigeos)+"/"+str(zona_t)+"/"+ str(ubigeos) + str(zona_t) + str(secc_conv) + aeu_conv + ".pdf", "rb")), output)

                        # print "Encontro el archivo en el servidor"
                        append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/list_segm_tab/"+ str(ubigeos)+"/"+str(zona_t)+"/"+ str(ubigeos) + str(zona_t) + str(secc_conv) + aeu_conv + ".pdf", "rb")), output)
                        lista_totales.append(str(ubigeos) + " ," + str(zona_t) + ", " + str(secc_conv) + ", " + str(aeutes.aeu_final) + "<br/>")

                        # # Escribimos la Salida Final del Reporte
                        a = output.write(file("//srv-fileserver/CPV2017/segm_tab/urbano/"+str(ubigeos)+"/"+str(zona_t)+"/" + str(ubigeos) + str(zona_t) + str(secc_conv) + aeu_conv + ".pdf", "wb"))
                        # msg = 'exito'
                    else:
                        msg = "no hay igualdas"
    return HttpResponse(lista_totales)

def unir_secciones_tab(request):
    # A = Path('../Zonas/'+str(ubig)+'.pdf')
    # B = Path('../Croquis2/'+str(ubig)+'.pdf')
    msg = ''
    totales = 10
    lista = []
    lista_totales = []
    c = 0
    lista_distrito = []

    # lista_distrito.append('020601')
    # lista_distrito.append('021509')
    # lista_distrito.append('021806')
    # lista_distrito.append('022001')
    # lista_distrito.append('030212')
    # lista_distrito.append('030602')
    # lista_distrito.append('050507')
    # lista_distrito.append('050601')
    #
    # lista_distrito.append('050617')
    # lista_distrito.append('060903')
    # lista_distrito.append('080301')
    # lista_distrito.append('080205')
    # lista_distrito.append('080206')
    #
    # lista_distrito.append('080207')
    # lista_distrito.append('080402')
    # lista_distrito.append('080407')
    # lista_distrito.append('090203')
    # lista_distrito.append('090208')
    #
    # lista_distrito.append('090301')
    # lista_distrito.append('110107')
    # lista_distrito.append('110204')
    # lista_distrito.append('120201')
    #
    # lista_distrito.append('120501')
    # lista_distrito.append('120708')
    # lista_distrito.append('130202')
    # lista_distrito.append('131203')
    #
    # lista_distrito.append('130701')
    # lista_distrito.append('130705')
    # lista_distrito.append('131203')
    # lista_distrito.append('140107')
    #
    # lista_distrito.append('150508')
    # lista_distrito.append('150604')
    lista_distrito.append('150116')
    # lista_distrito.append('150705')
    # lista_distrito.append('170102')
    # lista_distrito.append('180106')

    #lista_distrito.append('180208')
    # lista_distrito.append('180210')
    # lista_distrito.append('190111')
    #lista_distrito.append('180210')
    #lista_distrito.append('210407')
    #lista_distrito.append('230106')
    #lista_distrito.append('230109')
    #lista_distrito.append('240103')
    #lista_distrito.append('240105')
    #lista_distrito.append('240106')
    # lista_distrito.append('150116')

    listin = []

    for ubigein in lista_distrito:
        if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein)) == False:
            os.mkdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein))
        total_zonas = int(str(Tab_Aeus.objects.filter(ubigeo=ubigein).values_list('zona',flat=True).distinct().count()))
        for zona_totales in range(total_zonas):
            zoner = str(zona_totales + 1).zfill(3) + "00"
            listin.append(str(ubigein) + ": " + zoner + "<br/>")
            if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein) + "\\" + zoner) == False:
                os.mkdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein) + "\\" + zoner)

    for ubigeos in lista_distrito:
        total_zonas_ubigeo = Tab_Aeus.objects.filter(ubigeo=ubigeos).values_list('zona',flat=True)
        zona_dif = list(set(total_zonas_ubigeo))
        for zona_t in zona_dif:
            total_secc_zona = Tab_Aeus.objects.filter(ubigeo=ubigeos, zona=zona_t).values_list('seccion',flat=True)
            secc_dif = list(set(total_secc_zona))
            for secc in secc_dif:
                lista.append(zona_t)
                # for aeutes in cond:
                secc_conv = str(secc).zfill(3)
                A = Path("\\\srv-fileserver\\CPV2017\\list_segm_tab\\" + str(ubigeos) + "\\" + str(zona_t) + "\\" + str(ubigeos) + str(zona_t) + str(secc_conv) + '.pdf')
                B = Path("\\\srv-fileserver\\CPV2017\\croquis_segm_tab\\urbano\\" + str(ubigeos) + "\\" + str(zona_t) + "\\" + str(ubigeos) + str(zona_t) + str(secc_conv) +'.pdf')
                if Path(A, B):
                    print "Se va a generar el PDF de Ubigeo: "+ str(ubigeos) + " de zona: "+ str(zona_t)+ " y de Seccion: "+str(secc_conv)
                    output = PdfFileWriter()
                    # Aniadimos los reportes, estos podemos cargarlos desde archivos temporales

                    append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/croquis_segm_tab/urbano/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + str(secc_conv) + ".pdf","rb")), output)

                    append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/list_segm_tab/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + str(secc_conv) + ".pdf","rb")), output)
                    lista_totales.append(str(ubigeos) + " ," + str(zona_t) + ", " + str(secc_conv) + "<br/>")
                    # # # Escribimos la Salida Final del Reporte
                    a = output.write(file("//srv-fileserver/CPV2017/segm_tab/urbano/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + str(secc_conv) + ".pdf","wb"))
                    # msg = 'exito'
                else:
                    msg = "no hay igualdas"
    return HttpResponse(lista_totales)

def unir_zona_tab(request):
    # A = Path('../Zonas/'+str(ubig)+'.pdf')
    # B = Path('../Croquis2/'+str(ubig)+'.pdf')
    msg = ''

    lista_totales = []

    lista_distrito = []
    # lista_distrito.append('020601')
    # lista_distrito.append('021509')
    ## lista_distrito.append('021806')
    lista_distrito.append('022001')
    # lista_distrito.append('030212')
    # lista_distrito.append('030602')
    # lista_distrito.append('050507')
    # lista_distrito.append('050601')
    # lista_distrito.append('050617')
    # lista_distrito.append('060903')

    ##lista_distrito.append('080301')
    # lista_distrito.append('080205')
    # lista_distrito.append('080206')
    # lista_distrito.append('080207')
    # lista_distrito.append('080402')
    # lista_distrito.append('080407')
    # lista_distrito.append('090203')

    #
    # lista_distrito.append('090208')
    # lista_distrito.append('090301')
    #
    # lista_distrito.append('110107')
    # lista_distrito.append('110204')
    # lista_distrito.append('120201')
    #
    # lista_distrito.append('120501')
    # lista_distrito.append('120708')
    # lista_distrito.append('130202')
    # lista_distrito.append('131203')
    #
    # lista_distrito.append('130701')
    # lista_distrito.append('130705')
    # lista_distrito.append('131203')
    # lista_distrito.append('140107')
    # lista_distrito.append('150116')
    # lista_distrito.append('150508')
    ##lista_distrito.append('150604')
    # lista_distrito.append('150705')
    ##lista_distrito.append('170102')
    # lista_distrito.append('180106')

    # lista_distrito.append('180208')
    # lista_distrito.append('180210')
    ##lista_distrito.append('190111')
    # lista_distrito.append('180210')
    ## lista_distrito.append('210407')
    # lista_distrito.append('230106')
    # lista_distrito.append('230109')
    # lista_distrito.append('240103')
    # lista_distrito.append('240105')

    listin = []
    tam_distrito = 1
    for ubigein in lista_distrito:

        if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein)) == False:
            os.mkdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein))
        total_zonas = Tab_Aeus.objects.filter(ubigeo=ubigein).values_list('zona',flat=True)

        for zona_totales in total_zonas:
            # zoner = str(zona_totales).zfill(3) + "00"
            listin.append(str(ubigein) + ": " + str(zona_totales) + "<br/>")
            if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein) + "\\" + str(zona_totales)) == False:
                os.mkdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein) + "\\" + str(zona_totales))

    for ubigeos in lista_distrito:
        total_zonas_ubigeo = Tab_Aeus.objects.filter(ubigeo=ubigeos).values_list('zona',flat=True)
        zona_dif = list(set(total_zonas_ubigeo))
        for zona_t in zona_dif:

            # total_aes_zona = int(str(Tab_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos], zona=zona_conv).values_list('aeu_final',flat=True).distinct().count()))
            # total_secc_zona = int(Tab_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos], zona=zona_conv).values_list('seccion',flat=True).distinct().count())

            #lista.append(zona_t + 1)
            # cond = Tab_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos], zona=zona_conv, aeu_final=aeu + 1)
            # for aeutes in cond:
            #secc_conv = str(aeu + 1).zfill(3)
            A = Path("\\\srv-fileserver\\CPV2017\\list_segm_tab\\" + str(ubigeos) + "\\" + str(zona_t) + "\\" + str(ubigeos) + str(zona_t) + '.pdf')
            B = Path("\\\srv-fileserver\\CPV2017\\croquis_segm_tab\\urbano\\" + str(ubigeos) + "\\" + str(zona_t) + "\\" + str(ubigeos) + str(zona_t) + '.pdf')
            if Path(A, B):
                print "Se Creo el PDF de Ubigeo: "+str(ubigeos)+" de Zona: "+ str(zona_t)
                output = PdfFileWriter()
                # Aniadimos los reportes, estos podemos cargarlos desde archivos temporales
                # append_pdf(PdfFileReader(file("srv-fileserver/CPV2017/croquis_segm_tab/urbano/"+lista_distrito[ubigeos]+"/"+zona_conv+"/"+ str(lista_distrito[ubigeos]) + zona_conv + str(secc_conv) + str(aeutes.aeu_final) + ".pdf", "rb")), output)
                append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/croquis_segm_tab/urbano/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + ".pdf", "rb")), output)
                #print "Encontro el archivo en el servidor"
                append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/list_segm_tab/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) +  ".pdf", "rb")), output)
                lista_totales.append(str(ubigeos) + " ," + str(zona_t) + ", "  + "<br/>")
                # # Escribimos la Salida Final del Reporte
                a = output.write(file("//srv-fileserver/CPV2017/segm_tab/urbano/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + ".pdf", "wb"))
                # msg = 'exito'
            else:
                msg = "no hay igualdas"
    return HttpResponse(lista_totales)

def unir_aes_esp(request):
    # A = Path('../Zonas/'+str(ubig)+'.pdf')
    # B = Path('../Croquis2/'+str(ubig)+'.pdf')
    msg = ''
    lista = []
    lista_totales = []

    lista_distrito = []
    #lista_distrito.append('020601')
    #lista_distrito.append('021509')
    # lista_distrito.append('021806')
    # lista_distrito.append('022001')
    # lista_distrito.append('030212')
    # lista_distrito.append('030602')
    #lista_distrito.append('050507')
    #lista_distrito.append('050601')
    #lista_distrito.append('050617')
    #lista_distrito.append('060903')
    #lista_distrito.append('080301')
    #lista_distrito.append('080205')
    #lista_distrito.append('080206')
    #lista_distrito.append('080207')
    #lista_distrito.append('080402')
    #lista_distrito.append('080407')
    #lista_distrito.append('090203')
    #lista_distrito.append('090208')
    #lista_distrito.append('090301')
    #lista_distrito.append('110107')
    #lista_distrito.append('110204')
    #lista_distrito.append('120201')
    ##
    # lista_distrito.append('120501')
    # lista_distrito.append('120708')
    # lista_distrito.append('130202')
    # lista_distrito.append('131203')
    # lista_distrito.append('130701')
    # lista_distrito.append('130705')
    # lista_distrito.append('131203')
    # lista_distrito.append('140107')
    # lista_distrito.append('150108')
    lista_distrito.append('150133')
    # lista_distrito.append('150508')
    # lista_distrito.append('150604')
    # lista_distrito.append('150705')
    # lista_distrito.append('170102')
    # lista_distrito.append('180106')
    # lista_distrito.append('180208')
#
    # lista_distrito.append('180210')
    # lista_distrito.append('190111')
    # lista_distrito.append('180210')
    # lista_distrito.append('210407')
    # lista_distrito.append('230106')
    # lista_distrito.append('230109')
    # lista_distrito.append('240103')
    # lista_distrito.append('240105')
    # lista_distrito.append('240106')
    # lista_distritos = []
    # lista_distritos.append('021509')

    listin = []


    for ubigein in lista_distrito:
        if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_esp\\urbano\\" + str(ubigein)) == False:
            os.mkdir("\\\srv-fileserver\\CPV2017\\segm_esp\\urbano\\" + str(ubigein))
        total_zonas = Esp_Aeus.objects.filter(ubigeo= ubigein).values_list('zona',flat=True)
        cuchi_zona = list(set(total_zonas))
        for zona_totales in cuchi_zona:

            listin.append(str(ubigein) + ": " + str(zona_totales) + "<br/>")
            if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_esp\\urbano\\" + str(ubigein) + "\\" + str(zona_totales)) == False:
                os.mkdir("\\\srv-fileserver\\CPV2017\\segm_esp\\urbano\\" +  str(ubigein) + "\\" + str(zona_totales))

    for ubigeos in lista_distrito:
        total_zonas_ubigeo = Esp_Aeus.objects.filter(ubigeo= ubigeos).values_list('zona',flat=True)
        zona_dif = list(set(total_zonas_ubigeo))
        for zona_t in zona_dif:
            total_aes_zona = Esp_Aeus.objects.filter(ubigeo=ubigeos, zona=zona_t).values_list('aeu_final',flat=True)
            aes_zona = list(set(total_aes_zona))
            for aeu in aes_zona:
                lista.append(zona_t)
                cond = Esp_Aeus.objects.filter(ubigeo= ubigeos, zona=zona_t, aeu_final=aeu)
                for aeutes in cond:
                    secc_conv = str(aeutes.seccion).zfill(3)
                    aeu_conv = str(aeutes.aeu_final).zfill(3)
                    A = Path("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(ubigeos) + "\\" + str(zona_t) + "\\" +  str(ubigeos) + str(zona_t) + str(secc_conv) + str(aeu_conv) + '.pdf')

                    B = Path("\\\srv-fileserver\\CPV2017\\croquis_segm_esp\\urbano\\" + str(ubigeos) + "\\" + str(zona_t) + "\\" +  str(ubigeos) + str(zona_t) + str(secc_conv) + str(aeu_conv) + '.pdf')

                    if Path(A, B):
                        print "Se creo el PDF de Ubigeo: "+ str(ubigeos) + " de zona: "+ str(zona_t)+ " y AEU: "+str(aeu)
                        output = PdfFileWriter()
                        ## Aniadimos los reportes, estos podemos cargarlos desde archivos temporales

                        append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/croquis_segm_esp/urbano/" +  str(ubigeos) + "/" + str(zona_t) + "/" +  str(ubigeos) + str(zona_t) + str(secc_conv) + str(aeu_conv) + ".pdf","rb")), output)

                        #print "Encontro el archivo en el servidor"

                        append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/list_segm_esp/" +  str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + str(secc_conv) + str(aeu_conv) + ".pdf","rb")), output)
                        lista_totales.append(
                            str(ubigeos) + " ," + str(zona_t) + ", " + str(secc_conv) + ", " + str(aeutes.aeu_final) + "<br/>")
                        # # Escribimos la Salida Final del Reporte
                        a = output.write(file("//srv-fileserver/CPV2017/segm_esp/urbano/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + str(secc_conv) + str(aeu_conv) + ".pdf","wb"))
                    else:
                        msg = "no hay igualdas"
    return HttpResponse(lista_distrito)

def unir_secciones_esp(request):

    msg = ''

    lista = []
    lista_totales = []

    lista_distrito = []
    # lista_distrito.append('020601')
    # lista_distrito.append('021509')
    # lista_distrito.append('021806')
    # lista_distrito.append('022001')
    # lista_distrito.append('030212')
    # lista_distrito.append('030602')
    # lista_distrito.append('050507')
    # lista_distrito.append('050601')
    #
    # lista_distrito.append('050617')
    # lista_distrito.append('060903')
    # lista_distrito.append('080301')
    # lista_distrito.append('080205')
    # lista_distrito.append('080206')
    #
    # lista_distrito.append('080207')
    # lista_distrito.append('080402')
    # lista_distrito.append('080407')
    # lista_distrito.append('090203')
    # lista_distrito.append('090208')
    #
    # lista_distrito.append('090301')
    # lista_distrito.append('110107')
    # lista_distrito.append('110204')
    # lista_distrito.append('120201')
    #
    # lista_distrito.append('120501')
    # lista_distrito.append('120708')
    # lista_distrito.append('130202')
    # lista_distrito.append('131203')
    #
    # lista_distrito.append('130701')
    # lista_distrito.append('130705')
    # lista_distrito.append('131203')
    # lista_distrito.append('140107')
    #
    lista_distrito.append('150116')
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
    # lista_distrito.append('230106')
    # lista_distrito.append('230109')
    # lista_distrito.append('240103')
    # lista_distrito.append('240105')
    # lista_distrito.append('150116')
    listin = []


    for ubigein in lista_distrito:
        if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_esp\\urbano\\" + str(ubigein)) == False:
            os.mkdir("\\\srv-fileserver\\CPV2017\\segm_esp\\urbano\\" + str(ubigein))

        total_zonas = Esp_Aeus.objects.filter(ubigeo=ubigein).values_list('zona',flat=True)

        for zona_totales in total_zonas:

            listin.append(str(ubigein) + ": " + str(zona_totales) + "<br/>")
            if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_esp\\urbano\\" + str(ubigein) + "\\" + str(zona_totales)) == False:
                os.mkdir("\\\srv-fileserver\\CPV2017\\segm_esp\\urbano\\" + str(ubigein) + "\\" + str(zona_totales))

    for ubigeos in lista_distrito:
        total_zonas_ubigeo = Esp_Aeus.objects.filter(ubigeo=ubigeos).values_list('zona',flat=True)
        zona_dif = list(set(total_zonas_ubigeo))
        for zona_t in zona_dif:

            # total_aes_zona = int(str(Tab_Aeus.objects.filter(ubigeo=lista_distrito[ubigeos], zona=zona_conv).values_list('aeu_final',flat=True).distinct().count()))
            total_secc_zona = Esp_Aeus.objects.filter(ubigeo=ubigeos, zona=zona_t).values_list('seccion',flat=True)
            secc_dif = list(set(total_secc_zona))
            for aeu in secc_dif:
                lista.append(zona_t)

                # for aeutes in cond:
                secc_conv = str(aeu).zfill(3)
                A = Path("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(ubigeos) + "\\" + str(zona_t) + "\\" + str(ubigeos) + str(zona_t) + str(secc_conv) + '.pdf')
                B = Path("\\\srv-fileserver\\CPV2017\\croquis_segm_esp\\urbano\\" + str(ubigeos) + "\\" + str(zona_t) + "\\" + str(ubigeos) + str(zona_t) + str(secc_conv) + '.pdf')

                if Path(A, B):
                    print "Se va a crear el PDF de Ubigeo: "+ str(ubigeos) + " de zona: "+ str(zona_t)+ " y de AE: "+ str(aeu)
                    output = PdfFileWriter()
                    # Aniadimos los reportes, estos podemos cargarlos desde archivos temporales

                    append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/croquis_segm_esp/urbano/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + str(secc_conv) + ".pdf", "rb")), output)

                    append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/list_segm_esp/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + str(secc_conv) + ".pdf", "rb")), output)
                    lista_totales.append(str(ubigeos) + " ," + str(zona_t) + ", " + str(secc_conv) + "<br/>")
                    # # Escribimos la Salida Final del Reporte
                    a = output.write(file("//srv-fileserver/CPV2017/segm_esp/urbano/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + str(secc_conv) + ".pdf", "wb"))
                    # msg = 'exito'
                else:
                    msg = "no hay igualdas"
    return HttpResponse(lista_totales)

def unir_zona_esp(request):
    # A = Path('../Zonas/'+str(ubig)+'.pdf')
    # B = Path('../Croquis2/'+str(ubig)+'.pdf')
    msg = ''

    lista_totales = []
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
    # lista_distrito.append('080205')
    ## lista_distrito.append('080206')
    ## lista_distrito.append('080207')
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
    # lista_distrito.append('130202')
    # lista_distrito.append('131203')
    #
    #lista_distrito.append('130701')
    #lista_distrito.append('130705')
    #lista_distrito.append('131203')
    #lista_distrito.append('140107')
#
    lista_distrito.append('150108')
    #lista_distrito.append('150508')
    #lista_distrito.append('150604')
    #lista_distrito.append('150705')
    #lista_distrito.append('170102')
    #lista_distrito.append('180106')
    #lista_distrito.append('180208')
    #lista_distrito.append('180210')
    # lista_distrito.append('190111')
    #lista_distrito.append('180210')
    #lista_distrito.append('210407')
    #lista_distrito.append('230106')
    #lista_distrito.append('230109')
    #lista_distrito.append('240103')
    #lista_distrito.append('240105')
    #lista_distrito.append('240106')
    listin = []

    for ubigein in lista_distrito:
        if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_esp\\urbano\\" + str(ubigein)) == False:
            os.mkdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein))

        total_zonas = Esp_Aeus.objects.filter(ubigeo=ubigein).values_list('zona',flat=True)

        for zona_totales in total_zonas:

            listin.append(str(ubigein) + ": " + str(zona_totales) + "<br/>")
            if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_esp\\urbano\\" + str(ubigein) + "\\" + str(zona_totales)) == False:
                os.mkdir("\\\srv-fileserver\\CPV2017\\segm_tab\\urbano\\" + str(ubigein) + "\\" + str(zona_totales))

    for ubigeos in lista_distrito:
        total_zonas_ubigeo = Esp_Aeus.objects.filter(ubigeo=ubigeos).values_list('zona',flat=True)
        zonas_dif = list(set(total_zonas_ubigeo))

        for zona_t in zonas_dif:

            A = Path("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(ubigeos) + "\\" + str(zona_t) + "\\" + str(ubigeos) + str(zona_t) + '.pdf')
            B = Path("\\\srv-fileserver\\CPV2017\\croquis_segm_esp\\urbano\\" + str(ubigeos) + "\\" + str(zona_t) + "\\" + str(ubigeos) + str(zona_t) + '.pdf')
            if Path(A, B):
                print "Se genero el merge de Ubigeo: "+ ubigeos + " de Zona: "+ str(zona_t)
                output = PdfFileWriter()
                # Aniadimos los reportes, estos podemos cargarlos desde archivos temporales
                # append_pdf(PdfFileReader(file("srv-fileserver/CPV2017/croquis_segm_tab/urbano/"+lista_distrito[ubigeos]+"/"+zona_conv+"/"+ str(lista_distrito[ubigeos]) + zona_conv + str(secc_conv) + str(aeutes.aeu_final) + ".pdf", "rb")), output)
                append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/croquis_segm_esp/urbano/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + ".pdf", "rb")), output)
                #print "Encontro el archivo en el servidor"
                append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/list_segm_esp/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + ".pdf", "rb")), output)
                lista_totales.append(str(ubigeos) + " ," + str(zona_t) + ", " + "<br/>")
                # # Escribimos la Salida Final del Reporte
                a = output.write(file("//srv-fileserver/CPV2017/segm_esp/urbano/" + str(ubigeos) + "/" + str(zona_t) + "/" + str(ubigeos) + str(zona_t) + ".pdf", "wb"))
                # msg = 'exito'
            else:
                msg = "no hay igualdas"
    return HttpResponse(lista_totales)

def unir_ae_rur_simple(request):

    lista_distrito =[]
    ubigeosa = os.listdir("\\\srv-fileserver\\CPV2017\\croquis_segm_esp\\rural")
    lista_distrito.append('110104')

    for ubigein in ubigeosa:
        if os.path.exists("\\\srv-fileserver\\CPV2017\\segm_esp\\rural\\" + str(ubigein)) == False:
            os.mkdir("\\\srv-fileserver\\CPV2017\\segm_esp\\rural\\" + str(ubigein))


    for ubigeos in ubigeosa:

        lista_listado = os.listdir("\\\srv-fileserver\\CPV2017\\list_seg_esp_rur\\" + str(ubigeos))
        lista_croquis = os.listdir("\\\srv-fileserver\\CPV2017\\croquis_segm_esp\\rural\\" + str(ubigeos))

        for croquis in lista_croquis:

            if (croquis.split("."))[1] == "pdf":

                pdf_croquis = croquis
                pdf_listado_index = lista_listado.index(croquis)
                pdf_listado = lista_listado[pdf_listado_index]

                print pdf_croquis, pdf_listado

                output = PdfFileWriter()
                append_pdf(PdfFileReader(
                    file("//srv-fileserver/CPV2017/croquis_segm_esp/rural/" + str(ubigeos) + "/" + str(pdf_croquis), "rb")),
                           output)
                append_pdf(PdfFileReader(
                    file("//srv-fileserver/CPV2017/list_seg_esp_rur/" + str(ubigeos) + "/" + str(pdf_listado), "rb")),
                           output)

                a = output.write(file("//srv-fileserver/CPV2017/segm_esp/rural/" + str(ubigeos) + "/" + str(pdf_listado), "wb"))
            else:
                continue

    return HttpResponse(lista_distrito)

#     for ubigeos in lista_distrito:
#
#         total_pdf_ubigeo = int(str(Seg_Esp_R_Aer.objects.filter(ubigeo=ubigeos, emp_aer=1).count()))
#         for pos in range(total_pdf_ubigeo):
#             rur = Seg_Esp_R_Aer.objects.filter(ubigeo=ubigeos, emp_aer=1).values_list('aer_ini_17', flat='true')
#
#             A = Path("\\\srv-fileserver\\CPV2017\\list_seg_esp_rur\\" + str(ubigeos) + "\\" + str(ubigeos)+ str(secc_conv) + str(aeutes.aeu_final) + '.pdf')
#
#             B = Path("\\\srv-fileserver\\CPV2017\\croquis_segm_esp\\rural\\" + str(ubigeos) + "\\" + str(ubigeos) + str(secc_conv) + str(aeutes.aeu_final) + '.pdf')
#
#             if Path(A, B):
#                 print "Existen los dos archivos"
#                 output = PdfFileWriter()
#                 ## Aniadimos los reportes, estos podemos cargarlos desde archivos temporales
#                 # append_pdf(PdfFileReader(file("srv-fileserver/CPV2017/croquis_segm_tab/urbano/"+lista_distrito[ubigeos]+"/"+zona_conv+"/"+ str(lista_distrito[ubigeos]) + zona_conv + str(secc_conv) + str(aeutes.aeu_final) + ".pdf", "rb")), output)
#                 append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/croquis_segm_esp/rural/" + str(ubigeos) + "/" + str(lista_distrito) + str(secc_conv) + str(aeutes.aeu_final) + ".pdf", "rb")), output)
#
#                 print "Encontro el archivo en el servidor"
#
#                 append_pdf(PdfFileReader(file("//srv-fileserver/CPV2017/list_seg_esp_rur/" + str(ubigeos) + "/" + str(ubigeos) + str(secc_conv) + str(aeutes.aeu_final) + ".pdf", "rb")), output)
#
#                 lista_totales.append(str(ubigeos) +  ", " + str(secc_conv) + ", " + str(aeutes.aeu_final) + "<br/>")
#                 # # Escribimos la Salida Final del Reporte
#                 a = output.write(file("//srv-fileserver/CPV2017/segm_esp/rural/" + str(ubigeos) + "/" + str(ubigeos)  + str(secc_conv) + str(aeutes.aeu_final) + ".pdf", "wb"))
#                 # msg = 'exito'
#             else:
#                 msg = "no hay igualdas"
#
#     return HttpResponse(lista_distrito)
# #
# output = PdfFileWriter()
#
# ## Aniadimos los reportes, estos podemos cargarlos desde archivos temporales
#
#
# append_pdf(PdfFileReader(file("Zonas/02060100100.pdf", "rb")), output)
# append_pdf(PdfFileReader(file("Croquis2/02060100100001.pdf", "rb")), output)
#
# # Escribimos la Salida Final del Reporte
# a = output.write(file("UnionFinalPDF.pdf", "wb"))
#
# return a