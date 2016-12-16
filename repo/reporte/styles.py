from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow
)

pdfmetrics.registerFont(TTFont('Roboto-Regular', "Fonts/Roboto-Regular.ttf"))
pdfmetrics.registerFont(TTFont('Roboto-Bold', "Fonts/Roboto-Bold.ttf"))


DOCUMENT_STYLE = {
                  'title': ParagraphStyle(
                                          'title',
                                          fontName='Roboto-Bold',
                                          fontSize=12,
                                          leading=12,
                                          leftIndent=0,
                                          rightIndent=0,
                                          firstLineIndent=0,
                                          alignment=TA_CENTER,
                                          spaceBefore=0,
                                          spaceAfter=0,
                                          bulletFontName='Roboto-Bold',
                                          bulletFontSize=10,
                                          bulletIndent=0,
                                          textColor= black,
                                          backColor=None,
                                          wordWrap=None,
                                          borderWidth= 0,
                                          borderPadding= 0,
                                          borderColor= None,
                                          borderRadius= None,
                                          allowWidows= 1,
                                          allowOrphans= 0,
                                          textTransform=None,  # 'uppercase' | 'lowercase' | None
                                          endDots=None,
                                          splitLongWords=1),
                  'subtitle': ParagraphStyle('subtitle',
                                             fontName='Roboto-Bold',
                                             fontSize=10,
                                             leading=12,
                                             leftIndent=0,
                                             rightIndent=0,
                                             firstLineIndent=0,
                                             alignment=TA_CENTER,
                                             spaceBefore=0,
                                             spaceAfter=0,
                                             bulletFontName='Roboto-Bold',
                                             bulletFontSize=10,
                                             bulletIndent=0,
                                             textColor= black,
                                             backColor=None,
                                             wordWrap=None,
                                             borderWidth= 0,
                                             borderPadding= 0,
                                             borderColor= None,
                                             borderRadius= None,
                                             allowWidows= 1,
                                             allowOrphans= 0,
                                             textTransform=None,  # 'uppercase' | 'lowercase' | None
                                             endDots=None,
                                             splitLongWords=1),
                  'normal': ParagraphStyle(
                                           'Normal',
                                           fontName='Roboto-Regular',
                                           fontSize=8,
                                           leading=12),
                  'text-bold': ParagraphStyle(
                                           'text-bold',
                                           fontName='Roboto-Bold',
                                           fontSize=8,
                                           leading=12),
                  'table-header': ParagraphStyle(
                                           'text-bold',
                                           fontName='Roboto-Bold',
                                           fontSize=7,
                                           leading=12),
                  'table-body': ParagraphStyle(
                                           'Normal',
                                           fontName='Roboto-Regular',
                                           fontSize=7,
                                           leading=12),
                  }
