from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

page_url = "http://catalogue.uci.edu/allcourses/compsci/"
page_response = requests.get(page_url)

cred = credentials.Certificate('planeater-382fd1e9a9ee.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

if __name__ == "__main__":
    soup = BeautifulSoup(page_response.text, "html5lib")
    #title  = str(soup.find("h1").string)

    allcourses = soup.find_all("div", class_="courseblock")
    for course in allcourses:
        course_block_title = str(course.find("p", class_="courseblocktitle").string)
        course_info = course_block_title.split(".")

        course_code = course_info[0].strip()
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
        print(course_desc)

        #print(title)

        doc_ref = db.collection(u'courselist').document(course_code)
        doc_ref.set({
            u'course_code': course_code,
            u'course_name': course_name,
            u'course_units': course_units,
            u'course_desc': course_desc
        })
