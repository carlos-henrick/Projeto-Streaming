from datetime import date

IDADES_VALIDAS = {
    "L": 0,
    10: 10,
    12: 12,
    14: 14,
    16: 16,
    18: 18
}

def validar_string(valor, nome, obrigatorio=True):
    if valor is None:
        return None if not obrigatorio else None
    if not isinstance(valor, str) or not valor.strip():
        return None
    return valor.strip()


def validar_int_positivo(valor, nome):
    try:
        valor = int(valor)
        if valor <= 0:
            raise ValueError
        return valor
    except:
        return f"{nome} inválido."

def validar_idade(valor):
    if valor is None:
        return None, "Idade é obrigatória."

    if isinstance(valor, str):
        valor = valor.strip().upper()
        if valor in IDADES_VALIDAS:
            return IDADES_VALIDAS[valor], None
        if valor.isdigit() and int(valor) in IDADES_VALIDAS:
            return int(valor), None

    if isinstance(valor, int) and valor in IDADES_VALIDAS:
        return valor, None

    return None, "Idade inválida. Use L, 10, 12, 14, 16 ou 18."

def validar_data_iso(data_raw):
    if not data_raw:
        return None, None
    try:
        return date.fromisoformat(data_raw), None
    except ValueError:
        return None, "Data inválida. Use YYYY-MM-DD."
