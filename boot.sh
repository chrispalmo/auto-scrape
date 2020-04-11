#!/bin/sh

gunicorn --config autoscrape/gunicorn/config-prod.py run:app