import csv
import os
import shutil
import math
import requests
import pandas as pd

API_KEY = os.environ["API_KEY"]
SAVE_DIR = "images/"

def get_addresses(csv_path):
    df = pd.read_csv(csv_path)
    return df['Address'].tolist()


def get_image(add, save_loc):
    base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
    url = base + requests.compat.quote_plus(add) + API_KEY #added url encoding
    img_file = add + ".jpg"

    response = requests.get(url, stream=True)
    print(response.status_code)
    with open(os.path.join(SAVE_DIR,img_file), 'wb') as out_file:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, out_file)
    del response

def filter_data(address):
    # Super quick and dirty address validation :P
    return isinstance(address, str) and len(address) > 4

def gen_streetview_images():
    addresses = list(filter(filter_data, get_addresses("addresses.csv")))
    for address in addresses:
        get_image(address, SAVE_DIR)

gen_streetview_images()
