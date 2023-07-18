# scraper.py

import requests
import csv
import time
import argparse
from urllib.parse import urlparse, parse_qs
import json
import copy
from retry import retry
from .constants import *

class BienIciScraper: 

	def __init__(
			self, 
			url, 
			limit, 
			output
		): 
		self.s = requests.Session()
		self.s.headers = HEADERS
		self.DATA = []
		self.total_scraped_results = 0
		self.page = 1
		self.limit = limit
		self.url = url
		self.output = output
		assert all([self.url, self.limit, self.output])

	def convert_url_to_api_parameters(self, url): 
		"""
		Convert a URL to API parameters for the Bienici API.

		Args:
			url (str): The URL to convert.

		Returns:
			dict: The API parameters.

		Raises:
			AssertionError: If the input URL is not provided or if any expected assertions fail during the conversion process.
		"""
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
		"""
		Retrieve location IDs for the given path.

		Args:
			path (str): The path containing the locations to retrieve IDs for.

		Returns:
			list: A list of location IDs.

		Raises:
			AssertionError: If the path is not provided, or if an expected assertion fails during the retrieval process.
		"""
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

	@retry(AssertionError, tries=3, delay=5, backoff=2)
	def go_api_page(self, params): 
		"""
		Send a GET request to the API page with the specified parameters.

		Args:
			params (dict): The parameters to include in the GET request.

		Returns:
			requests.Response: The response object from the API page.

		Raises:
			AssertionError: If the response status code is not 200 (OK) after retrying.
		"""
		print('going to page: %s' % self.page)
		response = self.s.get('https://www.bienici.com/realEstateAds.json', params=params, headers=HEADERS)
		assert response.status_code == 200
		return response

	def collect_results(self): 
		"""
		Collect the results by making API requests and scraping the data.

		Raises:
			AssertionError: If any of the assertions fail during the data collection process.
		"""

		params = self.convert_url_to_api_parameters(self.url)
		assert params

		while True: 

			assert self.page and isinstance(self.page, int)
			params["filters"]["page"] = self.page
			params["filters"]["from"] = (self.page-1)*24

			_params = copy.deepcopy(params)
			_params["filters"] = json.dumps(_params["filters"])
			assert _params

			response = self.go_api_page(_params)

			total_available_results = response.json()["total"]
			assert total_available_results is not None and isinstance(total_available_results, int)
			if self.limit:
				total_results_to_scrape = min(total_available_results, 2500, self.limit)
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
				
				if self.limit: 
					if self.total_scraped_results == self.limit: 
						print('limit reached')
						self.write_to_csv()
						return

			if self.total_scraped_results >= total_available_results: 
				print('all data collected')
				break

			self.page += 1

		self.write_to_csv()

	def write_to_csv(self): 
		"""
		Write the collected data to a CSV file.

		Raises:
			AssertionError: If the data or output file path is not provided.
		"""
		assert self.DATA 
		assert self.output

		with open(self.output, 'w') as f: 
			writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
			writer.writeheader()
			for d in self.DATA: 
				writer.writerow(d)

		print('csv written')

def scrape(
		url="https://www.bienici.com/recherche/achat/france/chateau",
		limit=2500, 
		output="data_bienici_lobstr_io.csv"
	): 

	"""
	Scrape the listings from the provided URL and save the results to a file.

	Parameters:
		url (str): The URL to scrape the listings from.
		file (str): The filename or path where the results will be saved.
		limit (int): The maximum number of listings to scrape.

	Returns:
		None
	"""

	assert all([url, limit, output])

	s = time.perf_counter()
	b = BienIciScraper(
		url=url, 
		limit=limit, 
		output=output
	)
	
	b.collect_results()
	
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

