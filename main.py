import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Función para verificar actualizaciones en GitHub
def check_for_updates():
    try:
        # Si el repositorio ya está clonado, actualiza
        if os.path.exists('.git'):
            # Obtiene los últimos cambios del repositorio remoto
            subprocess.run(['git', 'fetch'], check=True)
            
            # Compara los cambios locales con el repositorio remoto
            result = subprocess.run(['git', 'status', '-uno'], capture_output=True, text=True)
            if 'Your branch is behind' in result.stdout:
                update_repository()
            else:
                messagebox.showinfo("Actualización", "El repositorio está actualizado.")
        else:
            messagebox.showerror("Error", "No se detecta un repositorio git.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al verificar actualizaciones: {e}")

# Función para actualizar el repositorio
def update_repository():
    try:
        subprocess.run(['git', 'pull'], check=True)
        messagebox.showinfo("Actualización", "El repositorio se ha actualizado correctamente.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al actualizar el repositorio: {e}")

# Crear ventana principal de Tkinter
def create_menu():
    root = tk.Tk()
    root.title("Mi Aplicación")

    # Menú simple con dos botones
    menu_label = tk.Label(root, text="Bienvenido a la aplicación", font=("Arial", 14))
    menu_label.pack(pady=10)

    check_updates_btn = tk.Button(root, text="Verificar actualizaciones", command=check_for_updates)
    check_updates_btn.pack(pady=5)

    exit_btn = tk.Button(root, text="Salir", command=root.quit)
    exit_btn.pack(pady=5)

    root.mainloop()

# Ejecución principal de la aplicación
if __name__ == "__main__":
    # Cada vez que la aplicación se inicia, comprueba actualizaciones
    check_for_updates()
    
    # Crea el menú de la aplicación
    create_menu()
