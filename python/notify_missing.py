import os
from datetime import datetime, timedelta, timezone

import dotenv
import requests
import timeago
import yaml

# Load environment variables
dotenv.load_dotenv()
TAUTULLI_URL = os.getenv('TAUTULLI_URL')
TAUTULLI_API_KEY = os.getenv('TAUTULLI_API_KEY')
TAUTULLI_NOTIFIER_ID = os.getenv('TAUTULLI_NOTIFIER_ID')
NM_DATA_FOLDER_PATH = os.getenv('NM_DATA_FOLDER_PATH', os.path.join(os.path.expanduser('~'), '.apps/notify-status'))

# Static values
NOTIFICATION_SUBJECT = "<b>Missing Media</b>"

def notify_tautulli(body):
    if not TAUTULLI_URL or not TAUTULLI_API_KEY or not TAUTULLI_NOTIFIER_ID:
        print('Tautulli URL, API key or notifier ID not set. Not sending notification.')
        return

    params = {
        "apikey": TAUTULLI_API_KEY,
        "cmd": "notify",
        "notifier_id": TAUTULLI_NOTIFIER_ID,
        "subject": NOTIFICATION_SUBJECT,
        "body": body
    }

    r = requests.get(TAUTULLI_URL.rstrip('/') + '/api/v2', params=params)
    r.raise_for_status()

def initiate_data_store():
    if not os.path.exists(NM_DATA_FOLDER_PATH): # If the directory doesn't exist
        os.mkdir(NM_DATA_FOLDER_PATH) # Create it
        print(f"Created data folder on path '{NM_DATA_FOLDER_PATH}'.")
        return
    if not os.path.isdir(NM_DATA_FOLDER_PATH): # If not a directory
        raise Exception(f"{NM_DATA_FOLDER_PATH} is not a directory.") # Raise an error


def load_config():
    filepath = os.path.join(NM_DATA_FOLDER_PATH, "config.yaml")
    print(f"Loading config from {filepath}...")

    try:
        with open(filepath, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise Exception("services.yaml not found.")
    except yaml.YAMLError as e:
        raise Exception(f"Error while parsing services.yaml: {e}")
    except Exception as e:
        raise Exception(f"Error while loading services.yaml: {e}")


# ==== RADARR ====
class Radarr:
    def __init__(self, url, api_key):
        if not url or not api_key:
            raise Exception('Missing Radarr URL or API key')

        self.url = url
        self.api_key = api_key

    def get_system_status(self):
        response = requests.get(f'{self.url}/api/v3/system/status?apikey={self.api_key}')
        response.raise_for_status()
        system_status = response.json()

        return system_status

    def get_movies(self):
        response = requests.get(f'{self.url}/api/v3/movie?apikey={self.api_key}')
        response.raise_for_status()
        movies = response.json()

        return movies

    def get_tags(self):
        response = requests.get(f'{self.url}/api/v3/tag?apikey={self.api_key}')
        response.raise_for_status()
        tags = response.json()

        return tags

    def add_movie_tag(self, movie_ids, tags):
        payload = {
            'movieIds': movie_ids if isinstance(movie_ids, list) else [movie_ids],
            'applyTags': 'add',
            'tags': tags if isinstance(tags, list) else [tags]
        }

        response = requests.put(f'{self.url}/api/v3/movie/editor/?apikey={self.api_key}', json=payload)
        response.raise_for_status()

    def remove_movie_tag(self, movie_ids, tags):
        payload = {
            'movieIds': movie_ids if isinstance(movie_ids, list) else [movie_ids],
            'applyTags': 'remove',
            'tags': tags if isinstance(tags, list) else [tags]
        }

        response = requests.put(f'{self.url}/api/v3/movie/editor/?apikey={self.api_key}', json=payload)
        response.raise_for_status()

    def create_tag(self, label):
        payload = {
            'label': label
        }

        response = requests.post(f'{self.url}/api/v3/tag/?apikey={self.api_key}', json=payload)
        response.raise_for_status()

        tag_id = response.json()['id']
        return tag_id


if __name__ == '__main__':
    initiate_data_store() # Create the data folder if it doesn't exist
    config = load_config() # Load the services to check

    for instance in config["radarr"]:
        print()
        base_url = os.getenv(instance["base_url_env"])
        api_key = os.getenv(instance["api_key_env"])
        radarr = Radarr(base_url, api_key)

        # Get the name of the radarr instance
        system_status = radarr.get_system_status()
        instance_name = system_status['instanceName']
        print(f"> Processing {instance_name}.")

        # Get all tags
        tags = radarr.get_tags()
        print(f"Fetched {len(tags)} tags.")
        missing_tag_id = None

        # Create missing_notified tag if it doesn't exist
        if not any(tag['label'] == 'missing_notified' for tag in tags):
            missing_tag_id = radarr.create_tag('missing_notified')
            print("Missing tag 'missing_notified' created.")
        else:
            missing_tag_id = next(tag['id'] for tag in tags if tag['label'] == 'missing_notified')
            print(f"Missing tag 'missing_notified' already exists with id {missing_tag_id}.")

        # Get all movies
        movies = radarr.get_movies()
        print(f"Fetched {len(movies)} movies.")

        for movie in movies:
            # Convert the added date to a datetime object. The added date is in Zulu time ISO 8601 format.
            now = datetime.now(timezone.utc)
            added = datetime.fromisoformat(movie['added'])
            added_formatted = timeago.format(added, now)

            print(f"\t * {movie['title']}")
            print(f"\t\t - Added {added_formatted}")

            # Get list of tags for the movie
            movie_tags = [tag['label'] for tag in tags if tag['id'] in movie['tags']]
            if len(movie_tags) > 0:
                print(f"\t\t - Tags: {', '.join(movie_tags)}")

            # If the movie is already tagged as missing_notified and it's not missing anymore, remove the tag
            if 'missing_notified' in movie_tags and movie['hasFile']:
                print(f"\t\t - Movie not missing anymore. Removing 'missing_notified' tag.")
                radarr.remove_movie_tag(movie['id'], missing_tag_id)
                continue

            # If the movie is not missing, continue
            if movie['hasFile']:
                if 'missing_notified' in movie_tags:
                    print(f"\t\t - Movie now available. Removing 'missing_notified' tag.")
                    radarr.remove_movie_tag(movie['id'], missing_tag_id)
                else:
                    print(f"\t\t - Movie available.")
                continue

            # Check if the movie is available
            if movie['status'] != 'released':
                print(f"\t\t - Movie not released yet")
                continue
            else:
                print(f"\t\t - Movie released")

            released = datetime.fromisoformat(movie['digitalRelease'])
            released_formatted = timeago.format(released, now)

            # If the movie was added in the last 24 hours, continue
            threshold_hours = instance["missing_hours"]
            if now - added < timedelta(hours=threshold_hours):
                continue

            print(f"\t\t - Notifying on Tautulli")
            notify_tautulli(f"[{instance_name}] Movie <b>{movie['title']}</b> has been missing for more than {threshold_hours} hours.\n> Released {released_formatted}.\n> Added {added_formatted}.")
            radarr.add_movie_tag(movie['id'], missing_tag_id)
