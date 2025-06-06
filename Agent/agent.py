import json
import re
import time

import requests
from logger import get_logger
from os import path as osp

logger = get_logger(__name__)
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

base_dir = osp.dirname(osp.abspath(__file__))
with open(osp.join(base_dir, "config.json"), "r") as f:
    config = json.load(f)
key = config["key"]
excludePath = config["excludePath"]
server = config["apiServer"]


def on_modified(event):
    if len(excludePath) != 0 and re.search(excludePath, event.src_path) is not None:
        return 0
    else:
        logger.info("Notification, %s has been modified", event.src_path)
        path = event.src_path
        path = path.replace(config["rootPath"], "")
        try:
            response = requests.post(
                server, json={"key": key, "path": path}
            )
            logger.info(response.json())
        except requests.ConnectionError:
            logger.error("Server not found!")


def on_moved(event):
    if len(excludePath) != 0 and re.search(excludePath, event.src_path) is not None:
        return 0
    else:
        logger.info(
            "Notification, File %s has been moved to %s",
            event.src_path,
            event.dest_path,
        )
        path = event.dest_path
        path = path.replace(config["rootPath"], "")
        try:
            response = requests.post(
                server, json={"key": key, "path": path}
            )
            logger.info(response.json())
        except requests.ConnectionError:
            logger.error("Server not found!")


if __name__ == "__main__":
    patterns = [
        "*.html",
        "*.htm",
        "*.php",
        "*.txt",
        "*.jsp",
        "*.aspx",
        "*.shtml",
        "*.hta",
    ]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(
        patterns, ignore_patterns, ignore_directories, case_sensitive
    )
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = config["rootPath"]
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
