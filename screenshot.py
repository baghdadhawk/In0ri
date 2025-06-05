# coding=utf-8
import hashlib
import os
import time

from logger import get_logger
logger = get_logger(__name__)

from selenium import webdriver


if not os.path.exists("/opt/In0ri/FlaskApp/static/images/"):
    os.makedirs("/opt/In0ri/FlaskApp/static/images/")

# Use the geckodriver installed with the Docker image. This avoids
# downloading the driver at runtime which would fail without network
# access and slows startup.
firefox_path = os.environ.get("GECKODRIVER_PATH", "/usr/bin/geckodriver")


def screenshot(url):
    options = webdriver.FirefoxOptions()
    options.headless = True
    options.add_argument("--start-maximized")
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--no-sandbox')
    driver = webdriver.Firefox(options=options, executable_path=firefox_path)


    name = hashlib.md5(url.encode())
    try:
        driver.get(url)
        logger.info("Screenshoting...%s", url)
        time.sleep(6)
        driver.get_screenshot_as_file(
            "/opt/In0ri/FlaskApp/static/images/" + name.hexdigest() + ".png"
        )
    except Exception as e:
        logger.exception(e)
        logger.error("URL %s was died!", url)
        return None
    finally:
        driver.quit()

    return "/opt/In0ri/FlaskApp/static/images/" + name.hexdigest() + ".png"
