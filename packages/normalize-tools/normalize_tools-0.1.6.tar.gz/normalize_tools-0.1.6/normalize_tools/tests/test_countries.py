from normalize_tools import search_country_name, get_region, infer_country_from_email
from normalize_tools.countries import lookup_index
import pytest

from typing import Optional, Tuple


def test_el_salvador():
    assert search_country_name("El Salvador") == "El Salvador"

def test_particulas():
    assert search_country_name("De La Administracion") == ""


@pytest.mark.parametrize("input_str,expected", [
    # Español - exactos
    ("España", "España"),
    ("México", "México"),
    ("Estados Unidos", "Estados Unidos"),
    ("República Dominicana", "República Dominicana"),
    ("Reino Unido", "Reino Unido"),
    ("Guinea Ecuatorial", "Guinea Ecuatorial"),
    
    # Español - normalizados
    ("españa", "España"),
    ("MEXICO", "México"),
    ("republica dominicana", "República Dominicana"),
    ("reino unido", "Reino Unido"),
    
    # Inglés - comunes
    ("Spain", "España"),
    ("Mexico", "México"),
    ("United States", "Estados Unidos"),
    ("Dominican Republic", "República Dominicana"),
    ("United Kingdom", "Reino Unido"),
    ("Equatorial Guinea", "Guinea Ecuatorial"),

    # Mixtos - variantes válidas
    ("colombia", "Colombia"),
    ("COLOMBIA", "Colombia"),
    ("Venezuela", "Venezuela, República Bolivariana de"),
    ("venezuela", "Venezuela, República Bolivariana de"),
    ("Republic of Ireland", "Irlanda"),

    # Falsos positivos y negativos esperados
    ("", ""),
    ("   ", ""),
    ("LATAM", ""),
    ("Financiero", ""),
    ("Tecnológico", ""),
    ("Comercial", ""),
    ("Transylvania", ""),
    ("Moon", ""),
    ("Gotham", "")
])
def test_search_country_name(input_str, expected):
    country_name = search_country_name(input_str, lookup_index)
    assert country_name == expected


# Casos positivos claros
def test_es():
    assert get_region("España") == "España"

@pytest.mark.parametrize("pais", [
    "México", "Argentina", "Colombia", "Brasil", "Perú", "Uruguay",
    "Chile", "Ecuador", "Paraguay", "Bolivia, Estado Plurinacional de",
    "Costa Rica", "Guatemala", "Honduras", "El Salvador", "Nicaragua",
    "Panamá", "Cuba", "República Dominicana (la)", "Haití", "Jamaica",
    "Antigua y Barbuda", "Bahamas (las)", "Barbados", "Dominica",
    "Granada", "San Vicente y las Granadinas", "San Cristóbal y Nieves",
    "Santa Lucía", "Trinidad y Tobago", "Guyana", "Surinam", 
])
def test_latam_countries(pais):
    assert get_region(pais) == "LATAM"

@pytest.mark.parametrize("pais", [
    "Alemania", "Francia", "Italia", "Portugal", "China", "India",
    "Estados Unidos (los)", "Canadá", "Australia", "Sudáfrica",
    "Japón", "Arabia Saudita"
])
def test_otros(pais):
    assert get_region(pais) == "Otros"

# Casos inválidos o no presentes
@pytest.mark.parametrize("pais", [
    "Espana", "mexico", "perú", "republica dominicana",
    "Estados Unidos", "Brasil!", "Venezulea", "UK", "", " ", None
])
def test_no_en_lista(pais):
    assert get_region(pais) == ""

# Casos limítrofes que podrían confundirse si no se normaliza
@pytest.mark.parametrize("pais", [
    "Puerto Rico", "Guadalupe", "Martinica", "Aruba", "Curaçao",
    "San Bartolomé", "San Martín (parte francesa)", "Islas Vírgenes (EE.UU.)"
])
def test_otros_dependencias_latam_geo(pais):
    assert get_region(pais) == "Otros"

# Antártida (explícitamente excluida de LATAM)
def test_antartida():
    assert get_region("Antártida") == "Otros"


@pytest.mark.parametrize("email,expected", [
    ("usuario@gmail.com", (None, None)),                    # Dominio genérico
    ("persona@empresa.com", (None, None)),                  # Dominio corporativo
    ("persona@empresa.es", ("ES", "España")),               # ccTLD español
    ("persona@universidad.de", ("DE", "Alemania")),         # ccTLD alemán
    ("persona@gobierno.fr", ("FR", "Francia")),             # ccTLD francés
    ("persona@nombre.co.uk", ("GB", "Reino Unido")),   # Dominio doble, mapeado a Reino Unido
    ("alguien@correo.mx", ("MX", "México")),                # ccTLD mexicano
    ("correo@ministerio.it", ("IT", "Italia")),             # ccTLD italiano
    ("noreply@correo.cn", ("CN", "China")),                 # ccTLD chino
    ("nombre@empresa.us", ("US", "Estados Unidos")),  # ccTLD estadounidense
])
def test_valid_country_detection(email: str, expected: Tuple[Optional[str], Optional[str]]):
    assert infer_country_from_email(email) == expected


@pytest.mark.parametrize("email", [
    "usuario@dominio.unknown",          # TLD no reconocida
    "usuario@",                         # Dominio vacío
    "@dominio.es",                      # Parte local vacía
    "usuario@.es",                      # Dominio malformado
    "usuario",                          # Sin @
    "",                                 # Vacío
    None,                               # None explícito
])
def test_invalid_or_malformed_emails(email):
    result = infer_country_from_email(email)
    assert result == (None, None)


@pytest.mark.parametrize("email,expected", [
    ("persona@algo.co.jp", ("JP", "Japón")),           # Subdominios que contienen código de país
    ("persona@mail.gov.uk", ("GB", "Reino Unido")),
    ("persona@service.gc.ca", ("CA", "Canadá")),       # Canadá
    ("persona@empresa.com.ar", ("AR", "Argentina")),   # ccTLD compuesto
])
def test_compound_ccTLDs(email: str, expected: Tuple[Optional[str], Optional[str]]):
    assert infer_country_from_email(email) == expected

