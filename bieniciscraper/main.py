#!/usr/bin/env python3

import argparse
from .scraper import scrape
from .constants import MIN_LIMIT_VAL, MAX_LIMIT_VAL

def range_limited_integer_type(arg):
    try:
        f = int(arg)
    except ValueError:    
        raise argparse.ArgumentTypeError("must be an integer")
    if f < MIN_LIMIT_VAL or f > MAX_LIMIT_VAL:
        raise argparse.ArgumentTypeError("must be < " + str(MAX_LIMIT_VAL) + " and > " + str(MIN_LIMIT_VAL))
    return f

def main():
    parser = argparse.ArgumentParser(description='bienici listings scraper')
    
    parser.add_argument(
        '-u', 
        '--url', 
        type=str,
        required=False,
        default='https://www.bienici.com/recherche/achat/france/chateau', 
        help='url to scrape the listings from — by default https://www.bienici.com/recherche/achat/france/chateau'
    )
    
    parser.add_argument(
        '-l', 
        '--limit', 
        type=range_limited_integer_type,
        required=False, 
        default=2500, 
        help='maximum number of listings to scrape — by default 2500'
    )

    parser.add_argument(
        '-o', 
        '--output', 
        type=str,
        required=False, 
        default='data_bienici_lobstr_io.csv',
        help='filename to save the results — by default data_bienici_lobstr_io.csv'
    )

    args = parser.parse_args()

    scrape(url=args.url, limit=args.limit, output=args.output)

if __name__ == '__main__':
    main()
