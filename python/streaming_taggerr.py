import os

import dotenv
import requests
import yaml
from radarr import Radarr

dotenv.load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
ST_APP_DIR = os.getenv('ST_APP_DIR', os.path.join(os.path.expanduser('~'), '.apps/streaming-taggerr'))

headers = {'Content-Type': 'application/json'}

def initiate_data_store():
    if not os.path.exists(ST_APP_DIR): # If the directory doesn't exist
        os.mkdir(ST_APP_DIR) # Create it
        print(f"Created data folder on path '{ST_APP_DIR}'.")
        return
    if not os.path.isdir(ST_APP_DIR): # If not a directory
        raise Exception(f"{ST_APP_DIR} is not a directory.") # Raise an error


def load_config():
    filepath = os.path.join(ST_APP_DIR, "config.yaml")
    print(f"Loading config from {filepath}...")

    try:
        with open(filepath, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise Exception("config.yaml not found.")
    except yaml.YAMLError as e:
        raise Exception(f"Error while parsing config.yaml: {e}")
    except Exception as e:
        raise Exception(f"Error while loading config.yaml: {e}")


if __name__ == '__main__':
    initiate_data_store() # Create the data folder if it doesn't exist
    config = load_config() # Load the services to check

    for instance in config["radarr"]:
        print()
        base_url = os.getenv(instance["base_url_env"])
        api_key = os.getenv(instance["api_key_env"])
        radarr = Radarr(base_url, api_key)

        # Get the name of the radarr instance
        instance_name = radarr.get_system_status()['instanceName']
        print(f"> Processing {instance_name}.")

        # Get existing tags
        existing_tags = radarr.get_tags()
        st_tags = [tag for tag in existing_tags if tag['label'].startswith(config["tag_prefix"].lower())]
        wanted_tags = [f"{config['tag_prefix']}{provider}".lower() for provider in config["providers"]]
        print(f"Found {len(st_tags)} existing ST tags ({len(existing_tags)} total).")

        tags = {} # Map tag label to tag id

        # Delete tags that are no longer in the config
        for tag in st_tags:
            if tag["label"] not in wanted_tags:
                print(f"Deleting tag {tag['label']}...")
                radarr.delete_tag(tag['id'])
            else:
                tags[tag["label"]] = tag["id"] # Add the tag to the map

        # Create tags that are in the config but not in the existing tags
        for provider_tag in wanted_tags:
            if not any(tag['label'] == provider_tag for tag in existing_tags):
                print(f"Creating tag {provider_tag}...")
                new_tag_id = radarr.create_tag(provider_tag)
                tags[provider_tag] = new_tag_id # Add the tag to the map
            else:
                tags[provider_tag] = next(tag['id'] for tag in existing_tags if tag['label'] == provider_tag) # Add the tag to the map

        # Get all movies
        movies = radarr.get_movies()
        print(f"Fetched {len(movies)} movies.")

        for movie in movies:
            tmdbResponse = requests.get(f'https://api.themoviedb.org/3/movie/{movie["tmdbId"]}/watch/providers?api_key={TMDB_API_KEY}', headers=headers)
            tmdbResponse.raise_for_status()
            tmdbProviders = tmdbResponse.json()

            if config["provider_region"] not in tmdbProviders["results"]:
                print(f"Movie {movie['title']} has no providers for region {config['provider_region']}.")
                continue

            if "flatrate" not in tmdbProviders["results"][config["provider_region"]]:
                print(f"Movie {movie['title']} has no flatrate providers.")
                continue

            flatrateProviders = tmdbProviders["results"][config["provider_region"]]["flatrate"]
            available_providers = set(map(lambda provider: provider["provider_name"], flatrateProviders))
            wanted_providers = set(config["providers"]).intersection(available_providers)

            if len(wanted_providers) == 0:
                print(f"Movie {movie['title']} is not available on any of the wanted providers.")
                continue

            print(f"Movie {movie['title']} is available on: {', '.join(wanted_providers)}.")

            for provider in wanted_providers:
                provider_tag = f"{config['tag_prefix']}{provider}".lower()
                if provider_tag not in movie["tags"]:
                    radarr.add_movie_tag(movie["id"], tags[provider_tag])
