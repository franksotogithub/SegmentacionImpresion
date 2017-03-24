from __future__ import unicode_literals

from django.db import models
from datetime import datetime


class Via(models.Model):
    p20 = models.CharField(primary_key=True, db_column='P20', max_length=254, db_index=True)
    p20_nombre = models.CharField(db_column='P20_NOMBRE', max_length=254)

    def __unicode__(self):
        return '%s , %s' % (self.p20, self.p20_nombre)

    class Meta:
        managed = False
        db_table = 'TB_TIPO_VIA'


class Departamento(models.Model):
    ccdd = models.CharField(primary_key=True, db_column='CCDD', max_length=2, db_index=True)
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=50)

    # fec_carga = models.CharField(db_column='FEC_CARGA', max_length=40, blank=True)

    def __unicode__(self):
        return '%s , %s' % (self.ccdd, self.departamento)

    # def __str__(self):
    #     return self.departamento

    class Meta:
        managed = False
        db_table = 'TB_DEPARTAMENTO'


class Provincia(models.Model):
    cod_prov = models.CharField(primary_key=True, db_column='COD_PROV', max_length=4, db_index=True)
    ccdd = models.ForeignKey(Departamento, db_column='CCDD', db_index=True)
    ccpp = models.CharField(db_column='CCPP', max_length=2)
    provincia = models.CharField(db_column='PROVINCIA', max_length=50)

    # fec_carga = models.CharField(db_column='FEC_CARGA', max_length=40)

    def __unicode__(self):
        return '%s , %s' % (self.ccdd, self.ccpp)

    class Meta:
        managed = False
        db_table = 'TB_PROVINCIA'


class Distrito(models.Model):
    ubigeo = models.CharField(primary_key=True, db_column='UBIGEO', max_length=6, db_index=True)
    ccdd = models.ForeignKey(Departamento, db_column='CCDD', db_index=True)
    ccpp = models.CharField(max_length=2, db_column='CCPP', db_index=True)
    ccdi = models.CharField(db_column='CCDI', max_length=2)
    distrito = models.CharField(db_column='DISTRITO', max_length=50)
    cod_prov = models.ForeignKey(Provincia, db_column='COD_PROV')
    id_estrato = models.CharField(db_column='id_estrato', max_length=2)
    flag_legajo_u = models.IntegerField(db_column='FLAG_LEGAJO_U')
    flag_legajo_r = models.IntegerField(db_column='FLAG_LEGAJO_R')
    cant_pag_u = models.CharField(db_column='CANT_PAG_U', max_length = 3)
    est_imp_u = models.CharField(db_column='EST_IMP_U', max_length = 1)
    cant_pag_r = models.CharField(db_column='CANT_PAG_R', max_length = 3)
    est_imp_r = models.CharField(db_column='EST_IMP_R', max_length = 1)

    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.ccdd)

    class Meta:
        managed = False
        db_table = 'TB_DISTRITO'


class Ccpp(models.Model):
    id = models.CharField(db_column='ID', db_index=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=254)
    # ccdd = models.CharField(db_column='CCDD', max_length=254)
    # ccpp = models.IntegerField(db_column='CCPP')
    # ccdi = models.IntegerField(db_column='CCDI')
    codccpp = models.CharField(db_column='CODCCPP', max_length=254)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=254)
    area = models.CharField(db_column='AREA', max_length=1)
    viv_ccpp = models.IntegerField(db_column='VIV_CCPP')
    categoria = models.CharField(db_column='CATEGORIA', max_length=254)
    categoria_o = models.CharField(db_column='CATEGORIA_O', max_length=50)
    llave_ccpp = models.CharField(primary_key=True, db_column='LLAVE_CCPP', max_length=10, db_index=True)

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'TB_CCPP'


class Zonacensal(models.Model):
    ubigeo = models.CharField(db_column='UBIGEO', max_length=255)
    ccdd = models.CharField(db_column='CCDD', max_length=255)
    ccpp = models.CharField(db_column='CCPP', max_length=255)
    ccdi = models.CharField(db_column='CCDI', max_length=255)
    codccpp = models.CharField(db_column='CODCCPP', max_length=255)
    zona = models.CharField(db_column='ZONA', max_length=255)
    idccpp = models.CharField(db_column='IDCCPP', max_length=40)
    idzona = models.CharField(db_column='IDZONA', max_length=40)

    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.ccdd)

    class Meta:
        managed = False
        db_table = 'TB_ZONA_CENSAL'


class Manzanas(models.Model):
    ubigeo = models.CharField(db_column='UBIGEO', max_length=255)
    codccpp = models.CharField(db_column='CODCCPP', max_length=255)
    zona = models.CharField(db_column='ZONA', max_length=255)
    manzana = models.CharField(db_column='MANZANA', max_length=255)
    viv_mz = models.CharField(db_column='VIV_MZ', max_length=255)
    cant_aeus = models.CharField(db_column='CANT_AEUS', max_length=255)
    aeus = models.CharField(db_column='AEUS', max_length=255)
    llave_mzs = models.CharField(db_column='LLAVE_MZS', max_length=255)

    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.codccpp)

    class Meta:
        managed = False
        db_table = 'TB_MZN'


class ViviendaUrbana(models.Model):
    objectid = models.CharField(primary_key=True, db_column='OBJECTID', max_length=6)
    id = models.IntegerField(db_column='ID')
    ubigeo = models.ForeignKey(Distrito, db_column='UBIGEO')
    ccdd = models.CharField(db_column='CCDD', max_length=2)
    ccpp = models.CharField(db_column='CCPP', max_length=2)
    ccdi = models.CharField(db_column='CCDI', max_length=2)
    codccpp = models.CharField(db_column="CODCCPP", max_length=4)
    zona = models.CharField(db_column='ZONA', max_length=5)
    manzana = models.CharField(db_column='MANZANA', max_length=4)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=60)
    departamento = models.CharField(db_column='DEPARTAMEN', max_length=60)
    provincia = models.CharField(db_column='PROVINCIA', max_length=50)
    distrito = models.CharField(db_column='DISTRITO', max_length=50)
    area = models.IntegerField(db_column='AREA')
    frente_ord = models.IntegerField(db_column='FRENTE_ORD')
    id_reg_or = models.IntegerField(db_column='ID_REG_OR')
    uso_local = models.IntegerField(db_column='USOLOCAL')
    aeu = models.IntegerField(db_column='AEU')
    or_viv_aeu = models.IntegerField(db_column='OR_VIV_AEU')
    corte = models.IntegerField(db_column='CORTE')
    aeu_final = models.IntegerField(db_column="AEU_FINAL")
    id_viv = models.ForeignKey('ViviendaU', db_column='LLAVE_VIV', db_index=True)
    llave_aeu = models.IntegerField(db_column='LLAVE_AEU')

    # llave_mzs = models.CharField(db_column='LLAVE_MZS', max_length=40)

    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.id)

    class Meta:
        managed = False
        db_table = 'TB_VIVIENDAS_URBANO'

# [AREA]
# [CCDD]
# [DEPARTAMENTO]
# [CCPP]
# [PROVINCIA]
# [CCDI]
#  [DISTRITO]
#   FROM [CPV_SEGMENTACION].[dbo].[VW_MARCO_UBIGEOS_SEGMENTADOS]

class VW_Marco_Ubigeos_Segmentados(models.Model):
    id = models.CharField(primary_key=True, db_column='ID', max_length=6)
    area = models.ForeignKey(Distrito, db_column='AREA')
    ccdd = models.CharField(db_column='CCDD', max_length=2)
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=2)
    ccpp = models.CharField(db_column='CCPP', max_length=2)
    provincia = models.CharField(db_column="PROVINCIA", max_length=4)
    ccdi = models.CharField(db_column='CCDI', max_length=5)
    distrito = models.CharField(db_column='DISTRITO', max_length=4)


    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.id)

    class Meta:
        managed = False
        db_table = 'VW_MARCO_UBIGEOS_SEGMENTADOS'

class Tb_Marco_Ubigeos_Segmentados(models.Model):
    id = models.CharField(primary_key=True, db_column='ID', max_length=6)
    area = models.ForeignKey(Distrito, db_column='AREA')
    ccdd = models.CharField(db_column='CCDD', max_length=2)
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=2)
    ccpp = models.CharField(db_column='CCPP', max_length=2)
    provincia = models.CharField(db_column="PROVINCIA", max_length=4)
    ccdi = models.CharField(db_column='CCDI', max_length=5)
    distrito = models.CharField(db_column='DISTRITO', max_length=4)


    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.id)

    class Meta:
        managed = False
        db_table = 'TB_MARCO_UBIGEOS_SEGMENTADOS'



class ViviendaU(models.Model):
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6)
    codccpp = models.CharField(db_column="CODCCPP")
    zona = models.CharField(db_column='ZONA', max_length=5)
    manzana = models.CharField(db_column='MANZANA', max_length=4)
    area = models.IntegerField(db_column='AREA')
    frente_ord = models.IntegerField(db_column='FRENTE_ORD')
    id_reg_or = models.IntegerField(db_column='ID_REG_OR')
    aer_ini = models.CharField(db_column='AER_INI', max_length=3)
    aer_fin = models.CharField(db_column='AER_FIN', max_length=3)
    p19a = models.IntegerField(db_column='P19A')
    p20 = models.ForeignKey(Via, db_column='P20', null=True, blank=True)
    p20_o = models.CharField(db_column='P20_O', max_length=50)
    p21 = models.CharField(db_column='P21', max_length=60)
    p21_a = models.CharField(db_column='P21_A', max_length=100)
    p22_a = models.CharField(db_column='P22_A', max_length=4)
    p22_b = models.CharField(db_column='P22_B', max_length=4)
    p23 = models.CharField(db_column='P23', max_length=3)
    id_p23 = models.IntegerField(db_column='ID_P23')
    p23_nombre = models.CharField(db_column='P23_NOMBRE', max_length=50)
    p23_vivpiso = models.IntegerField(db_column='P23_VIVPISO')
    p23_viviendas = models.IntegerField(db_column='P23_VIVIENDAS')
    p23_registros = models.IntegerField(db_column='P23_REGISTROS')
    p24 = models.CharField(db_column='P24', max_length=4)
    p25 = models.CharField(db_column='P25', max_length=4)
    p26 = models.CharField(db_column='P26', max_length=2)
    p27_a = models.CharField(db_column='P27_A', max_length=4)
    p27_b = models.CharField(db_column='P27_B', max_length=4)
    p28 = models.CharField(db_column='P28', max_length=4)
    p29 = models.IntegerField(db_column='P29')
    p29_a = models.IntegerField(db_column='P29_A')
    p29_1 = models.IntegerField(db_column='P29_1')
    p29_1_nombre = models.CharField(db_column='P29_1_NOMBRE', max_length=50)
    p29m = models.IntegerField(db_column='P29M')
    p29_o = models.CharField(db_column='P29_O', max_length=50)
    p29_8_o = models.CharField(db_column='P29_8_O', max_length=100)
    p29_p = models.CharField(db_column='P29_P', max_length=100)
    p30 = models.IntegerField(db_column='P30')
    p31 = models.IntegerField(db_column='P31')
    p32 = models.CharField(db_column='P32', max_length=100)
    p35 = models.CharField(db_column='P35', max_length=100)
    or_viv_aeu = models.IntegerField(db_column='OR_VIV_AEU')
    id_viv = models.CharField(primary_key=True, db_column='LLAVE_VIV', max_length=100)

    def __unicode__(self):
        return self.id_viv

    class Meta:
        managed = False
        db_table = 'TB_CPV0301_VIVIENDA_U'


class Aeus(models.Model):
    objectid = models.IntegerField(db_column='OBJECTID')
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6)
    zona = models.CharField(db_column='ZONA', max_length=5)
    aeu_final = models.IntegerField(db_column='AEU_FINAL')
    sum_viv_ae = models.IntegerField(db_column='SUM_VIV_AE')
    seccion = models.IntegerField(db_column='SECCION')
    llave_seccion = models.CharField(db_column='LLAVE_SECCION', max_length=6)
    llave_ccpp = models.ForeignKey(Ccpp, db_column='LLAVE_CCPP')
    llave_aeu = models.CharField(primary_key=True, db_column='LLAVE_AEU', db_index=True)

    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'TB_AEUS'


class Esp_Aeus(models.Model):
    objectid = models.IntegerField(db_column='OBJECTID')
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6)
    codccpp = models.CharField(db_column='CODCCPP', max_length=6)
    zona = models.CharField(db_column='ZONA', max_length=5)
    aeu_final = models.IntegerField(db_column='AEU_FINAL')
    cant_viv = models.IntegerField(db_column='CANT_VIV')
    seccion = models.IntegerField(db_column='SECCION')
    llave_seccion = models.CharField(db_column='LLAVE_SECC', max_length=6)
    llave_aeu = models.CharField(primary_key=True, db_column='LLAVE_AEU', db_index=True)
    llave_ccpp = models.ForeignKey(Ccpp, db_column='LLAVE_CCPP')

    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'SEGM_ESP_AEU'


class Rutas(models.Model):
    ubigeo = models.CharField(primary_key=True, db_column='UBIGEO', max_length=6, db_index=True)
    objectid = models.IntegerField(db_column='OBJECTID')
    zona = models.CharField(db_column='ZONA', max_length=5)
    manzana = models.CharField(db_column='MANZANA', max_length=4)
    aeu = models.IntegerField(db_column='AEU')
    id_ruta = models.CharField(db_column='ID_RUTA', max_length=254)
    viv_aeu = models.IntegerField(db_column='VIV_AEU')
    flag = models.IntegerField(db_column='FLAG')
    aeu_final = models.IntegerField(db_column='AEU_FINAL')
    seccion = models.IntegerField(db_column='SECCION')
    est_seg = models.CharField(db_column='EST_SEG', max_length=1)
    est_croquis = models.CharField(db_column='EST_CROQUIS', max_length=1)
    llave_mzs = models.CharField(db_column='LLAVE_MZS', max_length=1)
    llave_aeu = models.ForeignKey(Aeus, db_column='LLAVE_AEU')

    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.objectid)

    class Meta:
        managed = False
        db_table = 'TB_RUTAS'


class Secciones(models.Model):
    objectid = models.CharField(primary_key=True, db_column='OBJECTID', max_length=254, db_index=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=254)
    zona = models.CharField(db_column='ZONA', max_length=254)
    seccion = models.IntegerField(db_column='SECCION')
    cant_viv = models.IntegerField(db_column='CANT_VIV')
    llave_seccion = models.CharField(db_column='ZONA', max_length=40)

    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'TB_SECCIONES'


class v_ReporteSecciones(models.Model):
    id = models.CharField(db_column='ID', primary_key=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6, db_index=True)
    codccpp = models.CharField(db_column='CODCCPP', max_length=10)
    zona = models.CharField(db_column='ZONA', max_length=5)
    seccion = models.IntegerField(db_column='SECCION')
    aeu_final = models.IntegerField(db_column='AEU_FINAL')
    manzanas = models.CharField(db_column='MANZANAS', max_length=6)
    cant_viv = models.IntegerField(db_column='CANT_VIV')

    def __unicode__(self):
        return '%s , %s' % (self.manzanas, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REPORTE_SECCIONES'


class v_ReporteResumenDistrito(models.Model):
    id = models.CharField(db_column='ID', primary_key=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6, db_index=True)
    codccpp = models.CharField(db_column='CODCCPP', max_length=6)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=6)
    zona = models.CharField(db_column='ZONA', max_length=5)
    cant_secciones = models.IntegerField(db_column='CANT_SECCIONES')
    cant_aeus = models.IntegerField(db_column='CANT_AEUS')
    cant_mzs = models.IntegerField(db_column='CANT_MZS')
    cant_viv = models.IntegerField(db_column='CANT_VIV')
    prom_viv_aeu = models.FloatField(db_column='PROM_VIV_AEU')
    prom_mzs_aeu = models.FloatField(db_column='PROM_MZS_AEU')

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REPORTE_RESUMEN_DISTRITO'

class v_ReporteResumenDistritoTab(models.Model):
    id = models.CharField(db_column='ID', primary_key=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6, db_index=True)
    codccpp = models.CharField(db_column='CODCCPP', max_length=6)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=6)
    zona = models.CharField(db_column='ZONA', max_length=5)
    cant_secciones = models.CharField(db_column='CANT_SECCIONES', max_length=6)
    cant_aeus = models.CharField(db_column='CANT_AEUS')
    cant_mzs = models.CharField(db_column='CANT_MZS', max_length=6)
    cant_viv = models.CharField(db_column='CANT_VIV', max_length=6)
    prom_viv_aeu = models.CharField(db_column='PROM_VIV_AEU', max_length=6)
    prom_mzs_aeu = models.CharField(db_column='PROM_MZS_AEU', max_length=6)

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REPORTE_RESUMEN_DISTRITO_TAB'

class v_ReporteCabViviendas(models.Model):
    id = models.CharField(db_column='ID', primary_key=True)
    ccdd = models.CharField(db_column='CCDD', max_length=6, db_index=True)
    departamento = models.CharField(db_column="DEPARTAMENTO", max_length=50)
    ccpp = models.CharField(db_column='CCPP', max_length=50)
    provincia = models.CharField(db_column='PROVINCIA', max_length=50)
    ccdi = models.CharField(db_column='CCDI', max_length=50)
    distrito = models.CharField(db_column='DISTRITO', max_length=50)
    codccpp = models.CharField(db_column='CODCCPP',  max_length=50)
    nomccpp = models.CharField(db_column='NOMCCPP',  max_length=50)
    cat_ccpp = models.CharField(db_column='CAT_CCPP', max_length=50)
    zona = models.CharField(db_column='ZONA', max_length=50)
    zona_convert = models.CharField(db_column='ZONA_CONVERT', max_length=50)
    seccion = models.CharField(db_column='SECCION', max_length=50)
    seccion_convert = models.CharField(db_column='SECCION_CONVERT', max_length=50)
    aeu_final = models.CharField(db_column='AEU_FINAL', max_length=20)
    aeu_convert = models.CharField(db_column='AEU_CONVERT', max_length=20)
    cant_viv = models.CharField(db_column='CANT_VIV', max_length=30)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=40)

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REP_CAB_VIVIENDA_ESP'


class v_ReporteViviendas(models.Model):
    id = models.CharField(db_column='ID', primary_key=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6, db_index=True)
    codccpp = models.CharField(db_column="CODCCPP")
    zona = models.CharField(db_column='ZONA', max_length=5)
    manzana = models.CharField(db_column='MANZANA', max_length=4)
    frente_ord = models.IntegerField(db_column='FRENTE_ORD')
    seccion = models.CharField(db_column='SECCION', max_length=3)
    id_reg_or = models.IntegerField(db_column='ID_REG_OR')
    aer_ini = models.CharField(db_column='AER_INI', max_length=3)
    aer_fin = models.CharField(db_column='AER_FIN', max_length=3)
    tipo_via = models.CharField(db_column='TIPO_VIA', max_length=50)
    nombre_via = models.CharField(db_column='NOMBRE_VIA', max_length=50)
    npuerta = models.CharField(db_column='N_PUERTA', max_length=50)
    p19a = models.CharField(db_column='P19A', max_length=50)
    p20 = models.ForeignKey(Via, db_column='P20', null=True, blank=True)
    p20_o = models.CharField(db_column='P20_O', max_length=50)
    p21 = models.CharField(db_column='P21', max_length=60)
    p21_a = models.CharField(db_column='P21_A', max_length=100)
    p22_a = models.CharField(db_column='P22_A', max_length=4)
    p22_b = models.CharField(db_column='P22_B', max_length=4)
    p23 = models.CharField(db_column='P23', max_length=3)
    id_p23 = models.CharField(db_column='ID_P23', max_length=50)
    p23_nombre = models.CharField(db_column='P23_NOMBRE', max_length=50)
    p23_Tpiso = models.CharField(db_column='P23_TPISO', max_length=50)
    p23_vivpiso = models.CharField(db_column='P23_VIVPISO')
    p23_viviendas = models.CharField(db_column='P23_VIVIENDAS', max_length=50)
    p23_registros = models.CharField(db_column='P23_REGISTROS', max_length=50)
    p24 = models.CharField(db_column='P24', max_length=4)
    p25 = models.CharField(db_column='P25', max_length=4)
    p26 = models.CharField(db_column='P26', max_length=2)
    p27_a = models.CharField(db_column='P27_A', max_length=4)
    p27_b = models.CharField(db_column='P27_B', max_length=4)
    p28 = models.CharField(db_column='P28', max_length=4)
    p29 = models.CharField(db_column='P29', max_length=50)
    p29_a = models.CharField(db_column='P29_A', max_length=50)
    p29_1 = models.CharField(db_column='P29_1', max_length=50)
    p29_1_nombre = models.CharField(db_column='P29_1_NOMBRE', max_length=50)
    #p29m = models.CharField(db_column='P29M', max_length=50)
    p29_o = models.CharField(db_column='P29_O', max_length=50)
    p29_8_o = models.CharField(db_column='P29_8_O', max_length=100)
    p29_p = models.CharField(db_column='P29_P', max_length=100)
    p30 = models.CharField(db_column='P30', max_length=100)
    p31 = models.CharField(db_column='P31', max_length=50)
    p32 = models.CharField(db_column='P32', max_length=100)
    p35 = models.CharField(db_column='P35', max_length=100)
    #id_viv = models.CharField(db_column='LLAVE_VIV', max_length=100)
    aeu_final = models.CharField(db_column='AEU_FINAL', max_length=100)
    or_viv_aeu = models.CharField(db_column='OR_VIV_AEU', max_length=100)
    p20_nombre = models.CharField(db_column='P20_NOMBRE', max_length=100)

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REPORTE_VIVIENDAS'

class Vw_reporte_legajo(models.Model):
    id = models.CharField(primary_key=True, db_column='ID', db_index=True)
    ccdd = models.CharField(db_column='CCDD', db_index=True)
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=30)
    ccpp = models.CharField(db_column='CCPP', max_length=6)
    provincia = models.CharField(db_column='PROVINCIA', max_length=30)
    ccdi = models.CharField(db_column='CCDI', max_length=5)
    distrito = models.IntegerField(db_column='DISTRITO', max_length=30)
    cant_aeu_u = models.CharField(db_column='CANT_AE_U', max_length=4)
    cant_secc_u = models.CharField(db_column='CANT_SECC_u', max_length=4)
    cant_zonas_u = models.CharField(db_column='CANT_ZONAS_U', max_length=4)
    cant_zonas_r = models.CharField(db_column='CANT_ZONAS_R', max_length=4)
    cant_ae_r = models.CharField(db_column='CANT_AE_R', max_length=4)
    cant_secc_r = models.CharField(db_column='CANT_SECC_R', max_length=4)


    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REPORTE_LEGAJO'


class Tb_Calidad_Aeu(models.Model):
    objectid = models.CharField(primary_key=True, db_column='OBJECTID', db_index=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6)
    codccpp = models.CharField(db_column='CODCCPP', max_length=6)
    zona = models.CharField(db_column='ZONA', max_length=5)
    aeu_final = models.CharField(db_column='AEU_FINAL', max_length=5)
    cant_viv = models.IntegerField(db_column='CANT_VIV')
    seccion = models.IntegerField(db_column='SECCION')
    llave_seccion = models.CharField(db_column='LLAVE_SECC', max_length=6)
    llave_aeu = models.CharField(primary_key=True, db_column='LLAVE_AEU', db_index=True)
    llave_ccpp = models.ForeignKey(Ccpp, db_column='LLAVE_CCPP')
    est_seg = models.CharField(db_column='EST_SEG', max_length=2)
    est_croquis = models.CharField(db_column='EST_CROQUIS', max_length=2)
    est_cont = models.CharField(db_column='EST_CONT', max_length=2)
    est_imp = models.CharField(db_column='EST_IMP', max_length=2)
    est_imp_secc = models.CharField(db_column='EST_IMP_SECC', max_length=2)
    est_con_aeu =  models.CharField(db_column='EST_CON_AEU', max_length=2)
    est_con_secc = models.CharField(db_column='EST_CON_SECC', max_length=2)
    cont_urb_error_01 = models.CharField(db_column='CONT_URB_ERROR_01', max_length=2)
    cont_urb_error_02 = models.CharField(db_column='CONT_URB_ERROR_02', max_length=2)
    cont_urb_error_03 = models.CharField(db_column='CONT_URB_ERROR_03', max_length=2)
    cont_urb_error_04 = models.CharField(db_column='CONT_URB_ERROR_04', max_length=2)
    cont_urb_error_05 = models.CharField(db_column='CONT_URB_ERROR_05', max_length=2)
    cont_urb_error_06 = models.CharField(db_column='CONT_URB_ERROR_06', max_length=2)
    cont_urb_error_07 = models.CharField(db_column='CONT_URB_ERROR_07', max_length=2)
    cont_urb_error_08 = models.CharField(db_column='CONT_URB_ERROR_08', max_length=2)
    cont_urb_error_09 = models.CharField(db_column='CONT_URB_ERROR_09', max_length=2)
    cont_urb_error_10 = models.CharField(db_column='CONT_URB_ERROR_10', max_length=2)
    cont_urb_error_11 = models.CharField(db_column='CONT_URB_ERROR_11', max_length=2)
    cont_urb_error_12 = models.CharField(db_column='CONT_URB_ERROR_12', max_length=2)
    nom_reg = models.CharField(db_column='NOM_REG', max_length=50)
    fec_reg = models.CharField(db_column='FEC_REG', max_length=50)
    cant_reg = models.CharField(db_column='CANT_REG', max_length=50)

    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'TB_CALIDAD_AEU'


class Tab_Aeus(models.Model):
    objectid = models.CharField(primary_key=True, db_column='OBJECTID', db_index=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6)
    # objectid = models.CharField(primary_key=True, db_column='OBJECTID', max_length=254, db_index=True)
    codccpp = models.CharField(db_column='CODCCPP', max_length=6)
    zona = models.CharField(db_column='ZONA', max_length=5)
    aeu_final = models.CharField(db_column='AEU_FINAL', max_length=5)
    cant_viv = models.IntegerField(db_column='CANT_VIV')
    seccion = models.IntegerField(db_column='SECCION')
    llave_seccion = models.CharField(db_column='LLAVE_SECC', max_length=6)
    llave_aeu = models.CharField(primary_key=True, db_column='LLAVE_AEU', db_index=True)
    llave_ccpp = models.ForeignKey(Ccpp, db_column='LLAVE_CCPP')
    est_imp = models.CharField(db_column='EST_IMP', max_length=2)
    est_imp_secc = models.CharField(db_column='EST_IMP_SECC', max_length=2)
    est_con_aeu =  models.CharField(db_column='EST_CON_AEU', max_length=2)
    est_con_secc = models.CharField(db_column='EST_CON_SECC', max_length=2)
    cont_urb_error_01 = models.CharField(db_column='CONT_URB_ERROR_01', max_length=2)
    cont_urb_error_02 = models.CharField(db_column='CONT_URB_ERROR_02', max_length=2)
    cont_urb_error_03 = models.CharField(db_column='CONT_URB_ERROR_03', max_length=2)
    cont_urb_error_04 = models.CharField(db_column='CONT_URB_ERROR_04', max_length=2)
    cont_urb_error_05 = models.CharField(db_column='CONT_URB_ERROR_05', max_length=2)
    cont_urb_error_06 = models.CharField(db_column='CONT_URB_ERROR_06', max_length=2)
    cont_urb_error_07 = models.CharField(db_column='CONT_URB_ERROR_07', max_length=2)
    cont_urb_error_08 = models.CharField(db_column='CONT_URB_ERROR_08', max_length=2)
    cont_urb_error_09 = models.CharField(db_column='CONT_URB_ERROR_09', max_length=2)
    cont_urb_error_10 = models.CharField(db_column='CONT_URB_ERROR_10', max_length=2)
    cont_urb_error_11 = models.CharField(db_column='CONT_URB_ERROR_11', max_length=2)
    cont_urb_error_12 = models.CharField(db_column='CONT_URB_ERROR_12', max_length=2)
    nom_reg = models.CharField(db_column='NOM_REG', max_length=50)
    fec_reg = models.CharField(db_column='FEC_REG', max_length=50) #CANT_PAG
    cant_pag = models.CharField(db_column='CANT_PAG', max_length=50)

    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'SEGM_TAB_AEU'

class Tab_Secciones(models.Model):
    objectid = models.CharField(primary_key=True, db_column='OBJECTID', max_length=254, db_index=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=254)
    codccpp = models.CharField(db_column='CODCCPP', max_length=254)
    zona = models.CharField(db_column='ZONA', max_length=254)
    seccion = models.CharField(db_column='SECCION', max_length=4)
    cant_viv = models.IntegerField(db_column='CANT_VIV')
    llave_secc = models.CharField(db_column='LLAVE_SECC', max_length=254)
    est_imp_secc = models.CharField(db_column='EST_IMP_SECC', max_length=2)
    est_imp_zona = models.CharField(db_column='EST_IMP_ZONA', max_length=2)
    est_con_secc = models.CharField(db_column='EST_CON_SECCION', max_length=2)
    est_con_zona = models.CharField(db_column='EST_CON_ZONA', max_length=2)
    cant_pag = models.CharField(db_column='CANT_PAG', max_length=2)
    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'SEGM_TAB_SECCION'


class Tab_u_Secciones(models.Model):
    objectid = models.CharField(primary_key=True, db_column='OBJECTID', max_length=254, db_index=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=254)
    distope = models.CharField(db_column='DISTOPE', max_length=6)
    zona = models.CharField(db_column='ZONA', max_length=254)
    subZona = models.CharField(db_column='SUBZONA')
    subZona = models.CharField(db_column='SUBZONA')

    seccion = models.CharField(db_column='SECCION', max_length=4)
    cant_viv = models.IntegerField(db_column='CANT_VIV')
    llave_secc = models.CharField(db_column='LLAVE_SECC', max_length=254)
    est_imp_secc = models.CharField(db_column='EST_IMP_SECC', max_length=2)
    est_imp_zona = models.CharField(db_column='EST_IMP_ZONA', max_length=2)
    est_con_secc = models.CharField(db_column='EST_CON_SECCION', max_length=2)
    est_con_zona = models.CharField(db_column='EST_CON_ZONA', max_length=2)
    cant_pag = models.CharField(db_column='CANT_PAG', max_length=2)

    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'SEGM_TAB_SECCION'


class Tab_Zonas(models.Model):
    id = models.CharField(db_column='ID', primary_key=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6, db_index=True)
    codccpp = models.CharField(db_column='CODCCPP', max_length=6)
    zona = models.CharField(db_column='ZONA', max_length=6)
    llave_ccpp = models.CharField(db_column='LLAVE_CCPP', max_length=5)
    llave_zona = models.CharField(db_column='LLAVE_ZONA', max_length=6)
    fec_carga = models.DateTimeField(db_column='FEC_CARGA')
    flag_proc = models.CharField(db_column='FLAG_PROC', max_length=6)
    etiq_zona = models.CharField(db_column='ETIQ_ZONA', max_length=6)
    est_imp_zona = models.CharField(db_column='EST_IMP_ZONA', max_length=2)
    est_con_zona = models.CharField(db_column='EST_CON_ZONA', max_length=2)
    cant_pag = models.CharField(db_column='CANT_PAG', max_length=2)
    flag = models.IntegerField(db_column='FLAG_CALIDAD')

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'TB_ZONA'


class Tab_Sub_Zonas(models.Model):
    id = models.CharField(db_column='ID', primary_key=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6)
    distope = models.CharField(db_column='DISTOPE', max_length=6)
    zona = models.CharField(db_column='ZONA', max_length=6)
    idzona = models.CharField(db_column='IDZONA', max_length=5)
    subZona = models.CharField(db_column='SUBZONA')
    cant_viv = models.IntegerField(db_column='CANT_VIV')
    cant_pag = models.IntegerField(db_column='CANT_PAG')
    flag_imp_leg_subzona = models.CharField(db_column='FLAG_IMP_LEG_SUZONA')
    flag_imp_leg_dist = models.CharField(db_column='FLAG_IMP_LEG_DIST')
    flag_control_leg_dist = models.CharField(db_column='FLAG_CONTROL_LEG_SUBZONA')
    flag_control_leg_dist = models.CharField(db_column='FLAG_CONTROL_LEG_DIST')
    cant_imp_leg_subzona = models.IntegerField(db_column='CANT_IMP_LEG_SUBZONA')
    cant_imp_leg_dist = models.IntegerField(db_column='CANT_IMP_LEG_DIST')

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'TB_ZONA'


class segm_r_scr(models.Model):
    idscr = models.CharField(db_column='IDSCR', primary_key=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=10, db_index=True)
    scr = models.CharField(db_column='SCR', max_length=6)
    cant_pag = models.CharField(db_column='CANT_PAG', max_length=6)
    est_imp = models.CharField(db_column='EST_IMP', max_length=5)
    flag_legajo = models.CharField(db_column='FLAG_LEGAJO', max_length=5)


    def __unicode__(self):
        return '%s , %s' % (self.idscr, self.ubigeo)
    class Meta:
        managed = False
        db_table = 'SEGM_R_SCR'

class  segm_r_emp(models.Model):

    idruta = models.CharField(db_column='IDRUTA', max_length=10)
    objectid = models.CharField(db_column='OBJECTID', primary_key=True)
    emp = models.CharField(db_column='EMP', max_length=6)
    cant_pag = models.CharField(db_column='CANT_PAG', max_length=6)
    est_imp = models.CharField(db_column='EST_IMP', max_length=5)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=10, db_index=True)
    idscr = models.CharField(db_column='IDSCR', primary_key=True)
    flag_legajo = models.CharField(db_column='FLAG_LEGAJO', max_length=5)



    def __unicode__(self):
        return '%s , %s' % (self.idruta, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'SEGM_R_EMP'



# class VerificaImpresion(models.Model):
#     TIPO_CHOICES = (
#         (1, "AEU"),
#         (2, "seccion"),
#         (3, "Zonas")
#     )
#
#     ESTADO_IMPRESION_CHOICES = (
#         (0, "por imprimir"),
#         (1, "impreso"),
#         (2, "reimpreso"),
#     )
#
#     ESTADO_CONFIRMACION_CHOICES = (
#         (0, "NO CONFIRMADO"),
#         (1, "CONFIRMADO"),
#     )
#     id = models.AutoField(primary_key=True)
#     aeu_id = models.ForeignKey(Tab_Aeus, blank=True, null=True, default=None)
#     seccion_id = models.ForeignKey(Tab_Secciones, blank=True, null=True, default=None)
#     zona_id = models.ForeignKey(Tab_Zonas, blank=True, null=True, default=None)
#     estado_impresion = models.PositiveIntegerField(default=0, choices=ESTADO_IMPRESION_CHOICES)
#     estado_confirmacion = models.PositiveIntegerField(default=0, choices=ESTADO_CONFIRMACION_CHOICES)
#     tipo = models.PositiveIntegerField(choices=TIPO_CHOICES)
#
#     class Meta:
#         managed = False
#         db_table = 'ESTADOS'


class Vw_Rep_Cab_Seccion_Tab(models.Model):
    id = models.CharField(primary_key=True, db_column='ID', max_length=4, db_index=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=50)
    ccdd = models.CharField(db_column='CCDD', max_length=50)
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=50)
    ccpp = models.CharField(db_column='CCPP', max_length=50)
    provincia = models.CharField(db_column='PROVINCIA', max_length=50)
    ccdi = models.CharField(db_column='CCDI', max_length=50)
    distrito = models.CharField(db_column='DISTRITO', max_length=50)
    codccpp = models.CharField(db_column='CODCCPP', max_length=50)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=50)
    cat_ccpp = models.CharField(db_column='CAT_CCPP', max_length=50)
    zona = models.CharField(db_column='ZONA', max_length=50)
    zona_convert = models.CharField(db_column='ZONA_CONVERT', max_length=50)
    seccion = models.CharField(db_column='SECCION', max_length=50)
    seccion_convert = models.CharField(db_column='SECCION_CONVERT', max_length=50)
    aeu_inicial = models.CharField(db_column='AEU_INICIAL', max_length=50)
    aeu_final = models.CharField(db_column='AEU_FINAL', max_length=50)
    cant_viv = models.CharField(db_column='CANT_VIV', max_length=50)

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REP_CAB_SECCION_TAB'

class Vw_Rep_Cab_Seccion_Esp(models.Model):
    id = models.CharField(primary_key=True, db_column='ID', max_length=4, db_index=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=50)
    ccdd = models.CharField(db_column='CCDD', max_length=50)
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=50)
    ccpp = models.CharField(db_column='CCPP', max_length=50)
    provincia = models.CharField(db_column='PROVINCIA', max_length=50)
    ccdi = models.CharField(db_column='CCDI', max_length=50)
    distrito = models.CharField(db_column='DISTRITO', max_length=50)
    codccpp = models.CharField(db_column='CODCCPP', max_length=50)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=50)
    cat_ccpp = models.CharField(db_column='CAT_CCPP', max_length=50)
    zona = models.CharField(db_column='ZONA', max_length=50)
    zona_convert = models.CharField(db_column='ZONA_CONVERT', max_length=50)
    seccion = models.CharField(db_column='SECCION', max_length=50)
    seccion_convert = models.CharField(db_column='SECCION_CONVERT', max_length=50)
    aeu_inicial = models.CharField(db_column='AEU_INICIAL', max_length=50)
    aeu_final = models.CharField(db_column='AEU_FINAL', max_length=50)
    cant_viv = models.CharField(db_column='CANT_VIV', max_length=50)

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REP_CAB_SECCION_ESP'

class Vw_Rep_Cab_Zona_Esp(models.Model):
    id = models.CharField(primary_key=True, db_column='ID', max_length=4, db_index=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=50)
    ccdd = models.CharField(db_column='CCDD', max_length=50)
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=50)
    ccpp = models.CharField(db_column='CCPP', max_length=50)
    provincia = models.CharField(db_column='PROVINCIA', max_length=50)
    ccdi = models.CharField(db_column='CCDI', max_length=50)
    distrito = models.CharField(db_column='DISTRITO', max_length=50)
    codccpp = models.CharField(db_column='CODCCPP', max_length=50)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=50)
    cat_ccpp = models.CharField(db_column='CAT_CCPP', max_length=50)
    zona = models.CharField(db_column='ZONA', max_length=50)
    zona_convert = models.CharField(db_column='ZONA_CONVERT', max_length=50)
    aeu_inicial = models.CharField(db_column='AEU_INICIAL', max_length=50)
    aeu_final = models.CharField(db_column='AEU_FINAL', max_length=50)
    seccion_inicial = models.CharField(db_column='SECCION_INICIAL', max_length=50)
    seccion_final = models.CharField(db_column='SECCION_FINAL', max_length=50)
    cant_viv = models.CharField(db_column='CANT_VIV', max_length=50)

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REP_CAB_ZONA_ESP'

class Vw_Rep_Cab_Zona_Tab(models.Model):
    id = models.CharField(primary_key=True, db_column='ID', max_length=4, db_index=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=50)
    ccdd = models.CharField(db_column='CCDD', max_length=50)
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=50)
    ccpp = models.CharField(db_column='CCPP', max_length=50)
    provincia = models.CharField(db_column='PROVINCIA', max_length=50)
    ccdi = models.CharField(db_column='CCDI', max_length=50)
    distrito = models.CharField(db_column='DISTRITO', max_length=50)
    codccpp = models.CharField(db_column='CODCCPP', max_length=50)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=50)
    cat_ccpp = models.CharField(db_column='CAT_CCPP', max_length=50)
    zona = models.CharField(db_column='ZONA', max_length=50)
    zona_convert = models.CharField(db_column='ZONA_CONVERT', max_length=50)
    aeu_inicial = models.CharField(db_column='AEU_INICIAL', max_length=50)
    aeu_final = models.CharField(db_column='AEU_FINAL', max_length=50)
    seccion_inicial = models.CharField(db_column='SECCION_INICIAL', max_length=50)
    seccion_final = models.CharField(db_column='SECCION_FINAL', max_length=50)
    cant_viv = models.CharField(db_column='CANT_VIV', max_length=50)

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REP_CAB_ZONA_TAB'

class Tab_Rutas(models.Model):
    objectid = models.IntegerField(db_column='OBJECTID')
    ubigeo = models.CharField(primary_key=True, db_column='UBIGEO', max_length=6, db_index=True)
    codccpp = models.CharField(db_column='CODCCPP', max_length=4)
    zona = models.CharField(db_column='ZONA', max_length=5)
    manzana = models.CharField(db_column='MANZANA', max_length=4)
    aeu = models.IntegerField(db_column='AEU')
    cant_viv = models.IntegerField(db_column='CANT_VIV')
    aeu_final = models.IntegerField(db_column='AEU_FINAL')
    seccion = models.IntegerField(db_column='SECCION')
    idmanzana = models.CharField(db_column='IDMANZANA', max_length=50)
    llave_mzs = models.CharField(db_column='LLAVE_MZS', max_length=1)
    llave_aeu = models.ForeignKey(Aeus, db_column='LLAVE_AEU')
    llave_ruta = models.CharField(db_column='LLAVE_RUTA', max_length=1)

    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.objectid)

    class Meta:
        managed = False
        db_table = 'SEGM_TAB_RUTAS'

class Tab_ViviendaUrbana(models.Model):
    objectid = models.CharField(primary_key=True, db_column='OBJECTID', max_length=6)
    id = models.IntegerField(db_column='ID')
    ubigeo = models.ForeignKey(Distrito, db_column='UBIGEO')
    codccpp = models.CharField(db_column='CODCCPP', max_length=4)
    zona = models.CharField(db_column='ZONA', max_length=5)
    manzana = models.CharField(db_column='MANZANA', max_length=4)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=60)
    departamento = models.CharField(db_column='DEPARTAMEN', max_length=60)
    provincia = models.CharField(db_column='PROVINCIA', max_length=50)
    distrito = models.CharField(db_column='DISTRITO', max_length=50)
    area = models.IntegerField(db_column='AREA')
    frente_ord = models.IntegerField(db_column='FRENTE_ORD')
    id_reg_or = models.IntegerField(db_column='ID_REG_OR')
    edificacio = models.IntegerField(db_column='EDIFICACIO')
    uso_local = models.IntegerField(db_column='USOLOCAL')
    cond_solo = models.IntegerField(db_column='COND_SOLO')
    aeu = models.IntegerField(db_column='AEU')
    or_viv_aeu = models.IntegerField(db_column='OR_VIV_AEU')
    flg_corte = models.IntegerField(db_column='FLG_CORTE')
    flg_mzn = models.IntegerField(db_column='FLG_MZ')
    aeu_final = models.IntegerField(db_column="AEU_FINAL")
    #id_viv = models.ForeignKey('ViviendaU', db_column='LLAVE_VIV', db_index=True)
    llave_aeu = models.IntegerField(db_column='LLAVE_AEU')

    # llave_mzs = models.CharField(db_column='LLAVE_MZS', max_length=40)

    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.id)

    class Meta:
        managed = False
        db_table = 'SEGM_TAB_VIVIENDA_U'


class v_ReporteSecciones_Tab(models.Model):
    id = models.CharField(db_column='ID', primary_key=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6, db_index=True)
    codccpp = models.CharField(db_column='CODCCPP', max_length=10)
    zona = models.CharField(db_column='ZONA', max_length=5)
    seccion = models.IntegerField(db_column='SECCION')
    aeu_final = models.IntegerField(db_column='AEU_FINAL')
    manzanas = models.CharField(db_column='MANZANAS', max_length=6)
    cant_viv = models.IntegerField(db_column='CANT_VIV')

    def __unicode__(self):
        return '%s , %s' % (self.manzanas, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REPORTE_SECCIONES_TAB'


class v_ReporteViviendas_Tab(models.Model):
    id = models.CharField(db_column='ID', primary_key=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6, db_index=True)
    codccpp = models.CharField(db_column="CODCCPP", max_length=50)
    zona = models.CharField(db_column='ZONA', max_length=5)
    manzana = models.CharField(db_column='MANZANA', max_length=4)
    #area = models.IntegerField(db_column='AREA')
    frente_ord = models.CharField(db_column='FRENTE_ORD', max_length=50)
    id_reg_or = models.CharField(db_column='ID_REG_OR', max_length=50)
    aer_ini = models.CharField(db_column='AER_INI', max_length=3)
    aer_fin = models.CharField(db_column='AER_FIN', max_length=3)
    p19a = models.CharField(db_column='P19A', max_length=50)
    p20 = models.ForeignKey(Via, db_column='P20', null=True, blank=True)
    p20_o = models.CharField(db_column='P20_O', max_length=50)
    p21 = models.CharField(db_column='P21', max_length=60)
    p21_a = models.CharField(db_column='P21_A', max_length=100)
    p22_a = models.CharField(db_column='P22_A', max_length=4)
    p22_b = models.CharField(db_column='P22_B', max_length=4)
    p23 = models.CharField(db_column='P23', max_length=3)
    id_p23 = models.CharField(db_column='ID_P23', max_length=50)
    p23_nombre = models.CharField(db_column='P23_NOMBRE', max_length=50)
    p23_Tpiso = models.CharField(db_column='P23_TPISO', max_length=50)
    p23_vivpiso = models.CharField(db_column='P23_VIVPISO', max_length=50)
    p23_viviendas = models.CharField(db_column='P23_VIVIENDAS', max_length=50)
    p23_registros = models.CharField(db_column='P23_REGISTROS', max_length=50)
    p24 = models.CharField(db_column='P24', max_length=4)
    p25 = models.CharField(db_column='P25', max_length=4)
    p26 = models.CharField(db_column='P26', max_length=2)
    p27_a = models.CharField(db_column='P27_A', max_length=4)
    p27_b = models.CharField(db_column='P27_B', max_length=4)
    p28 = models.CharField(db_column='P28', max_length=4)
    p29 = models.CharField(db_column='P29', max_length=50)
    p29_a = models.CharField(db_column='P29_A', max_length=50)
    p29_1 = models.CharField(db_column='P29_1', max_length=50)
    p29_1_nombre = models.CharField(db_column='P29_1_NOMBRE', max_length=50)
    #p29m = models.CharField(db_column='P29M', max_length=50)
    p29_o = models.CharField(db_column='P29_O', max_length=50)
    p29_8_o = models.CharField(db_column='P29_8_O', max_length=100)
    p29_p = models.CharField(db_column='P29_P', max_length=100)
    p30 = models.CharField(db_column='P30', max_length=50)
    p31 = models.CharField(db_column='P31', max_length=50)
    p32 = models.CharField(db_column='P32', max_length=100)
    p35 = models.CharField(db_column='P35', max_length=100)
    aeu_final = models.IntegerField(db_column='AEU_FINAL')
    or_viv_aeu = models.IntegerField(db_column='OR_VIV_AEU')
    p20_nombre = models.CharField(db_column='P20_NOMBRE', max_length=50)

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REPORTE_VIVIENDAS_TAB'

class v_ReporteCabViviendasTab(models.Model):
    id = models.CharField(db_column='ID', primary_key=True)
    ccdd = models.CharField(db_column='CCDD', max_length=6, db_index=True)
    departamento = models.CharField(db_column="DEPARTAMENTO", max_length=50)
    ccpp = models.CharField(db_column='CCPP', max_length=50)
    provincia = models.CharField(db_column='PROVINCIA', max_length=50)
    ccdi = models.CharField(db_column='CCDI', max_length=50)
    distrito = models.CharField(db_column='DISTRITO', max_length=50)
    codccpp = models.CharField(db_column='CODCCPP',  max_length=50)
    nomccpp = models.CharField(db_column='NOMCCPP',  max_length=50)
    cat_ccpp = models.CharField(db_column='CAT_CCPP', max_length=50)
    zona = models.CharField(db_column='ZONA', max_length=50)
    zona_convert = models.CharField(db_column='ZONA_CONVERT', max_length=50)
    seccion = models.CharField(db_column='SECCION', max_length=50)
    seccion_convert = models.CharField(db_column='SECCION_CONVERT', max_length=50)
    aeu_final = models.CharField(db_column='AEU_FINAL', max_length=20)
    aeu_convert = models.CharField(db_column='AEU_CONVERT', max_length=20)
    cant_viv = models.CharField(db_column='CANT_VIV', max_length=30)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=40)

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REP_CAB_VIVIENDA_TAB'

class v_ReporteFrecuenciaDistrital2(models.Model):
    id = models.CharField(db_column='ID', primary_key=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6, db_index=True)
    viviendas_aeu = models.IntegerField(db_column='FRECUENCIA')
    frecuencia = models.IntegerField(db_column='FRECUENCIA')
    p_frecuencia = models.CharField(db_column='P_FRECUENCIA', max_length=4)
    p_frecuencia_acumulada = models.CharField(db_column='P_FRECUENCIA_ACUMULADA', max_length=6)

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REPORTE_FRECUENCIA_DISTRITAL_2'


class v_ReporteResumenDistritoTab(models.Model):
    id = models.CharField(db_column='ID', primary_key=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6, db_index=True)
    codccpp = models.CharField(db_column='CODCCPP', max_length=6)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=6)
    zona = models.CharField(db_column='ZONA', max_length=6)
    cant_secciones = models.IntegerField(db_column='CANT_SECCIONES')
    cant_aeus = models.IntegerField(db_column='CANT_AEUS')
    cant_mzs = models.IntegerField(db_column='CANT_MZS')
    cant_viv = models.IntegerField(db_column='CANT_VIV')
    prom_viv_aeu = models.CharField(db_column='PROM_VIV_AEU', max_length=6)
    prom_mzs_aeu = models.CharField(db_column='PROM_MZS_AEU', max_length=6)

    def __unicode__(self):
        return '%s , %s' % (self.id, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'VW_REPORTE_RESUMEN_DISTRITO_TAB'


class Tab_ViviendaRural(models.Model):
    id = models.CharField(primary_key=True, db_column='ID', max_length=6)
    ubigeo = models.ForeignKey(Distrito, db_column='UBIGEO')
    codccpp = models.CharField(db_column='CODCCPP', max_length=4)
    area = models.CharField(db_column='AREA', max_length=5)
    id_reg_or = models.CharField(db_column='ID_REG_OR', max_length=4)
    usolocal = models.CharField(db_column='USO_LOCAL', max_length=60)
    or_viv_ae = models.CharField(db_column='OR_VIV_AER', max_length=60)
    id_viv = models.ForeignKey('ViviendaU', db_column='IDVIV', db_index=True)

    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.id)

    class Meta:
        managed = False
        db_table = 'TB_VIVIENDA_R'


class Seg_R_Aer_Viv(models.Model):
    objectid = models.CharField(primary_key=True, db_column='OBJECTID', max_length=6)
    ubigeo = models.ForeignKey(Distrito, db_column='UBIGEO')
    scr_ini = models.CharField(db_column='SCR_INI', max_length=4)
    scr_fin = models.CharField(db_column='SCR_FIN', max_length=5)
    aer_ini = models.CharField(db_column='AER_INI', max_length=4)
    aer_fin = models.CharField(db_column='AER_FIN', max_length=60)
    codccpp = models.CharField(db_column='CODCCPP', max_length=60)
    or_viv_aer = models.CharField(db_column='OR_VIV_AER', max_length=60)
    or_ccpp_ae = models.CharField(db_column='OR_CCPP_AE', max_length=60)
    idscr = models.CharField(db_column='IDSCR', max_length=60)
    idaer = models.CharField(db_column='IDAER', max_length=60)
    idccpp = models.CharField(db_column='IDCCPP', max_length=60)
    idviv = models.CharField(db_column='IDVIV', max_length=60)

    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.objectid)

    class Meta:
        managed = False
        db_table = 'TB_VIVIENDA_R'


class Seg_Esp_R_Aer(models.Model):
    objectid = models.CharField(primary_key=True, db_column='OBJECTID', max_length=6)
    ubigeo = models.ForeignKey(Distrito, db_column='UBIGEO')
    ccpp_aer = models.CharField(db_column='CCPP_AER', max_length=4)
    emp_aer = models.CharField(db_column='EMP_AER', max_length=5)
    viv_aer = models.CharField(db_column='VIV_AER', max_length=5)
    aer_ini_17 = models.CharField(db_column='AER_INI_17', max_length=4)
    aer_fin_17 = models.CharField(db_column='AER_FIN_17', max_length=60)
    idaer = models.CharField(db_column='IDAER', max_length=60)
    scr_ini = models.CharField(db_column='SCR_INI', max_length=60)
    scr_fin = models.CharField(db_column='SCR_FIN', max_length=60)
    idscr = models.CharField(db_column='IDSCR', max_length=60)
    est_reg = models.CharField(db_column='EST_SEG', max_length=60)
    est_croquis = models.CharField(db_column='EST_CROQUIS', max_length=60)
    est_cont = models.CharField(db_column='EST_CONT', max_length=60)

    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.objectid)

    class Meta:
        managed = False
        db_table = 'SEGM_ESP_R_AER'


class Vw_Seg_Esp_R_Aer(models.Model):
    # id = models.CharField(db_column='ID',primary_key=True)
    ubigeo = models.ForeignKey(Distrito, db_column='UBIGEO')
    scr_ini = models.CharField(db_column='SCR_INI', max_length=60)
    scr_fin = models.CharField(db_column='SCR_FIN', max_length=60)
    aer_ini = models.CharField(db_column='AER_INI_17', max_length=4)
    aer_fin = models.CharField(db_column='AER_FIN_17', max_length=60)
    codccpp = models.CharField(db_column='CODCCPP', max_length=60)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=60)
    categoria_o = models.CharField(db_column='CATEGORIA_O', max_length=60)
    or_viv_aer = models.CharField(db_column='OR_VIV_AER', max_length=60)
    idscr = models.CharField(db_column='IDSCR', max_length=60)
    idaer = models.CharField(db_column='IDAER', primary_key=True)
    idccpp = models.CharField(db_column='LLAVE_CCPP', max_length=60)
    idviv = models.CharField(db_column='IDVIV', max_length=60)
    p32 = models.CharField(db_column='P32', max_length=60)
    id_reg_or = models.CharField(db_column='ID_REG_OR', max_length=60)
    p20 = models.CharField(db_column='P20', max_length=60)
    p20_nombre = models.CharField(db_column='P20_NOMBRE', max_length=60)
    p21 = models.CharField(db_column='P21', max_length=60)
    p22_a = models.CharField(db_column='P22_A', max_length=60)
    p26 = models.CharField(db_column='P26', max_length=60)
    p28 = models.CharField(db_column='P28', max_length=60)


    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.scr_ini)

    class Meta:
        managed = False
        db_table = 'VW_SEGM_R_AER_VIV'

class Vw_Seg_R_Aer_Ccpp(models.Model):
    # id = models.CharField(db_column='ID',primary_key=True)
    ubigeo = models.ForeignKey(Distrito, db_column='UBIGEO')
    scr_ini = models.CharField(db_column='SCR_INI', max_length=60)
    scr_fin = models.CharField(db_column='SCR_FIN', max_length=60)
    aer_ini = models.CharField(db_column='AER_INI', max_length=4)
    aer_fin = models.CharField(db_column='AER_FIN', max_length=60)
    codccpp = models.CharField(db_column='CODCCPP', max_length=60)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=60)
    categoria_o = models.CharField(db_column='CATEGORIA_O', max_length=60)
    viv_ccpp = models.CharField(db_column='VIV_CCPP', max_length=60)
    idscr = models.CharField(db_column='IDSCR', max_length=60)
    idaer = models.CharField(db_column='IDAER', primary_key=True)
    idccpp = models.CharField(db_column='IDCCPP', max_length=60)

    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.scr_ini)

    class Meta:
        managed = False
        db_table = 'VW_SEGM_R_AER_CCPP'

class Seg_R_Secc_Ccpp(models.Model):
    objectid = models.CharField(db_column='OBJECTID', max_length=6)
    ubigeo = models.ForeignKey(Distrito, db_column='UBIGEO')
    scr_ini = models.CharField(db_column='SCR_INI', max_length=60)
    scr_fin = models.CharField(db_column='SCR_FIN', max_length=60)
    aer_ini = models.CharField(db_column='AER_INI', max_length=4)
    aer_fin = models.CharField(db_column='AER_FIN', max_length=60)
    codccpp = models.CharField(db_column='CODCCPP', max_length=60)
    idscr = models.CharField(db_column='IDSCR', max_length=60)
    idaer = models.CharField(db_column='IDAER', max_length=60)
    idccpp = models.CharField(primary_key=True, db_column='IDCCPP', max_length=60)

    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.objectid)

    class Meta:
        managed = False
        db_table = 'SEGM_R_SECCION_CCPP'


class Vw_Seg_Esp_R_Secdist_Secc(models.Model):
    # id = models.CharField(db_column='ID',primary_key=True)
    #ubigeo = models.ForeignKey(Distrito, db_column='UBIGEO')
    ubigeo = models.CharField(db_column='UBIGEO', max_length=10)
    scr_ini = models.CharField(db_column='SCR_INI', max_length=10)
    scr_fin = models.CharField(db_column='SCR_FIN', max_length=10)
    aer_ini = models.CharField(db_column='AER_INI', max_length=4)
    aer_fin = models.CharField(db_column='AER_FIN', max_length=4)
    codccpp = models.CharField(db_column='CODCCPP', max_length=10)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=60)
    categoria_o = models.CharField(db_column='CATEGORIA_O', max_length=60)
    viv_ccpp = models.CharField(db_column='VIV_CCPP', max_length=60)
    idscr = models.CharField(primary_key=True,db_column='IDSCR', max_length=60)
    idaer = models.CharField(db_column='IDAER', max_length=60)
    idccpp = models.CharField(db_column='IDCCPP', max_length=60)

    # models.ForeignKey(Seg_R_Secc_Ccpp, db_column='IDCCPP')
    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.scr_ini)

    class Meta:
        managed = False
        db_table = 'VW_SEGM_R_SECDIST_CCPP'


class Calidad_Error_urb(models.Model):

    id= models.IntegerField(primary_key=True,db_column='ID')
    ubigeo = models.CharField(db_column='UBIGEO', max_length=7)
    zona = models.CharField( db_column='ZONA', max_length=7)
    seccion = models.CharField(db_column='SECCION',max_length=4 )
    aeu = models.CharField(db_column='AEU',max_length=3)
    ind1 = models.IntegerField(db_column='IND1')
    ind2 = models.IntegerField(db_column='IND2')
    ind3 = models.IntegerField(db_column='IND3')
    ind4 = models.IntegerField(db_column='IND4')
    ind5 = models.IntegerField(db_column='IND5')
    ind6 = models.IntegerField(db_column='IND6')
    ind7 = models.IntegerField(db_column='IND7')
    #check = models.IntegerField(db_column='CHECK_CALID')


    def __unicode__(self):
        return '{}, {}, {}'.format(self.ubigeo, self.zona, self.aeu)

    #Funcion meta
    class Meta:
        #Usa una tabla no se crea (False=usa/True=crea)
        managed = False
        #Tabla a la que se referencia
        db_table = 'CALIDAD_U_SEGM'


class Calidad_Error_rural(models.Model):
    id= models.IntegerField(primary_key=True,db_column='ID')
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6)
    emp = models.CharField(db_column='EMP',max_length=3)
    ind1 = models.IntegerField(db_column='IND1')
    ind2 = models.IntegerField(db_column='IND2')
    ind3 = models.IntegerField(db_column='IND3')
    ind4 = models.IntegerField(db_column='IND4')

    def __unicode__(self):
        return '{}, {}'.format(self.ubigeo, self.emp)

    #Funcion meta
    class Meta:
        #Usa una tabla no se crea (False=usa/True=crea)
        managed = False
        #Tabla a la que se referencia
        db_table = 'CALIDAD_r_SEGM'


class SegmentacionJefe(models.Model):
    ubigeo= models.IntegerField(primary_key=True,db_column='UBIGEO')
    ccdd = models.CharField(db_column='CCDD', max_length=6)
    ccpp = models.CharField(db_column='CCPP',max_length=3)
    ccdi = models.IntegerField(db_column='CCDI')
    equipo = models.IntegerField(db_column='EQUIPO')
    segmentista = models.IntegerField(db_column='SEGMENTISTA')
    estado = models.IntegerField(db_column='ESTADO')

    def __unicode__(self):
        return '{}'.format(self.ubigeo)

    #Funcion meta
    class Meta:
        #Usa una tabla no se crea (False=usa/True=crea)
        managed = False
        #Tabla a la que se referencia
        db_table = 'TB_MODULO_ASIGN_R'





class Usuario_Segm(models.Model):
    segmentista= models.IntegerField(primary_key=True,db_column='SEGMENTISTA')
    equipo = models.CharField(db_column='EQUIPO', max_length=6)
    user_segm = models.CharField(db_column='USER_SEGMENTISTA')
    user_equipo = models.IntegerField(db_column='USER_EQUIPO')


    def __unicode__(self):
        return '{}'.format(self.segmentista)

    #Funcion meta
    class Meta:
        #Usa una tabla no se crea (False=usa/True=crea)
        managed = False
        #Tabla a la que se referencia
        db_table = 'segm_r_user'


class Calidad_input(models.Model):
    ubigeo= models.CharField(primary_key=True,db_column='UBIGEO')
    estado = models.CharField(db_column='ESTADO', max_length=6)
    fechaEnvio = models.DateField (db_column='FECHA_ENVIO')
    fechaValid = models.DateField (db_column='FECHA_VALIDACION')



    def __unicode__(self):
        return '{}'.format(self.ubigeo)

    #Funcion meta
    class Meta:
        #Usa una tabla no se crea (False=usa/True=crea)
        managed = False
        #Tabla a la que se referencia
        db_table = 'SEGM_CONTROL_CALIDAD_INPUT_U'


class Calidad_input_rural(models.Model):
    ubigeo = models.CharField(primary_key=True, db_column='UBIGEO')
    estado = models.CharField(db_column='ESTADO', max_length=6)
    fechaEnvio = models.DateField(db_column='FECHA_ENVIO')
    fechaValid = models.DateField(db_column='FECHA_VALIDACION')

    def __unicode__(self):
        return '{}'.format(self.ubigeo)

    # Funcion meta
    class Meta:
        # Usa una tabla no se crea (False=usa/True=crea)
        managed = False
        # Tabla a la que se referencia
        db_table = 'SEGM_CONTROL_CALIDAD_INPUT_R'






