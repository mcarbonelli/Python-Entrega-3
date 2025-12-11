from django.contrib import admin
from .models import Operador, Cliente, Novedad, Lote, NovedadLectura


@admin.register(Operador)
class OperadorAdmin(admin.ModelAdmin):
    list_display = ['cod_ope', 'user', 'get_email']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['cod_cli', 'denominacion', 'domicilio']
    search_fields = ['denominacion', 'domicilio']
    list_per_page = 50


@admin.register(Novedad)
class NovedadAdmin(admin.ModelAdmin):
    list_display = ['cod_novedad', 'descripcion']
    search_fields = ['descripcion']


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ['cod_lectura', 'cliente', 'ruta', 'orden', 'numero_medidor', 
                   'lectura_anterior', 'lectura_actual', 'consumo_kwh', 'abierta', 'ano_consumo', 'mes_consumo']
    list_filter = ['ano_consumo', 'mes_consumo', 'ruta', 'abierta', 'enviado_comercial']
    search_fields = ['cliente__denominacion', 'numero_medidor', 'suministro_numero']
    list_per_page = 50
    readonly_fields = ['consumo_kwh', 'fecha_hora_registro']
    
    fieldsets = (
        ('Periodo', {
            'fields': ('ano_consumo', 'mes_consumo')
        }),
        ('Cliente y Suministro', {
            'fields': ('cliente', 'suministro_numero')
        }),
        ('Ruta', {
            'fields': ('area', 'ruta', 'orden')
        }),
        ('Medidor', {
            'fields': ('tipo_medidor', 'numero_medidor')
        }),
        ('Lecturas', {
            'fields': ('lectura_anterior', 'lectura_actual', 'consumo_kwh')
        }),
        ('Novedades', {
            'fields': ('novedad_libre',)
        }),
        ('Estado', {
            'fields': ('abierta', 'enviado_comercial')
        }),
        ('Auditoría', {
            'fields': ('operador', 'fecha_hora_registro', 'ubi_gps')
        }),
    )


@admin.register(NovedadLectura)
class NovedadLecturaAdmin(admin.ModelAdmin):
    list_display = ['lectura', 'novedad', 'fecha_registro']
    list_filter = ['novedad', 'fecha_registro']
    search_fields = ['lectura__cliente__denominacion', 'novedad__descripcion']
