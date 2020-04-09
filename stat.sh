#!/bin/sh

. ./bin/activate

gunicorn --bind 127.0.0.1:5050 wsgi:app
