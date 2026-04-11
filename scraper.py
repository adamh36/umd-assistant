import requests 
from bs4 import BeautifulSoup


def get_page_text(url):

    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        main = soup.find("main")

        if main:
            result = main.get_text()
            
        else: 
            result = soup.get_text()
                  
        result = " ".join(result.split())
        return result

    else:
        print("Bad request")

print(get_page_text("https://umdearborn.edu/academics"))


def get_links(url):

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        links = []
        if response.status_code == 200:
            for a_tag in soup.find_all("a", href = True): # finds every <a> tag that actually has an href, skips empty ones
                href = a_tag['href'] #  pulls the URL string out of the tag, like opening an envelope to read the address

                # Handle relative links 
                if href.startswith("/"):
                    href = "https://umdearborn.edu" + href

            # Only keep umdearborn links
                if "umdearborn.edu" in href:
                    links.append(href)

        return links
    
    except Exception as e:

        print(f"ERROS: {e}")
        return []

print(get_links("https://umdearborn.edu/academics"))