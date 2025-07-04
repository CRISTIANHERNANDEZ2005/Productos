from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    estado_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'codigo_producto')

    def validate_precio(self, value):
        """Validación personalizada para el precio"""
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0")
        return value

    def validate_stock(self, value):
        """Validación personalizada para el stock"""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value

class ProductoListSerializer(serializers.ModelSerializer):
    """Serializador para listar productos (sin descripción completa)"""
    estado_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Producto
        fields = ['id', 'codigo_producto', 'nombre', 'categoria', 'precio', 'stock', 'estado_stock', 'activo', 'fecha_creacion']

class ProductoCreateSerializer(serializers.ModelSerializer):
    """Serializador específico para crear productos"""
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria']
        read_only_fields = ('codigo_producto', 'fecha_creacion', 'fecha_actualizacion')

class ProductoUpdateSerializer(serializers.ModelSerializer):
    """Serializador específico para actualizar productos"""
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'activo']
        read_only_fields = ('codigo_producto', 'fecha_creacion', 'fecha_actualizacion') 