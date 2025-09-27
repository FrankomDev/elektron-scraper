#!/usr/bin/env bash

mkdir img
python3 -m venv .venv
echo "Creating Python venv..."
cp env.py.example env.py
echo "Installing dependencies..."
.venv/bin/pip install requests beautifulsoup4 markdownify python-dateutil