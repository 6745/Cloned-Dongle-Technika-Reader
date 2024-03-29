import serial
import time
import argparse
import json
import pyautogui
print(" ██████╗██╗   ██╗██╗      ██████╗ ███╗   ██╗ ██████╗     ██╗   ██╗     ██╗")
print("██╔════╝╚██╗ ██╔╝██║     ██╔═══██╗████╗  ██║██╔════╝     ██║   ██║    ███║")
print("██║      ╚████╔╝ ██║     ██║   ██║██╔██╗ ██║██║  ███╗    ██║   ██║    ╚██║")
print("██║       ╚██╔╝  ██║     ██║   ██║██║╚██╗██║██║   ██║    ╚██╗ ██╔╝     ██║")
print("╚██████╗   ██║   ███████╗╚██████╔╝██║ ╚████║╚██████╔╝     ╚████╔╝      ██║")
print(" ╚═════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝       ╚═══╝       ╚═╝")
print("                                                                          ")
print("By Github.com/6745")

parser = argparse.ArgumentParser()
parser.add_argument("COM", help="Serial port identifier")
parser.add_argument("BAUD", type=int, help="Baud rate")
args = parser.parse_args()

ser = serial.Serial(args.COM, args.BAUD)
ignore_list = ["Error in communication", "Authentication failed", "Timeout in communication","CRC_A does not match"]
reset_timer = 10  # Set the reset timer to 10 second
while True:
    data = ser.readline().decode('utf-8').strip()
    if data.startswith("Name:"):
        name = data     
        debug = data.replace("Name:", "").replace("\x00", "").replace("Error in communication", "BLOCK READ FAILED").replace("Timeout in communication", "BLOCK READ TIMEOUT",).replace("CRC_A does not match.","CRC FAIL")
        print(debug) #debug 
        if not any(ignore_string in name for ignore_string in ignore_list):
            name = data
            if len(debug) == 20:
                print("DEBUG: Block Read Success! Updating local_card in config.json...")  # debug

                # Load the existing settings from config.json
                with open("Data/System/JSON/config.json", "r") as file:
                    settings = json.load(file)

                # Update the local_card value
                settings["network"]["local_card"] = debug

                # Save the updated settings back to config.json
                with open("Data/System/JSON/config.json", "w") as file:
                    json.dump(settings, file, indent=4)
                pyautogui.click()
                time.sleep(5)
                pyautogui.click()
                print("DEBUG: local_card updated in config.json!")

                # Sleep for 10 seconds
                time.sleep(reset_timer)

                # After 10 seconds, reset local_card to an empty string
                print("DEBUG: Resetting local_card to an empty string in config.json after 10 seconds!")
                settings["network"]["local_card"] = ""

                # Save the updated settings back to config.json
                with open("Data/System/JSON/config.json", "w") as file:
                    json.dump(settings, file, indent=4)

                print("DEBUG: local_card reset to an empty string in config.json!")
