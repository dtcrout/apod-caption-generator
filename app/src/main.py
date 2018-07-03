"""main.py"""

import requests
import json

URL = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=5'

if __name__ == "__main__":
    # Make request to get metadata
    req = requests.get(URL)
    s = json.loads(req.text)

    print([i['explanation'] for i in s if "copyright" not in i.keys()])
