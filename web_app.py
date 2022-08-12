from flask import Flask,render_template,redirect,request
import caption_this
import pyttsx3
import time


def text_to_speech(text, gender):
    """
    Function to convert text to speech
    :param text: text
    :param gender: gender
    :return: None
    """
    voice_dict = {'Male': 0, 'Female': 1}
    code = voice_dict[gender]

    engine = pyttsx3.init()

    # Setting up voice rate
    engine.setProperty('rate', 125)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 0.8)

    # Change voices: 0 for male and 1 for female
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[code].id)

    engine.say(text)
    engine.runAndWait()

app = Flask(__name__)

caption=''
@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/",methods=['POST'])
def prediction():
    if request.method == 'POST':
        f=request.files['userfile']
        path="./static/{}".format(f.filename)
        f.save(path)
        caption =  caption_this.caption_it(path)
        result_dic={
            'image':path,
            'caption':caption}
        text_to_speech(text=caption, gender='Female')
    return render_template("index.html",result=result_dic)

# @app.route("/recommend",methods=['GET','POST'])
# def recommend():
#     if request.method =="Post":
#         rec=request.form
#         print(rec)
#     return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
