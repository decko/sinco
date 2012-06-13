from gestao.models import Conselho, Conselheiro, Legislacao, Mandato, CargosPrevistos, Reuniao
from django.forms import ModelForm
from django.contrib.localflavor.br.forms import BRPhoneNumberField
from django.contrib import admin


class ConselhoForm(ModelForm):
    telefone = BRPhoneNumberField()

    class Meta:
        model = Conselho


class ConselheiroForm(ModelForm):
    telefone = BRPhoneNumberField()

    class Meta:
        model = Conselheiro


class MandatoInline(admin.TabularInline):
    model = Mandato


class ConselhoAdmin(admin.ModelAdmin):
    form = ConselhoForm
    list_display = ('nome', 'categoria', 'email', 'presidente', 'n_cargos', 'previstos_cargos')
    list_filter = ('categoria',)
    search_fields = ['nome']
    inlines = [
        MandatoInline,
    ]


class MandatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'atribuicao', 'cargo', 'conselho', 'jeton')
    list_filter = ('jeton',)


class CargosPrevistosAdmin(admin.ModelAdmin):
    list_display = ('legislacao', 'conselho', 'atribuicao', 'cargo', 'poder')


class LegislacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'categoria', 'conselho', 'n_cargos', 'link')


class ReuniaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'conselho', 'ata')


class ConselheiroAdmin(admin.ModelAdmin):
    form = ConselheiroForm
    list_display = ('nome', 'telefone', 'email', 'conselhos')

#   class LiderancaAdmin(admin.ModelAdmin):
#   list_display = ('nome', 'email', 'telefone')
#   list_filter = ('entidade',)
#   filter_horizontal = ('entidade',)
#   search_fields = ['nome']

#class DemandaAdmin(admin.ModelAdmin):
#   list_display = ('prazo', 'demanda', 'responsavel', 'situacao', 'prioridade')
#   filter_horizontal = ('entidade',)

#class AudienciaAdmin(admin.ModelAdmin):
#   list_display = ('demanda', 'data', 'local')
#   raw_id_field = ('demanda',)
#   filter_horizontal = ('presenca',)

#class ResponsavelAdmin(admin.ModelAdmin):
#   pass


admin.site.register(Conselho, ConselhoAdmin)
admin.site.register(Conselheiro, ConselheiroAdmin)
admin.site.register(Legislacao, LegislacaoAdmin)
admin.site.register(Mandato, MandatoAdmin)
admin.site.register(CargosPrevistos, CargosPrevistosAdmin)
admin.site.register(Reuniao, ReuniaoAdmin)
