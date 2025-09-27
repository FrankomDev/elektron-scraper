#!/usr/bin/env bash

mkdir img
echo "Creating Python venv..."
python3 -m venv .venv
cp env.py.example env.py
echo "Installing dependencies..."
.venv/bin/pip install requests beautifulsoup4 markdownify python-dateutil