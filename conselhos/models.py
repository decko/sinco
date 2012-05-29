# -*- coding: utf-8 -*-
#
#  Copyleft (c) 2011 André Filipe A. Brito e contribuidores
#
#  
#  Conselhos is free software under terms of the GNU Affero General Public
#  License version 3 (AGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#
from django.db import models

  

class Legislacao(models.Model):
	CATEGORIA_CHOICES = ((L, 'Lei'),(D, 'Decreto'),(I, 'Instrução Normativa'),(P,'Portaria'))
    titulo = models.CharField('Titulo da Legislação', max_length=300)
    data = models.DateField('Data da Publicação')
    categoria = models.CharField('Categoria da Publicação', max_length=1, choices=CATEGORIA_CHOICES)
    n_cargos = models.IntegerField('Numero de Cargos', max_length=2)
    texto = models.TextField('Texto')

    class Meta:
        verbose_name = _('Legislação')
        verbose_name_plural = _('Legislações')

    def __unicode__(self):
        pass

class Conselheiro(models.Model):
	nome = models.CharField('Nome Completo', max_length=50)
	endereco = models.TextField('Endereço Completo')
	telefone = models.IntegerField('Telefone para Contato', max_length=10)
	vinculo = models.TextField('Vinculo Politico')

    class Meta:
        verbose_name = _('Conselheiro')
        verbose_name_plural = _('Conselheiros')

    def __unicode__(self):
        pass
    

class Conselho(models.Model):
	CATEGORIA_CHOICES = ('Comunitário', ((TE,'Territorial'),(TM,'Temático')), 'de Estado',((D,'Administração Direta'),(I,'Administração Indireta')))
	nome = models.CharField('Nome do Conselho', max_length=150)
	endereco = models.TextField('Endereço Atual')
	conselheiros = models.ForeignKey(Conselheiro)
    class Meta:
        verbose_name = _('Conselho')
        verbose_name_plural = _('Conselhos')

    def __unicode__(self):
        pass
    