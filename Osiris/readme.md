# Osiris

https://www.osiris.universiteitutrecht.nl/osistu_ospr/OnderwijsCatalogusZoekCursus.do

Het script (osiris.py) kan al auth opvragen (requestToken en de juiste cookies), maar bij
het opvragen van zoekresultaten met een POST request met PRECIES DEZELFDE (naast de auth)
HEADERS EN PARAMS KRIJGT HIJ NIET DEZELFDE PAGINA ALS IN DE BROWSER (met developer console)

Het heeft heel misschien te maken met javascrub. In ieder geval is het zo dat de data waar
we naar zoeken (alle cursussen in `<section class='tweedekolom'>`) zitten in de response body
als we de browser gebruiken maar de tweede kolom is vooralsnog leeg als het via osiris.py gaat :(

