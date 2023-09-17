#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Description:  Checks for new releases of apps and sends a Tautulli notification.
Author:       /u/siffreinsg
Requires:     dotenv, requests, PyYAML

Environment variables:
    TAUTULLI_URL - Tautulli URL
    TAUTULLI_APIKEY - Tautulli API key
    TAUTULLI_NOTIFIER_ID - Tautulli notifier ID
    GITHUB_TOKEN - GitHub token
    VN_DATA_FOLDER_PATH - Path to the data folder (default: ~/.apps/version-notifier)

Usage:
    python version_notifier.py
'''
import os

import dotenv
import requests
import yaml

# Load environment variables
dotenv.load_dotenv()
TAUTULLI_URL = os.getenv('TAUTULLI_URL')
TAUTULLI_APIKEY = os.getenv('TAUTULLI_APIKEY')
TAUTULLI_NOTIFIER_ID = os.getenv('TAUTULLI_NOTIFIER_ID')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
VN_DATA_FOLDER_PATH = os.getenv('VN_DATA_FOLDER_PATH', os.path.join(os.path.expanduser('~'), '.apps/version-notifier'))

# Static values
NOTIFICATION_SUBJECT = "<b>Version Notifier</b>"
GITHUB_HEADERS = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
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


def notify_tautulli(body):
    if not TAUTULLI_URL or not TAUTULLI_APIKEY or not TAUTULLI_NOTIFIER_ID:
        raise ValueError('Tautulli URL, API key or notifier ID not set.')

    params = {
        "apikey": TAUTULLI_APIKEY,
        "cmd": "notify",
        "notifier_id": TAUTULLI_NOTIFIER_ID,
        "subject": NOTIFICATION_SUBJECT,
        "body": body
    }
    requests.get(TAUTULLI_URL.rstrip('/') + '/api/v2', params=params)


def check_app_update(service):
    repo = service['repo']
    target_commitish = service['target_commitish'] if ("target_commitish" in service) else None

    response = requests.get(
        f"https://api.github.com/repos/{repo}/releases",
        params=GITHUB_PARAMS,
        headers=GITHUB_HEADERS
    )

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code} while fetching {response.url}.")

    releases = response.json()

    if target_commitish:
        releases = [release for release in releases if (release.get("target_commitish") == target_commitish)] # Get the releases for the target branch

    if len(releases) == 0:
        return None

    latest = releases[0] # Get the latest release
    last_version_notified = get_version_file(service) # Get the last version notified
    if last_version_notified != latest.get("tag_name"): # If the latest version is different from the last version notified
        return latest # Return the latest release

if __name__ == '__main__':
    initiate_data_store() # Create the data folder if it doesn't exist
    services = load_services() # Load the services to check

    for service in services: # For each service
        label, display_name, repo = service["label"], service["display_name"], service["repo"]
        print(f"Checking updates for {display_name}...")

        try:
            release = check_app_update(service)
        except Exception as e:
            print(f"Error while checking updates for {display_name}: {e}")
            notify_tautulli(f"Erreur lors de la recherche de mises à jour de <b>{display_name}</b>: <pre language=\"python\">{e}</pre>")
        else:
            if not release:
                print(f"No update found for {display_name}.")
                continue

            version = release.get("tag_name")
            print(f"Update found for {display_name}: {version}.")
            update_version_file(service, version)

            notify_tautulli(f"Mise à jour de <b>{display_name}</b> à la version <code>{version}</code> disponible.")
