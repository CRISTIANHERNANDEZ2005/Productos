from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Count, Avg
from .models import Producto
from .serializers import (
    ProductoSerializer, 
    ProductoListSerializer, 
    ProductoUpdateSerializer
)

class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el CRUD completo de productos.
    
    list: Obtiene todos los productos
    create: Crea un nuevo producto
    retrieve: Obtiene un producto específico
    update: Actualiza un producto completo
    partial_update: Actualiza parcialmente un producto
    destroy: Elimina un producto
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activo', 'stock', 'categoria']
    search_fields = ['nombre', 'descripcion', 'codigo_producto']
    ordering_fields = ['nombre', 'precio', 'fecha_creacion', 'stock', 'categoria']
    ordering = ['-fecha_creacion']

    def get_serializer_class(self):
        """Retorna el serializador apropiado según la acción"""
        if self.action == 'list':
            return ProductoListSerializer
        elif self.action in ['update', 'partial_update']:
            return ProductoUpdateSerializer
        return ProductoSerializer

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Endpoint para obtener solo productos activos"""
        productos = Producto.objects.filter(activo=True)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def con_stock(self, request):
        """Endpoint para obtener productos con stock disponible"""
        productos = Producto.objects.filter(stock__gt=0, activo=True)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sin_stock(self, request):
        """Endpoint para obtener productos sin stock"""
        productos = Producto.objects.filter(stock=0, activo=True)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stock_bajo(self, request):
        """Endpoint para obtener productos con stock bajo (≤5)"""
        productos = Producto.objects.filter(stock__lte=5, stock__gt=0, activo=True)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """Endpoint para obtener productos por categoría"""
        categoria = request.query_params.get('categoria', '')
        if categoria:
            productos = Producto.objects.filter(categoria__icontains=categoria, activo=True)
        else:
            productos = Producto.objects.filter(activo=True)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Endpoint para obtener estadísticas de productos"""
        total_productos = Producto.objects.count()
        productos_activos = Producto.objects.filter(activo=True).count()
        productos_sin_stock = Producto.objects.filter(stock=0, activo=True).count()
        productos_stock_bajo = Producto.objects.filter(stock__lte=5, stock__gt=0, activo=True).count()
        
        # Estadísticas por categoría
        categorias = Producto.objects.filter(activo=True).values('categoria').annotate(
            total=Count('id'),
            precio_promedio=Avg('precio')
        ).exclude(categoria__isnull=True).exclude(categoria='')
        
        # Productos más caros
        productos_caros = Producto.objects.filter(activo=True).order_by('-precio')[:5]
        productos_caros_serializer = ProductoListSerializer(productos_caros, many=True)
        
        return Response({
            'resumen': {
                'total_productos': total_productos,
                'productos_activos': productos_activos,
                'productos_sin_stock': productos_sin_stock,
                'productos_stock_bajo': productos_stock_bajo,
            },
            'categorias': list(categorias),
            'productos_mas_caros': productos_caros_serializer.data
        })

    @action(detail=True, methods=['post'])
    def activar_desactivar(self, request, pk=None):
        """Endpoint para activar/desactivar un producto"""
        producto = self.get_object()
        producto.activo = not producto.activo
        producto.save()
        serializer = self.get_serializer(producto)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def ajustar_stock(self, request, pk=None):
        """Endpoint para ajustar el stock de un producto"""
        producto = self.get_object()
        cantidad = request.data.get('cantidad', 0)
        operacion = request.data.get('operacion', 'sumar')  # 'sumar' o 'restar'
        
        try:
            cantidad = int(cantidad)
            if operacion == 'restar':
                if producto.reducir_stock(cantidad):
                    mensaje = f"Stock reducido en {cantidad} unidades"
                else:
                    return Response(
                        {'error': 'Stock insuficiente para realizar la operación'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                producto.aumentar_stock(cantidad)
                mensaje = f"Stock aumentado en {cantidad} unidades"
            
            serializer = self.get_serializer(producto)
            return Response({
                'mensaje': mensaje,
                'producto': serializer.data
            })
        except ValueError:
            return Response(
                {'error': 'La cantidad debe ser un número entero'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        """Sobrescribir destroy para hacer soft delete"""
        producto = self.get_object()
        producto.activo = False
        producto.save()
        return Response(
            {'mensaje': 'Producto desactivado correctamente'},
            status=status.HTTP_204_NO_CONTENT
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        producto = serializer.save()
        from .serializers import ProductoSerializer
        read_serializer = ProductoSerializer(producto)
        headers = self.get_success_headers(serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
