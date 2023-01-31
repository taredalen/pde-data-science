


# Importing the necessary Libraries
from flask_cors import cross_origin
from flask import Flask, render_template, request
import speech_recognition as sr

app = Flask(__name__)
r = sr.Recognizer()

def stt():
    with sr.Microphone as source2:
        r.adjust_for_ambient_noise(source2, duration=0.2)
        audio2  = r.listen(source2)

        text = r.recognize_google(audio2)
        text = text.lower()

        print(text)

        return text



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