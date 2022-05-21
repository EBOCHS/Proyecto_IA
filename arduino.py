import serial

led=0
mot=0

serialArduino = serial.Serial("COM6",9600) 


def showMenu():
    if led==1:        
        print('''**********************
*  MENU DE OPCIONES  *
**********************
*                    *
*  L >> APAGAR LED   *
*  M >> Servo Motor  *
*  X >> Salir        *
*                    *
**********************\n''')
    else:
        print('''**********************
*  MENU DE OPCIONES  *
**********************
*                    *
*  L >> ENCENDER LED *
*  M >> Servo Motor  *
*  X >> Salir        *
*                    *
**********************\n''')



while True:
    showMenu()
    opcion = input('Que opción desea: ').upper()
    if opcion=='L':
        if led==1:
            led=0
            print('Se APAGO el led...\n')
        else:
            led=1
            print('Se ENCENDIO el led...\n')
        cad = str(led) + ","+ str(mot)
        serialArduino.write(cad.encode('ascii'))        
    elif opcion=='M':
        mot = int(input("Introduce un valor entre 1 y 180: "))
        print("Se envió el valor de {} para el motor...\n".format(mot))
        cad = str(led) + "," + str(mot)
        serialArduino.write(cad.encode('ascii'))
    elif opcion=='X':
        print("Saliendo del sistema...\n")
        serialArduino.close()
        break
    else:
        print("Opcion no válida...\n")




