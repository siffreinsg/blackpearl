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
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)

    # Delete empty collections
    for section in plex.library.sections(): # Loop through sections
        for collection in section.collections(): # Loop through collections in section
            if not collection.items(): # If collection is empty
                print(f"Deleting empty collection {collection.title} from section {section.title}.")
                collection.delete() # Delete collection
                notify_tautulli(f"Deleted empty collection <b>{collection.title}</b> from section <b>{section.title}</b>.")
