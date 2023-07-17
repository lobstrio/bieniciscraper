# bienici-listings-scraper

`bienici-listings-scraper ` will let you download **all listings from any Bien'Ici search URL** 💛

With **8 main attributes** per listing: 

* city
* postal_code
* ad_type
* property_type
* reference
* title
* publication_date
* modification_date
* new_property
* rooms_quantity
* bedrooms_quantity
* price
* photos

Below, the power of the `.py` script: 

```bash
python3 bien-ici-scraper.py -u https://www.bienici.com/recherche/achat/france/chateau -p 1  
going to page: 1
total results: 555
total results to scrape: 25
scraped: Domaine 6 hectares proche Etretat
scraped: Château à vendre dans le lot avec dépendances et piscine.
scraped: Château en vente à LURCY LEVIS
scraped: Manoir 15 pièces BIVIERS
scraped: Château
scraped: DOMAINE D'EXCEPTION MONTS DU LYONNAIS
scraped: Château
scraped: Eyzines - Domaine de 463m² avec 6800m² de terrain - piscine - dépendance
scraped: Magnifique Château du 17ème siècle avec conciergerie indépen
scraped: Istres (13)  -  UNIQUE !!!
scraped: Château
scraped: A VENDRE, RARE,04210,Château du XIII ièm siècle, pour les amoureux de l' AUTHENTICITE !
scraped: Vente Château 8 pièces
scraped: Exclusivité : Château entre Armagnac et Lomagne
scraped: Magnifique maison de Maître historique
scraped: Vente Château 8 pièces
scraped: Château
scraped: Château 5 chambre(s) à vendre
scraped: Domaine et Château avec Parc de plus de 18000m² !
scraped: Vente Château 29 pièces
scraped: CHATEAU
scraped: MORVAN LAVAULT DE FRETOY
scraped: Château
scraped: Château fin XIXe -début XXe Siècle
max page reached
csv written
elapsed: 0.50 s
~~ success
_       _         _            
| |     | |       | |          
| | ___ | |__  ___| |_ __ __  
| |/ _ \| '_ \/ __| __/| '__|
| | (_) | |_) \__ \ |_ | |  
|_|\___/|_.__/|___/\__||_|  

```

You can scrape the data from any search URL of any kind, using the dynamic `-u` argument. Data is afterwards immediately exported to a clean and structured `.csv` file named as `data_bienici_lobstr_io.csv`, in the same folder of your .py script.

## Feature Support

`bienici-listings-scraper.py` is a Python scraper, which let you download listings from **any** Bien'Ici URL.

* all listings
* 8 attributes per listing
* possibly limited collection scope with max page `-p` dynamic argument
* any search url supported with `-u` dynamic argument
* elegant `@class` structure
* data exported in structure `.csv` file

`bienici-listings-scraper` supports Python 3.9.6.

## Installation

To run `bienici-listings-scraper`:

1. Download the `.py` file
2. Install dependencies
3. Run the `.py` script

```bash
$ pip3 install requests retry
$ python3 -u https://www.bienici.com/recherche/achat/france/chateau -p 1 bienici-listings-scraper.py
```

NB: by default, listings are scraped from this specific search URL https://www.bienici.com/recherche/achat/france/chateau.

✨

## Notes

This Python script collect data from internal Bien'Ici API, and does convert any Bien'Ici search URL into avaialable API request, through advanced website-side JS reverse-engineering. Any location, any flat type, any budget, any advanced requests (balcon, digicode, dernier étage): collect data from any starting search URL.

Beware: you can scrape __up to 2,500 ads per search url__. In fact, Bien'ici gives access to a maximum of 100 pages, and limits the display thereafter.
If you want to bypass this limitation, please do split your main search link within smaller scope links

💇

For example, if you want to scrape all listings from Paris, **split** within neighborhoods: 
75001 all listings
75002 all listings
etc.
