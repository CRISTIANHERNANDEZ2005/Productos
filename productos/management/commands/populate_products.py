from django.core.management.base import BaseCommand
from productos.models import Producto
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Pobla la base de datos con productos de ejemplo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Número de productos a crear (default: 20)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Datos de ejemplo
        productos_data = [
            # Electrónicos
            {
                'nombre': 'iPhone 15 Pro',
                'descripcion': 'Smartphone Apple con chip A17 Pro, cámara triple de 48MP y pantalla Super Retina XDR de 6.1"',
                'precio': Decimal('999.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Smartphones'
            },
            {
                'nombre': 'Samsung Galaxy S24 Ultra',
                'descripcion': 'Flagship de Samsung con S Pen integrado, cámara de 200MP y procesador Snapdragon 8 Gen 3',
                'precio': Decimal('1199.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Smartphones'
            },
            {
                'nombre': 'MacBook Pro 14" M3',
                'descripcion': 'Laptop profesional con chip M3, 14" Liquid Retina XDR y hasta 22 horas de batería',
                'precio': Decimal('1999.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Laptops'
            },
            {
                'nombre': 'Dell XPS 13 Plus',
                'descripcion': 'Laptop ultrabook con pantalla InfinityEdge, procesador Intel Core i7 y diseño premium',
                'precio': Decimal('1499.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Laptops'
            },
            {
                'nombre': 'iPad Pro 12.9" M2',
                'descripcion': 'Tablet profesional con chip M2, pantalla Liquid Retina XDR y compatibilidad con Apple Pencil',
                'precio': Decimal('1099.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Tablets'
            },
            
            # Gaming
            {
                'nombre': 'PlayStation 5',
                'descripcion': 'Consola de nueva generación con SSD ultrarrápido, ray tracing y compatibilidad con PS4',
                'precio': Decimal('499.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Gaming'
            },
            {
                'nombre': 'Xbox Series X',
                'descripcion': 'Consola más potente de Microsoft con 4K gaming, ray tracing y Game Pass',
                'precio': Decimal('499.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Gaming'
            },
            {
                'nombre': 'Nintendo Switch OLED',
                'descripcion': 'Consola híbrida con pantalla OLED de 7", mejor audio y mayor almacenamiento',
                'precio': Decimal('349.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Gaming'
            },
            
            # Audio
            {
                'nombre': 'AirPods Pro 2',
                'descripcion': 'Auriculares inalámbricos con cancelación activa de ruido y audio espacial',
                'precio': Decimal('249.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Audio'
            },
            {
                'nombre': 'Sony WH-1000XM5',
                'descripcion': 'Auriculares over-ear con la mejor cancelación de ruido del mercado',
                'precio': Decimal('399.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Audio'
            },
            
            # Accesorios
            {
                'nombre': 'Apple Watch Series 9',
                'descripcion': 'Reloj inteligente con monitor cardíaco, GPS y hasta 18 horas de batería',
                'precio': Decimal('399.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Wearables'
            },
            {
                'nombre': 'Magic Keyboard',
                'descripcion': 'Teclado inalámbrico de Apple con diseño minimalista y teclas scissor-switch',
                'precio': Decimal('99.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Accesorios'
            },
            {
                'nombre': 'Magic Mouse 2',
                'descripcion': 'Mouse inalámbrico con superficie táctil y hasta 2 meses de batería',
                'precio': Decimal('79.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Accesorios'
            },
            
            # Monitores
            {
                'nombre': 'LG 27" 4K UltraFine',
                'descripcion': 'Monitor 4K con pantalla IPS, 99% sRGB y diseño minimalista',
                'precio': Decimal('699.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Monitores'
            },
            {
                'nombre': 'Samsung Odyssey G9',
                'descripcion': 'Monitor gaming ultrawide de 49" con 240Hz y curvatura 1000R',
                'precio': Decimal('1299.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Monitores'
            },
            
            # Almacenamiento
            {
                'nombre': 'Samsung 970 EVO Plus 1TB',
                'descripcion': 'SSD NVMe de alta velocidad con hasta 3,500 MB/s de lectura',
                'precio': Decimal('89.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Almacenamiento'
            },
            {
                'nombre': 'WD My Passport 2TB',
                'descripcion': 'Disco duro externo portátil con encriptación de hardware',
                'precio': Decimal('79.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Almacenamiento'
            },
            
            # Cámaras
            {
                'nombre': 'Canon EOS R6 Mark II',
                'descripcion': 'Cámara mirrorless full-frame con 24.2MP y grabación 4K 60fps',
                'precio': Decimal('2499.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Cámaras'
            },
            {
                'nombre': 'GoPro Hero 11 Black',
                'descripcion': 'Cámara de acción con sensor 27MP y estabilización HyperSmooth 5.0',
                'precio': Decimal('399.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Cámaras'
            },
            
            # Smart Home
            {
                'nombre': 'Amazon Echo Dot 5th Gen',
                'descripcion': 'Altavoz inteligente con Alexa, control de hogar y audio mejorado',
                'precio': Decimal('49.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Smart Home'
            },
            {
                'nombre': 'Philips Hue Starter Kit',
                'descripcion': 'Kit de iluminación inteligente con 3 bombillas y bridge',
                'precio': Decimal('199.99'),
                'stock': random.randint(5, 50),
                'categoria': 'Smart Home'
            }
        ]

        # Limitar al número solicitado
        productos_data = productos_data[:count]
        
        productos_creados = 0
        
        for data in productos_data:
            # Verificar si el producto ya existe
            if not Producto.objects.filter(nombre=data['nombre']).exists():
                producto = Producto.objects.create(**data)
                productos_creados += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Producto creado: {producto.nombre} - ${producto.precio}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Producto ya existe: {data["nombre"]}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Se crearon {productos_creados} productos exitosamente!'
            )
        )
        
        # Mostrar estadísticas
        total_productos = Producto.objects.count()
        productos_activos = Producto.objects.filter(activo=True).count()
        productos_sin_stock = Producto.objects.filter(stock=0).count()
        
        self.stdout.write(f'\n📊 Estadísticas:')
        self.stdout.write(f'   Total de productos: {total_productos}')
        self.stdout.write(f'   Productos activos: {productos_activos}')
        self.stdout.write(f'   Productos sin stock: {productos_sin_stock}') 