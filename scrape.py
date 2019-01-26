from bs4 import BeautifulSoup
import requests

page_url = "http://catalogue.uci.edu/allcourses/compsci/"
page_response = requests.get(page_url)


if __name__ == "__main__":
    soup = BeautifulSoup(page_response.text, "html5lib")
    titletag = soup.title
    titlestr = str(titletag.string)
    print(titlestr)

    allcourses = soup.find_all("div", class_="courseblock")
    for course in allcourses:
        print(course.prettify())
