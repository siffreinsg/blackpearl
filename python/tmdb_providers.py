import os

import dotenv
import requests

dotenv.load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
ST_APP_DIR = os.getenv('ST_APP_DIR', os.path.join(os.path.expanduser('~'), '.apps/streaming-tag'))

tmdbHeaders = {'Content-Type': 'application/json'}

tmdbResponseRegions = requests.get(f'https://api.themoviedb.org/3/watch/providers/regions?api_key={TMDB_API_KEY}', headers=tmdbHeaders)
tmdbRegions = tmdbResponseRegions.json()

tmdbResponseProviders = requests.get(f'https://api.themoviedb.org/3/watch/providers/movie?api_key={TMDB_API_KEY}', headers=tmdbHeaders)
tmdbProviders = tmdbResponseProviders.json()

allProviders = [p["provider_name"] for p in tmdbProviders["results"]]
providers = sorted(set(allProviders))

with open(os.path.join(ST_APP_DIR, "providers.txt"), "w") as f:
    f.write("Regions\n-------\n")
    for r in tmdbRegions["results"]:
        f.write(str(r["iso_3166_1"])+"\t"+str(r["english_name"])+"\n")
    f.write("\n\nProviders\n---------\n")
    for p in providers:
        f.write(str(p)+"\n")
