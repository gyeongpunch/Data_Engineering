#!/bin/bash
set -e

exec jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --port=8888 --NotebookApp.token=''
