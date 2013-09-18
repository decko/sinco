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
from sinco.core.models import Conselho, Conselheiro, Legislacao, Mandato, CargosPrevistos, Reuniao, CargoRegimental, EstruturaRegimental, Telefone

#Importa a classe ModelForm para personalização de formulário
from django.forms import ModelForm

#Importa a classe BRPhoneNumberField para validação dos Telefones nos modelos
from django.contrib.localflavor.br.forms import BRPhoneNumberField

#Importa o Admin
from django.contrib import admin

#Utiliza django-admin-flexselect para filtrar os cargos disponiveis por conselho
from flexselect import FlexSelectWidget


class MandatoWidget(FlexSelectWidget):

    trigger_fields = ['conselho']

    def details(self, base_field_instance, instance):
        return ""

    def queryset(self, instance):

        if not instance.id:
            conselho = instance.conselho.id
            estrutura = EstruturaRegimental.objects.filter(conselho=conselho).latest('data')
            return CargoRegimental.objects.filter(estrutura=estrutura).exclude(mandato__data_termino__isnull=True, mandato__data_inicial__isnull=False)
        else:
            cargo = instance.cargo.id
            return CargoRegimental.objects.filter(pk=cargo)

    def empty_choices_text(self, instance):
        """
        If either of the trigger_fields is None this function will be called
        to get the text for the empty choice in the select box of the base
        field.

        - instance: A partial instance of the parent model loaded from the
                    request.
        """
        return "-----"


#Personalização do campo telefone no modelo Conselho
class TelefoneForm(ModelForm):
    numero = BRPhoneNumberField()

    class Meta:
        model = Telefone


#Insere o Modelo 'Mandato' dentro do formulário de Conselho
class MandatoInline(admin.TabularInline):
    model = Mandato


#Insere o Modelo 'CargosPrevistos' dentro do formulário de Legislação
class CargosPrevistosInLine(admin.TabularInline):
    model = CargosPrevistos


class TelefoneInLineConselheiro(admin.TabularInline):
    form = TelefoneForm
    fields = ('conselheiro', 'numero', 'tipo')
    model = Telefone


class TelefoneInLineConselho(admin.TabularInline):
    form = TelefoneForm
    fields = ('conselho', 'numero', 'tipo')
    model = Telefone


#Define a interface admin de Conselhos
class ConselhoAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ('nome', 'categoria', 'email', 'presidente', 'n_cargos', 'previstos_cargos')
    list_filter = ('categoria',)
    inlines = [
        TelefoneInLineConselho,
    ]


#Define a interface admin de Mandatos
class MandatoAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cargo":
            kwargs['widget'] = MandatoWidget(
                base_field=db_field,
                modeladmin=self,
                request=request,
            )
            kwargs['label'] = 'Cargo'
        return super(MandatoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ('titular', 'suplente', 'suplente_exercicio', 'cargo', 'conselho', 'jeton')
    list_filter = ('jeton',)


#Define a interface admin de CamposPrevistos
class CargosPrevistosAdmin(admin.ModelAdmin):
    search_fields = ['conselho', 'atribuicao']
    list_display = ('legislacao', 'conselho', 'atribuicao', 'cargo', 'poder')


#Define a interface admin de Legislação
class LegislacaoAdmin(admin.ModelAdmin):
    search_fields = ['titulo', 'data', 'ementa']
    list_display = ('titulo', 'data', 'categoria', 'ementa', 'n_cargos', 'url')
    inlines = [
        CargosPrevistosInLine,
    ]


#Define a interface admin de Reuniões dos Conselhos
class ReuniaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'conselho', 'ata')


#Define a interface admin de Conselheiros
class ConselheiroAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ('nome', 'email', 'conselhos')
    inlines = [
        TelefoneInLineConselheiro,
    ]


class CargoRegimentalAdmin(admin.ModelAdmin):
    search_fields = ['conselho', '__unicode__']
    list_display = ('conselho', '__unicode__')


class TelefoneForm(ModelForm):
    numero = BRPhoneNumberField()

    class Meta:
        model = Telefone


class TelefoneAdmin(admin.ModelAdmin):
    form = TelefoneForm
    list_display = ('numero', 'tipo')


admin.site.register(Conselho, ConselhoAdmin)
admin.site.register(Conselheiro, ConselheiroAdmin)
admin.site.register(Legislacao, LegislacaoAdmin)
admin.site.register(Mandato, MandatoAdmin)
admin.site.register(CargosPrevistos, CargosPrevistosAdmin)
admin.site.register(Reuniao, ReuniaoAdmin)
admin.site.register(EstruturaRegimental)
admin.site.register(CargoRegimental, CargoRegimentalAdmin)
admin.site.register(Telefone, TelefoneAdmin)
