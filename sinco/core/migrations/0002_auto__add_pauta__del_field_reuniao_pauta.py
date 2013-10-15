# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pauta'
        db.create_table(u'core_pauta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pauta', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('reuniao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Reuniao'])),
            ('tags', self.gf('tags.fields.TagField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Pauta'])

        # Deleting field 'Reuniao.pauta'
        db.delete_column(u'core_reuniao', 'pauta')


    def backwards(self, orm):
        # Deleting model 'Pauta'
        db.delete_table(u'core_pauta')

        # Adding field 'Reuniao.pauta'
        db.add_column(u'core_reuniao', 'pauta',
                      self.gf('django.db.models.fields.TextField')(default=datetime.datetime(2013, 10, 9, 0, 0)),
                      keep_default=False)


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
        u'core.pauta': {
            'Meta': {'object_name': 'Pauta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pauta': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'reuniao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Reuniao']"}),
            'tags': ('tags.fields.TagField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        u'core.reuniao': {
            'Meta': {'ordering': "['-data']", 'object_name': 'Reuniao'},
            'ata': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'conselho': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Conselho']"}),
            'data': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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