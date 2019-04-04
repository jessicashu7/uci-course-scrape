import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, render_template


cred = credentials.Certificate('planeater-382fd1e9a9ee.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route('/', methods= ['GET'] )
def main():
    source = retrieve_source()
    return render_template("index.html", source = source)


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
