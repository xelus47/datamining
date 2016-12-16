# Osiris

https://www.osiris.universiteitutrecht.nl/osistu_ospr/OnderwijsCatalogusZoekCursus.do

De basis van de mijn is bijna af. Vergelijk de volgende twee javascript snippets (Firefox console):
```javascript
>> // eerste poging
>> a0=document['form0']
← '<form id="form0" name="form0" (...)>'
>> a0['event'].value='zoeken'
← 'zoeken'
>> a0.submit()
```

```javascript
>> // tweede poging
>> a0=document['form0']
← '<form id="form0" name="form0" (...)>'
>> a0['event'].value='zoeken'
← 'zoeken'
>> _validateForm(a0)
← true
>> a0.submit()
```

De eerste poging levert een lege 'tweedekolom' op, maar de tweede poging levert de lijst van cursussen op zoals we willen.
Dus het geheim zit nu nog in `_validateForm(form)`.