from django.contrib import admin
from django.utils.html import format_html
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo_producto', 
        'nombre', 
        'categoria', 
        'precio_formateado', 
        'stock',
        'estado_stock', 
        'activo', 
        'fecha_creacion'
    ]
    list_filter = ['activo', 'categoria', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion', 'codigo_producto']
    readonly_fields = ['codigo_producto', 'fecha_creacion', 'fecha_actualizacion']
    list_editable = ['activo', 'stock']
    list_per_page = 20
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo_producto', 'nombre', 'descripcion', 'categoria')
        }),
        ('Precio y Stock', {
            'fields': ('precio', 'stock')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def precio_formateado(self, obj):
        """Formatea el precio con símbolo de moneda"""
        return f"${obj.precio:,.2f}"
    precio_formateado.short_description = "Precio"
    precio_formateado.admin_order_field = 'precio'
    
    def stock_display(self, obj):
        """Muestra el stock con colores según el estado"""
        if obj.stock == 0:
            return format_html('<span style="color: red;">{}</span>', obj.stock)
        elif obj.stock <= 5:
            return format_html('<span style="color: orange;">{}</span>', obj.stock)
        else:
            return format_html('<span style="color: green;">{}</span>', obj.stock)
    stock_display.short_description = "Stock"
    stock_display.admin_order_field = 'stock'
    
    def estado_stock(self, obj):
        """Muestra el estado del stock con colores"""
        estado = obj.estado_stock
        if estado == "Sin stock":
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', estado)
        elif estado == "Stock bajo":
            return format_html('<span style="color: orange; font-weight: bold;">{}</span>', estado)
        elif estado == "Disponible":
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', estado)
        else:
            return format_html('<span style="color: gray; font-weight: bold;">{}</span>', estado)
    estado_stock.short_description = "Estado"
    
    actions = ['activar_productos', 'desactivar_productos', 'aumentar_stock']
    
    def activar_productos(self, request, queryset):
        """Acción para activar productos seleccionados"""
        updated = queryset.update(activo=True)
        self.message_user(request, f'{updated} productos han sido activados.')
    activar_productos.short_description = "Activar productos seleccionados"
    
    def desactivar_productos(self, request, queryset):
        """Acción para desactivar productos seleccionados"""
        updated = queryset.update(activo=False)
        self.message_user(request, f'{updated} productos han sido desactivados.')
    desactivar_productos.short_description = "Desactivar productos seleccionados"
    
    def aumentar_stock(self, request, queryset):
        """Acción para aumentar stock de productos seleccionados"""
        # Esta es una acción de ejemplo, en un caso real podrías usar un formulario
        for producto in queryset:
            producto.stock += 10
            producto.save()
        self.message_user(request, f'Stock aumentado en 10 unidades para {queryset.count()} productos.')
    aumentar_stock.short_description = "Aumentar stock en 10 unidades"
