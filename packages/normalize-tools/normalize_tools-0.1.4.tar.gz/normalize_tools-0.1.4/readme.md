# Utilidades de formateo o estimacion de valores
Se incluyen las siguientes en cuanto a normalización:

**Países**
- `search_country_name(user_input: str) -> str`: Devuelve el pais normalizado si `user_input` puede identificarse como tal. No usa IA, estimación clásica
- `get_region(pais: str) -> str`: Devuelve region de entre las siguientes `'España', 'LATAM', 'Otros'` si el pais informado va debidamente normalizado, `''` en otro caso

**Teléfonos**
- `normalize_phone(candidate: str, default_region: str = 'ES') -> tuple[str, str]`: Devuelve el prefijo internacional como +nn y el numero sin prefijo o ValueError si el numero no es parseable.


Y para inferir el pais usamos:
- 