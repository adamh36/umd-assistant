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

