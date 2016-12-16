# listton =[]
#
# for i in range (54):
#     listton.append(i)
#
# print listton[0:30]
#
# print listton[30:]
# print listton

from django.http import HttpResponse
import string
from PyPDF2 import PdfFileWriter, PdfFileReader
import PyPDF2
#
# def prueba(request):
#
#     #even = PdfFileReader(open('even.pdf', 'rb'))
#     pdf_file = PdfFileReader(open('sample2.pdf','rb'))
#
#
#     number_of_pages = pdf_file.getNumPages()
#     return HttpResponse(number_of_pages)


#
# def prueba(request):
#
#     data = "carrillo rosales anthony"
#     info = (data[:10] + '..') if len(data) > 10 else data
#
#     print info
#
#     return HttpResponse(info)

def prueba(request):

    #data = "carrillo rosales anthony"
    data = "PF de: NOLASCOZ ANTONIO WAITA GRASA"
    data = list(data)
    #info = (data[:10] + '..') if len(data) > 10 else data

    # cadena.find('ha')

    x = 0

    if len(data)>30:
        for i in range( -1, len(data)):
            pos = "i: "+ data[-i]
            print pos
            if data[-i]==" ":
                # new_data = string.replace(data," ", "\n")
                data[-i]='\n'
                #data = data.replace(" ", "\n")
                break
        # if data.find(' ')>=0:
        #     print 'Existe caracter'
        # else:
        #     print 'No existe nada'

        print ''.join(data)
        #print info
    else:
        data = data
        print ''.join(data)

    return HttpResponse(data)

