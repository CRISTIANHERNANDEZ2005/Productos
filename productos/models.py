from django.db import models
from typing import Any
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# Create your models here.

class Producto(models.Model):
    objects: models.Manager  # type: ignore
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre del Producto",
        help_text="Nombre descriptivo del producto"
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada del producto"
    )
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Precio",
        validators=[MinValueValidator(Decimal('0.01'), message="El precio debe ser mayor a 0")]
    )
    stock = models.IntegerField(
        verbose_name="Stock Disponible",
        validators=[MinValueValidator(0, message="El stock no puede ser negativo")],
        default=0
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    # Campos adicionales útiles
    categoria = models.CharField(
        max_length=50, 
        verbose_name="Categoría",
        blank=True,
        null=True
    )
    codigo_producto = models.CharField(
        max_length=20, 
        verbose_name="Código de Producto",
        unique=True,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['categoria']),
            models.Index(fields=['activo']),
        ]

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    def tiene_stock(self):
        """Verifica si el producto tiene stock disponible"""
        return self.stock > 0 and self.activo

    def reducir_stock(self, cantidad):
        """Reduce el stock del producto"""
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
            return True
        return False

    def aumentar_stock(self, cantidad):
        """Aumenta el stock del producto"""
        self.stock += cantidad
        self.save()

    @property
    def estado_stock(self):
        """Retorna el estado del stock como texto"""
        if not self.activo:
            return "Inactivo"
        elif self.stock == 0:
            return "Sin stock"
        elif self.stock <= 5:
            return "Stock bajo"
        else:
            return "Disponible"

    def save(self, *args, **kwargs):
        # Generar código de producto automáticamente si no existe
        if not self.codigo_producto:
            ultimo_producto = Producto.objects.order_by('-id').first()
            if ultimo_producto:
                ultimo_numero = int(ultimo_producto.codigo_producto[3:]) if ultimo_producto.codigo_producto else 0
                self.codigo_producto = f"PRO{ultimo_numero + 1:04d}"
            else:
                self.codigo_producto = "PRO0001"
        super().save(*args, **kwargs)
