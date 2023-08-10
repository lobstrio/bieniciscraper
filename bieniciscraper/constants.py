# constants.py
__all__ = [
    "MIN_LIMIT_VAL", 
    "MAX_LIMIT_VAL", 
    "HEADERS", 
    "FIELDNAMES", 
    "BOOLEAN_VALUES", 
    "ENERGY_CLASSIFICATION_VALUES", 
    "NUMBER_VALUES", 
    "URL_PARAMETERS", 
    "REVERSED_URL_PARAMETERS", 
    "SORT_OPTIONS", 
    "REVERSED_SORT_OPTIONS", 
    "FILTER_TYPE_OPTIONS", 
    "FRENCH_SLUG_TO_DB", 
    "DEFAULT_PROPERTY_TYPES", 
    "DEFAULT_SORT_BY", 
    "ROOMS_PATTERN_PLUS", 
    "ROOMS_PATTERN_MINUS", 
    "ROOMS_PATTERN_RANGE", 
    "ROOMS_PATTERN_SINGLE"
]

MIN_LIMIT_VAL = 1
MAX_LIMIT_VAL = 2500

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
    "hasFirePlace": True,
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
    "hasFirePlace": "cheminee",
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

ROOMS_PATTERN_PLUS = re.compile(r"(\d+)-pi[èe]ces?-et-plus")
ROOMS_PATTERN_MINUS = re.compile(r"(\d+)-pi[èe]ces?-et-moins")
ROOMS_PATTERN_RANGE = re.compile(r"de-(\d+)-a-(\d+)-?pi[èe]ces?")
ROOMS_PATTERN_SINGLE = re.compile(r"(\d+)-pi[èe]ces?")