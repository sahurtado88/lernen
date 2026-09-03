"""Calculadora básica en consola."""
OPCIONES_VALIDAS = frozenset({"1", "2", "3", "4"})


def pedir_numero(mensaje: str) -> float:
    while True:
        entrada = input(mensaje)
        try:
            return float(entrada)
        except ValueError:
            print("Entrada inválida. Escribe un número.")


def calcular(opcion: str, a: float, b: float) -> float:
    if opcion == "1":
        return a + b
    if opcion == "2":
        return a - b
    if opcion == "3":
        return a * b
    if opcion == "4":
        if b == 0:
            raise ZeroDivisionError("No se puede dividir entre cero.")
        return a / b
    raise ValueError("Opción inválida")


def mostrar_menu() -> None:
    print("\n=== Calculadora ===")
    print("1) Sumar")
    print("2) Restar")
    print("3) Multiplicar")
    print("4) Dividir")
    print("5) Salir")


def main() -> None:
    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-5): ").strip()

        if opcion == "5":
            print("Hasta luego.")
            break

        if opcion not in OPCIONES_VALIDAS:
            print("Opción inválida. Intenta de nuevo.")
            continue

        num1 = pedir_numero("Primer número: ")
        num2 = pedir_numero("Segundo número: ")

        try:
            resultado = calcular(opcion, num1, num2)
            print(f"Resultado: {resultado}")
        except ZeroDivisionError as error:
            print(error)


if __name__ == "__main__":
    main()
