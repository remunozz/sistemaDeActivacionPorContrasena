from time import sleep  # Importa la biblioteca "time" para gestionar pausas de tiempo
from machine import Pin, SoftI2C, PWM # Importa las clases Pin, SoftI2C y PWM (Pulse Width Modulation - Modulación de Ancho de Pulso), desde el módulo machine, se utilizan para controlar pines GPIO, comunicación I2C, y movimiento del servomotor respectivamente.
from lcd_api import LcdApi  # Importa la clase "LcdApi" para el control de la pantalla LCD
from i2c_lcd import I2cLcd  # Importa la clase "I2cLcd" para la comunicación I2C con la pantalla LCD
from utime import sleep, sleep_ms  # Importa la biblioteca "utime" para gestionar el tiempo de manera más precisa
from hashlib import sha256 # Importar la función de resumen criptográfico SHA-256 (Secure Hash Algorithm 256 bits) desde el módulo hashlib en Python

# Configura el display LCD
I2C_ADDR = 0x27 # Configura la dirección I2C del dispositivo LCD
totalRows = 2 # Numero de filas del LCD
totalColumns = 16 # Numero de columnas LCD

i2c = SoftI2C (scl=Pin(22), sda= Pin(21), freq=10000) # Configura la comunicación I2C
lcd = I2cLcd (i2c, I2C_ADDR, totalRows, totalColumns)  # Crea un objeto "I2cLcd" para comunicarse con el display LCD

# Configura el servomotor
servo_pin = Pin(15)  # Configura el pin al que está conectado el servomotor
servo_motor = PWM(servo_pin, freq = 50)  # Crea un objeto PWM para controlar el servomotor, con frecuencia de 50 Hz equivalente a un periodo de 20 ms

# Función que controla el servomotor
def controller_servo_motor(angle):
    if angle == 180: # Movimiento del servo de 180°
        for i in range (4900, 8000): # Se configura la resolución de 16 bits para que el servo gire de 90° a 180°, con incremento
            servo_motor.duty_u16(i) # Se utiliza para establecer el ciclo de trabajo del PWM (Pulse Width Modulation) del servo motor en un valor específico representado por i. El ciclo de trabajo controla la posición del servo motor
            sleep_ms(1) # Tiempo de retardo entre cada paso
    if angle == 90: # Movimiento del servo de 90°
        for k in range (8000, 4900, -1): # Se configura la resolución de 16 bits para que el servo gire de 180° a 90°, con decremento
            servo_motor.duty_u16(k) # Se utiliza para establecer el ciclo de trabajo del PWM (Pulse Width Modulation) del servo motor en un valor específico representado por k. El ciclo de trabajo controla la posición del servo motor
            sleep_ms(1) # Tiempo de retardo entre cada paso

# Configura el teclado matricial
# Clase teclado
class Key:
    def __init__(self, name):
        self.name = name
        self.active = False

row_pins = [2,4,5,19] #Configura los pines de las filas del teclado matricial
col_pins = [12,27,26,25] # Configura los pines de las columnas del teclado matricial

# Definición de las teclas
keys = [
  [Key('1'), Key('2'), Key('3'), Key('A')],
  [Key('4'), Key('5'), Key('6'), Key('B')],
  [Key('7'), Key('8'), Key('9'), Key('C')],
  [Key('*'), Key('0'), Key('#'), Key('D')]
]

# Definición de los pines de las filas como salida
row_pins = [Pin(pin_num, mode=Pin.OUT) for pin_num in row_pins]

# Definición de los pines de las columnas de salida
col_pins = [Pin(pin_num, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_num in col_pins]

# Escaneo del teclado 
def scan_keys():
    # Poniendo todas las filas en alto
    for row, row_pin in enumerate(row_pins):
        row_pin.on()

        # revisa cada columna para ver si se presiona la tecla
        # y establece la tecla "activa" en el teclado matricial
        for col, col_pin in enumerate(col_pins):
            keys[row][col].active = bool(col_pin.value())
        
        # Establece las filas en bajo
        row_pin.off()

# Inicializa un buffer para almacenar la contraseña ingresada
# rastreando la entrada del usuario
entered_password = '' 

# Define la contraseña que debe ingresar el usuario
# Se crea una contraseña segura con SHA256, la contraseña es:'1234567890'
correct_hash = b'\xc7u\xe7\xb7W\xed\xe60\xcd\n\xa1\x11;\xd1\x02f\x1a\xb3\x88)\xcaR\xa6B*\xb7\x82\x86/&\x86F'

# Mensaje inicial o de bienvenida al sistema
def mensajeDeBienvenida():
    lcd.putstr('Bienvenido al sistema : ')
    sleep(2) # Temporizador de 2 segundos para el mensaje inicial o de bienvenida al sistema

# Mensaje de estado de reposo 
def mansajeEstadoDeReposo():
    lcd.clear() # Limpia el displey LCD
    lcd.putstr('Ingrese la contrasena: ')
    
# Flag o marcador para limpiar LCD 
count = 1
# Flag o marcador para distinguir cuando se ha entrado al Estado de Contraseña Correcta
count_1 = 0

# LLamado a la función mensajeDeBienvenida 
mensajeDeBienvenida()

# LLamado a la funcion mansajeEstadoDeReposo
mansajeEstadoDeReposo() 

while True:  # Inicia un bucle infinito para controlar el sistema
        
        scan_keys() # Escaneando el teclado
        for row in keys: # Iteración a través de las filas en la matriz keys. En este contexto, row representa una fila de teclas
            for key in row: # Iteración a través de las teclas individuales en la fila actual (representada por row). key representa una tecla en la fila  
                if key.active: # Esto verifica si la tecla actual (key) está activa. El atributo active generalmente se establece en True si la tecla se ha presionado o está en un estado activo
                    if count : # Validación del flag o marcador que indica limpiar el display lcd 
                        lcd.clear() # Limpia el display LCD 
                        count = 0  # Pone el flag o marcador en 0, booleano False
                    if key.name is 'D': # Verifica si se preciona la tecla D, estado salir del modo ingreso de contraeña
                        lcd.clear() # Limpia el display LCD 
                        if sha256(entered_password.encode()).digest() == correct_hash: # Comparar la clave ingresada por el usuario con la almacenada en el sistema en SHA-256 
                            lcd.putstr('Contrasena Correcta') # Se muestra mensaje en displey LCD al usuario, Contraseña Correcta
                            controller_servo_motor(180) # Activación del servomotor que se mueve desde la posición de 90° a 180°
                            print('\nEstado de Contraseña Correcta') # Se muestra en consola Estado contraseña correcta
                            count_1 = 1
                        else:
                            lcd.putstr('Contrasena Incorrecta') # Se muestra mensaje en displey LCD al usuario, Contraseña Incorrecta
                            sleep(2) # Temporizador para el mensaje de Contraseña Incorrecta de 2 segundos
                            entered_password = '' # Se limpia el buffer o string que almacena la contraseña
                            mansajeEstadoDeReposo() # LLamado a la funcion mansajeEstadoDeReposo
                            print('\nEstado de Reposo') # Se muestra en consola Estado de Reposo
                            count = 1 # Pone el flag o marcador en 1, booleano True                       
                    elif key.name is '#':
                        lcd.clear() # Limpia el displey LCD
                        lcd.putstr('Reestableciendo')
                        print ('\nEstado de Reestablecer') # Se muestra en consola Estado de Reestablecer (Reestablecer la contraseña)
                        sleep(2) # Temporizador de 2 segundos para el mensaje Reestableciendo de 2 segundos
                        if count_1 == 1: # Indica que viene del Estado de Contraseña Correcta
                            controller_servo_motor(90) # Reestablecimiento de la posición inicial del servomotor que se mueve desde la posición de 90° a 180°
                            count_1 = 0 # Pone el flag o marcador en 0, booleano False 
                        entered_password = '' # Se limpia el buffer o string que almacena la contraseña
                        mansajeEstadoDeReposo() # LLamado a la funcion mansajeEstadoDeReposo
                        print('\nEstado de Reposo') # Se muestra en consola Estado de Reposo
                        count = 1 # Pone el flag o marcador en 1, booleano True                             
                    else:
                        lcd.putstr('*')  # Muestra un asterisco en el displey LCD, como indicación de ingreso de un caracter para la contraseña por parte del usuario 
                        print(key.name, end='') # Se muestra en consola los caracteres de la contraseña que ingresa el ususario
                        entered_password += key.name # String que almacena los caracteres que conforman la clave ingresada por el ususario
                    sleep(0.25) # Temporizdor de duracíón de la tecla oprimida (debounce button press )