import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

def normalize_phone(candidate: str, default_region: str = 'ES') -> tuple[str, str]:
    """
    Normaliza un número de teléfono a (prefijo internacional, número nacional sin espacios).

    Args:
        candidate (str): Número de teléfono en cualquier formato.
        default_region (str): Región por defecto para inferencia, ISO 3166-1 (ej. 'ES').

    Returns:
        tuple[str, str]: (prefijo internacional, número nacional) en formato E.164.

    Raises:
        ValueError: Si el número no es válido o no puede parsearse.
    """
    if not isinstance(candidate, str) or not candidate.strip():
        raise ValueError("Número vacío o no válido")

    try:
        parsed = phonenumbers.parse(candidate, default_region)
        if not (phonenumbers.is_possible_number(parsed) and phonenumbers.is_valid_number(parsed)):
            raise ValueError("Número no válido o no posible")

        international_prefix = f"+{parsed.country_code}"
        national_number = str(parsed.national_number)

        return international_prefix, national_number

    except NumberParseException as e:
        raise ValueError(f"Número no parseable: {e}")
