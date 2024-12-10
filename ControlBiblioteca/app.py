import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

# Conexión a la base de datos
def conexion():
    return sqlite3.connect("biblioteca.db")

# Registrar préstamo
def registrar_prestamo():
    libro_id = libros_combobox.get().split(" - ")[0]
    persona = persona_entry.get()
    fecha_prestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not persona:
        messagebox.showerror("Error", "El nombre de la persona no puede estar vacío.")
        return

    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO prestamos (libro_id, persona, fecha_prestamo)
    VALUES (?, ?, ?)
    """, (libro_id, persona, fecha_prestamo))
    conn.commit()
    conn.close()

    messagebox.showinfo("Éxito", "Préstamo registrado.")
    persona_entry.delete(0, END)
    actualizar_prestamos()

# Actualizar lista de préstamos
def actualizar_prestamos():
    for row in prestamos_tree.get_children():
        prestamos_tree.delete(row)

    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT prestamos.id, libros.titulo, prestamos.persona, prestamos.fecha_prestamo, prestamos.fecha_devolucion
    FROM prestamos
    INNER JOIN libros ON prestamos.libro_id = libros.id
    """)
    for row in cursor.fetchall():
        prestamos_tree.insert("", END, values=row)
    conn.close()

# Registrar devolución
def registrar_devolucion():
    selected_item = prestamos_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Selecciona un préstamo para marcar como devuelto.")
        return

    prestamo_id = prestamos_tree.item(selected_item[0])["values"][0]
    fecha_devolucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE prestamos
    SET fecha_devolucion = ?
    WHERE id = ?
    """, (fecha_devolucion, prestamo_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Éxito", "Préstamo marcado como devuelto.")
    actualizar_prestamos()

# Interfaz gráfica
root = Tk()
root.title("Control de Préstamos de Biblioteca")

# Selección de libro
Label(root, text="Seleccione un libro:").grid(row=0, column=0, pady=5)
libros_combobox = ttk.Combobox(root, state="readonly")
libros_combobox.grid(row=0, column=1, pady=5)

conn = conexion()
cursor = conn.cursor()
cursor.execute("SELECT id, titulo FROM libros")
libros_combobox["values"] = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
conn.close()

# Nombre de la persona
Label(root, text="Nombre de la persona:").grid(row=1, column=0, pady=5)
persona_entry = Entry(root)
persona_entry.grid(row=1, column=1, pady=5)

# Botón para registrar préstamo
registrar_button = Button(root, text="Registrar Préstamo", command=registrar_prestamo)
registrar_button.grid(row=2, column=0, columnspan=2, pady=10)

# Tabla de préstamos
prestamos_tree = ttk.Treeview(root, columns=("ID", "Libro", "Persona", "Fecha Préstamo", "Fecha Devolución"), show="headings")
prestamos_tree.grid(row=3, column=0, columnspan=2, pady=10)

prestamos_tree.heading("ID", text="ID")
prestamos_tree.heading("Libro", text="Libro")
prestamos_tree.heading("Persona", text="Persona")
prestamos_tree.heading("Fecha Préstamo", text="Fecha Préstamo")
prestamos_tree.heading("Fecha Devolución", text="Fecha Devolución")

prestamos_tree.column("ID", width=30)
prestamos_tree.column("Libro", width=150)
prestamos_tree.column("Persona", width=100)
prestamos_tree.column("Fecha Préstamo", width=150)
prestamos_tree.column("Fecha Devolución", width=150)

# Botón para registrar devolución
devolver_button = Button(root, text="Registrar Devolución", command=registrar_devolucion)
devolver_button.grid(row=4, column=0, columnspan=2, pady=10)

actualizar_prestamos()
root.mainloop()
