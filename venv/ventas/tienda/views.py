from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Producto, Venta, Auditoria
from .forms import ProductoForm, VentaForm
from django.http import HttpResponse
from docx import Document
from .models import Auditoria
from django.contrib import messages


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
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Venta, Auditoria
from .forms import VentaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def registrar_venta(request):
    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)  # No guarda aún en la BD

            if venta.producto.stock >= venta.cantidad:
                venta.save()  # Aquí ya se descuenta el stock porque está en el modelo Venta

                # Registrar en auditoría solo UNA VEZ
                Auditoria.objects.create(
                    usuario=request.user if request.user.is_authenticated else None,
                    accion="VENTA",
                    modelo_afectado="Venta",
                    detalles=f"Se vendieron {venta.cantidad} unidades de {venta.producto.nombre}",
                )

                messages.success(request, "✅ Venta registrada con éxito.")
                return redirect("lista_productos")
            else:
                messages.error(request, "⚠️ Error: Stock insuficiente.")
        else:
            messages.error(request, "⚠️ Error: Formulario inválido.")

    else:
        form = VentaForm()

    return render(request, "tienda/form_venta.html", {"form": form})  



@login_required
def lista_auditoria(request):
    auditorias = Auditoria.objects.all().order_by("-fecha")
    return render(request, "tienda/auditoria.html", {"auditorias": auditorias})


def generar_auditoria_word(request):
    # Crea un nuevo documento
    doc = Document()
    doc.add_heading('Auditoría de Acciones', 0)
    
    # Obtiene todas las entradas de auditoría
    auditorias = Auditoria.objects.all()
    
    # Añade los datos de auditoría al documento
    doc.add_heading('Historial de Auditoría:', level=1)
    for auditoria in auditorias:
        doc.add_paragraph(f"Usuario: {auditoria.usuario}")
        doc.add_paragraph(f"Acción: {auditoria.accion}")
        doc.add_paragraph(f"Modelo Afectado: {auditoria.modelo_afectado}")
        doc.add_paragraph(f"Fecha: {auditoria.fecha}")
        doc.add_paragraph('-' * 20)
    
    # Añade los productos y su stock al documento
    doc.add_heading('Productos y Stock:', level=1)
    productos = Producto.objects.all()
    
    for producto in productos:
        doc.add_paragraph(f"Nombre: {producto.nombre}")
        doc.add_paragraph(f"Precio: ${producto.precio}")
        doc.add_paragraph(f"Stock: {producto.stock}")
        doc.add_paragraph('-' * 20)
    
    # Crea la respuesta para descargar el archivo
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=auditoria_productos.docx'
    doc.save(response)
    
    return response
