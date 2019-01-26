from bs4 import BeautifulSoup
import requests

page_url = "http://catalogue.uci.edu/allcourses/compsci/"
page_response = requests.get(page_url)


if __name__ == "__main__":
    soup = BeautifulSoup(page_response.text, "html5lib")
    print(soup.title)
