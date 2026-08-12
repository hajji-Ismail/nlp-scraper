
import sqlite3
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def ScrapeYahooNews():
    folder_path = Path("./data")
        
    folder_path.mkdir(parents=True, exist_ok=True)


    


   
    
    
    article_id = 1
    seen_urls = set()
   
    request_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }
    
    # Iterate page index explicitly from 1 to 20
    for page_index in range(1, 21):
        url = f"https://www.yahoo.com/news/world/{page_index}"
        print(f"\n--- Requesting Yahoo News Page {page_index}/20: {url} ---")
        
        try:
                response = requests.get(url, headers=request_headers, timeout=15)
        except Exception as e:
                print(f"Error fetching directory page {page_index}: {e}")
                continue 
        
        if response.status_code != 200:
                print(f"Yahoo rejected page {page_index}. Status code: {response.status_code}")
                continue
            
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all('li', attrs={'class': "list-none"})
        
        if not articles:
            print(f"No articles found on page {page_index}.")
            continue
            
      
            
        for let in articles:
            TitleLinkContainer = let.find("h3")
            if not TitleLinkContainer:
                continue
                    
            TitleLink = TitleLinkContainer.find("a")
            if not TitleLink or not TitleLink.get('href'):
                    continue
                    
            headline = TitleLink.get_text(strip=True)
            raw_link = TitleLink.get('href')
                
               
            if raw_link.startswith('/'):
                    article_url = "https://www.yahoo.com" + raw_link
            else:
                    article_url = raw_link
                    
            if article_url in seen_urls:
                    continue
                
            print(f"Scraping ID {article_id}: {headline[:50]}...")
                
            try:
                time.sleep(1)  
                maindata = requests.get(article_url, headers=request_headers, timeout=15)
                    
                if maindata.status_code == 200:
                        soupmain = BeautifulSoup(maindata.content, "html.parser")
                        
                        time_tag = soupmain.find("time")
                        timestamp = time_tag.get('datetime') if time_tag else "N/A"
                        
                        paragraphs = soupmain.find_all("p")
                        article_body = " ".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                        
                        if not article_body:
                            article_body = "No content available"
                        
                       

                        sql = "INSERT INTO news (`URL`, `date`, `headline`, `body of the article`) VALUES ($1, $2,$3 ,$4 )"
                        cursor.execute(sql, (article_url, timestamp, headline, article_body))
                        conn.commit()
                                                    
                        seen_urls.add(article_url)
                        article_id += 1
                        
                else:
                        print(f"Failed to fetch article body. Status: {maindata.status_code}")
                        
            except Exception as e:
                    print(f"Error scraping article {article_url}: {e}")
                    
        # Delay between shifting pages
        time.sleep(0.5)
  
        


# Execution
ScrapeYahooNews()