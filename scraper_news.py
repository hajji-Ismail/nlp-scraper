import requests
from bs4 import BeautifulSoup
import hashlib
import csv 
from pathlib import Path
def Scraper() :
    folder_path = Path("./data")

    folder_path.mkdir(parents=True, exist_ok=True)
    url = "https://cbn.com/lp/cbn-news"

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response= requests.get(url,headers)
    
    if response.status_code == 200 :
        soup = BeautifulSoup(response.text, "html.parser")
        with open("data/newsdata.csv", mode="w", newline="" ,encoding="utf-8") as file :
            writer = csv.writer(file)
            writer.writerow(["Unique ID", "URL", "Date", "Headline", "Body"])

        
        
            articles = soup.find_all("div", class_="news-header__card")
            for article in articles :
                heading_tag = article.find("h3", class_="news-card__heading")
                headline = heading_tag.get_text(strip=True) if heading_tag else "No Headline"
        
       
                inner_card = article.find("div", class_="news-card")
                relative_url = inner_card["about"] if (inner_card and inner_card.has_attr("about")) else ""
                url = "https://www.cbn.com" + relative_url if relative_url else "No URL"
        
   
                unique_id = hashlib.md5(relative_url.encode()).hexdigest() if relative_url else "No ID"
        
                img_tag = article.find("img")
                date = img_tag["src"].split("/public/")[1].split("/")[0] if (img_tag and "/public/" in img_tag["src"]) else "No Date on Card"
        
                category_tag = article.find("div", class_="news-card__category")
                body = category_tag.get_text(strip=True) if category_tag else "No Snippet Text"
                writer.writerow([unique_id, url, date, headline, body])



        

Scraper()
    
