def multiplicar(a: int, b: int) -> int:
    """Retorna o produto de dois números."""
    return a * b

def dividir(a: float, b: float) -> float:
    """Retorna o resultado da divisão de a por b. Levanta erro se b for zero."""
    if b == 0:
        raise ValueError("Divisor não pode ser zero.")
    return a / b