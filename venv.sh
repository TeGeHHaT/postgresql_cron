#!/bin/bash

ROOT=`dirname "$0"`
VENV="$ROOT/venv"
PIP="$VENV/bin/pip"

rm -rf $VENV
python3 -m venv $VENV
$PIP install --upgrade psycopg2-binary python-dotenv croniter
