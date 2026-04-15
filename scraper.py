import time
import requests 
from bs4 import BeautifulSoup


def get_page_text(soup): # function to extract the main text content from a BeautifulSoup object representing a webpage, which we will use as the text to chunk and embed for our knowledge base
        main = soup.find("main")

        if main:
            result = main.get_text()
            
        else: 
            result = soup.get_text()
                  
        result = " ".join(result.split())
        return result

def get_links(soup): # function to extract all the relevant links from a BeautifulSoup object representing a webpage, which we will use to find more pages to crawl on the UMD website
        links = []
        for a_tag in soup.find_all("a", href = True): # finds every <a> tag that actually has an href, skips empty ones
                href = a_tag['href'] #  pulls the URL string out of the tag, like opening an envelope to read the address

                # Handle relative links 
                if href.startswith("/"):
                    href = "https://umdearborn.edu" + href

                if "umdearborn.edu" in href and "my.umdearborn.edu" not in href:
                    links.append(href)


        return links
    
def crawl(start_url, max_pages=100): # function to crawl the website starting from a given URL, with a limit on the maximum number of pages to visit
    visited = set()
    to_visit = [start_url]  # start with one URL to visit
    
    while len(to_visit) > 0 and len(visited) < max_pages:
        url = to_visit.pop(0)  # grab the next URL to visit
        
        if url in visited:
            continue  # skip

        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
            response = requests.get(url, timeout=10, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
        
            text = get_page_text(soup)  # get the page

            filename = f"data/page_{len(visited)}.txt"
            with open(filename, "w") as file:
                file.write(text)
                print(f"txtfile '{filename}' was created")

            links = get_links(soup)  # get the link
        
            visited.add(url)  # mark as visited
        
            for link in links:
                if link not in visited:
                    to_visit.append(link)  # append new link to: to_visit list

        except Exception as e:
                print(f"Skipping {url}: {e}") 
                continue           
        time.sleep(1.5)    # be polite and wait a bit before the next request

crawl("https://umdearborn.edu/academics")