# -*- coding: utf-8 -*-
#
#  Copyleft (c) 2011 André Filipe A. Brito e contribuidores
#
#
#  Conselhos is free software under terms of the GNU Affero General Public
#  License version 3 (AGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#
import os

from datetime import datetime

from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

from tags.fields import TagField

CARGO_CHOICES = (
    ('Membro Nato',
        (
            ('MNSC', 'Membro Nato da Sociedade Civil'),
            ('MNPP', 'Membro Nato do Poder Público')
        )
    ),
    ('Indicação Institucional',
        (
            ('IISC', 'Indicação Institucional da Sociedade Civil'),
            ('IISCE', 'Indicação Institucional da Sociedade Civil por Eleição'),
            ('IIPP', 'Indicação Institucional do Poder Público')
        )
    ),
    ('Indicação',
        (
            ('IPGA', 'Indicação por Gestor da Área'),
            ('IPGAT', 'Indicação por Gestor da Área por Lista Triplice'),
            ('IPG', 'Indicação pelo Governador'),
            ('IPGT', 'Indicação pelo Governador por Lista Triplice'),
            ('IPS', 'Indicação pelo Segmento da Sociedade Cívil'),
            ('IPSE', 'Indicação pelo Segmento da Sociedade Cívil por Eleição')
        )
    )
)
PODER_CHOICES = (
    ('Poderes Distritais',
        (
            ('PED', 'Poder Executivo Distrital'),
            ('PLD', 'Poder Legislativo Distrital'),
            ('PJD', 'Poder Judiciario Distrital')
        )
    ),
    ('Poderes Federais',
        (
            ('PEF', 'Poder Executivo Federal'),
            ('PLF', 'Poder Legislativo Federal'),
            ('PJF', 'Poder Judiciario Federal')
        )
    ),
    ('SC', 'Sociedade Cívil')
)


class Conselheiro(models.Model):
    nome = models.CharField(u'Nome Completo', max_length=50)
    endereco = models.TextField(u'Endereço Completo', blank=True, null=True)
    email = models.EmailField(u'E-Mail', blank=True, null=True)
    vinculo = models.TextField(u'Vinculo Politico', blank=True, null=True)
    descricao = models.TextField(u'Descrição', blank=True, null=True)

    class Meta:
        verbose_name = 'conselheiro'
        ordering = ['nome']

    def __unicode__(self):
        return u'%s' % self.nome

    def conselhos(self):
        if self.titular.all():
            return u"Titular no %s" % (", titular no ".join([unicode(mandato.conselho) for mandato in self.titular.all()]) + ", suplente no ".join([unicode(mandato.conselho) for mandato in self.suplente.all()]))
        elif self.suplente.all():
            return u"Suplente no %s" % (", suplente no".join([unicode(mandato.conselho) for mandato in self.suplente.all()]))
        else:
            return "%s" % ("Sem mandato")


class Conselho(models.Model):
    CATEGORIA_CHOICES = (
        ('Conselhos Comunitários',
            (
                ('CTPC', 'Conselho Comunitário Territorial - Prefeitura Comunitária'),
                ('CTAC', 'Conselho Comunitário Territorial - Associação Comunitária'),
                ('CTCC', 'Conselho Comunitário Territorial - Conselho da Cidade/Bairro'),
                ('CCST', 'Conselho Comunitário Setorial')
            )
        ),
        ('Conselhos de Estado',
            (
                ('CEADG', 'Conselho de Estado de Administração Direta - Gestor de Politicas Públicas'),
                ('CEADA', 'Conselho de Estado de Administração Direta - Administração de Órgão Públicos'),
                ('CEADFP', 'Conselho de Estado de Administração Direta - Administração de Fundos Públicos'),
                ('CEADFI', 'Conselho de Estado de Administração Direta - Fiscais e Patrimoniais'),
                ('CEADFF', 'Conselho de Estado de Administração Direta - Fiscais de Fundos Federais'),
                ('CEADAN', 'Conselho de Estado de Administração Direta - Normativos e Reguladores'),
                ('CEAIAD', 'Conselho de Estado de Administração Indireta - Administração'),
                ('CEAIFI', 'Conselho de Estado de Administração Indireta - Fiscal'),
            )
        ),
        ('NC', 'Não Classificado')
    )
    nome = models.CharField('Nome do Conselho', max_length=150)
    categoria = models.CharField('Categoria', max_length=6, choices=CATEGORIA_CHOICES)
    email = models.EmailField('E-Mail', blank=True)
    endereco = models.TextField('Endereço Atual', blank=True)
    site = models.URLField('Endereço do Site na Internet', blank=True)
    atribuicoes = models.TextField('Atribuições')

    class Meta:
        verbose_name = 'conselho'

    def __unicode__(self):
        return self.nome

    def presidente(self):
        return self.mandato_set.get(atribuicao='P', data_termino__isnull=True)

    def estrutura_vigente(self):
        return self.estruturaregimental_set.latest('data')

    def cargos_estrutura_vigente(self):
        return self.estruturaregimental_set.latest('data').cargoregimental_set.all()

    def cargos_vagos(self):
        return self.estruturaregimental_set.latest('data').cargoregimental_set.filter( Q(mandato__data_termino__lte = datetime.today()) | Q(mandato__isnull = True))

    def mandato(self):
        return self.mandato_set.filter(data_termino__isnull=True)

    def n_cargos(self):
        return self.mandato_set.filter(data_termino__isnull=True).count()

    def previstos_cargos(self):
        return self.legislacao_set.filter(n_cargos__isnull=False).latest('data').n_cargos


class Legislacao(models.Model):
    CATEGORIA_CHOICES = (('LF', 'Lei Federal'), ('LD', 'Lei Distrital'), ('D', 'Decreto'), ('I', 'Instrução Normativa'), ('P', 'Portaria'), ('R', 'Regimento Interno'))
    titulo = models.CharField('Titulo da Legislação', max_length=300)
    ementa = models.CharField('Ementa da Matéria', max_length=600, blank=True)
    conselho = models.ForeignKey(Conselho)
    data = models.DateField('Data da Publicação')
    categoria = models.CharField('Categoria da Publicação', max_length=2, choices=CATEGORIA_CHOICES)
    link = models.URLField('Link para o texto', blank=True, null=True)
    n_cargos = models.IntegerField('Nº de Cargos Previstos', blank=True, null=True)
    texto = models.TextField('Texto', blank=True, null=True)

    class Meta:
        verbose_name = 'legislação'
        verbose_name_plural = 'legislações'
        ordering = ['-data']

    def __unicode__(self):
        if self.ementa:
            return "%s %s, que %s" % (self.get_categoria_display(), self.titulo, self.ementa)
        else:
            return "%s %s" % (self.get_categoria_display(), self.titulo)

    def n_cargos_previstos(self):
        return self.cargosprevistos_set.count()

    def url(self):
        if self.link:
            return '<a href=\"%s\">Clique aqui.</a>' % (self.link)
        else:
            return "Não encontrado"
    url.allow_tags = True


class CargosPrevistos(models.Model):
    atribuicao = models.CharField('Atribuição do Conselheiro', max_length=1, choices=(('P', 'Presidente'), ('V', 'Vice-Presidente'), ('C', 'Conselheiro')))
    cargo = models.CharField('Categoria do Cargo', max_length=5, choices=CARGO_CHOICES)
    legislacao = models.ForeignKey(Legislacao)
    origem = models.CharField('Origem', max_length=50, blank=True, null=True)
    poder = models.CharField(max_length=50, choices=PODER_CHOICES)

    class Meta:

        verbose_name = 'cargo previsto'
        verbose_name_plural = 'cargos previstos'

    def __unicode__(self):
        if self.origem:
            return u"%s, %s, através do(a) %s pelo(a) %s" % (self.get_atribuicao_display(), self.get_cargo_display(), self.get_poder_display(), self.origem)
        else:
            return u"%s, %s, através do(a) %s" % (self.get_atribuicao_display(), self.get_cargo_display(), self.get_poder_display())

    def conselho(self):
        return Conselho.objects.get(legislacao=self.legislacao_id)


class Telefone(models.Model):
    conselho = models.ForeignKey(Conselho, blank=True, null=True)
    conselheiro = models.ForeignKey(Conselheiro, blank=True, null=True)
    numero = models.CharField('Telefone para Contato', max_length=13, blank=True, null=True)
    tipo = models.CharField('Tipo', max_length=2, choices=(('PI', 'Principal'), ('C', 'Contato'), ('I', 'Institucional'), ('PE', 'Pessoal')))

    class Meta:
        verbose_name = u'telefone'
        verbose_name_plural = u'telefones'

    def __unicode__(self):
        return self.numero

    def atribuido(self):
        if self.conselheiro.nome:
            return self.conselheiro.nome
        else:
            return self.conselho.nome


class EstruturaRegimental(models.Model):
    conselho = models.ForeignKey(Conselho)
    data = models.DateField('Data do Inicio da Vigencia')

    class Meta:
        verbose_name = "estrutura regimental"
        verbose_name_plural = "estruturas regimentais"
        ordering = ['-data']

    def __unicode__(self):
        return u"Estrutura com inicio de vigência em %s para o %s" % (str(self.data), self.conselho)


class CargoRegimental(models.Model):
    estrutura = models.ForeignKey(EstruturaRegimental)
    cargo = models.CharField('Categoria do Cargo', max_length=5, choices=CARGO_CHOICES)
    origem = models.CharField('Origem', max_length=50, blank=True, null=True)
    poder = models.CharField(max_length=50, choices=PODER_CHOICES)
    legislacao = models.ForeignKey(Legislacao, blank=True, null=True)

    class Meta:

        verbose_name = 'cargo regimental'
        verbose_name_plural = 'cargos regimentais'

    def __unicode__(self):
        if self.origem:
            return u"%s, através do(a) %s pelo(a) %s" % (self.get_cargo_display(), self.get_poder_display(), self.origem)
        else:
            return u"%s, através do(a) %s" % (self.get_cargo_display(), self.get_poder_display())

    def conselho(self):
        return self.estrutura.conselho

    def mandato_vigente(self):
        if self.mandato_set.all().exclude(data_termino__isnull=False):
            return self.mandato_set.all().exclude(data_termino__isnull=False)[0]


class Mandato(models.Model):
    CARGO_CHOICES = (
        ('Membro Nato',
            (
                ('MNSC', 'Membro Nato da Sociedade Civil'),
                ('MNPP', 'Membro Nato do Poder Público')
            )
        ),
        ('Indicação Institucional',
            (
                ('IISC', 'Indicação Institucional da Sociedade Civil'),
                ('IISCE', 'Indicação Institucional da Sociedade Civil por Eleição'),
                ('IIPP', 'Indicação Institucional do Poder Público')
            )
        ),
        ('Indicação',
            (
                ('IPGA', 'Indicação por Gestor da Área'),
                ('IPGAT', 'Indicação por Gestor da Área por Lista Triplice'),
                ('IPG', 'Indicação pelo Governador'),
                ('IPGT', 'Indicação pelo Governador por Lista Triplice'),
                ('IPS', 'Indicação pelo Segmento da Sociedade Cívil'),
                ('IPSE', 'Indicação pelo Segmento da Sociedade Cívil por Eleição')
            )
        )
    )
    titular = models.ForeignKey(Conselheiro, blank=True, null=True, related_name='titular')
    suplente = models.ForeignKey(Conselheiro, blank=True, null=True, related_name='suplente')
    suplente_exercicio = models.BooleanField('Suplente em Execicio')
    data_inicial = models.DateField('Data de Inicio do Mandato')
    data_final = models.DateField('Data Prevista para Encerramento do Mandato', blank=True, null=True)
    data_termino = models.DateField('Data de Encerramento do Mandato', blank=True, null=True)
    conselho = models.ForeignKey(Conselho)
    atribuicao = models.CharField('Atribuição do Conselheiro', max_length=1, choices=(('P', 'Presidente'), ('V', 'Vice-Presidente'), ('C', 'Conselheiro')))
    cargo = models.ForeignKey(CargoRegimental)
    jeton = models.BooleanField('Recebe Jeton?')

    class Meta:
        verbose_name = 'mandato'
        ordering = ['-data_inicial', 'titular']

    def __unicode__(self):
        if not self.suplente_exercicio:
            return u'%s' % self.titular.nome
        else:
            return u'%s' % self.suplente.nome

    def clean(self):
        if self.titular == self.suplente:
            raise ValidationError('O Titular e o Suplente da vaga não podem ser a mesma pessoa')

        if self.data_final:
            if self.data_final < self.data_inicial:
                raise ValidationError('A Data Prevista para o Encerramento do Mandato deve ser posterior à Data de Inicio do Mandato')

        if self.data_termino:
            if self.data_termino < self.data_inicial:
                raise ValidationError('A Data de Encerramento do Mandato não deve ser anterior à Data de Inicio de Mandato')


class Reuniao(models.Model):
    def get_image_path(instance, filename):
        return os.path.join(slugify(str(instance.conselho)), 'reuniao', filename)

    conselho = models.ForeignKey(Conselho)
    data = models.DateField('Data da Reunião')
    ata = models.FileField('Arquivo da Ata', upload_to=get_image_path, blank=True)
    texto_ata = models.TextField('Texto da Ata', blank=True)

    class Meta:
        verbose_name = 'reunião'
        verbose_name_plural = 'reuniões'
        ordering = ['-data']

    def __unicode__(self):
        return self.conselho.__unicode__()

    def url(self):
        if self.ata:
            return self.ata.url
        else:
            return ""

    def save(self):
        arquivo, ponto, extensao = self.ata.name.rpartition('.')
        self.ata.name = slugify(self.data) + '.' + extensao
        super(Reuniao, self).save()


class Pauta(models.Model):
    pauta = models.CharField('Pauta', max_length=300)
    reuniao = models.ForeignKey(Reuniao)
    tags = TagField('Tags', max_length=300)