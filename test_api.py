#!/usr/bin/env python3
"""
Script para probar la API de productos
Ejecutar: python test_api.py
"""

import requests
import json
import time

# Configuración
BASE_URL = "https://productos-wgge.onrender.com/api"
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def print_response(response, title=""):
    """Imprime la respuesta de forma legible"""
    print(f"\n{'='*50}")
    if title:
        print(f"📋 {title}")
    print(f"{'='*50}")
    print(f"Status: {response.status_code}")
    print(f"URL: {response.url}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def test_api():
    """Prueba todos los endpoints de la API"""
    
    print("🚀 Iniciando pruebas de la API de Productos")
    print("="*60)
    
    # 1. Listar productos
    print("\n1️⃣ Probando listar productos...")
    response = requests.get(f"{BASE_URL}/productos/", headers=HEADERS)
    print_response(response, "Listar Productos")
    
    # 2. Crear un producto
    print("\n2️⃣ Probando crear un producto...")
    nuevo_producto = {
        "nombre": "Test Product API",
        "descripcion": "Producto de prueba creado desde la API",
        "precio": "99.99",
        "stock": 10,
        "categoria": "Test"
    }
    response = requests.post(f"{BASE_URL}/productos/", 
                           headers=HEADERS, 
                           data=json.dumps(nuevo_producto))
    print_response(response, "Crear Producto")
    
    if response.status_code == 201:
        producto_id = response.json()['id']
        print(f"✅ Producto creado con ID: {producto_id}")
        
        # 3. Obtener producto específico
        print("\n3️⃣ Probando obtener producto específico...")
        response = requests.get(f"{BASE_URL}/productos/{producto_id}/", headers=HEADERS)
        print_response(response, f"Obtener Producto {producto_id}")
        
        # 4. Actualizar producto
        print("\n4️⃣ Probando actualizar producto...")
        actualizacion = {
            "nombre": "Test Product API - Actualizado",
            "precio": "149.99",
            "stock": 15
        }
        response = requests.patch(f"{BASE_URL}/productos/{producto_id}/", 
                                headers=HEADERS, 
                                data=json.dumps(actualizacion))
        print_response(response, f"Actualizar Producto {producto_id}")
        
        # 5. Ajustar stock
        print("\n5️⃣ Probando ajustar stock...")
        ajuste_stock = {
            "cantidad": 5,
            "operacion": "sumar"
        }
        response = requests.post(f"{BASE_URL}/productos/{producto_id}/ajustar_stock/", 
                               headers=HEADERS, 
                               data=json.dumps(ajuste_stock))
        print_response(response, f"Ajustar Stock Producto {producto_id}")
        
        # 6. Activar/Desactivar producto
        print("\n6️⃣ Probando activar/desactivar producto...")
        response = requests.post(f"{BASE_URL}/productos/{producto_id}/activar_desactivar/", 
                               headers=HEADERS)
        print_response(response, f"Activar/Desactivar Producto {producto_id}")
        
        # 7. Eliminar producto (soft delete)
        print("\n7️⃣ Probando eliminar producto (soft delete)...")
        response = requests.delete(f"{BASE_URL}/productos/{producto_id}/", headers=HEADERS)
        print_response(response, f"Eliminar Producto {producto_id}")
    
    # 8. Probar endpoints especiales
    print("\n8️⃣ Probando endpoints especiales...")
    
    # Productos activos
    response = requests.get(f"{BASE_URL}/productos/activos/", headers=HEADERS)
    print_response(response, "Productos Activos")
    
    # Productos con stock
    response = requests.get(f"{BASE_URL}/productos/con_stock/", headers=HEADERS)
    print_response(response, "Productos con Stock")
    
    # Productos sin stock
    response = requests.get(f"{BASE_URL}/productos/sin_stock/", headers=HEADERS)
    print_response(response, "Productos sin Stock")
    
    # Productos con stock bajo
    response = requests.get(f"{BASE_URL}/productos/stock_bajo/", headers=HEADERS)
    print_response(response, "Productos con Stock Bajo")
    
    # Productos por categoría
    response = requests.get(f"{BASE_URL}/productos/por_categoria/?categoria=Electrónicos", headers=HEADERS)
    print_response(response, "Productos por Categoría")
    
    # Estadísticas
    response = requests.get(f"{BASE_URL}/productos/estadisticas/", headers=HEADERS)
    print_response(response, "Estadísticas")
    
    # 9. Probar filtros y búsqueda
    print("\n9️⃣ Probando filtros y búsqueda...")
    
    # Búsqueda
    response = requests.get(f"{BASE_URL}/productos/?search=laptop", headers=HEADERS)
    print_response(response, "Búsqueda por 'laptop'")
    
    # Filtro por categoría
    response = requests.get(f"{BASE_URL}/productos/?categoria=Smartphones", headers=HEADERS)
    print_response(response, "Filtro por categoría 'Smartphones'")
    
    # Ordenamiento
    response = requests.get(f"{BASE_URL}/productos/?ordering=-precio", headers=HEADERS)
    print_response(response, "Ordenamiento por precio descendente")
    
    # Combinación de filtros
    response = requests.get(f"{BASE_URL}/productos/?activo=true&ordering=-fecha_creacion", headers=HEADERS)
    print_response(response, "Filtros combinados")
    
    print("\n" + "="*60)
    print("✅ Pruebas completadas!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor.")
        print("   Asegúrate de que el servidor Django esté ejecutándose en http://localhost:8000")
        print("   Ejecuta: python manage.py runserver")
    except Exception as e:
        print(f"❌ Error inesperado: {e}") 