#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Description:  Send a Tautulli notification when disk usage exceeds a threshold.
Author:       /u/siffreinsg
Requires:     subprocess, requests

Tautulli script trigger:
   * Notify on recently added
Tautulli script arguments:
   * Recently Added:
        --homepath "/home/seedbox" --threshold 2500 --notifier_id 2 --subject "Tautulli" --body "Path {path} disk usage is {usage} GB exceeding threshold {threshold} GB."

Usage:
    python notify_disk_usage.py --homepath "/home/seedbox" --threshold 2500 --notifier_id 2 --subject "Tautulli" --body "Path {path} disk usage is {usage} GB exceeding threshold {threshold} GB."
'''

import argparse
import os
import subprocess

import requests

TAUTULLI_URL = os.getenv('TAUTULLI_URL')
TAUTULLI_APIKEY = os.getenv('TAUTULLI_APIKEY')

def notify_tautulli(notifier_id, body):
    if not TAUTULLI_URL or not TAUTULLI_APIKEY:
        raise ValueError('Tautulli URL or API key not set.')

    params = {
        "apikey": TAUTULLI_APIKEY,
        "cmd": "notify",
        "notifier_id": notifier_id,
        "subject": '<b>Tautulli (Black Pearl)</b>',
        "body": body
    }
    requests.get(TAUTULLI_URL.rstrip('/') + '/api/v2', params=params)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=True)
    parser.add_argument('--threshold', type=int, required=True)
    parser.add_argument('--notifier_id', type=int, required=True)
    opts = parser.parse_args()

    du_cmd = ['du', '-s', opts.path]
    disk_usage = int(subprocess.check_output(du_cmd).split(maxsplit=1)[0])
    disk_usage_gb = disk_usage / 1_000_000

    if disk_usage_gb >= opts.threshold:
        body = f"Path {opts.path} disk usage is {round(disk_usage_gb, 2)} GB."
        notify_tautulli(opts.notifier_id, body)
