#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Description:  Send a Tautulli notification from command line
Author:       /u/siffreinsg
Requires:     requests

Usage:
    echo "Hello world!" | python tautulli_notify.py --notifier_id 2
'''

import argparse
import os
import sys

import requests

TAUTULLI_URL = os.getenv('TAUTULLI_URL')
TAUTULLI_APIKEY = os.getenv('TAUTULLI_APIKEY')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--notifier_id', type=int, required=True)
    parser.add_argument('--tautulli_url', type=str, required=False, default=TAUTULLI_URL)
    parser.add_argument('--tautulli_apikey', type=str, required=False, default=TAUTULLI_APIKEY)
    opts = parser.parse_args()

    if not opts.tautulli_url or not opts.tautulli_apikey:
        raise ValueError('Tautulli URL or API key not set.')

    body = sys.stdin.read()

    params = {
        "apikey": opts.tautulli_apikey,
        "cmd": "notify",
        "notifier_id": opts.notifier_id,
        "subject": '<b>Tautulli (Black Pearl)</b>',
        "body": body
    }

    requests.get(opts.tautulli_url.rstrip('/') + '/api/v2', params=params)
