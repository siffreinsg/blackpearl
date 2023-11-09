import requests


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

    def delete_tag(self, id):
        response = requests.delete(f'{self.url}/api/v3/tag/{id}?apikey={self.api_key}')
        response.raise_for_status()
