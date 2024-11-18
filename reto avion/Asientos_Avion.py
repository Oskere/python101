# Inicialización de las listas
asientos = [["O","O","O","O"],["O","O","O","O"],["O","O","O","O"]]
usuarios = [["" for _ in range(4)] for _ in range(3)] 
letras = ["A", "B", "C", "D"]

# Definicion de funciones:

def mostrar_asientos():
    """Funcion para mostrar todos los asientos disponibles y reservados."""
    print("Estos son los asientos:\n(' - Nombre' = reservado)\n")
    for i, fila in enumerate(asientos):
        for j, asiento in enumerate(fila):
            letra_fila = letras[i]
            numero_columna = j + 1
            if asiento == "O":
                print(f"{letra_fila}{numero_columna}", end=" | ")
            else:
                print(f"{letra_fila}{numero_columna} - {usuarios[i][j]}", end=" | ")
        print()

def reservar_asiento_individual():
    """funcion para reservar un solo asiento."""
    print("Aquí puedes ver los asientos disponibles:")
    for i, fila in enumerate(asientos):
        for j, asiento in enumerate(fila):
            if asiento == "O":
                print(f"El asiento {letras[i]}{j+1} está Libre")
    fila = int(input("¿En qué fila quieres reservar el asiento? "))
    posicion = int(input("¿En qué posición dentro de la fila? "))

    if asientos[fila - 1][posicion - 1] == "O":
        asientos[fila - 1][posicion - 1] = "X"  # Marcar el asiento como reservado
        usuarios[fila - 1][posicion - 1] = nombre  # Guardar el nombre del usuario
        print(f"El asiento en la fila {fila}, posición {posicion} ha sido reservado.")
    else:
        print(f"El asiento en la fila {fila}, posición {posicion} no está disponible.")

def reservar_asientos_consecutivos():
    """funcion para reservar varios asientos consecutivos."""
    num = int(input("¿Cuántos asientos consecutivos quieres reservar? "))
    reservado = False
    for a, asiento in enumerate(asientos, start=1):
        consecutivos = 0
        posibles_asientos = []
        # Buscar posibles asientos consecutivos
        for l, letra in enumerate(asiento):
            if letra == "O":
                consecutivos += 1
            else:
                consecutivos = 0
            if consecutivos == num:
                posibles_asientos.append((l - num + 1, l))
                consecutivos = 0
        
        if posibles_asientos:
            if reservado:
                break
            print(f"\nFila {a}:")
            for inicio, fin in posibles_asientos:
                print(f"¡Hay {num} asientos consecutivos libres en la fila {a}, entre las posiciones {inicio + 1} y {fin + 1}!")
                reserva = input(f"¿Quieres reservar estos asientos en la fila {a} de la posición {inicio + 1} a {fin + 1}? (s/n): ").strip().lower()
                if reserva == "s":
                    for i in range(inicio, fin + 1):
                        asientos[a - 1][i] = "X"
                        usuarios[a - 1][i] = nombre
                    print(f"Los asientos de la fila {a} de la posición {inicio + 1} a {fin + 1} han sido reservados.")
                    reservado = True
                    break
                else:
                    print(f"No se han reservado los asientos de la fila {a} de la posición {inicio + 1} a {fin + 1}.")
        else:
            print(f"\nNo hay suficientes asientos libres consecutivos en la fila {a}.\n")
    else:
        print("Introduce un valor correcto.")

def cancelar_reserva():
    """Funcion para cancelar una reserva."""
    cancelar = input("¿Quieres cancelar alguna reserva? (s/n): ").strip().lower()
    
    if cancelar == "s":
        fila_cancelar = int(input("¿En qué fila está la reserva que deseas cancelar? ")) - 1
        inicio_cancelar = int(input("¿Desde qué posición deseas cancelar la reserva (inicio)? ")) - 1
        fin_cancelar = int(input("¿Hasta qué posición deseas cancelar la reserva (fin)? ")) - 1
        
        # Cancelar la reserva
        if 0 <= fila_cancelar < len(asientos) and 0 <= inicio_cancelar <= fin_cancelar < len(asientos[fila_cancelar]):
            if all(asientos[fila_cancelar][i] == "X" for i in range(inicio_cancelar, fin_cancelar + 1)):
                for i in range(inicio_cancelar, fin_cancelar + 1):
                    asientos[fila_cancelar][i] = "O"  # Marcar como libre
                    usuarios[fila_cancelar][i] = ""  # Borrar el nombre del usuario
                print(f"La reserva en la fila {fila_cancelar + 1} desde la posición {inicio_cancelar + 1} hasta la posición {fin_cancelar + 1} ha sido cancelada.")
            else:
                print("No se puede cancelar la reserva porque los asientos no están ocupados.")
        else:
            print("La fila o las posiciones proporcionadas no son válidas.")

def cambiar_usuario():
    """Funcion para cambiar de usuario."""
    global nombre
    print("Sesión cerrada de manera exitosa.")
    sesion = input("¿Quieres iniciar sesión de nuevo? (s/n)").strip().lower()
    if sesion == "s":
        nombre = input("Introduce tu nombre de usuario: ")

# Main

if __name__ == "__main__":    
    nombre = input("Introduce tu nombre de usuario: ")
    while eleccion != 0:
        eleccion = int(input("¿Qué operación deseas realizar?\n1- Ver todos los asientos.\n2- Reservar asientos\n3- Cancelar reserva\n4- Cambiar de Usuario\n0- Apagar programa\n"))
        
        match eleccion:
            case 1:
                mostrar_asientos()
            case 2:
                cantidad = input("¿Quieres reservar uno o varios asientos consecutivos? (u/v) ").strip().lower()
                if cantidad == "u":
                    reservar_asiento_individual()
                elif cantidad == "v":
                    reservar_asientos_consecutivos()
                else:
                    print("Opción no válida.")
            case 3:
                cancelar_reserva()
            case 4:
                cambiar_usuario()