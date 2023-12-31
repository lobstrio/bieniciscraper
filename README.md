# bieniciscraper

`bieniciscraper` is a Python package that allows you to scrape all real estate listings from any Bien'Ici URL 💛

## Table

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Command-line Arguments](#command-line-arguments)
5. [Important Notes](#important-notes)
6. [Disclaimer](#disclaimer)
7. [License](#license)

## Features

* All search URLs accepted
* All listings collected
* __13 attributes per__ listing
* Limit the scope of scraping with the dynamic `-l` argument
* Use any search URL with the `-u` dynamic argument
* Export data with a customized file name using the `-o` dynamic argument
* A resilient structure with the applied `retry` logic
* Exports data in a structured `.csv` file format

## Installation

```bash
$ pip3 install bieniciscraper
```

> **Note**: The installation will also install the `requests` and `retry` external libraries.

## Usage

```bash
$ bieniciscraper -u https://www.bienici.com/recherche/achat/france/chateau -l 10 -o demo.csv
going to page: 1
total results: 591
total results to scrape: 10
scraped: Château à vendre dans le lot avec dépendances et piscine.
scraped: Turenne Collonges la rouge - Demeure du XVIII siècle de 300 m² habitables sur une parcelle 1,9 ha à rénover entièrement
scraped: Manoir 15 pièces BIVIERS
scraped: Château du XVIème siècle et son parc au coeur de Lyon
scraped: Domaine 3 hectares proche Etretat
scraped: Vente Château 19 pièces
scraped: ANCIENNE DEPENDANCE DE L'ABBAYE DE CONQUES, CONSTITUEE D'UN CHATEAU
scraped: Château
scraped: Vente Château 8 pièces
scraped: DOMAINE D'EXCEPTION MONTS DU LYONNAIS
limit reached
csv written
elapsed: 1.20 s
~~ success
 _       _         _            
| |     | |       | |          
| | ___ | |__  ___| |_ __ __  
| |/ _ \| '_ \/ __| __/| '__|
| | (_) | |_) \__ \ |_ | |  
|_|\___/|_.__/|___/\__||_|  

```

## Command-line Arguments

* `--url/-u`: Specify your search URL.
* `--limit/-l`: Limit the number of items you want to scrape.
* `--output/-o`: Name the file in which data will be saved.

## Important Notes

This Python script collects data from the internal Bien'Ici API. It can convert any Bien'Ici search URL into an available API request using advanced website-side JS reverse-engineering.

Beware: scraping is limited to **2,500 ads per search url**. Bien'ici allows access to a maximum of 100 pages and then limits the display. To bypass this limitation, split your main search link into smaller scoped links:

For instance, to scrape all listings from Paris, **divide** by neighborhoods: \
75001 all listings \
75002 all listings \
... and so on.

💇

Always ensure that your usage adheres to the legal constraints relevant in your jurisdiction.
If you have package-related request, please contact us at: contact@lobstr.io.

## Disclaimer

This tool is intended for educational use. Always ensure that scraping a website is within your legal rights before using this or any other scraping tool. Respect the `robots.txt` of websites and be conscious of ethical and legal considerations.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
