"""get_metadata.py"""

import configparser
import json
from os import path
import requests
import sys

# Current directory
FILE_DIR = path.dirname(path.abspath(__file__))

# Load config file
config = configparser.ConfigParser()
config.read(path.join(FILE_DIR, '../resources/config'))

URL = config.get('urls', 'url')
API_KEY = config.get('keys', 'api_key')

def get_metadata(date):
    """
    Given a date, return metadata for NASA apod dataset.

    Input
    -----
    date: str
        Date is in YYYY-MM-DD format.

    Returns
    -------
    json
    """

    # Make payload
    payload = {}
    payload['api_key'] = API_KEY
    payload['date'] = date

    # Make GET request
    req = requests.get(URL, params=payload)
    s = json.loads(req.text)

    return(s)

if __name__ == "__main__":
    date = sys.argv[1]
    print(get_metadata(date))
