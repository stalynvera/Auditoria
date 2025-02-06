from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Producto, Venta, Auditoria
from .forms import ProductoForm, VentaForm

def registrar_accion(usuario, accion, modelo, detalles):
    Auditoria.objects.create(
        usuario=usuario,
        accion=accion,
        modelo_afectado=modelo,
        detalles=detalles
    )

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, "tienda/productos.html", {"productos": productos})

@login_required
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            registrar_accion(request.user, "CREAR", "Producto", f"Agregó {producto.nombre}")
            return redirect("lista_productos")
    else:
        form = ProductoForm()
    return render(request, "tienda/form_producto.html", {"form": form})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            registrar_accion(request.user, "EDITAR", "Producto", f"Editó {producto.nombre}")
            return redirect("lista_productos")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "tienda/form_producto.html", {"form": form})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        registrar_accion(request.user, "ELIMINAR", "Producto", f"Eliminó {producto.nombre}")
        producto.delete()
        return redirect("lista_productos")
    return render(request, "tienda/confirmar_eliminar.html", {"producto": producto})

@login_required
def registrar_venta(request):
    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.usuario = request.user
            venta.save()
            registrar_accion(request.user, "VENTA", "Venta", f"Vendió {venta.cantidad} de {venta.producto.nombre}")
            return redirect("lista_productos")
    else:
        form = VentaForm()
    return render(request, "tienda/form_venta.html", {"form": form})

@login_required
def lista_auditoria(request):
    auditorias = Auditoria.objects.all().order_by("-fecha")
    return render(request, "tienda/auditoria.html", {"auditorias": auditorias})
