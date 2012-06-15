# -*- coding: utf-8 -*-
#
#  Copyleft (c) 2011 André Filipe A. Brito e contribuidores
#
#
#  Conselhos is free software under terms of the GNU Affero General Public
#  License version 3 (AGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#
#Importa os Modelos
from gestao.models import Conselho, Conselheiro, Legislacao, Mandato, CargosPrevistos, Reuniao

#Importa a classe ModelForm para personalização de formulário
from django.forms import ModelForm

#Importa a classe BRPhoneNumberField para validação dos Telefones nos modelos
from django.contrib.localflavor.br.forms import BRPhoneNumberField

#Importa o Admin
from django.contrib import admin


#Personalização do campo telefone no modelo Conselho
class ConselhoForm(ModelForm):
    telefone = BRPhoneNumberField()

    class Meta:
        model = Conselho


#Personalização do campo telefone no modelo Conselheiro
class ConselheiroForm(ModelForm):
    telefone = BRPhoneNumberField()

    class Meta:
        model = Conselheiro


#Insere o Modelo 'Mandato' dentro do formulário de Conselho
class MandatoInline(admin.TabularInline):
    model = Mandato


#Insere o Modelo 'CargosPrevistos' dentro do formulário de Legislação
class CargosPrevistosInLine(admin.TabularInline):
    model = CargosPrevistos


#Define a interface admin de Conselhos
class ConselhoAdmin(admin.ModelAdmin):
    form = ConselhoForm
    list_display = ('nome', 'categoria', 'email', 'presidente', 'n_cargos', 'previstos_cargos')
    list_filter = ('categoria',)
    search_fields = ['nome']
    inlines = [
        MandatoInline,
    ]


#Define a interface admin de Mandatos
class MandatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'atribuicao', 'cargo', 'conselho', 'jeton')
    list_filter = ('jeton',)


#Define a interface admin de CamposPrevistos
class CargosPrevistosAdmin(admin.ModelAdmin):
    list_display = ('legislacao', 'conselho', 'atribuicao', 'cargo', 'poder')


#Define a interface admin de Legislação
class LegislacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'categoria', 'conselho', 'n_cargos', 'link')
    inlines = [
        CargosPrevistosInLine,
    ]


#Define a interface admin de Reuniões dos Conselhos
class ReuniaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'conselho', 'ata')


#Define a interface admin de Conselheiros
class ConselheiroAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    form = ConselheiroForm
    list_display = ('nome', 'telefone', 'email', 'conselhos')


admin.site.register(Conselho, ConselhoAdmin)
admin.site.register(Conselheiro, ConselheiroAdmin)
admin.site.register(Legislacao, LegislacaoAdmin)
admin.site.register(Mandato, MandatoAdmin)
admin.site.register(CargosPrevistos, CargosPrevistosAdmin)
admin.site.register(Reuniao, ReuniaoAdmin)
