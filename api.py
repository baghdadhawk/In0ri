import json
import os
import sys

import requests
from flask import Flask, request

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import re
import alert
import FlaskApp.database
from checkdefaced import check
from screenshot import screenshot
from logger import get_logger
logger = get_logger(__name__)


def slug(string):
    pattern = "|%[0-9]{1,}|%|--|#|;|/\*|'|\"|\\\*|\[|\]|xp_|\&gt|\&ne|\&lt|&"
    result = re.sub(pattern, "", string)
    # Strip trailing and leading whitespace to avoid accidental issues
    return result.strip()


app = Flask(__name__)


@app.route("/checkdeface", methods=["POST"])
def checkdeface():
    db = FlaskApp.database.Database("site")
    al = alert.Alert()
    res = {}
    body = json.loads(request.data)
    if len(body["key"]) == 0 and len(body["path"]) == 0: 
        res = {"status": "400 Bad Request!"}
        return res
    else: 
        key = slug(body["key"])
    
    active_key = {"active_key": key}
    data = db.get_single_data(active_key)
    if data is None:
        res = {"status": "404 Key Invalid!"}
        return res
    url = data["url"] + body["path"]
    receiver = data["email"]

    try:
        response = requests.get(url)
    except requests.ConnectionError:
        res = {"status": "500 Internal Server Error!"}
        return res

    if (response.status_code != 200) and (response.status_code != 302):
        res = {"status": "URL Invalid! " + url}
    else:
        img_path = screenshot(url)
        if img_path is None:
            logger.error("Failed to capture screenshot for %s", url)
            return {"status": "500 Internal Server Error!"}
        defaced = check(img_path)
        if defaced:
            al.sendBot(url, img_path)
            subject = "Website Defacement"
            message = (
                f"You website was defaced!\nURL: {url} \nPath infected: {body['path']}"
            )
            al.sendMessage(receiver, subject, message, img_path)
            res = {"status": "Website was defaced!"}
            logger.info("Website was defaced!")
        else:
            res = {"status": "Everything oke!"}
            logger.info("Everything oke!")
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8088")
