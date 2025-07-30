import pytest
from normalize_tools.countries import get_country_from_phone

@pytest.mark.parametrize("phone_number,expected_country", [
    ("+34 600000000", "España"),
    ("+1 2025550125", "Estados Unidos"),
    ("+52 5512345678", "México"),
    ("+49 3012345678", "Alemania"),
    ("+81 9012345678", "Japón"),
])
def test_valid_numbers(phone_number, expected_country):
    assert get_country_from_phone(phone_number) == expected_country

@pytest.mark.parametrize("phone_number,expected_country", [
    ("+34-600-000-000", "España"),
    ("+1 (202) 555-0125", "Estados Unidos"),
    (" +52 55 123 45678 ", "México"),
])
def test_valid_formats(phone_number, expected_country):
    assert get_country_from_phone(phone_number.strip()) == expected_country

@pytest.mark.parametrize("phone_number", [
    "+999999999999",      # prefijo inexistente
    "+",                  # solo símbolo
    "+1",                 # prefijo sin número
    "",                   # vacío
    None,                 # nulo
])
def test_invalid_inputs(phone_number):
    assert get_country_from_phone(phone_number) == ""

@pytest.mark.parametrize("phone_number,expected_country", [
    ("+1 8768224567", "Jamaica"),         # compartido con EE.UU.
    ("+44 7911123456", "Reino Unido"),    # prefijo similar a otros países de ex-colonias
])
def test_edge_case_shared_prefixes(phone_number, expected_country):
    assert get_country_from_phone(phone_number) == expected_country

@pytest.mark.parametrize("phone_number", [
    "+34 600",         # demasiado corto
    "+34 600000000000000",  # demasiado largo
])
def test_edge_case_lengths(phone_number):
    assert get_country_from_phone(phone_number) == ""
