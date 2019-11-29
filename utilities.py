import json
import requests

import pandas as pd

#functions used by more than one app

def read_data_from_file(filename):
    results = None
    with open(filename) as f:
        results = json.load(f)
        results = results["data"]
    return results

def read_data_from_url(url):
    r = requests.get(url)
    return r.json()["data"]
