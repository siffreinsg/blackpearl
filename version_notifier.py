#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Description:  Checks for new releases of apps and sends a Tautulli notification.
Author:       /u/siffreinsg
Requires:     requests

Environment variables:
    TAUTULLI_URL            URL of your Tautulli instance.
    TAUTULLI_APIKEY         API key of your Tautulli instance.
    GITHUB_TOKEN            GitHub token with access to the repos you want to check.
    DATA_FOLDER_PATH        Path to the folder where the version files will be stored.

Script arguments:
    --notifier_id [int]     Tautulli notifier ID to use for the notification.
    --cooldown [int]        Cooldown between each service check (in seconds).

Usage:
    python VersionNotifier.py --notifier_id 1 --cooldown 1
'''

import argparse
import os
import time

import dotenv
import requests
import yaml

# Load environment variables
dotenv.load_dotenv()
TAUTULLI_URL = os.getenv('TAUTULLI_URL')
TAUTULLI_APIKEY = os.getenv('TAUTULLI_APIKEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
DATA_FOLDER_PATH = os.getenv('DATA_FOLDER_PATH', os.path.join(os.path.expanduser('~'), '.apps/version-notifier'))

# Static values
NOTIFICATION_SUBJECT = "<b>Tautulli (Flying Dutchman)</b>"
GITHUB_HEADERS = {
        "Authorization": (f"Bearer {GITHUB_TOKEN}") if GITHUB_TOKEN else None,
        "Accept": "application/vnd.github.v3+json"
    }
GITHUB_PARAMS = {"per_page": 15}


def initiate_data_store():
    if not os.path.exists(DATA_FOLDER_PATH): # If the directory doesn't exist
        return os.mkdir(DATA_FOLDER_PATH) # Create it
    if not os.path.isdir(DATA_FOLDER_PATH): # If not a directory
        raise Exception(f"{DATA_FOLDER_PATH} is not a directory.") # Raise an error


def load_services():
    filepath = os.path.join(DATA_FOLDER_PATH, "services.yml")
    try:
        with open(filepath, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise Exception("services.yml not found.")
    except yaml.YAMLError as e:
        raise Exception(f"Error while parsing services.yaml: {e}")
    except Exception as e:
        raise Exception(f"Error while loading services.yaml: {e}")


def get_version_file(service):
    filename = f"version-{service['label']}.txt"
    filepath = os.path.join(DATA_FOLDER_PATH, filename)

    if not os.path.exists(filepath):
        return None

    with open(filepath, "r") as f:
        return f.read()


def update_version_file(service, version):
    filename = f"version-{service['label']}.txt"
    filepath = os.path.join(DATA_FOLDER_PATH, filename)

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
    repo, target_branch = service["repo"], service["branch"]

    response = requests.get(
        f"https://api.github.com/repos/{repo}/releases",
        params=GITHUB_PARAMS,
        headers=GITHUB_HEADERS
    )

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code} while fetching {response.url}.")

    for release in response.json(): # For each release
        branch = release.get("target_commitish")
        if branch != target_branch: # If not the correct branch
            continue # Skip

        last_version = get_version_file(service)
        version = release.get("tag_name")

        if version == last_version: # If the version is the same as the last one notified
            return None # We reached the last notified version, no need to check further

        return release # Return the release


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--notifier_id', type=int, required=True)
    parser.add_argument('--cooldown', type=int, required=False)
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

        if opts.cooldown:
            time.sleep(opts.cooldown)
