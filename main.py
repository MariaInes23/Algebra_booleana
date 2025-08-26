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

# Marco principal
marco = tk.Frame(ventana, bg="#e0f7fa", padx=30, pady=30)
marco.pack(fill='both', expand=True)

# Etiqueta
etiqueta = tk.Label(
    marco, 
    text="Ingresa expresión:", 
    font=("Consolas", 22, "bold"), 
    fg="#006064", 
    bg="#e0f7fa"
)
etiqueta.grid(row=0, column=0, sticky='w', pady=10)

# Entrada de expresión
entrada_expr = ttk.Entry(marco, width=80, font=("Consolas", 28))
entrada_expr.grid(row=1, column=0, sticky='we', pady=6)
  

# Estilo mejorado para el botón
estilo = ttk.Style()
estilo.theme_use('clam')  

estilo.configure(
    "BotonGrande.TButton",
    font=("Consolas", 20, "bold"),
    foreground="white",
    background="#00796b",
    padding=12,
    borderwidth=0,
    focusthickness=3,
    focuscolor='none'
)
estilo.map(
    "BotonGrande.TButton",
    background=[('active', '#004d40'), ('!disabled', '#00796b')],
    foreground=[('active', 'white'), ('!disabled', 'white')]
)

boton = ttk.Button(
    marco,
    text="Simplificar paso a paso",
    command=ejecutar_simplificacion,
    style="BotonGrande.TButton"
)
boton.grid(row=1, column=1, padx=10, pady=6, ipadx=25, ipady=15)

# Ayuda sobre la expresión
ayuda_lbl = tk.Label(
    marco,
    text="(Puede usar +, *, (). Para la negación usar ' o ´)",
    fg="#004d40",
    bg="#e0f7fa",
    font=("Consolas", 18)
)
ayuda_lbl.grid(row=2, column=0, columnspan=2, sticky='w', pady=4)

# Área de pasos
area_pasos = tk.Text(
    marco, 
    height=22, 
    wrap='word', 
    font=("Consolas", 18), 
    bg="#ffffff", 
    fg="#222", 
    relief="groove", 
    borderwidth=2
)
area_pasos.grid(row=3, column=0, columnspan=2, sticky='nsew', pady=10)

# Scrollbar
scroll = ttk.Scrollbar(marco, command=area_pasos.yview)
scroll.grid(row=3, column=2, sticky='ns', padx=(0,10))
area_pasos['yscrollcommand'] = scroll.set
area_pasos.config(state='disabled')

# Configuración de colores en los pasos
area_pasos.tag_config("expr_inicial", foreground="#01579b", font=("Consolas", 26, "bold"))
area_pasos.tag_config("paso", foreground="#e65100", font=("Consolas", 24, "bold"))
area_pasos.tag_config("expr", foreground="#263238", font=("Consolas", 22))
area_pasos.tag_config("regla", foreground="#30ac36", font=("Consolas", 22, "italic"))
area_pasos.tag_config("final", foreground="#b71c1c", font=("Consolas", 26, "bold"))


marco.rowconfigure(3, weight=1)
marco.columnconfigure(0, weight=1)

ventana.mainloop()
