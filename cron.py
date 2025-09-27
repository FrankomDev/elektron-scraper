#!./.venv/bin/python3
import requests
from bs4 import BeautifulSoup
import os

with open("last_id", "r") as f:
    current_id = int(f.read())

url = "https://zseis.zgora.pl/news.php?id="
r=requests.get(url+str(current_id+1))
soup = BeautifulSoup(r.text, "html.parser")
if not soup.find('div', class_="infotext_error"):
    print("found")
    os.system(f"./scraper.py {current_id+1} {current_id+1}")
    with open("last_id", "w") as f:
        f.write(str(current_id+1))
else:
    print("not found")
