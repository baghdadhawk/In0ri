from sys import argv

import alert
from checkdefaced import check
from logger import get_logger
logger = get_logger(__name__)
from screenshot import screenshot

script, url, receiver, *rest = argv
notify_clean = False
if rest:
    notify_clean = bool(int(rest[0]))


def main(url, receiver):
    al = alert.Alert()
    logger.info(url)
    img_path = screenshot(url)
    if img_path is None:
        logger.error("Failed to capture screenshot for %s", url)
        return

    defaced = check(img_path)
    if defaced:
        al.sendBot(url, img_path)
        subject = "Website Defacement"
        message = f"You website was defaced!\nURL: {url}"
        al.sendMessage(receiver, subject, message, img_path)
        logger.info("Website was defaced!")
    else:
        logger.info("Everything oke!")
        if notify_clean:
            al.sendBot(url, img_path)
            al.sendMessage(receiver, "All Good!", "Website looks fine.")


main(url, receiver)
