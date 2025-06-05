import imghdr
import os
import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage
import ssl


from logger import get_logger
logger = get_logger(__name__)
from telegram import Bot
import requests

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import FlaskApp.database as database

db = database.Database("setting")


class Alert:
    def sendMessage(self, receiver, subject, message, imagePath=None):
        for data in db.get_multiple_data():
            if "smtp" not in data:
                smtpArray = []
            else:
                smtpArray = data["smtp"]
        if len(smtpArray) == 0:
            return "1"
        for smtp in smtpArray:
            EMAIL_SERVER = smtp["smtp_server"]
            EMAIL_ADDRESS = smtp["smtp_address"]
            EMAIL_PASSWORD = smtp["smtp_password"]

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = receiver
        msg.set_content(message)

        try:
            if imagePath is not None:
                with open(imagePath, "rb") as f:
                    file_data = f.read()
                    file_type = imghdr.what(f.name)
                msg.add_attachment(
                    file_data, maintype="image", subtype=file_type, filename="Website image"
                )

            # Create SSL context
            context = ssl.create_default_context()

            # Try multiple connection methods
            try:
                # Method 1: SMTP_SSL (port 465)
                with smtplib.SMTP_SSL(EMAIL_SERVER, 465, context=context) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    smtp.send_message(msg)
                    logger.info("Email sent successfully via SMTP_SSL")
            except Exception as e1:
                logger.warning(f"SMTP_SSL failed: {e1}")
                try:
                    # Method 2: SMTP with STARTTLS (port 587)
                    with smtplib.SMTP(EMAIL_SERVER, 587) as smtp:
                        smtp.starttls(context=context)
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)
                        logger.info("Email sent successfully via SMTP with STARTTLS")
                except Exception as e2:
                    logger.warning(f"SMTP with STARTTLS failed: {e2}")
                    # Method 3: SMTP with less secure SSL context
                    context_insecure = ssl.create_default_context()
                    context_insecure.check_hostname = False
                    context_insecure.verify_mode = ssl.CERT_NONE

                    with smtplib.SMTP_SSL(EMAIL_SERVER, 465, context=context_insecure) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)
                        logger.info("Email sent successfully via insecure SSL context")

        except smtplib.SMTPException as e:
            logger.exception(f"SMTP Error: {e}")
            raise
        except Exception as e:
            logger.exception(f"General Error: {e}")
            raise

    def sendBot(self, url, img_path):
        for data in db.get_multiple_data():
            if "telegram" not in data:
                telegramArray = []
            else:
                telegramArray = data["telegram"]

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if len(telegramArray) == 0:
            return "1"
        for telegram in telegramArray:
            CHAT_ID = telegram["chat_id"]
            TOKEN = telegram["token"]

        bot = Bot(TOKEN)
        try:
            bot.sendPhoto(
                CHAT_ID,
                photo=open(img_path, "rb"),
                caption="⚠️"
                + "Website "
                + url
                + " was defaced!\n"
                + "At "
                + current_time,
            )
        except Exception:
            logger.error("Looks like CHAT_ID or TOKEN of telegram-bot was wrong!")

    def getBotInfo(self, CHAT_ID, TOKEN):
        """Validate the Telegram token and chat ID via the Bot API."""
        try:
            me_resp = requests.get(
                f"https://api.telegram.org/bot{TOKEN}/getMe", timeout=5
            ).json()
            if not me_resp.get("ok"):
                return "ERROR"
            first_name = me_resp.get("result", {}).get("first_name", "")

            chat_resp = requests.get(
                f"https://api.telegram.org/bot{TOKEN}/getChat",
                params={"chat_id": CHAT_ID},
                timeout=5,
            ).json()
            if not chat_resp.get("ok"):
                return "ERROR"
            title = chat_resp.get("result", {}).get("title", "")
            return first_name, title
        except Exception:
            return "ERROR"


# alert = Alert()
# print(alert.getBotInfo())
