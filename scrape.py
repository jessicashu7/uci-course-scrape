from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import unicodedata

cred = credentials.Certificate('planeater-382fd1e9a9ee.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def is_link(tag):
    return tag.has_attr('href') and tag.name == "a"

def get_urls_and_scrape():
    base_url = "http://catalogue.uci.edu/"
    page_response = requests.get(base_url + "allcourses")
    soup = BeautifulSoup(page_response.text, "html5lib")
    div = soup.find("div", id="atozindex")
    links = div.find_all(is_link)
    for l in links:
        url = base_url + l["href"]
        response = requests.get(url)
        scrape_and_store(response)

def scrape_and_store(page_response):
    soup = BeautifulSoup(page_response.text, "html5lib")
    allcourses = soup.find_all("div", class_="courseblock")
    for course in allcourses:
        course_block_title = unicodedata.normalize("NFKD", str(course.find("p", class_="courseblocktitle").string))
        course_info = course_block_title.split(".")

        course_code = unicodedata.normalize('NFKD',course_info[0].strip())
        course_name = course_info[1].strip()
        course_units = course_info[2].strip().split(" ")[0]
        print(course_code)
        print(course_name)
        print(course_units)
        print()
        courseblockdesc = course.find("div", class_="courseblockdesc")
        coursedesclist = courseblockdesc.find_all("p")
        course_desc = ""
        for cd in coursedesclist:
            if cd.string:
                course_desc += str(cd.string) + "\n"
        course_desc = unicodedata.normalize("NFKD", course_desc)
        print(course_desc)

        doc_ref = db.collection('courselist').document(course_code.replace("/","-")) #firestore won't allow / in the name
        doc_ref.set({
            'name': course_code, # + ": " + course_name, #displayed in autofill
            'course_code': course_code,
            'course_name': course_name,
            'course_units': course_units,
            'course_desc': course_desc
        })

if __name__ == "__main__":
    get_urls_and_scrape()
