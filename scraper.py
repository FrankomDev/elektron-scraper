#!./.venv/bin/python3

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from dateutil import parser
import sys
import json
import env as env

if env.STRAPI_URL == "" or env.STRAPI_TOKEN == "":
    print("Configure env.py!")
    sys.exit()

def print_help():
    print("\n====================")
    print("Usage:\n")
    print("./scraper.py [ID FIRST] [ID LAST]")
    print("Example: ./scraper.py 10 100")
    print("====================\n")
    sys.exit()

def api_send_post(title, image, date, content) -> bool:
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + env.STRAPI_TOKEN,
    }
    json_data = {
        "data": {
            "title": title,
            "image": image,
            "description": "",
            "customDate": date,
            "content": content,
        },
    }
    r = requests.post(env.STRAPI_URL+"/api/articles", headers=headers, json=json_data)
    if r.ok:
        return True
    return False

def api_send_image(i) -> int:
    with open (f"./img/{i}.jpg", "rb") as f:
        headers = {
            "Authorization": "Bearer " + env.STRAPI_TOKEN,
        }
        files = {
            "files": (f"{i}.jpg", f, "image/jpeg"),
        }
        response = requests.post(env.STRAPI_URL+"/api/upload", headers=headers, files=files)
        #print(response.text)
    r = json.loads(response.text)
    if r[0]['id']:
        return r[0]['id']
    else:
        return 230

url = "https://zseis.zgora.pl/news.php?id="
def publish_posts(i):
    try:
        r=requests.get(url=url+str(i))
        soup = BeautifulSoup(r.text, "html.parser")

        if not soup.find('div', class_="infotext_error"):
            title = soup.find('div', class_="news_title").text
            if soup.find('div', class_="news_content_text").find('img'):
                all_img = soup.find('div', class_="news_content_text").find_all('img')
                for image in all_img:
                    image['src'] = "https://zseis.zgora.pl/"+str(image['src'])
            content = md(str(soup.find('div', class_="news_content_text")))
            try:
                date = str(parser.parse(str(soup.find('span', class_="news_modtext").text), fuzzy=True)).replace(" ","T") + ".0Z"
                img = soup.find('div', class_="news_image").find('img').get('src')
                img_id = 0
                if img == "gfx/logo_zseis.gif":
                    img_id = 230
                else:
                    img_r = requests.get("https://zseis.zgora.pl/" + img)
                    img_r.raise_for_status()
                    with open("./img/"+str(i)+".jpg", "wb") as f:
                        f.write(img_r.content)
                    img_id = api_send_image(i)

                if api_send_post(title, img_id, date, content):
                    print("Done, ID: "+str(i))
            except Exception:
                #this is when date is null
                pass
            
    except Exception as e:
        print("Error! NewsID: "+str(i))
        print(e)
        sys.exit()

if len(sys.argv) >= 2:
    if sys.argv[1] == '-h' or sys.argv[1] == "--help":
        print_help()
    elif len(sys.argv) == 3:
        try:
            if int(sys.argv[1]) <= int(sys.argv[2]):
                for i in range (int(sys.argv[1]), int(sys.argv[2])+1):
                    publish_posts(i)
            else:
                print_help()
        except Exception:
            print_help()
    else:
        print_help()
else:
    print_help()

