from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import unicodedata
from flask import Flask, render_template

page_url = "http://catalogue.uci.edu/allcourses/compsci/"
page_response = requests.get(page_url)

cred = credentials.Certificate('planeater-382fd1e9a9ee.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route('/', methods= ['GET'] )
def main():
    #scrape_and_store()
    source = retrieve_source()
    return render_template("index.html", source = source)

def scrape_and_store():
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

        doc_ref = db.collection('courselist').document(course_code)
        doc_ref.set({
            'name': course_code + ": " + course_name,
            'course_code': course_code,
            'course_name': course_name,
            'course_units': course_units,
            'course_desc': course_desc
        })

def retrieve_source():
    source = []
    doc_ref = db.collection('courselist')
    docs = doc_ref.get()
    for doc in docs:
        d = doc.to_dict()
        dstring = u'{}: {}'.format(doc.id,d)
        print(dstring)
        print()
        source.append(d)
    for s in source:
        print(s)
    return source



if __name__ == "__main__":
    app.run(debug = True)
