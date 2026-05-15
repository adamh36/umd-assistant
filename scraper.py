import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


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
    
def crawl(start_url, max_pages=300): # function to crawl the website starting from a given URL, with a limit on the maximum number of pages to visit
    visited = set()
    to_visit = [start_url]  # start with one URL to visit

    with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            
    
            while len(to_visit) > 0 and len(visited) < max_pages:
                url = to_visit.pop(0)  # grab the next URL to visit
        
                if url in visited:
                    continue  # skip

        
                try:
                    page = browser.new_page()
                    page.goto(url, timeout=15000)
                    page.wait_for_timeout(2000)
                    html = page.content()
                    page.close()

                    soup = BeautifulSoup(html, "html.parser")
                    text = get_page_text(soup) # extract the main text content from the page using our get_page_text function, which will give us the text we want to chunk and embed for our knowledge base
               

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