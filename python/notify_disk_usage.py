#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Description:  Send a Tautulli notification when disk usage exceeds a threshold.
Author:       /u/siffreinsg
Requires:     subprocess, requests

Tautulli script trigger:
   * Notify on recently added

Environment variables:
    * TAUTULLI_URL - Tautulli URL, e.g. http://localhost:8181
    * TAUTULLI_APIKEY - Tautulli API key
    * TAUTULLI_NOTIFIER_ID - Tautulli notifier ID for the script notification agent
    * DISK_USAGE_PATH - Path to check disk usage for, default is home directory
    * DISK_USAGE_THRESHOLD - Disk usage threshold in GB, default is 2500 GB

Usage:
    python notify_disk_usage.py
'''

import os
import subprocess

import dotenv
import requests

# Load environment variables
dotenv.load_dotenv()
TAUTULLI_URL = os.getenv('TAUTULLI_URL')
TAUTULLI_APIKEY = os.getenv('TAUTULLI_APIKEY')
TAUTULLI_NOTIFIER_ID = os.getenv('TAUTULLI_NOTIFIER_ID')
DISK_USAGE_PATH = os.getenv('DISK_USAGE_PATH', os.path.expanduser('~') + '/')
DISK_USAGE_THRESHOLD = int(os.getenv('DISK_USAGE_THRESHOLD', 2500))

NOTIFICATION_SUBJECT = '<b>Disk Usage</b>'

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

if __name__ == '__main__':
    print(f"Checking disk usage for path {DISK_USAGE_PATH}...")

    du_cmd = ['du', '-s', DISK_USAGE_PATH]
    disk_usage = int(subprocess.check_output(du_cmd).split(maxsplit=1)[0])
    disk_usage_gb = round(disk_usage / 1_000_000, 2)

    print(f"Disk usage for path {DISK_USAGE_PATH} is about {disk_usage_gb} GB.")

    if disk_usage_gb >= DISK_USAGE_THRESHOLD:
        print(f"Disk usage for path {DISK_USAGE_PATH} exceeds threshold of {DISK_USAGE_THRESHOLD} GB.")
        notify_tautulli(
            f"Path <code>{DISK_USAGE_PATH}</code> disk usage is <b>{disk_usage_gb} GB</b> exceeding threshold of <b>{DISK_USAGE_THRESHOLD} GB</b>."
        )
