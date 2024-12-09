import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
import cv2
import webbrowser
import validators

# Silenciar advertencias de deprecación en macOS
os.environ['TK_SILENCE_DEPRECATION'] = '1'

def copiar_al_portapapeles(texto):
    ventana.clipboard_clear()
    ventana.clipboard_append(texto)
    ventana.update()
    messagebox.showinfo("Copiado", "El contenido ha sido copiado al portapapeles.")

def abrir_en_navegador(url):
    try:
        webbrowser.open(url, new=2)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el navegador:\n{str(e)}")

def mostrar_resultado_qr(datos):
    if not datos:
        messagebox.showerror("Error", "No se pudo decodificar el código QR.")
        return

    datos = datos.strip()

    ventana_resultado = tk.Toplevel(ventana)
    ventana_resultado.title("Resultado QR")
    ventana_resultado.geometry("400x200")

    etiqueta = tk.Label(ventana_resultado, text="Resultado del Código QR:", font=("Arial", 12))
    etiqueta.pack(pady=10)

    texto_resultado = tk.Text(ventana_resultado, height=5, width=40, wrap=tk.WORD, font=("Arial", 12))
    texto_resultado.insert(tk.END, datos)
    texto_resultado.configure(state="disabled")
    texto_resultado.pack(pady=10)

    if validators.url(datos):
        boton_abrir = tk.Button(
            ventana_resultado,
            text="Abrir en Navegador",
            command=lambda: abrir_en_navegador(datos)
        )
        boton_abrir.pack(pady=5)
    else:
        boton_copiar = tk.Button(ventana_resultado, text="Copiar al Portapapeles", command=lambda: copiar_al_portapapeles(datos))
        boton_copiar.pack(pady=5)

def generar_qr():
    texto = entrada_texto.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showerror("Error", "Por favor, ingrese algún texto para generar el QR.")
        return

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(texto)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((400, 400), Image.Resampling.LANCZOS)

    img_tk = ImageTk.PhotoImage(img)
    etiqueta_imagen.config(image=img_tk)
    etiqueta_imagen.image = img_tk

    archivo = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("Archivos PNG", "*.png")],
                                            title="Guardar código QR")
    if archivo:
        img.save(archivo)
        messagebox.showinfo("Éxito", f"El código QR ha sido guardado en: {archivo}")
    else:
        messagebox.showwarning("Cancelado", "No se guardó el archivo.")

def decodificar_qr():
    archivo = filedialog.askopenfilename(
        title="Seleccione una imagen para decodificar",
        filetypes=[
            ("Imágenes compatibles", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("Archivos PNG", "*.png"),
            ("Archivos JPG", "*.jpg"),
            ("Archivos JPEG", "*.jpeg"),
            ("Archivos BMP", "*.bmp"),
            ("Archivos GIF", "*.gif"),
            ("Todos los archivos", "*.*")
        ]
    )
    if not archivo:
        return

    imagen = cv2.imread(archivo)
    if imagen is None:
        messagebox.showerror("Error", "No se pudo cargar la imagen seleccionada.")
        return

    detector = cv2.QRCodeDetector()
    datos, _, _ = detector.detectAndDecode(imagen)
    mostrar_resultado_qr(datos)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Generador y Lector de QR")
ventana.geometry("500x650")
ventana.resizable(False, False)

# Widgets
etiqueta_instruccion = tk.Label(ventana, text="Ingrese texto para generar el código QR:", font=("Arial", 12))
etiqueta_instruccion.pack(pady=10)

entrada_texto = tk.Text(ventana, height=5, width=50, wrap=tk.WORD, font=("Arial", 12))
entrada_texto.pack(pady=10)

boton_generar = tk.Button(ventana, text="Generar Código QR", command=generar_qr, bg="green", fg="white", font=("Arial", 12))
boton_generar.pack(pady=10)

boton_descodificar = tk.Button(ventana, text="Decodificar Código QR", command=decodificar_qr, bg="blue", fg="white", font=("Arial", 12))
boton_descodificar.pack(pady=10)

etiqueta_imagen = tk.Label(ventana)
etiqueta_imagen.pack(pady=20)

# Inicio de la aplicación
ventana.mainloop()