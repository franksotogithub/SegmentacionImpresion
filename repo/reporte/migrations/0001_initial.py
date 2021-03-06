# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-16 21:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aeus',
            fields=[
                ('objectid', models.CharField(db_column='OBJECTID', primary_key=True, serialize=False)),
                ('shape', models.CharField(db_column='Shape', max_length=100)),
                ('ubigeo', models.CharField(db_column='UBIGEO', max_length=6)),
                ('zona', models.CharField(db_column='ZONA', max_length=5)),
                ('aeu_final', models.IntegerField(db_column='AEU_FINAL')),
                ('sum_viv_ae', models.IntegerField(db_column='SUM_VIV_AE')),
                ('seccion', models.IntegerField(db_column='SECCION')),
            ],
            options={
                'db_table': 'TB_AEUS',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('ccdd', models.CharField(db_column='CCDD', db_index=True, max_length=2, primary_key=True, serialize=False)),
                ('departamento', models.CharField(db_column='DEPARTAMENTO', max_length=50)),
                ('fec_carga', models.CharField(blank=True, db_column='FEC_CARGA', max_length=40)),
            ],
            options={
                'db_table': 'TB_DEPARTAMENTO',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('ubigeo', models.CharField(db_column='UBIGEO', max_length=6, primary_key=True)),
                ('ccdd', models.CharField(db_column='CCDD', max_length=2)),
                ('ccpp', models.CharField(db_column='CCPP', max_length=2)),
                ('ccdi', models.CharField(db_column='CCDI', max_length=2, primary_key=True, serialize=False)),
                ('distrito', models.CharField(db_column='DISTRITO', max_length=50)),
                ('region', models.CharField(db_column='REGION', max_length=1)),
                ('region_nat', models.CharField(db_column='REGION_NAT', max_length=10)),
                ('nro_aer', models.IntegerField(db_column='NRO_AER')),
                ('fec_carga', models.CharField(db_column='FEC_CARGA', max_length=40)),
            ],
            options={
                'db_table': 'TB_DISTRITO',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MaeProyecto',
            fields=[
                ('ubigeo', models.CharField(db_column='UBIGEO', max_length=6, primary_key=True, serialize=False)),
                ('ccdd', models.CharField(db_column='CCDD', max_length=2)),
                ('ccdi', models.CharField(db_column='CCDI', max_length=2)),
                ('zona', models.CharField(db_column='ZONA', max_length=5)),
                ('manzana', models.CharField(db_column='MANZANA', max_length=4)),
                ('codccpp', models.CharField(db_column='CODCCPP', max_length=4)),
                ('nomccpp', models.CharField(db_column='NOMCCPP', max_length=60)),
                ('departamento', models.CharField(db_column='DEPARTAMENTO', max_length=60)),
                ('provincia', models.CharField(db_column='PROVINCIA', max_length=50)),
                ('distrito', models.CharField(db_column='DISTRITO', max_length=50)),
                ('area', models.IntegerField(db_column='AREA')),
                ('frente_ord', models.IntegerField(db_column='FRENTE_ORD')),
                ('id_reg_or', models.IntegerField(db_column='ID_REG_OR')),
                ('aer_ini', models.CharField(db_column='AER_INI', max_length=3)),
                ('aer_fin', models.CharField(db_column='AER_FIN', max_length=3)),
                ('p19a', models.IntegerField(db_column='P19A')),
                ('p20', models.IntegerField(db_column='P20')),
                ('p20_o', models.CharField(db_column='P20_O', max_length=50)),
                ('p21', models.CharField(db_column='P21', max_length=60)),
                ('p21_a', models.CharField(db_column='P21_A', max_length=100)),
                ('p22_a', models.CharField(db_column='P22_A', max_length=4)),
                ('p22_b', models.CharField(db_column='P22_B', max_length=4)),
                ('p23', models.CharField(db_column='P23', max_length=3)),
                ('id_p23', models.IntegerField(db_column='ID_P23')),
                ('p23_nombre', models.CharField(db_column='P23_NOMBRE', max_length=50)),
                ('p23_vivpiso', models.IntegerField(db_column='P23_VIVPISO')),
                ('p23_viviendas', models.IntegerField(db_column='P23_VIVIENDAS')),
                ('p23_registros', models.IntegerField(db_column='P23_REGISTROS')),
                ('p24', models.CharField(db_column='P24', max_length=4)),
                ('p25', models.CharField(db_column='P25', max_length=4)),
                ('p26', models.CharField(db_column='P26', max_length=2)),
                ('p27_a', models.CharField(db_column='P27_A', max_length=4)),
                ('p27_b', models.CharField(db_column='P27_B', max_length=4)),
                ('p28', models.CharField(db_column='P28', max_length=4)),
                ('p29', models.IntegerField(db_column='P29')),
                ('p29_a', models.IntegerField(db_column='P29_A')),
                ('p29_1', models.IntegerField(db_column='P29_1')),
                ('p29_1_nombre', models.CharField(db_column='P29_1_NOMBRE', max_length=50)),
                ('p29m', models.IntegerField(db_column='P29M')),
                ('p29_o', models.CharField(db_column='P29_O', max_length=50)),
                ('p29_8_o', models.CharField(db_column='P29_8_O', max_length=100)),
                ('p29_p', models.CharField(db_column='P29_P', max_length=100)),
                ('p30', models.IntegerField(db_column='P30')),
                ('p31', models.IntegerField(db_column='P31')),
                ('p32', models.CharField(db_column='P32', max_length=100)),
                ('p35', models.CharField(db_column='P35', max_length=100)),
                ('or_viv_aeu', models.IntegerField(db_column='OR_VIV_AEU')),
            ],
            options={
                'db_table': 'TB_CPV0301_VIVIENDA_U',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('cod_prov', models.CharField(db_column='COD_PROV', db_index=True, max_length=4, primary_key=True, serialize=False)),
                ('ccpp', models.CharField(db_column='CCPP', max_length=2)),
                ('provincia', models.CharField(db_column='PROVINCIA', max_length=50)),
                ('fec_carga', models.CharField(db_column='FEC_CARGA', max_length=40)),
            ],
            options={
                'db_table': 'TB_PROVINCIA',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Depa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubigeo', models.CharField(max_length=255)),
                ('ccdd', models.CharField(max_length=255)),
                ('ccpp', models.CharField(blank=True, max_length=255)),
                ('ccdi', models.CharField(blank=True, max_length=255)),
                ('zona', models.CharField(blank=True, max_length=255)),
                ('manzana', models.CharField(blank=True, max_length=255)),
                ('codccpp', models.CharField(blank=True, max_length=255)),
                ('nomccpp', models.CharField(blank=True, max_length=255)),
                ('departamento', models.CharField(blank=True, max_length=255)),
                ('provincia', models.CharField(blank=True, max_length=255)),
                ('distrito', models.CharField(blank=True, max_length=255)),
                ('area', models.CharField(blank=True, max_length=255)),
                ('frente_ord', models.CharField(blank=True, max_length=255)),
                ('id_reg_or', models.CharField(blank=True, max_length=255)),
                ('aer_ini', models.CharField(blank=True, max_length=255)),
                ('aer_fin', models.CharField(blank=True, max_length=255)),
                ('p19a', models.CharField(blank=True, max_length=255)),
                ('p20', models.CharField(blank=True, max_length=255)),
                ('P20_O', models.CharField(blank=True, max_length=255)),
                ('p21', models.CharField(blank=True, max_length=255)),
                ('p21_a', models.CharField(blank=True, max_length=255)),
                ('p22_a', models.CharField(blank=True, max_length=255)),
                ('p23', models.CharField(blank=True, max_length=255)),
                ('id_p23', models.CharField(blank=True, max_length=255)),
                ('p23_nombre', models.CharField(blank=True, max_length=255)),
                ('p23_tpiso', models.CharField(blank=True, max_length=255)),
                ('p23_vivpiso', models.CharField(blank=True, max_length=255)),
                ('p23_viviendas', models.CharField(blank=True, max_length=255)),
                ('p23_registros', models.CharField(blank=True, max_length=255)),
                ('p24', models.CharField(blank=True, max_length=255)),
                ('p25', models.CharField(blank=True, max_length=255)),
                ('p26', models.CharField(blank=True, max_length=255)),
                ('p27_a', models.CharField(blank=True, max_length=255)),
                ('p27_b', models.CharField(blank=True, max_length=255)),
                ('p28', models.CharField(blank=True, max_length=255)),
                ('p29', models.CharField(blank=True, max_length=255)),
                ('p29_A', models.CharField(blank=True, max_length=255)),
                ('p29_1', models.CharField(blank=True, max_length=255)),
                ('p29_1_nombre', models.CharField(blank=True, max_length=255)),
                ('p29m', models.CharField(blank=True, max_length=255)),
                ('p29_o', models.CharField(blank=True, max_length=255)),
                ('p29_8_o', models.CharField(blank=True, max_length=255)),
                ('p29_p', models.CharField(blank=True, max_length=255)),
                ('P30', models.CharField(blank=True, max_length=255)),
                ('P31', models.CharField(blank=True, max_length=255)),
                ('P32', models.CharField(blank=True, max_length=255)),
                ('p35', models.CharField(blank=True, max_length=255)),
                ('or_viv_aeu', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'db_table': 'FISI2',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Pruebaaa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubigeo', models.CharField(max_length=255)),
                ('zona', models.CharField(blank=True, max_length=255)),
                ('area', models.CharField(blank=True, max_length=255)),
                ('aeu', models.CharField(blank=True, max_length=255)),
                ('aeu_seccion', models.CharField(blank=True, max_length=255)),
                ('aeu_zona', models.CharField(blank=True, max_length=255)),
                ('aeu_viv', models.CharField(blank=True, max_length=255)),
                ('aer_ini', models.CharField(blank=True, max_length=255)),
                ('aer_fin', models.CharField(blank=True, max_length=255)),
                ('estado_seg', models.CharField(blank=True, max_length=255)),
                ('estado_rep', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'db_table': 'MZN_PRUEBA_FISI',
                'managed': True,
            },
        ),
    ]
