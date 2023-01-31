import pyttsx3


def text_to_speech(text):
    """
    Function to convert text to speech
    :param text: text
    :param gender: gender
    :return: None
    """
    voice_dict = {'Male': 0, 'Female': 1}

    engine = pyttsx3.init()

    # Setting up voice rate
    engine.setProperty('rate', 125)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 0.8)

    engine.say(text)
    engine.runAndWait()


# Importing the necessary Libraries
from flask_cors import cross_origin
from flask import Flask, render_template, request

app = Flask(__name__)



@app.route('/', methods=['POST', 'GET', 'OPTIONS'])
@cross_origin()
def homepage():
    if request.method == 'POST':
        print(request.get_json())
        print("hello")
        #text = request.form['botMsg']
        #text_to_speech(text)
        return render_template('index.html')
    if request.method == 'GET':
        print("hello")
        return render_template('index.html')

if __name__ == "__main__":
    app.run(port=8000, debug=True)