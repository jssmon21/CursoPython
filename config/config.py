import sqlite3
class ConfigBd():

    def __init__(self):
        self.bd = self.createBd()
        self.createDatabase() #migration
        self.bd=self.createBd()
        self.populate() # seed
    def createBd(self):
        conn = sqlite3.connect('bd-si.db')
        return conn
    def discontecBd(self):
        if self.bd:
            self.bd.close()
            print("Conexion cerrada")
    def createDatabase(self):
        cursor = self.bd.cursor()
        try:
                    # 1. TABLA USUARIOS SISTEMA
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios_sistema (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    apellido VARCHAR(100) NOT NULL,
                    tipo_usuario VARCHAR(20) CHECK(tipo_usuario IN ('admin', 'ventas')) NOT NULL,
                    estado BOOLEAN DEFAULT 1,
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 2. TABLA CLIENTES
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre VARCHAR(100) NOT NULL,
                    apellido VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE,
                    telefono VARCHAR(20),
                    documento VARCHAR(20) UNIQUE NOT NULL,
                    tipo_documento VARCHAR(10) CHECK(tipo_documento IN ('DNI', 'CE', 'PASAPORTE')) DEFAULT 'DNI',
                    direccion TEXT,
                    fecha_nacimiento DATE,
                    estado_civil VARCHAR(20),
                    ingresos_mensuales DECIMAL(10,2),
                    estado VARCHAR(20) CHECK(estado IN ('activo', 'inactivo', 'prospecto', 'cliente')) DEFAULT 'prospecto',
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 3. TABLA PRODUCTOS (PROPIEDADES)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo_producto VARCHAR(20) UNIQUE NOT NULL,
                    titulo VARCHAR(200) NOT NULL,
                    descripcion TEXT,
                    tipo_propiedad VARCHAR(50) CHECK(tipo_propiedad IN ('casa', 'departamento', 'oficina', 'local', 'terreno')) NOT NULL,
                    direccion TEXT NOT NULL,
                    distrito VARCHAR(100),
                    provincia VARCHAR(100),
                    departamento VARCHAR(100),
                    area_total DECIMAL(8,2),
                    area_construida DECIMAL(8,2),
                    habitaciones INTEGER,
                    banos INTEGER,
                    estacionamientos INTEGER,
                    precio DECIMAL(12,2) NOT NULL,
                    moneda VARCHAR(5) CHECK(moneda IN ('PEN', 'USD')) DEFAULT 'PEN',
                    estado VARCHAR(20) CHECK(estado IN ('disponible', 'reservado', 'vendido', 'inactivo')) DEFAULT 'disponible',
                    fecha_publicacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 4. TABLA TRANSACCIONES INMOBILIARIAS (TRX IN)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transacciones (
                    id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo_transaccion VARCHAR(20) UNIQUE NOT NULL,
                    id_cliente INTEGER NOT NULL,
                    id_producto INTEGER NOT NULL,
                    id_usuario_ventas INTEGER NOT NULL,
                    tipo_transaccion VARCHAR(20) CHECK(tipo_transaccion IN ('venta', 'reserva', 'separacion')) NOT NULL,
                    precio_venta DECIMAL(12,2) NOT NULL,
                    moneda VARCHAR(5) CHECK(moneda IN ('PEN', 'USD')) DEFAULT 'PEN',
                    forma_pago VARCHAR(50) CHECK(forma_pago IN ('contado', 'financiado', 'credito_hipotecario')) NOT NULL,
                    cuota_inicial DECIMAL(12,2),
                    monto_financiado DECIMAL(12,2),
                    tasa_interes DECIMAL(5,2),
                    plazo_meses INTEGER,
                    cuota_mensual DECIMAL(10,2),
                    estado VARCHAR(20) CHECK(estado IN ('borrador', 'activa', 'completada', 'cancelada')) DEFAULT 'borrador',
                    fecha_transaccion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fecha_cierre DATETIME,
                    observaciones TEXT,
                    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
                    FOREIGN KEY (id_usuario_ventas) REFERENCES usuarios_sistema(id_usuario)
                )
            ''')
            
            # 5. TABLA PAGOS
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pagos (
                    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_transaccion INTEGER NOT NULL,
                    numero_cuota INTEGER,
                    tipo_pago VARCHAR(30) CHECK(tipo_pago IN ('inicial', 'cuota_mensual', 'pago_adicional', 'liquidacion')) NOT NULL,
                    monto DECIMAL(10,2) NOT NULL,
                    moneda VARCHAR(5) CHECK(moneda IN ('PEN', 'USD')) DEFAULT 'PEN',
                    fecha_vencimiento DATE,
                    fecha_pago DATETIME,
                    metodo_pago VARCHAR(30) CHECK(metodo_pago IN ('efectivo', 'transferencia', 'cheque', 'tarjeta')) NOT NULL,
                    numero_operacion VARCHAR(50),
                    estado VARCHAR(20) CHECK(estado IN ('pendiente', 'pagado', 'vencido', 'cancelado')) DEFAULT 'pendiente',
                    observaciones TEXT,
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_transaccion) REFERENCES transacciones(id_transaccion)
                )
            ''')
            
            # 6. TABLA DOCUMENTOS
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documentos (
                    id_documento INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_transaccion INTEGER,
                    id_producto INTEGER,
                    id_cliente INTEGER,
                    tipo_documento VARCHAR(50) CHECK(tipo_documento IN ('contrato', 'escritura', 'DNI', 'recibo_ingresos', 'planos', 'licencias', 'otros')) NOT NULL,
                    nombre_documento VARCHAR(200) NOT NULL,
                    ruta_archivo TEXT,
                    extension_archivo VARCHAR(10),
                    tamano_archivo INTEGER,
                    estado VARCHAR(20) CHECK(estado IN ('pendiente', 'recibido', 'validado', 'rechazado')) DEFAULT 'pendiente',
                    observaciones TEXT,
                    fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fecha_validacion DATETIME,
                    FOREIGN KEY (id_transaccion) REFERENCES transacciones(id_transaccion),
                    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
                    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
                )
            ''')
            
            # 7. TABLA REPORTES (Para auditoría y seguimiento)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reportes_actividad (
                    id_reporte INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_usuario INTEGER,
                    tipo_actividad VARCHAR(50) NOT NULL,
                    descripcion TEXT,
                    tabla_afectada VARCHAR(50),
                    id_registro_afectado INTEGER,
                    datos_anteriores TEXT,
                    datos_nuevos TEXT,
                    ip_address VARCHAR(45),
                    fecha_actividad DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios_sistema(id_usuario)
                )
            ''')
        except sqlite3.Error as e:
            print(f"❌ Error al crear la base de datos: {e}")
            self.bd.rollback()
            return False
        finally:
            self.discontecBd()
    def populate(self):
        """Función simple para poblar las tablas con datos del archivo datos.txt"""
        cursor = self.bd.cursor()
        
        try:
            # Leer el archivo de datos
            with open('config/datos.txt', 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Poblar usuarios_sistema
            usuarios_data = [
                ('ana.torres@sistema.com', 'password123', 'Ana', 'Torres', 'admin', 1),
                ('carlos.rivas@sistema.com', 'password456', 'Carlos', 'Rivas', 'ventas', 1),
                ('lucia.perez@sistema.com', 'password678', 'Lucia', 'Perez', 'ventas', 1),
                ('marco.diaz@sistema.com', 'password901', 'Marco', 'Diaz', 'admin', 0),
                ('jesus.montes@sistema.com', '123password', 'Jesus', 'Montes', 'admin', 1),
            ]
            
            cursor.executemany('''
                INSERT OR REPLACE INTO usuarios_sistema 
                (email, password, nombre, apellido, tipo_usuario, estado)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', usuarios_data)
            
            # Poblar clientes
            clientes_data = [
                ('Juan', 'Gomez', 'juan.gomez@mail.com', '999111222', 'DNI00000001', 'activo'),
                ('Maria', 'Lopez', 'maria.lopez@mail.com', '999333444', 'DNI00000002', 'activo'),
                ('Pedro', 'Ramirez', 'pedro.ramirez@mail.com', '999555666', 'DNI00000003', 'activo'),
                ('Ana', 'Castro', 'ana.castro@mail.com', '999777888', 'DNI00000004', 'activo'),
            ]
            
            cursor.executemany('''
                INSERT OR REPLACE INTO clientes 
                (nombre, apellido, email, telefono, documento, estado)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', clientes_data)
            
            # Poblar productos
            productos_data = [
                ('PROP0001', 'Departamento 2 dormitorios en Miraflores', 'Departamento 2 dormitorios en Miraflores', 'departamento', 'Miraflores', 120000, 'disponible'),
                ('PROP0002', 'Casa familiar en Surco', 'Casa familiar en Surco', 'casa', 'Surco', 250000, 'disponible'),
                ('PROP0003', 'Oficina comercial en San Isidro', 'Oficina comercial en San Isidro', 'oficina', 'San Isidro', 180000, 'reservado'),
                ('PROP0004', 'Departamento 1 dormitorio en Barranco', 'Departamento 1 dormitorio en Barranco', 'departamento', 'Barranco', 95000, 'vendido'),
                ('PROP0005', 'Departamento 3 dormitorios con vista al mar en Magdalena', 'Departamento 3 dormitorios con vista al mar en Magdalena', 'departamento', 'Magdalena', 210000, 'disponible'),
                ('PROP0006', 'Casa de playa amoblada en Asia', 'Casa de playa amoblada en Asia', 'casa', 'Asia', 320000, 'disponible'),
                ('PROP0007', 'Oficina corporativa en centro empresarial de San Borja', 'Oficina corporativa en centro empresarial de San Borja', 'oficina', 'San Borja', 195000, 'disponible'),
                ('PROP0008', 'Local en avenida principal de La Victoria', 'Local en avenida principal de La Victoria', 'local', 'La Victoria', 150000, 'reservado'),
                ('PROP0009', 'Departamento tipo loft en Barranco', 'Departamento tipo loft en Barranco', 'departamento', 'Barranco', 110000, 'disponible'),
                ('PROP0010', 'Casa de campo con terreno amplio en Cieneguilla', 'Casa de campo con terreno amplio en Cieneguilla', 'casa', 'Cieneguilla', 280000, 'disponible'),
                ('PROP0011', 'Oficina pequeña para startup en Miraflores', 'Oficina pequeña para startup en Miraflores', 'oficina', 'Miraflores', 90000, 'vendido'),
                ('PROP0012', 'Departamento dúplex en San Miguel', 'Departamento dúplex en San Miguel', 'departamento', 'San Miguel', 175000, 'disponible'),
                ('PROP0013', 'Local en centro comercial de Jesús María', 'Local en centro comercial de Jesús María', 'local', 'Jesús María', 230000, 'reservado'),
                ('PROP0014', 'Terreno urbano para proyecto inmobiliario en Lurín', 'Terreno urbano para proyecto inmobiliario en Lurín', 'terreno', 'Lurín', 400000, 'disponible'),
                ('PROP0015', 'Departamento amoblado para alquiler en Surquillo', 'Departamento amoblado para alquiler en Surquillo', 'departamento', 'Surquillo', 105000, 'vendido'),
            ]
            
            cursor.executemany('''
                INSERT OR REPLACE INTO productos 
                (codigo_producto, titulo, descripcion, tipo_propiedad, direccion, precio, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', productos_data)
            
            # Poblar transacciones
            transacciones_data = [
                ('TRX000001', 1, 1, 2, 'venta', 120000, 'contado', 'activa', '2025-01-18'),
                ('TRX000002', 2, 2, 2, 'venta', 250000, 'contado', 'activa', '2025-01-19'),
                ('TRX000003', 3, 3, 1, 'reserva', 180000, 'contado', 'activa', '2025-01-21'),
                ('TRX000004', 4, 4, 4, 'venta', 95000, 'contado', 'activa', '2025-01-22'),
            ]
            
            cursor.executemany('''
                INSERT OR REPLACE INTO transacciones 
                (codigo_transaccion, id_cliente, id_producto, id_usuario_ventas, tipo_transaccion, 
                precio_venta, forma_pago, estado, fecha_transaccion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', transacciones_data)
            
            # Poblar pagos
            pagos_data = [
                (1, 'inicial', 30000, '2025-01-18', 'transferencia', 'OP000001', 'pagado'),
                (2, 'inicial', 50000, '2025-01-19', 'efectivo', 'OP000002', 'pagado'),
                (3, 'inicial', 20000, '2025-01-21', 'tarjeta', 'OP000003', 'pendiente'),
                (4, 'inicial', 95000, '2025-01-22', 'transferencia', 'OP000004', 'pagado'),
            ]
            
            cursor.executemany('''
                INSERT OR REPLACE INTO pagos 
                (id_transaccion, tipo_pago, monto, fecha_pago, metodo_pago, numero_operacion, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', pagos_data)
            
            # Poblar documentos
            documentos_data = [
                (1, 1, 'contrato', 'Contrato de compra', 'validado', '2025-01-15'),
                (2, 2, 'escritura', 'Titulo de propiedad', 'validado', '2025-01-10'),
                (3, 3, 'contrato', 'Contrato de alquiler', 'validado', '2025-01-20'),
                (4, 4, 'escritura', 'Escritura publica', 'validado', '2025-01-05'),
            ]
            
            cursor.executemany('''
                INSERT OR REPLACE INTO documentos 
                (id_transaccion, id_producto, tipo_documento, nombre_documento, estado, fecha_subida)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', documentos_data)
            
            # Confirmar cambios
            self.bd.commit()
            print("✅ Datos poblados correctamente")
            
            # Mostrar estadísticas
            cursor.execute("SELECT COUNT(*) FROM usuarios_sistema")
            print(f"   - Usuarios: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM clientes")
            print(f"   - Clientes: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM productos")
            print(f"   - Productos: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM transacciones")
            print(f"   - Transacciones: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM pagos")
            print(f"   - Pagos: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM documentos")
            print(f"   - Documentos: {cursor.fetchone()[0]}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al poblar datos: {e}")
            self.bd.rollback()
            return False
    