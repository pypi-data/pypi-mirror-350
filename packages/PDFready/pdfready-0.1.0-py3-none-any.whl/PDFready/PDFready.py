from tkinter import * # Importar tkinter para la interfaz gráfica
from tkinter import filedialog # Importar filedialog para abrir archivos
from PIL import ImageTk, Image # Importar PIL para manejar imágenes
from pdf2image import convert_from_path # Importar pdf2image para convertir PDF a imágenes
import os # Importar os para manejar rutas de archivos
import json # Importar json para manejar archivos JSON

root = Tk() # Crear la ventana principal
root.title("PDF Reader") # Título de la ventana
root.geometry("800x600") # Dimensiones de la ventana
root.config(bg="lightblue")   # Color de fondo

progress_file = "progress.json"
current_file = None

pdf_pages = []
page_index = 0  

image_label = Label(root)
image_label.pack(pady=20)

page_label = Label(root, text="", bg="lightblue", font=("arial", 12))
page_label.pack(pady=10)



def show_page(index):
    global image_label, pdf_pages
    if 0 <= index < len(pdf_pages):
        # Redimensionar imagen para que se ajuste a la ventana
        resized_img = pdf_pages[index].resize((750, 500), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(resized_img)
        image_label.configure(image=img)
        image_label.image = img
        page_label.config(text=f"página {index + 1} de {len(pdf_pages)}")
    else:
        print(f"Índice fuera de rango: {index}")

def open_pdf():
    global pdf_pages, page_index, current_file
    file_path = filedialog.askopenfilename(
        title="Seleccionar PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    if file_path:
        try:
            pdf_pages = convert_from_path(file_path, dpi=100)
            print(f"Páginas cargadas: {len(pdf_pages)}")
            if pdf_pages:
                current_file = file_path 
                # Cargar el progreso desde el archivo JSON
                if os.path.exists(progress_file):
                    with open(progress_file, 'r') as f:
                        progress = json.load(f)
                        page_index = progress.get(current_file, 0)
                else: 
                    page_index = 0
                show_page(page_index)
            else:
                print("No se pudieron cargar páginas.")
        except Exception as e:
            print(f"Error al convertir PDF: {e}")

def next_page():
    global page_index
    if page_index + 1 < len(pdf_pages):
        page_index += 1
        show_page(page_index)

def previous_page():
    global page_index
    if page_index - 1 >= 0:
        page_index -= 1
        show_page(page_index)

btn_frame = Frame(root, bg="lightblue")
btn_frame.pack(pady=10)

Button(btn_frame, text="Abrir PDF", command=open_pdf, width=15).grid(row=0, column=0, padx=10)
Button(btn_frame, text="Página Anterior", command=previous_page, width=15).grid(row=0, column=1, padx=10)
Button(btn_frame, text="Página Siguiente", command=next_page, width=15).grid(row=0, column=2, padx=10)

def on_closing():
    if current_file:
        try:
            if os.path.exists(progress_file):
                with open(progress_file, 'r') as f:
                    progress = json.load(f)
            else:
                progress = {}
            progress[current_file] = page_index
            with open(progress_file, 'w') as f:
                json.dump(progress, f)
        except Exception as e:
            print(f"Error al guardar el progreso: {e}")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop() # Iniciar el bucle principal de la interfaz gráfica


