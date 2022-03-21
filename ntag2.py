"""
This example shows connecting to the PN532 and reading an NTAG215
type RFID tag
"""

import RPi.GPIO as GPIO

import pn532.pn532 as nfc
import sqlite3
import ATM
from pn532 import *

pn532 = PN532_SPI(cs=4, reset=20, debug=False)
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with NTAG215 cards
pn532.SAM_configuration()


def readCard():
    print('Waiting for RFID/NFC card to read from!')
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is not None:
            break

    bArr = [hex(i) for i in uid]
    bStr = ""

    for i in bArr:
        bStr += str(i)

    return bStr


def write_UID_to_pass(userID):
    uid = readCard()
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute("UPDATE users SET password=? WHERE userID=?", (uid, userID,))
    db.commit()
    db.close()
    print("success")


# print(readCard())