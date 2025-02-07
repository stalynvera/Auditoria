from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Producto, Venta, Auditoria
from django.contrib.auth.models import User

@receiver(post_save, sender=Producto)
def registrar_auditoria_producto(sender, instance, created, **kwargs):
    accion = 'CREAR' if created else 'EDITAR'
    
    # Registrar en la tabla Auditoria sin modificar el stock
    Auditoria.objects.create(
        accion=accion,
        modelo_afectado='Producto',
        detalles=f"Nombre: {instance.nombre}, Precio: {instance.precio}, Stock: {instance.stock}",
    )


@receiver(post_delete, sender=Producto)
def eliminar_auditoria_producto(sender, instance, **kwargs):
    # Registrar en la tabla Auditoria sin el campo usuario
    Auditoria.objects.create(
        accion='ELIMINAR',
        modelo_afectado='Producto',
        detalles=f"Nombre: {instance.nombre}, Precio: {instance.precio}, Stock: {instance.stock}",
    )

@receiver(post_save, sender=Venta)
def registrar_auditoria_venta(sender, instance, created, **kwargs):
    accion = 'VENTA' if created else 'EDITAR'
    
    # Registrar en la tabla Auditoria sin modificar el stock
    Auditoria.objects.create(
        accion=accion,
        modelo_afectado='Venta',
        detalles=f"Producto: {instance.producto.nombre}, Cantidad: {instance.cantidad}, Total: {instance.producto.precio * instance.cantidad}",
    )



@receiver(post_delete, sender=Venta)
def eliminar_auditoria_venta(sender, instance, **kwargs):
    # Registrar en la tabla Auditoria sin el campo usuario
    Auditoria.objects.create(
        accion='ELIMINAR',
        modelo_afectado='Venta',
        detalles=f"Producto: {instance.producto.nombre}, Cantidad: {instance.cantidad}, Total: {instance.producto.precio * instance.cantidad}",
    )
