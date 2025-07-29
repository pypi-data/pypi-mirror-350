import pandas as pd
from  unidecode import unidecode
from babel import Locale, UnknownLocaleError
from typing import Dict, List, Optional, Set
from normalize_tools.traductions import traducciones, unique_languages
from functools import reduce
import re

def strip_parenthesis(nombre: str) -> str:
    return re.sub(r"\s+\(.*?\)$", "", nombre)

# Descartar particulas de los principales idiomas es, en, fr, de
stop_particles = {
    # Incluyo republica por que da falsos positivos a la primera encontrada Congo
    "es": {
        "el", "la", "los", "las", "un", "una", "unos", "unas",
        "de", "del", "al", "a", "en", "por", "para", "con", "sin", "sobre",
        "entre", "tras", "hacia", "hasta",
        "y", "o", "u", "ni", "que", "como", "pero", "republica"
    },
    "en": {
        "the", "a", "an",
        "of", "in", "on", "at", "by", "with", "without", "about", "against",
        "from", "to", "into", "over", "under",
        "and", "or", "nor", "but", "so", "yet", "republic"
    },
    "fr": {
        "le", "la", "les", "un", "une", "des", "du", "de", "au", "aux",
        "en", "dans", "avec", "sans", "par", "pour", "sur", "sous", "chez",
        "et", "ou", "ni", "mais", "que", "dont", "comme", "republique"
    },
    "de": {
        "der", "die", "das", "ein", "eine", "einer", "eines", "einem", "einen",
        "den", "dem", "des",
        "von", "zu", "mit", "nach", "aus", "über", "unter", "für", "ohne",
        "um", "an", "auf", "in", "bei", "zwischen",
        "und", "oder", "aber", "sondern", "doch", "denn", "republik"
    }
}

def tokenize(text: str, stop_particles: Dict[str, set] = stop_particles) -> Set[str]:
    tokens = text.split()
    all_stop_particles = reduce(set.union, stop_particles.values())
    return {t for t in tokens if t not in all_stop_particles}


# Formatear nombres
def normalize(n: Optional[str]) -> str:
    # Normaliza cadenas eliminando tildes, convirtiendo a minúsculas y eliminando espacios

    if pd.isna(n):
        return ""
    return unidecode(str(n).strip().lower())

def get_translations_for_country(iso_code, unique_languages):
    # Devuelve una lista de traducciones normalizadas del nombre de un país para cada idioma dado

    translations = []
    for lang in unique_languages:
        try:
            name = Locale(lang).territories.get(iso_code)
            if name:
                translations.append(normalize(name))
        except (UnknownLocaleError, KeyError):
            continue
    return translations

def create_datastructures(countries_file = "data/origin_country.csv", languages_file = "data/idiomas_x_pais.csv"):
    # Crea los dataframes de países e idiomas y añade traducciones a los países

   
    df_countries = pd.read_csv(countries_file)
    df_languages = pd.read_csv(languages_file)
    unique_languages = df_languages['language_code'].dropna().unique().tolist()

    df_countries["translations"] = df_countries["code"].apply(lambda c: get_translations_for_country(c, unique_languages))
    return df_countries, unique_languages

def build_lookup_index(df: pd.DataFrame) -> Dict[str, str]:
    # Construye un diccionario de búsqueda rápida (lookup) con variantes normalizadas del nombre del país
   
    lookup: Dict[str, str] = {}
    for _, row in df.iterrows():
        name_es: str = row['name_es']
        variants: List[str] = row['translations']

        for variant in variants:
            if variant not in lookup:
                lookup[variant] = name_es

    return lookup

# Diccionario precargado con las traducciones disponibles (importado)
lookup_index = traducciones


def search_country_name(user_input: str, lookup_index: Dict[str, str] = lookup_index) -> str:
    user_input = normalize(user_input)
    if not user_input:
        return ""
    
    input_tokens = tokenize(user_input)

    for key, value in lookup_index.items():
        key_tokens = set(key.split())
        if input_tokens == key_tokens:
            return strip_parenthesis(value)

    for key, value in lookup_index.items():
        key_tokens = set(key.split())
        if input_tokens.issubset(key_tokens):
            return strip_parenthesis(value)

    return ""



def get_region(pais: str) -> str:
    """
    Clasifica un país en una de las tres regiones: 'España', 'LATAM', 'Otros'.
    
    Parámetros:
    pais (str): Nombre del país ya normalizado.
    
    Retorno:
    str: 'España', 'LATAM', 'Otros' o '' si el país no está en la lista.
    """

    paises_es = {"España"}
    paises_latam = {
        'Venezuela, República Bolivariana de', 'El Salvador', 'Panamá', 'Jamaica', 'Costa Rica', 'Paraguay', 'Granada', 'Belice', 'Barbados', 'Argentina', 'Perú', 'San Cristóbal y Nieves', 'Honduras', 'Colombia', 'República Dominicana (la)', 'Surinam', 'Ecuador', 'Santa Lucía', 'Brasil', 'San Vicente y las Granadinas', 'México', 'Guyana', 'Bahamas (las)', 'Nicaragua', 'Trinidad y Tobago', 'Chile', 'Antigua y Barbuda', 'Haití', 'Cuba', 'Dominica', 'Uruguay', 'Bolivia, Estado Plurinacional de', 'Guatemala'
    }

    paises_resto = {'Macao', 'Países Bajos (los)', 'Sri Lanka', 'Hong Kong', 'Islas Caimán (las)', 'Taiwán (Provincia de China)', 'Svalbard y Jan Mayen', 'Botsuana', 'Turquía', 'Guernsey', 'Uganda', 'Nueva Zelanda', 'Lao, (la) República Democrática Popular', 'Mauritania', 'Bielorrusia', 'Uzbekistán', 'Ghana', 'Anguila', 'Malaui', 'Eslovenia', 'Pitcairn', 'Andorra', 'Italia', 'Corea (la República Democrática Popular de)', 'Kuwait', 'Malí', 'Antártida', 'Territorios Australes Franceses (los)', 'Curaçao', 'Kenia', 'Kiribati', 'Liechtenstein', 'Ruanda', 'Bosnia y Herzegovina', 'Aruba', 'Emiratos Árabes Unidos (Los)', 'Mauricio', 'Islas Marshall (las)', 'Bután', 'Madagascar', 'Palestina, Estado de', 'Gambia (La)', 'Samoa Americana', 'Islas Marianas del Norte (las)', 'Albania', 'Indonesia', 'Guinea', 'Guinea-Bisáu', 'Senegal', 'Grecia', 'Zimbabue', 'Libia', 'Islas Turcas y Caicos (las)', 'Catar', 'Eritrea', 'Rumania', 'Japón', 'Arabia Saudita', 'Noruega', 'Filipinas (las)', 'Zambia', 'Puerto Rico', 'Cabo Verde', 'Moldavia (la República de)', 'Santa Sede[Estado de la Ciudad del Vaticano] (la)', 'Bélgica', 'Guam', 'Sudán (el)', 'Camerún', 'Liberia', 'Mayotte', 'Mozambique', 'Finlandia', 'Nepal', 'Corea (la República de)', 'San Marino', 'Estados Unidos (los)', 'Bulgaria', 'Bangladés', 'Comoras', 'Suazilandia', 'China', 'Estonia', 'Guadalupe', 'Samoa', 'Bermudas', 'Chipre', 'Groenlandia', 'Croacia', 'Jordania', 'Santa Helena, Ascensión y Tristán de Acuña', 'Ucrania', 'Micronesia (los Estados Federados de)', 'Montenegro', 'Somalia', 'Santo Tomé y Príncipe', 'Malasia', 'Tayikistán', 'Yemen', 'Austria', 'Myanmar', 'Marruecos', 'Camboya', 'Irak', 'Sahara Occidental', 'Congo (la República Democrática del)', 'Tanzania, República Unida de', 'Tonga', 'Sudáfrica', 'Yibuti', 'Francia', 'Sudán del Sur', 'Vanuatu', 'Tokelau', 'Irlanda', 'Kirguistán', 'San Pedro y Miquelón', 'Territorio Británico del Océano Índico (el)', 'Afganistán', 'Kazajistán', 'Papúa Nueva Guinea', 'Timor-Leste', 'Níger (el)', 'Jersey', 'Pakistán', 'Portugal', 'Azerbaiyán', 'Gabón', 'Turkmenistán', 'Montserrat', 'Polonia', 'Guayana Francesa', 'Argelia', 'Fiyi', 'Letonia', 'Isla de Navidad', 'Canadá', 'Benín', 'Túnez', 'Alemania', 'Wallis y Futuna', 'Reunión', 'Omán', 'Siria, (la) República Árabe', 'Suiza', 'Luxemburgo', 'Armenia', 'Mongolia', 'San Bartolomé', 'Mónaco', 'Congo', 'Nueva Caledonia', 'Islas de Ultramar Menores de Estados Unidos (las)', 'Lituania', 'Isla de Man', 'Reino Unido (el)', 'Sierra Leona', 'Namibia', 'Dinamarca', 'Serbia', 'Sint Maarten (parte holandesa)', 'Palaos', 'Singapur', 'Niue', 'Isla Heard e Islas McDonald', 'Brunéi Darussalam', 'Israel', 'Cote d Ivoire', 'Baréin', 'Bonaire, San Eustaquio y Saba', 'Malta', 'Nauru', 'Islas Cook (las)', 'Burkina Faso', 'Isla Norfolk', 'Islas Åland', 'Maldivas', 'Egipto', 'Islas Vírgenes (EE.UU.)', 'Islas Salomón (las)', 'Polinesia Francesa', 'Angola', 'Chad', 'Isla Bouvet', 'Islas Malvinas [Falkland] (las)', 'Tailandia', 'Suecia', 'India', 'Nigeria', 'Togo', 'Macedonia (la antigua República Yugoslava de)', 'República Centroafricana (la)', 'Lesoto', 'Georgia del sur y las islas sandwich del sur', 'Tuvalu', 'Rusia, (la) Federación de', 'Australia', 'Martinica', 'Etiopía', 'Georgia', 'Islas Feroe (las)', 'Eslovaquia', 'Viet Nam', 'Irán (la República Islámica de)', 'Seychelles', 'Hungría', 'San Martín (parte francesa)', 'Guinea Ecuatorial', 'Islandia', 'Islas Vírgenes (Británicas)', 'República Checa (la)', 'Islas Cocos (Keeling)', 'Gibraltar', 'Líbano', 'Burundi'}
    if pais in paises_es:
        return "España"
    elif pais in paises_latam:
        return "LATAM"
    elif pais in paises_resto:  # Este conjunto debe contener todos los nombres del CSV
        return "Otros"
    else:
        return ""

if __name__ == "__main__":
    paises = ['Perú', 'México', 'España', 'Portugal', 'Colombia', 'Argentina',
       'Chile', 'Ecuador', 'Bolivia', 'Uruguay', 'Panamá', 'Brasil',
       'Guinea-Bisáu', 'Peru', 'Bélgica', 'Reino Unido', 'Venezuela',
       'Paraguay', 'República Dominicana', 'Francia', 'Alemania',
       'Noruega', 'Italia', 'El Salvador', 'Honduras', 'colombia',
       'Estados Unidos', 'venezuela', 'Grecia', 'LATAM', 'Rusia',
       'United Kingdom', 'Greece', 'Financiero', 'Italy', 'Ireland',
       'Germany', 'Mexico', 'Montenegro', 'Romania', 'France',
       'Australia', 'United States', 'Brazil', 'Netherlands',
       'Switzerland', 'Morocco', 'Canada', 'Suecia', 'Russia', 'Israel',
       'Tecnológico', 'Equatorial Guinea', 'Belgium', 'Puerto Rico',
       'Poland', 'Austria', 'Bulgaria', 'Croatia', 'Thailand', 'Turkey',
       'Cuba', 'Guatemala', 'Territorio Británico del Océano Índico',
       'Panama', 'Japón', 'Andorra', 'Ireland {Republic}',
       'Dominican Republic', 'Armenia', 'Nicaragua', 'Laos', 'Sweden',
       'Costa Rica', 'Spain', 'Republica Dominicana', 'Haiti',
       'Finlandia', 'Malta', 'Indonesia', 'Nigeria', 'Japan', 'Marruecos',
       'Tuvalu', 'Egipto', 'Mauritius', 'Bosnia and Herzegovina',
       'United Arab Emirates', 'Moldova', 'republica dominicana',
       'Denmark', 'argentina', 'Czech Republic', 'Suiza', 'MÉXICO',
       'bolivia', 'Namibia', 'Albania', 'Samoa', 'Grenada', 'Korea South',
       'Georgia', 'Belgica', 'Angola', 'Bangladesh', 'Finland',
       'Argentinas', 'República Argentina', 'Philippines', 'Afghanistan',
       'China', 'panama', 'Bhutan', 'Libia', 'Anguila', 'Irlanda',
       'Islas Georgia del Sur y Sandwich del Sur', 'India', 'Canadá',
       'Afganistán', 'Guinea Ecuatorial', 'Estonia', 'Gambia',
       'Países Bajos', 'Rumanía', 'Madagascar', 'Guinea', 'Croacia',
       'Dinamarca', 'Polonia', 'Islandia', 'Singapur', 'Bahamas',
       'Nueva Zelanda', 'Pakistán', 'Tailandia', 'Irán', 'Túnez',
       'Letonia', 'Emiratos Árabes Unidos', 'Líbano', 'Ucrania',
       'Arabia Saudí', 'Turquía', 'Viet Nam', 'Micronesia',
       'Comunicaciones', 'De La Administración', 'Transportes',
       'Comercial', 'Corea del Sur', 'Malasia', 'Algeria', 'Norway',
       'Isla Norfolk', 'Camerún', 'Serbia', 'Mozambique', 'Kenia',
       'Bangladés', 'Islas Salomón', 'Omán', 'Hungría', 'Chad',
       'Trinidad y Tobago', 'Eslovaquia', 'ESPAÑA', 'Luxemburgo',
       'Filipinas', 'Senegal', 'Czechia', 'Catar', 'Níger', 'Argelia',
       'Sudán', 'Zimbabue', 'Mauricio', 'Vietnam', 'Jordania', 'Surinam']
    


    procesados = 0
    correctos = 0
    no_encontrados = 0
    lNo_encontrados = []
    for pais in paises:
        new_pais = search_country_name(pais)
        if new_pais == pais:
            correctos += 1
            print("*", end="")
        print(f"{pais:>30s} -> {new_pais:>30s}")
        procesados += 1
        if not new_pais:
            no_encontrados +=1
            lNo_encontrados.append(pais)


    print (f"Distintos del original {procesados}/{len(paises)} = {procesados/len(paises)*100:.2f}%")
    print (f"Encontrados........... {procesados-no_encontrados}/{procesados} ={(procesados-no_encontrados)/procesados*100:.2f}%")
    print (f"No encontrados........... {no_encontrados}/{procesados} = {no_encontrados/procesados*100:.2f}%")
    print("\n".join(lNo_encontrados))


