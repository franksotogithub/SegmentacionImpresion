from __future__ import unicode_literals

from django.db import models


class MaeProyecto(models.Model):
    ubigeo = models.CharField(primary_key=True, db_column='UBIGEO', max_length=6)
    ccdd = models.CharField(db_column='CCDD', max_length=2)
    ccpp = models.CharField(db_column='CCPP', max_length=2)
    ccdi = models.CharField(db_column='CCDI', max_length=2)
    zona = models.CharField(db_column='ZONA', max_length=5)
    manzana = models.CharField(db_column='MANZANA', max_length=4)
    codccpp = models.CharField(db_column='CODCCPP', max_length=4)
    nomccpp = models.CharField(db_column='NOMCCPP', max_length=60)
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=60)
    provincia = models.CharField(db_column='PROVINCIA', max_length=50)
    distrito = models.CharField(db_column='DISTRITO', max_length=50)
    area = models.IntegerField(db_column='AREA')
    frente_ord = models.IntegerField(db_column='FRENTE_ORD')
    id_reg_or = models.IntegerField(db_column='ID_REG_OR')
    aer_ini = models.CharField(db_column='AER_INI', max_length=3)
    aer_fin = models.CharField(db_column='AER_FIN', max_length=3)
    p19a = models.IntegerField(db_column='P19A')
    p20 = models.IntegerField(db_column='P20')
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

    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.ccdd)

    class Meta:
        managed =False
        db_table = 'TB_CPV0301_VIVIENDA_U'