#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
/home/torin/miniconda3/envs/isdp4/bin/gunicorn -c config.gunicorn.py dashboard:server