import pytest

# Suponemos que esta es la función que vas a testear
from normalize_tools.phones import normalize_phone

@pytest.mark.parametrize("input_str, expected", [
    # Casos válidos (formato internacional correcto)
    ("+34699111222", ("+34", "699111222")),
    ("699111222", ("+34", "699111222")),  # Por defecto se entiende que es ES
    ("+33123456789", ("+33", "123456789")),
    ("++34699111222", ("+34", "699111222")),
      # Región se debe forzar a FR en un test posterior

    # Casos técnicamente posibles pero inválidos
    ("12345", None),
    ("000000000", None),
    ("999999999", None),
    ("0123456789", None),

    # Casos maliciosos / deformes
    ("abc", None),
    ("123456; DROP TABLE users", None),
    ("+34-6(9)9 111-222", ("+34", "699111222")),
  

    # Ambigüedad regional
    ("+14155552671", ("+1", "4155552671")),
    ("", None),
    ("     ", None),
])
def test_normalize_phone_default_es(input_str, expected):
    # Simula que el default_region = 'ES' dentro de la función
    if expected is None:
        with pytest.raises(ValueError):
            normalize_phone(input_str)
    else:
        result = normalize_phone(input_str)
        assert result == expected

def test_normalize_phone_fr():
    input_str = "0123456789"
    expected = ("+33", "123456789")
    result = normalize_phone(input_str, default_region="FR")
    assert result == expected
