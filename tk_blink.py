### IMPORTS
import tkinter as tk
from tkinter import ttk
from pymata4 import pymata4
from i2c import LiquidCrystal_I2C

#Definición de board
board = pymata4.Pymata4()

r = 3
g = 5
b = 6
#Definición de pines y de tk
board.set_pin_mode_digital_output(8) # Definir pin8 como salida
board.set_pin_mode_digital_input(7) # Definir pin7 como entrada
board.set_pin_mode_pwm_output(3)
board.set_pin_mode_pwm_output(5)
board.set_pin_mode_pwm_output(6)
LCD = LiquidCrystal_I2C(0x27, 0, 1, board) # Definición de LCD con I2C
root = tk.Tk() # Definición de la raíz de tkinter
root.geometry("700x700") # Tamaño de la ventana
root.title("Firmata") # Definición del título de la ventana


def on_select(event):
    # Obtener el valor seleccionado
    selected = combobox.get()
    # Actualizar la etiqueta con el valor seleccionado

# Función de boton de ON
def buttonON_click():
    board.digital_pin_write(8, 1)
    print("Botón ON presionado")


# funcion de boton de OFF
def buttonOFF_click():
    board.digital_pin_write(8, 0)
    print("Botón OFF presionado")

frame1 = tk.Frame(root, width=400, height=100)
frame1.place(x=150,y=200)

# Definición de botones
buttonON = ttk.Button(frame1, text="ON", command=buttonON_click)
buttonOFF = ttk.Button(frame1, text="OFF", command=buttonOFF_click)
buttonON.pack(side="left")
buttonOFF.pack(side="right")

# Definición de led
canvas = tk.Canvas(root, width=50, height=50)
canvas.place(x=250, y=300)
circle = canvas.create_oval(0, 0, 50, 50, fill="gray")

# Condición de encendido del led
def check_condition():
    if board.digital_read(7)[0] == 1:
        canvas.itemconfig(circle, fill="green")
    else:
        canvas.itemconfig(circle, fill="grey")
    root.after(1, check_condition)
root.after(1, check_condition)


label = ttk.Label(root, text="Introduce tu mensaje:")
label.place(x=200,y=400)



entry = ttk.Entry(root)
entry.place(x=350,y=400)

def send_message():
    message = entry.get()
    if "/" in message:
        lines = message.split("/")
        LCD.enable_backlight()
        LCD.clear()
        LCD.print(lines[0])
        LCD.set_cursor(0, 1)
        LCD.print(lines[1])
        print(f"Línea 1: {lines[0]}")
        print(f"Línea 2: {lines[1]}")
    else: 
        LCD.enable_backlight()
        LCD.clear()
        LCD.print(message)
        print(f"Mensaje enviado: {message}")

send_button = ttk.Button(root,text="Enviar",command=send_message)
send_button.place(x=500,y=400)
# Crea una variable para almacenar el valor seleccionado
selected_value = tk.StringVar()

# Crea el widget Combobox
combobox = ttk.Combobox(root, textvariable=selected_value)
combobox["values"] = ("Red", "Green", "Blue", "Yellow", "White", "Magenta")
combobox.pack()
combobox.bind("<<ComboboxSelected>>", on_select)
def onChangeCombobox():
    current_value = selected_value.get()
    match current_value:
        case "Red":
            board.pwm_write(r, 255)
            board.pwm_write(b, 0)
            board.pwm_write(b, 0)
        case "Green":
            board.pwm_write(r, 0)
            board.pwm_write(g, 255)
            board.pwm_write(b, 0)
        case "Blue":
            board.pwm_write(r, 0)
            board.pwm_write(g, 0)
            board.pwm_write(b, 255)
        case "Yellow":
            board.pwm_write(r, 170)
            board.pwm_write(g, 205)
            board.pwm_write(b, 0)
        case "White":
            board.pwm_write(r, 255)
            board.pwm_write(g, 255)
            board.pwm_write(b, 255)
        case "Magenta":
            board.pwm_write(r, 255)
            board.pwm_write(g, 0)
            board.pwm_write(b, 255)
    #print(current_value)
    root.after(500, onChangeCombobox)
root.after(500, onChangeCombobox)
root.mainloop()