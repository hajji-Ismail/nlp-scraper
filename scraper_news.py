


import csv
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def ScrapeYahooNews():

    folder_path = Path("./data")

    folder_path.mkdir(parents=True, exist_ok=True)
    csv_file = "./data/newsdata.csv"
    headers_csv = ["unique ID", "URL", "date", "headline", "body of the article"]
    
    # Initialize the file and clear previous contents
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers_csv)
        
    article_id = 1
    seen_urls = set()
   
    request_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }
    
    # Iterate page index explicitly from 1 to 20
    for page_index in range(1, 7):
        url = f"https://www.yahoo.com/news/{page_index}"
        print(f"\n--- Requesting Yahoo News Page {page_index}/20: {url} ---")
        
        try:
            response = requests.get(url, headers=request_headers, timeout=15)
        except Exception as e:
            print(f"Error fetching directory page {page_index}: {e}")
            continue # Try the next page if this one fails
        
        if response.status_code != 200:
            print(f"Yahoo rejected page {page_index}. Status code: {response.status_code}")
            continue
            
        soup = BeautifulSoup(response.content, "html.parser")
        letters = soup.find_all('li', attrs={'class': "list-none"})
        
        if not letters:
            print(f"No articles found on page {page_index}.")
            continue
            
        # Open CSV in append mode to save records incrementally
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            for let in letters:
                TitleLinkContainer = let.find("h3")
                if not TitleLinkContainer:
                    continue
                    
                TitleLink = TitleLinkContainer.find("a")
                if not TitleLink or not TitleLink.get('href'):
                    continue
                    
                headline = TitleLink.get_text(strip=True)
                raw_link = TitleLink.get('href')
                
                # Format absolute URL path
                if raw_link.startswith('/'):
                    article_url = "https://www.yahoo.com" + raw_link
                else:
                    article_url = raw_link
                    
                # Deduplication check
                if article_url in seen_urls:
                    continue
                
                print(f"Scraping ID {article_id}: {headline[:50]}...")
                
                # Fetch individual article contents
                try:
                    time.sleep(1)  # Throttling to respect Yahoo's servers
                    maindata = requests.get(article_url, headers=request_headers, timeout=15)
                    
                    if maindata.status_code == 200:
                        soupmain = BeautifulSoup(maindata.content, "html.parser")
                        
                        # Extract exact timestamp string
                        time_tag = soupmain.find("time")
                        timestamp = time_tag.get('datetime') if time_tag else "N/A"
                        
                        # Extract full article text
                        paragraphs = soupmain.find_all("p")
                        article_body = " ".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                        
                        if not article_body:
                            article_body = "No content available"
                        
                        # Write structured record live to CSV
                        writer.writerow([article_id, article_url, timestamp, headline, article_body])
                        
                        seen_urls.add(article_url)
                        article_id += 1
                        
                    else:
                        print(f"Failed to fetch article body. Status: {maindata.status_code}")
                        
                except Exception as e:
                    print(f"Error scraping article {article_url}: {e}")
                    
        # Delay between shifting pages
        time.sleep(0.5)

    print(f"\nScrape completed successfully! Extracted {article_id - 1} total records across 20 pages into {csv_file}")

# Execution
ScrapeYahooNews()