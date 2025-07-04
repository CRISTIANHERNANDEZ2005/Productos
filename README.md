# API de Productos - Django REST Framework

Una API REST completa para gestionar productos, conectada a la base de datos Neon (PostgreSQL).

## 🚀 Características

- **CRUD completo** de productos
- **Filtros avanzados** por categoría, stock, estado
- **Búsqueda** por nombre, descripción y código
- **Ordenamiento** por múltiples campos
- **Gestión de stock** con validaciones
- **Soft delete** (desactivación en lugar de eliminación)
- **Estadísticas** de productos
- **Códigos automáticos** de producto
- **Admin de Django** mejorado

## 🛠️ Tecnologías

- **Django 5.2.3**
- **Django REST Framework**
- **PostgreSQL** (Neon)
- **Django Filter**
- **CORS Headers**

## 📋 Requisitos

- Python 3.8+
- PostgreSQL (Neon)
- pip

## 🔧 Instalación

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd proyecto-final
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
Crea un archivo `.env` en la raíz del proyecto:
```env
SECRET_KEY=tu-secret-key
DEBUG=True
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=tu-password
DB_HOST=ep-patient-dust-a8lpoedz-pooler.eastus2.azure.neon.tech
DB_PORT=5432
```

4. **Ejecutar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Ejecutar el servidor**
```bash
python manage.py runserver
```

## 📚 Endpoints de la API

### Base URL: `http://localhost:8000/api/`

### Productos

#### Listar productos
```
GET /api/productos/
```

**Parámetros de consulta:**
- `search`: Búsqueda por nombre, descripción o código
- `activo`: Filtrar por estado (true/false)
- `stock`: Filtrar por stock disponible
- `categoria`: Filtrar por categoría
- `ordering`: Ordenar por campo (-campo para descendente)

**Ejemplo:**
```
GET /api/productos/?search=laptop&activo=true&ordering=-precio
```

#### Obtener producto específico
```
GET /api/productos/{id}/
```

#### Crear producto
```
POST /api/productos/
```

**Body:**
```json
{
    "nombre": "Laptop Gaming",
    "descripcion": "Laptop para gaming con RTX 4060",
    "precio": "1299.99",
    "stock": 10,
    "categoria": "Electrónicos"
}
```

#### Actualizar producto
```
PUT /api/productos/{id}/
PATCH /api/productos/{id}/
```

#### Eliminar producto (soft delete)
```
DELETE /api/productos/{id}/
```

### Endpoints Especiales

#### Productos activos
```
GET /api/productos/activos/
```

#### Productos con stock
```
GET /api/productos/con_stock/
```

#### Productos sin stock
```
GET /api/productos/sin_stock/
```

#### Productos con stock bajo (≤5)
```
GET /api/productos/stock_bajo/
```

#### Productos por categoría
```
GET /api/productos/por_categoria/?categoria=Electrónicos
```

#### Estadísticas
```
GET /api/productos/estadisticas/
```

**Respuesta:**
```json
{
    "resumen": {
        "total_productos": 50,
        "productos_activos": 45,
        "productos_sin_stock": 5,
        "productos_stock_bajo": 3
    },
    "categorias": [
        {
            "categoria": "Electrónicos",
            "total": 20,
            "precio_promedio": 899.99
        }
    ],
    "productos_mas_caros": [...]
}
```

#### Activar/Desactivar producto
```
POST /api/productos/{id}/activar_desactivar/
```

#### Ajustar stock
```
POST /api/productos/{id}/ajustar_stock/
```

**Body:**
```json
{
    "cantidad": 5,
    "operacion": "sumar"  // "sumar" o "restar"
}
```

## 🗄️ Modelo de Datos

### Producto
- `id`: ID único (auto-incremento)
- `codigo_producto`: Código único generado automáticamente (PRO0001, PRO0002, etc.)
- `nombre`: Nombre del producto (máx. 100 caracteres)
- `descripcion`: Descripción detallada
- `precio`: Precio con 2 decimales (mín. 0.01)
- `stock`: Cantidad disponible (mín. 0)
- `categoria`: Categoría del producto (opcional)
- `activo`: Estado activo/inactivo
- `fecha_creacion`: Fecha de creación (automática)
- `fecha_actualizacion`: Fecha de última actualización (automática)

## 🔍 Filtros Disponibles

- **Por estado**: `?activo=true`
- **Por stock**: `?stock=0` (productos sin stock)
- **Por categoría**: `?categoria=Electrónicos`
- **Búsqueda**: `?search=laptop`
- **Ordenamiento**: `?ordering=-precio` (más caro primero)

## 📊 Admin de Django

Accede al admin en `http://localhost:8000/admin/` para:

- Ver productos con información visual (colores por estado de stock)
- Filtrar y buscar productos
- Editar productos directamente en la lista
- Ejecutar acciones en lote (activar, desactivar, aumentar stock)
- Ver estadísticas visuales

## 🧪 Ejemplos de Uso

### Crear un producto
```bash
curl -X POST http://localhost:8000/api/productos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "iPhone 15 Pro",
    "descripcion": "Smartphone Apple con chip A17 Pro",
    "precio": "999.99",
    "stock": 25,
    "categoria": "Smartphones"
  }'
```

### Buscar productos
```bash
curl "http://localhost:8000/api/productos/?search=iPhone&activo=true&ordering=-precio"
```

### Ajustar stock
```bash
curl -X POST http://localhost:8000/api/productos/1/ajustar_stock/ \
  -H "Content-Type: application/json" \
  -d '{"cantidad": 5, "operacion": "restar"}'
```

## 🔒 Seguridad

- **CORS** configurado para desarrollo
- **Validaciones** en modelos y serializers
- **Soft delete** para evitar pérdida de datos
- **Códigos únicos** generados automáticamente

## 🚀 Despliegue

Para producción, considera:

1. Cambiar `DEBUG=False`
2. Configurar `ALLOWED_HOSTS`
3. Usar variables de entorno para credenciales
4. Configurar CORS apropiadamente
5. Usar HTTPS
6. Configurar logging

## 📝 Notas

- Los productos eliminados se marcan como inactivos (soft delete)
- Los códigos de producto se generan automáticamente
- El stock no puede ser negativo
- Los precios deben ser mayores a 0
- Las fechas se actualizan automáticamente

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request 