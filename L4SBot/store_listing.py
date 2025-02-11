import json


def store_listing(symbol):
    """
    SAVE LISTING INTO LOCAL JSON FILE
    """
    with open("inviati.txt", 'a') as f:
        f.write(symbol + "\n")


def load_listing(file):
    """
    UPDATE JSON FILE
    """
    with open(file, "r+") as f:
        return json.load(f)


def check_existing_listing(symbol):
    with open('inviati.txt') as f:
        if symbol in f.read():
            return True
