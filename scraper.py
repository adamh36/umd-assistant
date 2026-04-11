import requests 
from bs4 import BeautifulSoup


def get_page_text(soup):
        main = soup.find("main")

        if main:
            result = main.get_text()
            
        else: 
            result = soup.get_text()
                  
        result = " ".join(result.split())
        return result

def get_links(soup):
        links = []
        for a_tag in soup.find_all("a", href = True): # finds every <a> tag that actually has an href, skips empty ones
                href = a_tag['href'] #  pulls the URL string out of the tag, like opening an envelope to read the address

                # Handle relative links 
                if href.startswith("/"):
                    href = "https://umdearborn.edu" + href

                if "umdearborn.edu" in href and "my.umdearborn.edu" not in href:
                    links.append(href)


        return links
    
def crawl(start_url, max_pages=100):
    visited = set()
    to_visit = [start_url]  # start with one URL to visit
    
    while len(to_visit) > 0 and len(visited) < max_pages:
        url = to_visit.pop(0)  # grab the next URL to visit
        
        if url in visited:
            continue  # skip

        try:
            response = requests.get(url)
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
                print(f"Skippinh {url}: {e}") 
                continue           

crawl("https://umdearborn.edu/academics")