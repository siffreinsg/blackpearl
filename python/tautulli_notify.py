'''
Description:  Send a Tautulli notification from command line
Author:       /u/siffreinsg
Requires:     requests

Environment variables:
    * TAUTULLI_URL - Tautulli URL, e.g. http://localhost:8181
    * TAUTULLI_API_KEY - Tautulli API key
    * TAUTULLI_NOTIFIER_ID - Tautulli notifier ID for the script notification agent

Arguments:
    * --notifier_id [int] - optional, Tautulli notifier ID for the script notification agent (default: env var TAUTULLI_NOTIFIER_ID)
    * --tautulli_url [str] - optional, Tautulli URL, e.g. http://localhost:8181 (default: env var TAUTULLI_URL)
    * --tautulli_api_key [str] - optional, Tautulli API key (default: env var TAUTULLI_API_KEY)
    * --subject [str] - optional, notification subject (default: <b>Tautulli (Black Pearl)</b>)
    * --body [str] - required, notification body

Usage:
    python tautulli_notify.py --notifier_id 2 --subject "Test subject" --body "Test notification"
'''

import argparse
import os
import sys

import requests

TAUTULLI_URL = os.getenv('TAUTULLI_URL')
TAUTULLI_API_KEY = os.getenv('TAUTULLI_API_KEY')
TAUTULLI_NOTIFIER_ID = os.getenv('TAUTULLI_NOTIFIER_ID')

def notify_tautulli(subject, body):
    if not TAUTULLI_URL or not TAUTULLI_API_KEY or not TAUTULLI_NOTIFIER_ID:
        print('Tautulli URL, API key or notifier ID not set. Not sending notification.')
        return

    params = {
        "apikey": TAUTULLI_API_KEY,
        "cmd": "notify",
        "notifier_id": TAUTULLI_NOTIFIER_ID,
        "subject": subject,
        "body": body
    }

    r = requests.get(TAUTULLI_URL.rstrip('/') + '/api/v2', params=params)
    r.raise_for_status()

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--notifier_id', type=int, required=False, default=TAUTULLI_NOTIFIER_ID)
    parser.add_argument('--tautulli_url', type=str, required=False, default=TAUTULLI_URL)
    parser.add_argument('--TAUTULLI_API_KEY', type=str, required=False, default=TAUTULLI_API_KEY)
    parser.add_argument('--subject', type=str, required=False, default='<b>Tautulli (Black Pearl)</b>')
    parser.add_argument('--body', type=str, required=True)
    opts = parser.parse_args()

    TAUTULLI_NOTIFIER_ID = opts.notifier_id
    TAUTULLI_URL = opts.tautulli_url
    TAUTULLI_API_KEY = opts.TAUTULLI_API_KEY

    notify_tautulli(opts.subject, opts.body)
