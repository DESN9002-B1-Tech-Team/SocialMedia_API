import os
from instabot import Bot
import shutil
from flask import Flask, jsonify
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

# Required Functions
def clean_up():
    dir_rem = "config"
    to_delete = ["tmp.jpg", "tmp.png", "tmp.jpeg"]
    if os.path.exists(dir_rem):
        try:
            shutil.rmtree(dir_rem)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    for file in to_delete:
        if os.path.exists(file):
            os.remove(file)


def upload_post(media, text):
    bot = Bot()

    bot.login(username="metalsecondaccount", password="DESN9002_test")
    bot.upload_photo(media, caption=text)


def download_media(url):
    filename = "tmp." + url.split(".")[-1]
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True

        with open(filename, 'wb') as tmp:
            shutil.copyfileobj(r.raw, tmp)
        return filename


# API Endpoint
class PyAPI_Insta(Resource):
    def get(self, content):
        data = content.split("../{}")
        try:
            clean_up()
        finally:
            # try:
            upload_post('tmp.jpg', data[1])
                # return (jsonify({"code": 0}))
            # except:
                # return (jsonify({"code": 1}))


# Adding API Endppoint
api.add_resource(PyAPI_Insta, '/post/<path:content>')


if __name__ == '__main__':
    app.run()
