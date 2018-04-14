#!/bin/bash

WORK_DIR=/home/foobargem/webapp/pandongbot
uwsgi --ini $WORK_DIR/uwsgi.ini
