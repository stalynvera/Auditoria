from django.urls import path
from . import views

urlpatterns = [
    path("productos/", views.lista_productos, name="lista_productos"),
    path("productos/agregar/", views.agregar_producto, name="agregar_producto"),
    path("productos/editar/<int:pk>/", views.editar_producto, name="editar_producto"),
    path("productos/eliminar/<int:pk>/", views.eliminar_producto, name="eliminar_producto"),
    path("ventas/", views.registrar_venta, name="registrar_venta"),
    path("auditoria/", views.lista_auditoria, name="lista_auditoria"),
    
]
