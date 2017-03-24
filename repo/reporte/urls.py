from django.conf.urls import url

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
import view_legajo
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

    url(r'^cargaraes/(\d+)/(\d+)/(\d+)/$', view_angular.aeus),

    url(r'^cargaraes_r/(\d+)/(\d+)/$', view_angular.dataImpresionRural),

    url(r'^cargardepas/$', view_angular.departamentos),
    url(r'^cargardeprov/(\d+)/$', view_angular.provincias),
    url(r'^cargardistrito/(\d+)/(\d+)/(\d+)/$', view_angular.distritos),
    url(r'^cargarzonas/(\d+)/$', view_angular.zonas),
    url(r'^cargarsecciones/(\d+)/(\d+)/$', view_angular.seccion),
    url(r'^cantidadaeus/(\d+)/(\d+)/$', view_angular.cant_aeus),
    url(r'^cargartablas/(\d+)/(\d+)/$', view_angular.cargar_tabla),
    url(r'^cargaraeusseccion/(\d+)/(\d+)/$', view_angular.aeus_Seccion),
    url(r'^cargarseccionzonas/(\d+)/(\d+)/$', view_angular.seccion_Zonas),
    url(r'^cargarzonasdistritos/(\d+)/$', view_angular.zonas_Distritos),
    url(r'^paginas/(\d+)/(\d+)/$', view_angular.prueba),
    url(r'^imprimir/$', view_imprimir.imprimir),
    url(r'^imprimirzona/$', view_imprimir.imprimi_zona), #imprimir_seccion_unica

    url(r'^imprimirseccionuni/$', view_imprimir.imprimir_seccion_unica),
    url(r'^procesoImpresionRural/$', view_imprimir.procesoImpresionRural),#impresion rural

    url(r'^guardarpags/$', view_angular.guardar_pag),
    url(r'^prueba/$', view_prueba.prueba),

    url(r'^aeuslegajos/(\d+)/(\d+)/(\d+)/$', view_angular.aeus_leg),
    url(r'^legajosRural/(\d+)/(\d+)/$', view_angular.legajoRural),


    url(r'^actconfirm/$', view_angular.actualizar_confir),
    url(r'^actconfirm_rural/$', view_angular.actualizar_confir_rural),

    url(r'^calidad/(\d+)/(\d+)/$', view_angular.calidad),  #calidad_errores
    url(r'^calidaderrores/(\d+)/(\d+)/(\d+)/$', view_angular.calidad_errores), #calidad_guardar_errors
    url(r'^calidadsaveerrores/$', view_angular.calidad_guardar_errors),  #/tablaReportetabular

    #url(r'^calidad_Indicadores_errors_urb/$', view_angular.calidad_Indicadores_errors_urb),



    url(r'^tablaReportetabular/(\d+)/(\d+)/(\d+)/$', view_angular.cargarTabla), #dataCro
    url(r'^tablaReporte/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/$', view_angular.dataCro), # generar_lote   #data_cobertura
    url(r'^tablaCobertura/(\d+)/(\d+)/(\d+)/(\d+)/$', view_angular.data_cobertura),  #data_prueba
    # unir_zonas
    # url(r'^obter/(\d+)/$', views.generar_lote),
    # r'^report/$'  union_pdf
    # unir_secciones
    url(r'^generarLegajo/(\d+)/$', view_legajo.generarLegajo),
    url(r'^generarLegajoRural/(\d+)/$', view_legajo.generarLegajo),

    url(r'^impresionEtiquetaRural/(\d+)/(\d+)/$', view_imprimir.procesoImpresionEtiquetaRural),

    url(r'^dataimpre/$', view_angular.data_prueba),

    #MODULO CONROL DE CALIDAD

    url(r'^listado_Urbano/(\d+)/(\d+)/(\d+)/$', view_angular.listado_Urbano),
    url(r'^calidadErrorUrb/(\d+)/(\d+)/(\d+)/$', view_angular.calidadErrorUrb),
    url(r'^guardarCalidadErrorUrb/$', view_angular.guardarCalidadErrorUrb),

    url(r'^listado_calid_muestreo/(\d+)/(\d+)/(\d+)/$', view_angular.listado_calid_muestreo),

    url(r'^calidadErrorRural/(\d+)/(\d+)/$', view_angular.calidadErrorRural),
    url(r'^guardarCalidadErrorRural/$', view_angular.guardarCalidadErrorRural),


    ##modulo segmentacion rural
    url(r'^listado_segm_rural/(\d+)/(\d+)/(\d+)/$', view_angular.listado_segm_rural),
    url(r'^guardar_Asig_segm/$', view_angular.guardar_Asig_segm),
    url(r'^guardar_Asig_Equi/$', view_angular.guardar_Asig_Equi),
    url(r'^guardar_validacion/(\d+)/(\d+)/$', view_angular.guardar_validacion),


#modulo monitoreo
    url(r'^listado_monit_calid/(\d+)/(\d+)/(\d+)/$', view_angular.listado_monit_calid),
    url(r'^listado_monit_calid_rural/(\d+)/(\d+)/(\d+)/$', view_angular.listado_monit_calid_rural),

    url(r'^guardar_validacion_input/(\d+)/(\d+)/$', view_angular.guardar_validacion_input),
    url(r'^guardar_validacion_input_rural/(\d+)/(\d+)/$', view_angular.guardar_validacion_input_rural),

#modulo calidad legajos
    url(r'^listado_calid_legajos/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/$', view_angular.listado_calid_legajos),








]
