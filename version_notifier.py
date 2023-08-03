#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Description:  Checks for new releases of apps and sends a Tautulli notification.
Author:       /u/siffreinsg
Requires:     requests

Environment variables:
    TAUTULLI_URL            URL of your Tautulli instance.
    TAUTULLI_APIKEY         API key of your Tautulli instance.
    VN_GITHUB_TOKEN         GitHub token with access to the repos you want to check.
    VN_DATA_FOLDER_PATH     Path to the folder where the data will be stored.

Script arguments:
    --notifier_id [int]     Tautulli notifier ID to use for the notification.

Usage:
    python VersionNotifier.py --notifier_id 1
'''

import argparse
import os

import dotenv
import requests
import yaml

# Load environment variables
dotenv.load_dotenv()
TAUTULLI_URL = os.getenv('TAUTULLI_URL')
TAUTULLI_APIKEY = os.getenv('TAUTULLI_APIKEY')
VN_GITHUB_TOKEN = os.getenv('VN_GITHUB_TOKEN')
VN_DATA_FOLDER_PATH = os.getenv('VN_DATA_FOLDER_PATH', os.path.join(os.path.expanduser('~'), '.apps/version-notifier'))

# Static values
NOTIFICATION_SUBJECT = "<b>Tautulli (Black Pearl)</b>"
GITHUB_HEADERS = {
        "Authorization": f"Bearer {VN_GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
GITHUB_PARAMS = {"per_page": 15}


def initiate_data_store():
    if not os.path.exists(VN_DATA_FOLDER_PATH): # If the directory doesn't exist
        os.mkdir(VN_DATA_FOLDER_PATH) # Create it
        print(f"Created data folder on path '{VN_DATA_FOLDER_PATH}'.")
        return
    if not os.path.isdir(VN_DATA_FOLDER_PATH): # If not a directory
        raise Exception(f"{VN_DATA_FOLDER_PATH} is not a directory.") # Raise an error


def load_services():
    filepath = os.path.join(VN_DATA_FOLDER_PATH, "services.yaml")
    print(f"Loading services from {filepath}...")

    try:
        with open(filepath, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise Exception("services.yaml not found.")
    except yaml.YAMLError as e:
        raise Exception(f"Error while parsing services.yaml: {e}")
    except Exception as e:
        raise Exception(f"Error while loading services.yaml: {e}")


def get_version_file(service):
    filename = f"version-{service['label']}.txt"
    filepath = os.path.join(VN_DATA_FOLDER_PATH, filename)

    if not os.path.exists(filepath):
        return None

    with open(filepath, "r") as f:
        return f.read()


def update_version_file(service, version):
    filename = f"version-{service['label']}.txt"
    filepath = os.path.join(VN_DATA_FOLDER_PATH, filename)

    with open(filepath, "w") as f:
        f.write(version)


def notify_tautulli(notifier_id, body):
    if not TAUTULLI_URL or not TAUTULLI_APIKEY:
        raise ValueError('Tautulli URL or API key not set.')

    params = {
        "apikey": TAUTULLI_APIKEY,
        "cmd": "notify",
        "notifier_id": notifier_id,
        "subject": NOTIFICATION_SUBJECT,
        "body": body
    }
    requests.get(TAUTULLI_URL.rstrip('/') + '/api/v2', params=params)


def check_app_update(service):
    repo, target_branch = service['repo'], service['branch']

    response = requests.get(
        f"https://api.github.com/repos/{repo}/releases",
        params=GITHUB_PARAMS,
        headers=GITHUB_HEADERS
    )

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code} while fetching {response.url}.")

    releases = [
            release for release in response.json()
            if release.get("target_commitish") == target_branch
        ] # Get the releases for the target branch

    if len(releases) == 0:
        return None

    latest = releases[0] # Get the latest release
    last_version_notified = get_version_file(service) # Get the last version notified
    if last_version_notified != latest.get("tag_name"): # If the latest version is different from the last version notified
        return latest # Return the latest release

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--notifier_id', type=int, required=True)
    opts = parser.parse_args()

    initiate_data_store() # Create the data folder if it doesn't exist
    services = load_services() # Load the services to check

    for service in services: # For each service
        label, display_name, repo, branch = service["label"], service["display_name"], service["repo"], service["branch"]
        print(f"Checking updates for {display_name} ({repo} on {branch})...")

        try:
            release = check_app_update(service)
        except Exception as e:
            print(f"Error while checking updates for {display_name}: {e}")
            notify_tautulli(
                opts.notifier_id,
                f"Erreur lors de la recherche de mises à jour de {display_name}: <pre language=\"python\">{e}</pre>"
            )
        else:
            if not release:
                print(f"No update found for {display_name}.")
                continue

            version = release.get("tag_name")
            print(f"Update found for {display_name}: {version}.")
            update_version_file(service, version)

            notify_tautulli(
                opts.notifier_id,
                f"Mise à jour de {display_name} à la version {version} disponible."
            )
