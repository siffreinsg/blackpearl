#! /bin/bash
cd /home/siffreinsg/scripts

export PATH="/home/$USER/.pyenv/bin:$PATH"
eval "$(pyenv init -)"

python3 version_notifier.py --notifier_id 2
