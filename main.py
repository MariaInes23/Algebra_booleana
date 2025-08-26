import tkinter as tk
from tkinter import ttk, messagebox
from analizador import analizar_expresion
from reglas import simplificar_con_pasos


def ejecutar_simplificacion():
    texto = entrada_expr.get()
    if not texto.strip():
        messagebox.showwarning("Atención", "Debes ingresar una expresión booleana.")
        return
    try:
        expresion = analizar_expresion(texto)
        pasos, expresion_final = simplificar_con_pasos(expresion)

        area_pasos.config(state='normal')
        area_pasos.delete('1.0', tk.END)
        
        for i, (regla, s) in enumerate(pasos):
            if i == 0:
                area_pasos.insert(tk.END, f"{s}\n", "expr_inicial")
            else:
                area_pasos.insert(tk.END, f"Paso {i}: ", "paso")
                area_pasos.insert(tk.END, f"{s}    ", "expr")
                if regla:
                    area_pasos.insert(tk.END, f"[{regla}]\n", "regla")
        area_pasos.insert(tk.END, "\nResultado final: " + str(expresion_final), "final")
        area_pasos.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Error de análisis", str(e))


# Ventana principal
ventana = tk.Tk()
ventana.title("Simplificador Booleano — Paso a Paso")
ventana.state("zoomed") 

marco = tk.Frame(ventana, bg="#77a6af", padx=40, pady=40)
marco.pack(fill='both', expand=True)

etiqueta = tk.Label(
    marco, 
    text="Ingresa expresión:",
    font=("Consolas", 20, "bold"), 
    fg="black"
)                   
etiqueta.grid(row=0, column=0, sticky='w', pady=10)

entrada_expr = ttk.Entry(marco, width=90, font=("Consolas", 35))
entrada_expr.grid(row=1, column=0, sticky='we', pady=6)
entrada_expr.insert(0, "AB + A(B´+C)")  

boton = ttk.Button(marco, text="Simplificar paso a paso", command=ejecutar_simplificacion)
boton.grid(row=1, column=1, padx=8, pady=6, ipadx=20, ipady=10)
boton.config(style="BotonGrande.TButton")

# Estilo del botón
estilo = ttk.Style()
estilo.configure("BotonGrande.TButton", font=("Consolas", 18, "bold"), padding=10)

ayuda_lbl = ttk.Label(
    marco,
    text="(usa +, concatenación/* para Y, ' o ´ para NO, paréntesis)",
    foreground="#555",
    font=("Consolas", 20)
)
ayuda_lbl.grid(row=2, column=0, columnspan=2, sticky='w', pady=4)

area_pasos = tk.Text(
    marco, 
    height=22, 
    wrap='word', 
    font=("Consolas", 16), 
    bg="#f3f3f3", 
    fg="#222", 
    relief="solid", 
    borderwidth=1
)
area_pasos.grid(row=3, column=0, columnspan=2, sticky='nsew', pady=8)

scroll = ttk.Scrollbar(marco, command=area_pasos.yview)
scroll.grid(row=3, column=2, sticky='ns')
area_pasos['yscrollcommand'] = scroll.set
area_pasos.config(state='disabled')

# Configuración de colores en los pasos
area_pasos.tag_config("expr_inicial", foreground="#2b3e50", font=("Consolas", 30, "bold"))
area_pasos.tag_config("paso", foreground="#d35400", font=("Consolas", 30, "bold"))
area_pasos.tag_config("expr", foreground="#34495e", font=("Consolas", 30))
area_pasos.tag_config("regla", foreground="#27ae60", font=("Consolas", 30, "italic"))
area_pasos.tag_config("final", foreground="#c0392b", font=("Consolas", 30, "bold"))

marco.rowconfigure(3, weight=1)
marco.columnconfigure(0, weight=1)

ventana.mainloop()
