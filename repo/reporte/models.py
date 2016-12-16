from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

# Create your models here.
class Pruebaaa(models.Model):
    ubigeo = models.CharField(max_length=255)
    zona = models.CharField(max_length=255, blank=True)
    area = models.CharField(max_length=255, blank=True)
    aeu = models.CharField(max_length=255, blank=True)
    aeu_seccion = models.CharField(max_length=255, blank=True)
    aeu_zona = models.CharField(max_length=255, blank=True)
    aeu_viv = models.CharField(max_length=255, blank=True)
    aer_ini = models.CharField(max_length=255, blank=True)
    aer_fin = models.CharField(max_length=255, blank=True)
    estado_seg = models.CharField(max_length=255, blank=True)
    estado_rep = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return '%s , %s' % (self.ubigeo, self.zona)

    class Meta:
        managed = True
        db_table = 'MZN_PRUEBA_FISI'

class Depa(models.Model):
    ubigeo = models.CharField(max_length=255)
    ccdd = models.CharField(max_length=255)
    ccpp = models.CharField(max_length=255, blank=True)
    ccdi = models.CharField(max_length=255, blank=True)
    zona = models.CharField(max_length=255, blank=True)
    manzana = models.CharField(max_length=255, blank=True)
    codccpp = models.CharField(max_length=255, blank=True)
    nomccpp = models.CharField(max_length=255, blank=True)
    departamento = models.CharField(max_length=255, blank=True)
    provincia = models.CharField(max_length=255, blank=True)
    distrito = models.CharField(max_length=255, blank=True)
    area = models.CharField(max_length=255, blank=True)
    frente_ord = models.CharField(max_length=255, blank=True)
    id_reg_or = models.CharField(max_length=255, blank=True)
    aer_ini = models.CharField(max_length=255, blank=True)
    aer_fin = models.CharField(max_length=255, blank=True)
    p19a = models.CharField(max_length=255, blank=True)
    p20 = models.CharField(max_length=255, blank=True)
    P20_O = models.CharField(max_length=255, blank=True)
    p21 = models.CharField(max_length=255, blank=True)
    p21_a = models.CharField(max_length=255, blank=True)
    p22_a = models.CharField(max_length=255, blank=True)
    p22_a = models.CharField(max_length=255, blank=True)
    p23 = models.CharField(max_length=255, blank=True)
    id_p23 = models.CharField(max_length=255, blank=True)
    p23_nombre = models.CharField(max_length=255, blank=True)
    p23_tpiso = models.CharField(max_length=255, blank=True)
    p23_vivpiso = models.CharField(max_length=255, blank=True)
    p23_viviendas = models.CharField(max_length=255, blank=True)
    p23_registros = models.CharField(max_length=255, blank=True)
    p24 = models.CharField(max_length=255, blank=True)
    p25 = models.CharField(max_length=255, blank=True)
    p26 = models.CharField(max_length=255, blank=True)
    p27_a = models.CharField(max_length=255, blank=True)
    p27_b = models.CharField(max_length=255, blank=True)
    p28 = models.CharField(max_length=255, blank=True)
    p29 = models.CharField(max_length=255, blank=True)
    p29_A = models.CharField(max_length=255, blank=True)
    p29_1 = models.CharField(max_length=255, blank=True)
    p29_1_nombre = models.CharField(max_length=255, blank=True)
    p29m = models.CharField(max_length=255, blank=True)
    p29_o = models.CharField(max_length=255, blank=True)
    p29_8_o = models.CharField(max_length=255, blank=True)
    p29_p = models.CharField(max_length=255, blank=True)
    P30 = models.CharField(max_length=255, blank=True)
    P31 = models.CharField(max_length=255, blank=True)
    P32 = models.CharField(max_length=255, blank=True)
    p35 = models.CharField(max_length=255, blank=True)
    or_viv_aeu = models.CharField(max_length=255, blank=True)


    # FROM[CPV_SEGMENTACION].[dbo].[TB_CPV0301_VIVIENDA_U]
    def __unicode__(self):
        return '%s , %s' % (self.ubigeo , self.ccdd)

    class Meta:
        managed = True
        db_table = 'FISI2'
