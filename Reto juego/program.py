import random
from os import system

def contadorIntentos (intentos):
    """Cuenta el numero de intentos que le quedan al usuario."""
    intentos -= 1
    if intentos == 0:
        print("Has agotado todos tus intentos...\n¡más suerte la proxima vez!")
    else:
        print(f"Te quedan {intentos}. Buena suerte!")
    return intentos

def adivinar (num,intentos,secreto):
    """Comprueba si el usuario ha acertado el numero o no."""
    if num > secreto:
        print("Lo siento, el numero que estoy pensando es MENOR que el que has introducido.")
        return False
    elif num < secreto:
        print("Lo siento, el numero que estoy pensando es MAYOR que el que has introducido.")
        return False
    else:
        print("¡Felicidades, has acertado el numero que estaba pensando!")
        print(f"El numero de intentos sobrantes es: {intentos}")
        return True
        
def leaderboard(scoreboard):
    """Imprime los tres primeros lugares (podio) y luego el resto en lista ordenada."""
    scoreboard.sort(key=lambda x: x[1], reverse=True)
    
    print("\n--- Podio ---")
    for i in range(min(3, len(scoreboard))):
        if i == 0:
            print(f"🥇 {scoreboard[i][0]}: {scoreboard[i][1]} puntos")
        elif i == 1:
            print(f"🥈 {scoreboard[i][0]}: {scoreboard[i][1]} puntos")
        elif i == 2:
            print(f"🥉 {scoreboard[i][0]}: {scoreboard[i][1]} puntos")
    
    print("\n--- Resto de jugadores ---")
    for i in range(3, len(scoreboard)):
        print(f"{scoreboard[i][0]}: {scoreboard[i][1]} puntos")


if __name__ == "__main__":
    scoreboard = []
    intentos = 3
    secreto = random.randint(0,10)
    fin = False
    puntos = 0
    nombre_usuario = input("¡Hola! ¿Cómo te llamas? ").strip()
    replay = ""

    while replay != "n":
        
        if intentos == 3:
            print(f"¡Bienvenido al juego de adivinar el número (0-10) {nombre_usuario}!")
        num = int(input("¿Que numero estoy pensando? -> "))
        fin = adivinar(num,intentos,secreto)

        if not fin:
            intentos = contadorIntentos(intentos)
        elif fin or intentos == 0:
            puntos = intentos * 10
            print(f"has conseguido un total de: {puntos}pt.")
            print(f"{nombre_usuario} y {puntos}")
            scoreboard.append([nombre_usuario,puntos])
            intentos = 3
            replay = input("¿Quieres jugar de nuevo?(s/n)").strip().lower()
            if replay == "s":
                system("cls")
                nombre_usuario = input("¡Hola! ¿Cómo te llamas? ").strip()
                secreto = random.randint(0, 20)
                fin = False

    system("cls")
    print("¡Gracias por jugar! Hasta luego.")
    leaderboard(scoreboard)
