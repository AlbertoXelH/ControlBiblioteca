import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect("biblioteca.db")
cursor = conn.cursor()

# Crear tabla de libros
cursor.execute("""
CREATE TABLE IF NOT EXISTS libros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL
)
""")

# Crear tabla de préstamos
cursor.execute("""
CREATE TABLE IF NOT EXISTS prestamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    libro_id INTEGER NOT NULL,
    persona TEXT NOT NULL,
    fecha_prestamo TEXT NOT NULL,
    fecha_devolucion TEXT DEFAULT 'Pendiente',
    FOREIGN KEY (libro_id) REFERENCES libros (id)
)
""")

# Insertar libros iniciales
cursor.executemany("""
INSERT INTO libros (titulo) VALUES (?)
""", [
    ("El Quijote",),
    ("Cien Años de Soledad",),
    ("1984",),
    ("La Odisea",)
])

conn.commit()
conn.close()

print("Base de datos creada exitosamente.")
