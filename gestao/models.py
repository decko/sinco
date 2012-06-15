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


class Conselheiro(models.Model):
    nome = models.CharField('Nome Completo', max_length=50)
    endereco = models.TextField('Endereço Completo', blank=True, null=True)
    telefone = models.CharField('Telefone para Contato', max_length=13, blank=True, null=True)
    email = models.EmailField('E-Mail', blank=True, null=True)
    vinculo = models.TextField('Vinculo Politico', blank=True, null=True)
    descricao = models.TextField('Descrição', blank=True, null=True)

    class Meta:
        verbose_name = 'Conselheiro'
        verbose_name_plural = 'Conselheiros'

    def __unicode__(self):
        return self.nome

    def conselhos(self):
        return "%s" % (", ".join([str(mandato.conselho) for mandato in self.mandato_set.all()]))


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
        )
    )
    nome = models.CharField('Nome do Conselho', max_length=150)
    categoria = models.CharField('Categoria', max_length=6, choices=CATEGORIA_CHOICES)
    email = models.EmailField('E-Mail', blank=True)
    telefone = models.CharField('Telefone para Contato', max_length=13, blank=True)
    endereco = models.TextField('Endereço Atual', blank=True)
    site = models.URLField('Endereço do Site na Internet', blank=True)
    atribuicoes = models.TextField('Atribuições')

    class Meta:
        verbose_name = 'conselho'
        verbose_name_plural = 'conselhos'

    def __unicode__(self):
        return self.nome

    def presidente(self):
        return self.mandato_set.get(atribuicao='P', data_final__isnull=True)

    def mandato(self):
        return self.mandato_set.filter(data_final__isnull=True)

    def n_cargos(self):
        return self.mandato_set.filter(data_final__isnull=True).count()

    def previstos_cargos(self):
        return self.legislacao_set.filter(n_cargos__isnull=False).latest('data').n_cargos


class Legislacao(models.Model):
    CATEGORIA_CHOICES = (('LF', 'Lei Federal'), ('LD', 'Lei Distrital'), ('D', 'Decreto'), ('I', 'Instrução Normativa'), ('P', 'Portaria'), ('R', 'Regimento Interno'))
    titulo = models.CharField('Titulo da Legislação', max_length=300)
    conselho = models.ForeignKey(Conselho)
    data = models.DateField('Data da Publicação')
    categoria = models.CharField('Categoria da Publicação', max_length=2, choices=CATEGORIA_CHOICES)
    link = models.URLField('Link para o texto', blank=True, null=True)
    n_cargos = models.IntegerField('Numero de Cargos Previstos na Legislação', blank=True, null=True)
    texto = models.TextField('Texto', blank=True, null=True)

    class Meta:
        verbose_name = 'legislação'
        verbose_name_plural = 'legislações'
        ordering = ['-data']

    def __unicode__(self):
        return self.titulo


class CargosPrevistos(models.Model):
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
    atribuicao = models.CharField('Atribuição do Conselheiro', max_length=1, choices=(('P', 'Presidente'), ('V', 'Vice-Presidente'), ('C', 'Conselheiro')))
    cargo = models.CharField('Categoria do Cargo', max_length=5, choices=CARGO_CHOICES)
    legislacao = models.ForeignKey(Legislacao)
    origem = models.CharField('Origem', max_length=50, blank=True, null=True)
    poder = models.CharField(max_length=50, choices=PODER_CHOICES)

    class Meta:

        def __unicode__(self):
            return self.cargo

    def conselho(self):
        return Conselho.objects.get(legislacao=self.legislacao_id)


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
    nome = models.ForeignKey(Conselheiro)
    data_inicial = models.DateField('Data de Inicio do Mandato')
    data_final = models.DateField('Data de Termino do Mandato', blank=True, null=True)
    atribuicao = models.CharField('Atribuição do Conselheiro', max_length=1, choices=(('P', 'Presidente'), ('V', 'Vice-Presidente'), ('C', 'Conselheiro')))
    cargo = models.CharField('Cargo do Conselheiro', max_length=5, choices=CARGO_CHOICES)
    conselho = models.ForeignKey(Conselho)
    jeton = models.BooleanField('Recebe Jeton?')

    class Meta:
        verbose_name = 'mandato'
        verbose_name_plural = 'mandatos'

    def __unicode__(self):
        #return self.get_atribuicao_display()
        return self.get_atribuicao_display() + (" no ") + self.conselho.__unicode__() + (" como ") + self.get_cargo_display()


class Reuniao(models.Model):
    conselho = models.ForeignKey(Conselho)
    data = models.DateField('Data da Reunião')
    pauta = models.TextField('Pauta da Reunião')
    ata = models.FileField('Arquivo da Ata', upload_to="legis", blank=True, null=True)
    texto_ata = models.TextField('Texto da Ata')

    class Meta:
        verbose_name = 'reunião'
        verbose_name_plural = 'reuniões'

    def __unicode__(self):
        return self.conselho.__unicode__()
