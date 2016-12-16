from __future__ import unicode_literals

from django.db import models


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
    id_reg_or = models.IntegerField(db_column='ID_REG_OR')
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


class Tab_Aeus(models.Model):
    objectid = models.CharField(primary_key=True, db_column='OBJECTID', db_index=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=6)
    # objectid = models.CharField(primary_key=True, db_column='OBJECTID', max_length=254, db_index=True)
    codccpp = models.CharField(db_column='CODCCPP', max_length=6)
    zona = models.CharField(db_column='ZONA', max_length=5)
    aeu_final = models.IntegerField(db_column='AEU_FINAL')
    cant_viv = models.IntegerField(db_column='CANT_VIV')
    seccion = models.IntegerField(db_column='SECCION')
    llave_seccion = models.CharField(db_column='LLAVE_SECC', max_length=6)
    llave_aeu = models.CharField(primary_key=True, db_column='LLAVE_AEU', db_index=True)
    llave_ccpp = models.ForeignKey(Ccpp, db_column='LLAVE_CCPP')
    est_imp = models.CharField(db_column='EST_IMP', max_length=2)

    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'SEGM_TAB_AEU'

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


class Tab_Secciones(models.Model):
    objectid = models.CharField(primary_key=True, db_column='OBJECTID', max_length=254, db_index=True)
    ubigeo = models.CharField(db_column='UBIGEO', max_length=254)
    codccpp = models.CharField(db_column='CODCCPP', max_length=254)
    zona = models.CharField(db_column='ZONA', max_length=254)
    seccion = models.IntegerField(db_column='SECCION')
    cant_viv = models.IntegerField(db_column='CANT_VIV')
    llave_secc = models.CharField(db_column='LLAVE_SECC', max_length=254)

    def __unicode__(self):
        return '%s , %s' % (self.objectid, self.ubigeo)

    class Meta:
        managed = False
        db_table = 'SEGM_TAB_SECCION'


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
