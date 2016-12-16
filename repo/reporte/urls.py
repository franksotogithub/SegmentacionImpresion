from django.conf.urls import url
# from reporte import view_test
# from reporte import view_distrital
# from reporte import view_urbana
# from reporte import view_seccion
# from reporte import view_zona
# from reporte import view_union
import view_test
import view_distrital
import view_urbana
import view_seccion
import view_zona
import view_union
import views_tab
import view_seccion_tab
import view_zona_tab
import view_carpeta
import view_angular
import view_esp_rural
import view_esp_comp_rural
import view_esp_secc_rural
import view_esp_ae_distrito_rural
import view_imprimir
import view_prueba
from . import views
from . import views_croquis

urlpatterns = [
    # url(r'^$', views.hello_world, name='hello'),
    url(r'^obtener/(\d+)/$', views.generar_pdf),
    url(r'^obtenercroquis/(\d+)/(\d+)/$', views_croquis.generar_croq),
    url(r'^obtenertodo/(\d+)/$', view_union.union_pdf),
    url(r'^obtenerzona/(\d+)/$', view_zona.generar_seccion),
    url(r'^obtenerseccion/(\d+)/$', view_seccion.generar_seccion),
    url(r'^obter/$', views.generar_lote),  # Genera Reporte AEU Espaciales
    url(r'^obterseccion/$', view_seccion.generar_lote_seccion), # Genera Reporte Secciones Espaciales
    url(r'^obterzona/$', view_zona.generar_lote_zona),   # Genera Reporte Zonas Espaciales
    url(r'^obterurbano/(\d+)/$', view_urbana.generar_urbana),
    url(r'^obterdistrito/$', view_distrital.generar_distrito_lote),
    url(r'^obtermergeseccion/$', view_test.unir_secciones),
    url(r'^obtermergezonas/$', view_test.unir_zonas),
    url(r'^obteneraes/$', view_test.unir_aes),
    url(r'^mergepdf/$', view_test.unir_zonas),
    url(r'^obteraetab/$', views_tab.generar_lote),  # Genera Reporte AEU Tabulares
    url(r'^obtersecciontab/$', view_seccion_tab.generar_lote_seccion),   # Genera Reporte Secciones Tabulares
    url(r'^obterzonatab/$', view_zona_tab.generar_lote_zona),  # Genera Reporte Zonas Tabulares
    url(r'^obtenermergeaesesp/$', view_test.unir_aes_esp), # Une Croquis y Listado de AEU Espaciales
    url(r'^obtenermergeseccesp/$', view_test.unir_secciones_esp),  # Une Croquis y Listado de Secciones Espaciales
    url(r'^obtenermergezonasesp/$', view_test.unir_zona_esp),  # Une Croquis y Listado de Zonas Espaciales
    url(r'^obtenermergeaestab/$', view_test.unir_aes_tab),   # Une Croquis y Listado de AEU Tabulares
    url(r'^obtenermergesecctab/$', view_test.unir_secciones_tab),  # Une Croquis y Listado de Secciones Tabulares
    url(r'^obtenermergezonatab/$', view_test.unir_zona_tab),   #  Une Croquis y Listado de Zona Tabulares

    url(r'^crear/$', view_carpeta.crearCarpeta),

    url(r'^obtermergeaersimples/$', view_test.unir_ae_rur_simple),

    url(r'^impresionesaeus/(\d+)/(\d+)/$', view_angular.aeus),
    url(r'^obteresprural/$', view_esp_rural.generar_lote),
    url(r'^obterespcomprural/$', view_esp_comp_rural.generar_lote),
    url(r'^obterespseccrural/$', view_esp_secc_rural.generar_lote),
    url(r'^obteresprurdistrital/$', view_esp_ae_distrito_rural.generar_lote),

    url(r'^cargaraes/(\d+)/(\d+)/$', view_angular.aeus),
    url(r'^cargardepas/$', view_angular.departamentos),
    url(r'^cargardeprov/(\d+)/$', view_angular.provincias),
    url(r'^cargardistrito/(\d+)/(\d+)/$', view_angular.distritos),
    url(r'^cargarzonas/(\d+)/$', view_angular.zonas),
    url(r'^cantidadaeus/(\d+)/(\d+)/$', view_angular.cant_aeus),
    url(r'^cargartablas/(\d+)/(\d+)/$', view_angular.cargar_tabla),
    url(r'^cargaraeusseccion/(\d+)/(\d+)/$', view_angular.aeus_Seccion),
    url(r'^cargarseccionzonas/(\d+)/(\d+)/$', view_angular.seccion_Zonas),
    url(r'^cargarzonasdistritos/(\d+)/$', view_angular.zonas_Distritos),
    url(r'^paginas/(\d+)/(\d+)/$', view_angular.prueba),
    url(r'^imprimir/$', view_imprimir.imprimir),
    url(r'^imprimirzona/$', view_imprimir.imprimi_zona), #imprimir_seccion_unica
    url(r'^imprimirseccionuni/$', view_imprimir.imprimir_seccion_unica),
    url(r'^prueba/$', view_prueba.prueba),

    url(r'^aeuslegajos/(\d+)/(\d+)/$', view_angular.aeus_leg),
    # unir_zonas
    # url(r'^obter/(\d+)/$', views.generar_lote),
    # r'^report/$'  union_pdf
    # unir_secciones
]
