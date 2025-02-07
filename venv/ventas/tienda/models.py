from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validar_precio(valor):
    """Validación personalizada para evitar precios negativos."""
    if valor < 0:
        raise ValidationError("El precio no puede ser negativo.")

def validar_stock(valor):
    """Validación para evitar stock negativo."""
    if valor < 0:
        raise ValidationError("El stock no puede ser negativo.")

class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_precio])
    stock = models.IntegerField(validators=[validar_stock])

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        """Validaciones al registrar una venta."""
        if self.cantidad > self.producto.stock:
            raise ValidationError(f"No hay suficiente stock para vender {self.cantidad} unidades.")

    def save(self, *args, **kwargs):
        """Reducción del stock al guardar la venta."""
        self.clean()  # Ejecuta validaciones antes de guardar
        self.producto.stock -= self.cantidad
        if self.producto.stock < 0:
            raise ValidationError("Stock insuficiente.")
        self.producto.save()    
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta de {self.cantidad} {self.producto.nombre}"

class Auditoria(models.Model):
    ACCIONES = [
        ("CREAR", "Crear"),
        ("EDITAR", "Editar"),
        ("ELIMINAR", "Eliminar"),
        ("VENTA", "Venta"),
    ]
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    modelo_afectado = models.CharField(max_length=50)
    detalles = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accion} en {self.modelo_afectado} - {self.fecha}"
