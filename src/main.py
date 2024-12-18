import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Base de datos
Base = declarative_base()

# Creación de la entidad
class Tarea(Base):
    __tablename__ = "tareas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    completada = Column(Boolean, default=False)

# Creación de la base de datos y tabla
motor_db = create_engine("sqlite:///tareas.db")
Base.metadata.create_all(motor_db)

# Creación de la sesión
Sesion = sessionmaker(bind=motor_db)
sesion = Sesion()

# Clase principal de la aplicación
class AppGestorTareas:
    def __init__(self, root):
        # Configuración de la ventana
        self.root = root
        self.root.title("Gestión de Tareas")

        ancho_ventana = 400
        alto_ventana = 600

        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        pos_x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        pos_y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
        self.root.configure(bg="#f5f5f5")

        # Widgets
        encabezado = tk.Label(root, text="Gestión de Tareas", font=("Arial", 20, "bold"), bg="#4caf50", fg="white")
        encabezado.pack(fill=tk.X, pady=10)

        self.frame_formulario = tk.Frame(root, bg="#f5f5f5")
        self.frame_formulario.pack(pady=10)

        self.etiqueta_titulo = tk.Label(self.frame_formulario, text="Título:", font=("Arial", 12), bg="#f5f5f5")
        self.etiqueta_titulo.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.entrada_titulo = tk.Entry(self.frame_formulario, width=40)
        self.entrada_titulo.grid(row=0, column=1, pady=5)

        self.etiqueta_descripcion = tk.Label(self.frame_formulario, text="Descripción:", font=("Arial", 12), bg="#f5f5f5")
        self.etiqueta_descripcion.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.entrada_descripcion = tk.Entry(self.frame_formulario, width=40)
        self.entrada_descripcion.grid(row=1, column=1, pady=5)

        self.boton_añadir = tk.Button(root, text="Añadir Tarea", command=self.añadir_tarea, bg="#4caf50", fg="white", font=("Arial", 12))
        self.boton_añadir.pack(pady=10)

        self.lista_tareas = tk.Listbox(root, width=50, height=15, font=("Arial", 10), selectbackground="#4caf50")
        self.lista_tareas.pack(pady=10)

        self.frame_botones = tk.Frame(root, bg="#f5f5f5")
        self.frame_botones.pack(pady=10)

        self.boton_completar = tk.Button(self.frame_botones, text="Completar", command=self.completar_tarea, bg="#ff9800", fg="white", font=("Arial", 10))
        self.boton_completar.grid(row=0, column=0, padx=10)

        self.boton_eliminar = tk.Button(self.frame_botones, text="Eliminar", command=self.eliminar_tarea, bg="#f44336", fg="white", font=("Arial", 10))
        self.boton_eliminar.grid(row=0, column=1, padx=10)

        self.boton_exportar_json = tk.Button(self.frame_botones, text="Exportar JSON", command=self.exportar_json, bg="#2196f3", fg="white", font=("Arial", 10))
        self.boton_exportar_json.grid(row=0, column=2, padx=10)

        self.boton_importar_json = tk.Button(self.frame_botones, text="Importar JSON", command=self.importar_json, bg="#673ab7", fg="white", font=("Arial", 10))
        self.boton_importar_json.grid(row=0, column=3, padx=10)

        # Cargar tareas desde la base de datos
        self.cargar_tareas_db()

    def cargar_tareas_db(self):
        self.lista_tareas.delete(0, tk.END)
        tareas = sesion.query(Tarea).all()
        for tarea in tareas:
            estado = "Completada" if tarea.completada else "Pendiente"
            self.lista_tareas.insert(tk.END, f"{tarea.id} - {tarea.titulo} - {estado}")

    def añadir_tarea(self):
        titulo = self.entrada_titulo.get()
        descripcion = self.entrada_descripcion.get()

        if titulo and descripcion:
            nueva_tarea = Tarea(titulo=titulo, descripcion=descripcion)
            sesion.add(nueva_tarea)
            sesion.commit()
            self.cargar_tareas_db()
            self.entrada_titulo.delete(0, tk.END)
            self.entrada_descripcion.delete(0, tk.END)
        else:
            messagebox.showwarning("Entrada vacía", "Ingrese un título y una descripción")

    def completar_tarea(self):
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            datos_tarea = self.lista_tareas.get(seleccion[0])
            id_tarea = int(datos_tarea.split(" - ")[0])
            tarea = sesion.query(Tarea).filter(Tarea.id == id_tarea).first()
            if tarea:
                tarea.completada = True
                sesion.commit()
                self.cargar_tareas_db()
            else:
                messagebox.showerror("Error", "No se encontró la tarea en la base de datos")
        else:
            messagebox.showwarning("Sin selección", "Seleccione una tarea para completar")

    def eliminar_tarea(self):
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            datos_tarea = self.lista_tareas.get(seleccion[0])
            id_tarea = int(datos_tarea.split(" - ")[0])
            tarea = sesion.query(Tarea).filter(Tarea.id == id_tarea).first()
            if tarea:
                sesion.delete(tarea)
                sesion.commit()
                self.cargar_tareas_db()
            else:
                messagebox.showerror("Error", "No se encontró la tarea en la base de datos")
        else:
            messagebox.showwarning("Sin selección", "Seleccione una tarea para eliminar")

    def exportar_json(self):
        tareas = sesion.query(Tarea).all()
        formato_json = [{"titulo": tarea.titulo, "descripcion": tarea.descripcion, "completada": tarea.completada} for tarea in tareas]
        with open("tareas_exportadas.json", "w") as archivo:
            json.dump(formato_json, archivo, indent=4)
        messagebox.showinfo("Éxito", "Tareas guardadas en: tareas_exportadas.json")

    def importar_json(self):
        try:
            with open("tareas_exportadas.json", "r") as archivo:
                lista_tareas = json.load(archivo)
            for datos_tarea in lista_tareas:
                tarea_existente = sesion.query(Tarea).filter(Tarea.titulo == datos_tarea["titulo"], Tarea.descripcion == datos_tarea["descripcion"]).first()
                if not tarea_existente:
                    nueva_tarea = Tarea(**datos_tarea)
                    sesion.add(nueva_tarea)
            sesion.commit()
            self.cargar_tareas_db()
            messagebox.showinfo("Éxito", "Tareas cargadas desde tareas_exportadas.json")
        except FileNotFoundError:
            messagebox.showerror("Archivo no encontrado", "No se pudo encontrar el archivo tareas_exportadas.json.")

# Bloque principal
if __name__ == "__main__":
    root = tk.Tk()
    app = AppGestorTareas(root)
    root.mainloop()
