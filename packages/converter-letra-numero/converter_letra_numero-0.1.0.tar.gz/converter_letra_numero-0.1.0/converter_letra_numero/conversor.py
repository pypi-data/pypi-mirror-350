def letra_para_numero(letra: str) -> int:
    """
    Converte uma letra maiúscula (A-Z) em número (0-25).
    Lança ValueError para entrada inválida.
    """
    if len(letra) != 1 or not letra.isalpha():
        raise ValueError("Informe uma única letra A-Z")
    codigo = ord(letra.upper()) - ord('A')
    if not (0 <= codigo <= 25):
        raise ValueError("Letra fora do intervalo A-Z")
    return codigo
