import serial
import time
import argparse
import os
import sys
import pyautogui

print(" ██████ ██████  ████████ ██████      ██    ██ ██████  ")
print("██      ██   ██    ██    ██   ██     ██    ██      ██ ")
print("██      ██   ██    ██    ██████      ██    ██  █████  ")
print("██      ██   ██    ██    ██   ██      ██  ██  ██      ")
print(" ██████ ██████     ██    ██   ██       ████   ███████ ")
print("By Github.com/6745")

parser = argparse.ArgumentParser()
parser.add_argument("COM", help="Serial port identifier")
parser.add_argument("BAUD", type=int, help="Baud rate")
args = parser.parse_args()

ser = serial.Serial(args.COM, args.BAUD)
ignore_list = ["Error in communication", " Authentication failed", "Timeout in communication","CRC_A does not match"]

while True:
    data = ser.readline().decode('utf-8').strip()
    if data.startswith("Name:"):
        name = data
        debug = data.replace("Name:", "").replace("\x00", "").replace("Error in communication", "BLOCK READ FAILED").replace("Timeout in communication", "BLOCK READ TIMEOUT",).replace("CRC_A does not match.","CRC FAIL")
        print(debug) #debug 
        if not any(ignore_string in name for ignore_string in ignore_list):
            name = data
            if len(debug) == 20:
                print("DEBUG: Block Read Success! Saving to file..") #debug 
                with open("CardNum.txt", "w") as file:
                    file.write(debug)
                pyautogui.click()
                time.sleep(5)
                print("DEBUG: NULLED FILE!")
                with open("CardNum.txt", "w") as file:
                    file.write("")
