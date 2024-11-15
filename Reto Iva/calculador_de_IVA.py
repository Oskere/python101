# Programa para calcular el IVA:

# Importante:
# Guardar historicos de las operaciones realizadas

# Asignación de variables
iva = 0.00
precioBase = 0.00
precioConIva = 0.00
totalIva = 0.00
user = ""
opcion = int(input("Introduce la opcion que deseas realizar:\n1 - Calcular el iva\n2 - Obtener el precio base\n"))
match opcion:
    case 1:
        # Recolectar datos de la transaccion:
        user = input("¿Quien está realziando la transaccion?\n")
        precioBase = float(input("Introduce el precio que quieres comprobar:\n"))
        iva = float(input("Introduce el porcentaje de IVA que se le aplica a esa transacción\n%"))

        # Convertir de % a float usable para el calculo:
        iva = iva / 100

        # Calculos:
        totalIva = precioBase * iva
        precioConIva = precioBase + totalIva

        # Imprimir resultados
        print(f"\nEl precio con IVA ascenderia a:  {precioConIva:.2f}€")
        print(f"\nEl total del IVA asciende a: {totalIva:.2f}")
    case 2:
        # Recolectar datos de la transaccion:
        user = input("¿Quien está realziando la consulta?\n")
        precioConIva = float(input("Introduce el precio que quieres comprobar:\n"))
        iva = int(input("Introduce el porcentaje de IVA que se le aplicó a esa transacción\n(si no lo sabes introduce 0 y se le asignará un valor por defecto)\n%"))
        
        # Asignar valor predeterminado al IVA
        if iva == 0:
            iva = 21
        
        # Convertir de % a float usable para el calculo:
        iva = iva / 100
        iva += 1

        # Calculos:
        precioBase = precioConIva / iva
        totalIva = precioConIva - precioBase

        # Imprimir resultados
        print(f"\nEl precio base es:  {precioBase:.2f}€")
        print(f"\nEl total del IVA es: {totalIva:.2f}€")



# # Bucles prueba:
# prueba = [1, 5, 6, 2]

# for index, valor in enumerate(prueba):
#     print(f"{index} -- {valor}")