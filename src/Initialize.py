import os
import zipfile

georges_de_lat = '../data/dictionaries/georges_de-lat'
georges_lat_de = '../data/dictionaries/georges_lat-de'
georges_lewis = '../data/dictionaries/lewis_short'

with zipfile.ZipFile(os.path.join(georges_de_lat, 'dict.zip'), 'r') as zip_ref:
    zip_ref.extractall(georges_de_lat)
