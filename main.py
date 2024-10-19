

import os
import subprocess
import sys
import time


# Function to install a package if it's not already installed
def install_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# List of packages to install
packages = [
   'tkinterweb',  # For flask
   'selenium',
   'pywebview',
   'webdriver-manager'
   
]
# Install each package
for package in packages:
    install_package(package)

import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



# Ruta a tu proyecto Git
GIT_PROJECT_PATH = r"D:\BackUp\2024\Programacion\git proyects\pythonDeploy"

# Diccionario de marcas de coches y sus páginas web
car_brands = {
    "Toyota": "https://www.toyota.com",
    "BMW": "https://www.bmw.com",
    "Mercedes": "https://www.mercedes-benz.com",
    "Audi": "https://www.audi.com",
    "Tesla": "https://www.tesla.com",
    "Ford": "https://www.ford.com"
}

# Variable para saber si se ha actualizado
updated = False

# Función para verificar actualizaciones en GitHub
def check_for_updates():
    global updated
    try:
        # Cambiar al directorio del proyecto Git
        os.chdir(GIT_PROJECT_PATH)
        
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
            messagebox.showerror("Error", "No se detecta un repositorio git en la ruta.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al verificar actualizaciones: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {e}")

# Función para actualizar el repositorio
def update_repository():
    global updated
    try:
        subprocess.run(['git', 'pull'], check=True)
        updated = True  # Marcamos que se ha actualizado
        messagebox.showinfo("Actualización", "El repositorio se ha actualizado correctamente.")
        show_restart_button()  # Mostramos el botón de relanzar
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al actualizar el repositorio: {e}")

# Función para relanzar la aplicación
def restart_application():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Mostrar botón de relanzar si se actualiza el repositorio
def show_restart_button():
    restart_btn.pack(pady=5)

# Función para iniciar Selenium y abrir la URL
def open_url_in_selenium(url):
    try:
        # Configurar el servicio de Chromedriver
        service = Service(ChromeDriverManager().install())
        
        # Opciones de Selenium para lanzar Chromium
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-fullscreen')  # Inicia en pantalla completa (sin barra de direcciones)
        options.add_argument('--hide-scrollbars')   # Oculta las barras de desplazamiento
        options.add_argument('--disable-infobars')  # Deshabilita la barra de información de Chrome
        options.add_argument('--kiosk')  # Modo kiosco (oculta barra de direcciones, menú, etc.)
        # Iniciar el driver de Selenium
        driver = webdriver.Chrome(service=service, options=options)
        
        # Actualizar la etiqueta de estado en el pie de página
        update_footer_status(f"Connecting to {url}...")
        
        # Abrir la URL en el navegador
        driver.get(url)
        
        # Actualizar la etiqueta cuando la página se cargue
        update_footer_status(f"Connected to {url}")
        time.sleep(500)  # Esperar 5 segundos
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el navegador: {e}")
        update_footer_status(f"Error connecting to {url}")

# Función para cargar la página web de la marca seleccionada
def load_car_brand_url():
    selected_brand = car_brand_var.get()  # Obtener marca seleccionada
    if selected_brand:
        url = car_brands.get(selected_brand)
        if url:
            # Iniciar el navegador con Selenium
            open_url_in_selenium(url)

# Función para actualizar la etiqueta en el pie de página
def update_footer_status(message):
    footer_label.config(text=message)

# Crear ventana principal de Tkinter
def create_menu():
    root = tk.Tk()
    root.title("Mi Aplicación")

    # Frame para la lista de marcas
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Menú de marcas de coches
    tk.Label(frame, text="Selecciona una marca de coche:").pack(pady=5)
    
    global car_brand_var
    car_brand_var = tk.StringVar()
    car_brand_menu = tk.OptionMenu(frame, car_brand_var, *car_brands.keys())
    car_brand_menu.pack(pady=5)

    # Botón para cargar la página de la marca
    load_btn = tk.Button(frame, text="Abrir página", command=load_car_brand_url)
    load_btn.pack(pady=5)

    # Menú de actualizaciones
    check_updates_btn = tk.Button(root, text="Verificar actualizaciones", command=check_for_updates)
    check_updates_btn.pack(pady=5)

    global restart_btn
    restart_btn = tk.Button(root, text="Relanzar aplicación", command=restart_application)
    restart_btn.pack_forget()  # Ocultamos el botón de relanzar hasta que sea necesario

    exit_btn = tk.Button(root, text="Salir", command=root.quit)
    exit_btn.pack(pady=5)

    # Pie de página (Footer) para mostrar la consola de estado
    global footer_label
    footer_label = tk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
    footer_label.pack(side=tk.BOTTOM, fill=tk.X)

    root.geometry("800x600")  # Tamaño de la ventana
    root.mainloop()

# Ejecución principal de la aplicación
if __name__ == "__main__":
    # Cada vez que la aplicación se inicia, comprueba actualizaciones
    check_for_updates()
    
    # Crea el menú de la aplicación
    create_menu()
