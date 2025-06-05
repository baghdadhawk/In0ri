from sys import argv

import alert
from checkdefaced import check
from logger import get_logger
logger = get_logger(__name__)
from screenshot import screenshot

script, url, receiver = argv


def main(url, receiver):
    al = alert.Alert()
    logger.info(url)
    img_path = screenshot(url)

    defaced = check(img_path)
    if defaced:
        al.sendBot(url, img_path)
        subject = "Website Defacement"
        message = f"You website was defaced!\nURL: {url}"
        al.sendMessage(receiver, subject, message, img_path)
        logger.info("Website was defaced!")
    logger.info("Everything oke!")


main(url, receiver)
