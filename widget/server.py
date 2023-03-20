# Importing the necessary Libraries
from flask_cors import cross_origin
from flask import Flask, render_template, request
#import speech_recognition as sr

app = Flask(__name__)
#r = sr.Recognizer()


@app.route('/', methods=['POST', 'GET', 'OPTIONS'])
@cross_origin()
def homepage():
    if request.method == 'POST':
        stt()
        print("not hello")
        return render_template('index.html')
    if request.method == 'GET':
        print("hello")
        return render_template('index.html')

if __name__ == "__main__":
    app.run(port=8000, debug=True)