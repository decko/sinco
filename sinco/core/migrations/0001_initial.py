# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Conselheiro'
        db.create_table(u'core_conselheiro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('endereco', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('vinculo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('descricao', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Conselheiro'])

        # Adding model 'Conselho'
        db.create_table(u'core_conselho', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('categoria', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('endereco', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('site', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('atribuicoes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['Conselho'])

        # Adding model 'Legislacao'
        db.create_table(u'core_legislacao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('ementa', self.gf('django.db.models.fields.CharField')(max_length=600, blank=True)),
            ('conselho', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Conselho'])),
            ('data', self.gf('django.db.models.fields.DateField')()),
            ('categoria', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('n_cargos', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('texto', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Legislacao'])

        # Adding model 'CargosPrevistos'
        db.create_table(u'core_cargosprevistos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('atribuicao', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('cargo', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('legislacao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Legislacao'])),
            ('origem', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('poder', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'core', ['CargosPrevistos'])

        # Adding model 'Telefone'
        db.create_table(u'core_telefone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conselho', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Conselho'], null=True, blank=True)),
            ('conselheiro', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Conselheiro'], null=True, blank=True)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=13, null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'core', ['Telefone'])

        # Adding model 'EstruturaRegimental'
        db.create_table(u'core_estruturaregimental', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conselho', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Conselho'])),
            ('data', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'core', ['EstruturaRegimental'])

        # Adding model 'CargoRegimental'
        db.create_table(u'core_cargoregimental', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estrutura', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.EstruturaRegimental'])),
            ('cargo', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('origem', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('poder', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('legislacao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Legislacao'], null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['CargoRegimental'])

        # Adding model 'Mandato'
        db.create_table(u'core_mandato', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titular', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='titular', null=True, to=orm['core.Conselheiro'])),
            ('suplente', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='suplente', null=True, to=orm['core.Conselheiro'])),
            ('suplente_exercicio', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('data_inicial', self.gf('django.db.models.fields.DateField')()),
            ('data_final', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('data_termino', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('conselho', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Conselho'])),
            ('atribuicao', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('cargo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.CargoRegimental'])),
            ('jeton', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['Mandato'])

        # Adding model 'Reuniao'
        db.create_table(u'core_reuniao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conselho', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Conselho'])),
            ('data', self.gf('django.db.models.fields.DateField')()),
            ('pauta', self.gf('django.db.models.fields.TextField')()),
            ('ata', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('texto_ata', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'core', ['Reuniao'])


    def backwards(self, orm):
        # Deleting model 'Conselheiro'
        db.delete_table(u'core_conselheiro')

        # Deleting model 'Conselho'
        db.delete_table(u'core_conselho')

        # Deleting model 'Legislacao'
        db.delete_table(u'core_legislacao')

        # Deleting model 'CargosPrevistos'
        db.delete_table(u'core_cargosprevistos')

        # Deleting model 'Telefone'
        db.delete_table(u'core_telefone')

        # Deleting model 'EstruturaRegimental'
        db.delete_table(u'core_estruturaregimental')

        # Deleting model 'CargoRegimental'
        db.delete_table(u'core_cargoregimental')

        # Deleting model 'Mandato'
        db.delete_table(u'core_mandato')

        # Deleting model 'Reuniao'
        db.delete_table(u'core_reuniao')


    models = {
        u'core.cargoregimental': {
            'Meta': {'object_name': 'CargoRegimental'},
            'cargo': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'estrutura': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.EstruturaRegimental']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legislacao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Legislacao']", 'null': 'True', 'blank': 'True'}),
            'origem': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'poder': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'core.cargosprevistos': {
            'Meta': {'object_name': 'CargosPrevistos'},
            'atribuicao': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'cargo': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legislacao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Legislacao']"}),
            'origem': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'poder': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'core.conselheiro': {
            'Meta': {'ordering': "['nome']", 'object_name': 'Conselheiro'},
            'descricao': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'endereco': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vinculo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.conselho': {
            'Meta': {'object_name': 'Conselho'},
            'atribuicoes': ('django.db.models.fields.TextField', [], {}),
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'endereco': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'core.estruturaregimental': {
            'Meta': {'ordering': "['-data']", 'object_name': 'EstruturaRegimental'},
            'conselho': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Conselho']"}),
            'data': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.legislacao': {
            'Meta': {'ordering': "['-data']", 'object_name': 'Legislacao'},
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'conselho': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Conselho']"}),
            'data': ('django.db.models.fields.DateField', [], {}),
            'ementa': ('django.db.models.fields.CharField', [], {'max_length': '600', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'n_cargos': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'texto': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'core.mandato': {
            'Meta': {'ordering': "['-data_inicial', 'titular']", 'object_name': 'Mandato'},
            'atribuicao': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'cargo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.CargoRegimental']"}),
            'conselho': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Conselho']"}),
            'data_final': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'data_inicial': ('django.db.models.fields.DateField', [], {}),
            'data_termino': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jeton': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'suplente': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'suplente'", 'null': 'True', 'to': u"orm['core.Conselheiro']"}),
            'suplente_exercicio': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'titular': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'titular'", 'null': 'True', 'to': u"orm['core.Conselheiro']"})
        },
        u'core.reuniao': {
            'Meta': {'ordering': "['-data']", 'object_name': 'Reuniao'},
            'ata': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'conselho': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Conselho']"}),
            'data': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pauta': ('django.db.models.fields.TextField', [], {}),
            'texto_ata': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'core.telefone': {
            'Meta': {'object_name': 'Telefone'},
            'conselheiro': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Conselheiro']", 'null': 'True', 'blank': 'True'}),
            'conselho': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Conselho']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['core']