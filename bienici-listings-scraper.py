import requests
import csv
import time
import argparse
from urllib.parse import urlparse, parse_qs
import json
import copy
from retry import retry

MIN_PAGE_VAL = 1
MAX_PAGE_VAL = 100

HEADERS = {
    'authority': 'www.bienici.com',
    'accept': '*/*',
    'accept-language': 'fr-FR,fr;q=0.9',
    'referer': 'https://www.bienici.com/recherche/achat/france/chateau?page=2&camera=11_2.3469385_48.8588675_0.9_0',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

FIELDNAMES = [
	'city', 
	'postal_code', 
	'ad_type', 
	'property_type', 
	'reference', 
	'title', 
	'publication_date', 
	'modification_date', 
	'new_property', 
	'rooms_quantity', 
	'bedrooms_quantity', 
	'price', 
	'photos'
]

BOOLEAN_VALUES = {
    "newProperty": True,
    "isOnLastFloor": True,
    "isGroundFloor": True,
    "isNotGroundFloor": True,
    "hasPool": True,
    "hasBalcony": True,
    "hasTerrace": True,
    "hasBalconyOrTerrace": True,
    "hasCellar": True,
    "hasParking": True,
    "hasFirePlace": True,
    "hasDoorCode": True,
    "hasIntercom": True,
    "hasGarden": True,
    "hasElevator": True,
    "workToDo": False,
    "has3DModel": True,
    "flatSharingNotAllowed": False,
    "isBuildingPlot": True,
    "isExclusiveSaleMandate": True,
    "hasCaretaker": True,
    "isDuplex": True,
    "hasSeparateToilet": True,
    "isFurnished": True,
    "isNotFurnished": True,
    "hasPhoto": True,
    "onTheMarket": True,
    "isPreview": True,
    "isEligibleForPinelLaw": True,
    "isEligibleForDenormandieLaw": True,
    "exportableAd": True,
    "isInStudentResidence": True,
    "isInSeniorResidence": True,
    "isInTourismResidence": True,
    "isInManagedResidence": True,
    "isNotInResidence": True,
    "isNotLifeAnnuitySale": True,
    "isLifeAnnuitySaleOnly": True,
    "needProfessionalPict": True,
    "needVirtualTour": True,
    "needHomeStaging": True,
    "hasNoPhoto": True,
    "hasNoAddress": True,
    "hasAddress": True,
    "hasNoPrice": True,
    "isPromotedAsExclusive": True,
    "hasToBeBuilt": True,
    "hasNotToBeBuilt": True,
    "opticalFiberStatus": "deploye",
    "chargingStations": True
}

ENERGY_CLASSIFICATION_VALUES = ["energyClassification"]
NUMBER_VALUES = ["minPrice", "maxPrice", "minBedrooms", "maxBedrooms", "minArea", "maxArea", "minGardenSurfaceArea", "maxGardenSurfaceArea"]

# Property URL parameters mapping
URL_PARAMETERS = {
    "minPrice": "prix-min",
    "maxPrice": "prix-max",
    "minArea": "surface-min",
    "maxArea": "surface-max",
    "page": "page",
    "camera": "camera",
    "newProperty": "neuf",
    "onTheMarket": "disponible",
    "isPreview": "en-avant-premiere",
    "listMode": "mode",
    "mapMode": "carte",
    "limit": "limite",
    "isOnLastFloor": "dernier-etage",
    "has3DModel": "modelisation-3d",
    "isLeading": "a-la-une",
    "highlighted": "recommande",
    "isGroundFloor": "rez-de-chaussee",
    "isNotGroundFloor": "pas-au-rez-de-chaussee",
    "hasPool": "piscine",
    "hasBalcony": "balcon",
    "hasTerrace": "terrasse",
    "hasBalconyOrTerrace": "balcon-ou-terrasse",
    "hasCellar": "cave",
    "hasParking": "parking",
    "hasFirePlace": "cheminee",
    "hasDoorCode": "digicode",
    "hasIntercom": "interphone",
    "hasGarden": "jardin",
    "hasElevator": "ascenseur",
    "workToDo": "sans-travaux",
    "flatSharingNotAllowed": "colocation-autorisee",
    "isBuildingPlot": "constructible",
    "isExclusiveSaleMandate": "exclusif",
    "hasCaretaker": "gardien",
    "isDuplex": "duplex",
    "hasSeparateToilet": "toilettes-separees",
    "isFurnished": "meuble",
    "isNotFurnished": "non-meuble",
    "hasPhoto": "photo",
    "geocoding": "geocoding",
    "reference": "reference",
    "queryString": "query-string",
    "adsNestedQueryString": "nested-query-string",
    "contactRequestsNestedQueryString": "contacts-nested-query-string",
    "isEligibleForPinelLaw": "eligible-loi-pinel",
    "isEligibleForDenormandieLaw": "eligible-loi-denormandie",
    "energyClassification": "classification-energetique",
    "exportableAd": "multidiffusable",
    "extensionType": "recherche-etendue",
    "isInStudentResidence": "residence-etudiants",
    "isInSeniorResidence": "residence-seniors",
    "isInTourismResidence": "residence-tourisme",
    "isInManagedResidence": "residence-geree",
    "isNotInResidence": "pas-en-residence",
    "isNotLifeAnnuitySale": "viagers-exclus",
    "isLifeAnnuitySaleOnly": "viagers-uniquement",
    "excludeAgencyNew": "8",
    "needProfessionalPict": "amelioration-photos-professionnelles",
    "needVirtualTour": "amelioration-visites-virtuelles",
    "needHomeStaging": "amelioration-home-staging-virtuels",
    "hasNoPhoto": "annonces-sans-photo",
    "hasNoAddress": "annonces-sans-adresse",
    "hasAddress": "annonces-avec-adresse",
    "hasNoPrice": "annonces-sans-prix",
    "minBedrooms": "chambres-min",
    "maxBedrooms": "chambres-max",
    "minGardenSurfaceArea": "surface-terrain-min",
    "maxGardenSurfaceArea": "surface-terrain-max",
    "isPromotedAsExclusive": "avant-premiere-bienici",
    "is3dHighlighted": "en-avant-en-3d",
    "hasToBeBuilt": "maisons-a-construire",
    "hasNotToBeBuilt": "maisons-a-construire-exclues",
    "opticalFiberStatus": "fibre",
    "chargingStations": "recharge-vehicule-electrique"
}

# Reverse mapping of URL parameters
REVERSED_URL_PARAMETERS = {v: k for k, v in URL_PARAMETERS.items()}

# Sort options mapping
SORT_OPTIONS = {
    "price": "prix",
    "pricePerSquareMeter": "prixm2",
    "surfaceArea": "surface",
    "roomsQuantity": "pieces",
    "relevance": "pertinence",
    "relevanceDev": "pertinencedev",
    "publicationDate": "publication",
    "modificationDate": "modification",
    "views": "vue",
    "viewers": "visiteurs",
    "followers": "favoris",
    "contactRequests": "contacts",
    "phoneDisplays": "appels"
}

# Reverse mapping of sort options
REVERSED_SORT_OPTIONS = {v: k for k, v in SORT_OPTIONS.items()}

FILTER_TYPE_OPTIONS = {
	"achat": "buy", 
	"location": "rent"
}

FRENCH_SLUG_TO_DB = {
   "parkingbox":"parking",
   "maison":"house",
   "maisonvilla":"house",
   "appartement":"flat",
   "parking":"parking",
   "terrain":"terrain",
   "batiment":"building",
   "chateau":"castle",
   "loft":"loft",
   "bureau":"office",
   "local":"premises",
   "commerce":"shop",
   "hotel":"townhouse",
   "annexe":"annexe",
   "autres":"others"
}

DEFAULT_PROPERTY_TYPES = ["house","flat","loft","castle","townhouse"]

DEFAULT_SORT_BY = ("relevance","desc")

class BienIciScraper: 

	def __init__(self): 
		self.s = requests.Session()
		self.s.headers = HEADERS
		self.DATA = []
		self.total_scraped_results = 0
		self.page = 1
		self.max_page = None

	def convert_url_to_api_parameters(self, url): 
		
		PARAMS = {"filters":{}}

		FILTERS = PARAMS["filters"]

		FILTERS["size"] = 24
		FILTERS["from"] = None
		FILTERS["page"] = None
		FILTERS["onTheMarket"] = [True]
		# d["extensionType"] = "extendedIfNoResult"
		#d["leadingCount"] = 2
		parsed_url = urlparse(url)
		query_params = parse_qs(parsed_url.query)
		path = parsed_url.path

		# /marseille-13000,paris-75000,montpellier-34000/
		# /france/
		location_ids = self.get_location_ids(path)
		if location_ids: 
			FILTERS["zoneIdsByTypes"] = {"zoneIds":location_ids}

		# /location/
		for k, v in FILTER_TYPE_OPTIONS.items(): 
			if k in path: 
				FILTERS["filterType"] = FILTER_TYPE_OPTIONS[k]

		# /maisonvilla,appartement,loft,chateau,bureau,hotel
		_property_types_values = []
		for k, v in FRENCH_SLUG_TO_DB.items(): 
			if k in path: 
				_property_types_values.append(v)

		_property_types_values = _property_types_values if _property_types_values else DEFAULT_PROPERTY_TYPES
		FILTERS["propertyType"] = _property_types_values
		
		if query_params: 
			for k, v in query_params.items(): 

				# prix-min=50
				if k in REVERSED_URL_PARAMETERS.keys():
					if REVERSED_URL_PARAMETERS[k] in NUMBER_VALUES: 
						FILTERS[REVERSED_URL_PARAMETERS[k]] = int(v[0])

				# balcon=oui
				if k in REVERSED_URL_PARAMETERS.keys() and REVERSED_URL_PARAMETERS[k] in BOOLEAN_VALUES.keys():	
					FILTERS[REVERSED_URL_PARAMETERS[k]] = BOOLEAN_VALUES[REVERSED_URL_PARAMETERS[k]]

				# classification-energetique=F
				if k == 'classification-energetique': 
					FILTERS["energyClassification"] = v[0].split(',')

				# tri=surface-desc
				if k == 'tri':
					for s in v: 
						t, w = s.split('-')
						assert all([t,w])
						FILTERS["sortBy"] = t
						FILTERS["sortOrder"] = w

		if not "sortBy" in FILTERS.keys(): 
			t,w = DEFAULT_SORT_BY
			FILTERS["sortBy"] = t
			FILTERS["sortOrder"] = w

		assert PARAMS
		return PARAMS

	@retry(AssertionError, tries=3, delay=5, backoff=2)
	def get_location_ids(self, path): 
		assert path and isinstance(path, str)
		# https://www.bienici.com/recherche/location/marseille-13000,paris-75000,montpellier-34000/
		path = [p for p in path.split('/') if p]
		locations = path[2].split(',')
		if len(locations) == 1 and "".join(locations) == 'france': 
			return []
		location_ids = []
		for l in locations: 
			url = 'https://res.bienici.com/suggest.json?q=%s' % l
			print('searching location id for %s' % l)
			response = self.s.get(url, headers=HEADERS)
			assert response.status_code == 200
			location_dict = response.json()[0]
			location_id = location_dict["zoneIds"][0]
			assert location_id
			print('found %s' % location_id)
			location_ids.append(location_id)
		return location_ids

	def collect_results(self, params): 

		assert params

		while True: 

			assert self.page and isinstance(self.page, int)
			params["filters"]["page"] = self.page
			params["filters"]["from"] = (self.page-1)*24

			_params = copy.deepcopy(params)
			_params["filters"] = json.dumps(_params["filters"])

			print('going to page: %s' % self.page)

			response = self.s.get('https://www.bienici.com/realEstateAds.json', params=_params, headers=HEADERS)
			assert response.status_code == 200

			total_available_results = response.json()["total"]
			assert total_available_results is not None and isinstance(total_available_results, int)
			if self.max_page:
				total_results_to_scrape = min(total_available_results, 2500, max_page*25)
			else: 
				total_results_to_scrape = min(total_available_results, 2500)

			assert all([total_available_results, total_results_to_scrape])

			if self.page == 1: 
				print("total results: %s" % total_available_results)
				print("total results to scrape: %s" % total_results_to_scrape)

			ads = response.json()["realEstateAds"]
			for ad in ads: 

				city = ad.get("city","")
				postal_code = ad.get("postalCode","")
				ad_type = ad.get("adType","")
				property_type = ad.get("propertyType","")
				reference = ad.get("reference","")
				title = ad.get("title","")
				publication_date = ad.get("publicationDate","")
				modification_date = ad.get("modificationDate","")
				new_property = ad.get("newProperty","")
				rooms_quantity = ad.get("roomsQuantity","")
				bedrooms_quantity = ad.get("bedroomsQuantity","")
				price = ad.get("price","")
				photos = ", ".join([u.get("url_photo","") for u in ad.get("photos",[])])

				VALUES = [
					city, 
					postal_code, 
					ad_type, 
					property_type, 
					reference, 
					title, 
					publication_date, 
					modification_date, 
					new_property, 
					rooms_quantity, 
					bedrooms_quantity, 
					price, 
					photos
				]

				print("scraped: %s" % title)
				
				d = dict(zip(FIELDNAMES, VALUES))
				self.DATA.append(d)
				self.total_scraped_results += 1

			if self.total_scraped_results >= total_available_results: 
				print('all data collected')
				break

			if self.max_page:
				if self.page == self.max_page: 
					print('max page reached')
					break

			self.page += 1

	def write_to_csv(self): 
		assert self.DATA 
		with open('data_bienici_lobstr_io.csv', 'w') as f: 
			writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
			writer.writeheader()
			for d in self.DATA: 
				writer.writerow(d)
		print('csv written')

def range_limited_integer_type(arg):
    try:
        f = int(arg)
    except ValueError:    
        raise argparse.ArgumentTypeError("must be an integer")
    if f < MIN_PAGE_VAL or f > MAX_PAGE_VAL:
        raise argparse.ArgumentTypeError("must be < " + str(MAX_PAGE_VAL) + " and > " + str(MIN_PAGE_VAL))
    return f


if __name__ == '__main__':
	s = time.perf_counter()

	argparser = argparse.ArgumentParser()
	argparser.add_argument(
		'--search-url', 
		'-u', 
		type=str, 
		required=False, 
		help='bienici search url', 
		default='https://www.bienici.com/recherche/achat/france/chateau'
	)

	argparser.add_argument(
		'--max-page', 
		'-p', 
		type=range_limited_integer_type, 
		required=False, 
		help='max page you want to reach (by default null) - must be between 1 and 100', 
		default=None
	)

	args = argparser.parse_args()

	search_url = args.search_url
	max_page = args.max_page
	assert search_url
	
	b = BienIciScraper()
	b.max_page = max_page
	params = b.convert_url_to_api_parameters(search_url)
	b.collect_results(params)
	b.write_to_csv()
	
	elapsed = time.perf_counter() - s
	elapsed_formatted = "{:.2f}".format(elapsed)
	print("elapsed:", elapsed_formatted, "s")
	print('''~~ success
_       _         _            
| |     | |       | |          
| | ___ | |__  ___| |_ __ __  
| |/ _ \| '_ \/ __| __/| '__|
| | (_) | |_) \__ \ |_ | |  
|_|\___/|_.__/|___/\__||_|  
''')

