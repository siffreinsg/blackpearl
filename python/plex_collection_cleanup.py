#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Description:  Deletes empty collections from Plex
Author:       /u/siffreinsg
Requires:     dotenv, requests, plexapi

Environment variables:
    * TAUTULLI_URL - Tautulli URL, e.g. http://localhost:8181
    * TAUTULLI_APIKEY - Tautulli API key
    * TAUTULLI_NOTIFIER_ID - Tautulli notifier ID for the script notification agent
    * PLEX_URL - Plex URL, e.g. http://localhost:32400
    * PLEX_TOKEN - Plex authentification token, see https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

Usage:
    python plex_collection_cleanup.py
'''

import os

import dotenv
import requests
from plexapi.server import PlexServer

# Load environment variables
dotenv.load_dotenv()
TAUTULLI_URL = os.getenv('TAUTULLI_URL')
TAUTULLI_APIKEY = os.getenv('TAUTULLI_APIKEY')
TAUTULLI_NOTIFIER_ID = os.getenv('TAUTULLI_NOTIFIER_ID')
PLEX_URL = os.getenv('PLEX_URL')
PLEX_TOKEN = os.getenv('PLEX_TOKEN')

NOTIFICATION_SUBJECT = '<b>Plex Collection Cleanup</b>'

def notify_tautulli(body):
    if not TAUTULLI_URL or not TAUTULLI_APIKEY or not TAUTULLI_NOTIFIER_ID:
        print('Tautulli URL, API key or notifier ID not set. Not sending notification.')
        return

    params = {
        "apikey": TAUTULLI_APIKEY,
        "cmd": "notify",
        "notifier_id": TAUTULLI_NOTIFIER_ID,
        "subject": NOTIFICATION_SUBJECT,
        "body": body
    }
    requests.get(TAUTULLI_URL.rstrip('/') + '/api/v2', params=params)

if __name__ == '__main__':
    # Load Plex server
    print ("Loading Plex server...")
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    print(f"Connected to {plex.friendlyName}.")

    # Delete empty collections
    for section in plex.library.sections(): # Loop through sections
        print(f"Checking section {section.title}...")
        for collection in section.collections(): # Loop through collections in section
            print(f"Checking collection {collection.title}...")
            if not collection.items(): # If collection is empty
                print(f"Collection {collection.title} from section {section.title} is empty, deleting...")
                collection.delete() # Delete collection
                notify_tautulli(f"Deleted empty collection <b>{collection.title}</b> from section <b>{section.title}</b>.")
