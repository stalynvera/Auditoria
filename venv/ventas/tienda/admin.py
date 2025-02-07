from django.contrib import admin
from .models import Producto, Venta, Auditoria

# Registra los modelos para que se puedan ver en el admin
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock')
    search_fields = ('nombre',)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'fecha', 'usuario')
    list_filter = ('fecha',)

class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'modelo_afectado', 'fecha')
    list_filter = ('accion', 'modelo_afectado', 'fecha')

admin.site.register(Auditoria, AuditoriaAdmin)
