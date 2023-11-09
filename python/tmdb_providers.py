'''
Description:  Generates a list of regions and providers for TMDb
Author:       /u/siffreinsg
Requires:     dotenv, requests

Environment variables:
    * TMDB_API_KEY - TMDb API key
    * ST_APP_DIR - Path to the Streaming Tagger app directory

Usage:
    python tmdb_providers.py
'''
import os

import dotenv
import requests

dotenv.load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
ST_APP_DIR = os.getenv('ST_APP_DIR', os.path.join(os.path.expanduser('~'), '.apps/streaming-taggerr'))

headers = {'Content-Type': 'application/json'}

responseRegions = requests.get(f'https://api.themoviedb.org/3/watch/providers/regions?api_key={TMDB_API_KEY}', headers=headers)
regions = responseRegions.json()["results"]

responseProviders = requests.get(f'https://api.themoviedb.org/3/watch/providers/movie?api_key={TMDB_API_KEY}', headers=headers)
providers = responseProviders.json()

allProviders = [p["provider_name"] for p in providers["results"]]
providerNames = sorted(set(allProviders))

with open(os.path.join(ST_APP_DIR, "providers.txt"), "w") as f:
    f.write("Regions\n-------\n")
    for region in regions:
        f.write(f"{region['iso_3166_1']}\t{region['english_name']}\n")

    f.write("\n\nProviders\n---------\n")
    for provider in providerNames:
        f.write(f"{provider}\n")
