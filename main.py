import os
import time
import PoGoCLI
import LocateIV
import ButtonPressing
from PIL import Image

import threading
from flask import Flask, render_template, request

# Static information
app = Flask(__name__)

name_box = 'images/Name_Box.png'
ok_button = 'images/Ok_Button.png'
okay_button = 'images/Okay_Button.png'
menu_button = "images/Menu_Button.png"
rename_button = 'images/Rename_Button.png'
appraise_button = 'images/Appraise_Button.png'

move = 'move' if os.name == 'nt' else 'mv'
string_finder = 'findstr' if os.name == 'nt' else 'grep'

# Change this based on the device. 
# Slower devices might need more time. 
sleep_time = 2

# Fancy list for renaming
# Might want to make this a csv so more fonts/ascii styling can be used. 
# TODO: Create CSV so it is easy to add and configure style. 
list_of_iv_numbers = ['⓪', '①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '⑪', '⑫', '⑬', '⑭', '⑮', 'Error']

@app.route('/', methods=['GET'])
def serve_iv():
    temp_iv = request.args.get('iv', default = "0-0-0")
    iv = temp_iv.split('+')
    print(iv)
    return render_template('main.html', Attack=list_of_iv_numbers[int(iv[0])], Defense=list_of_iv_numbers[int(iv[1])], Health_Points=list_of_iv_numbers[int(iv[2])])

# If window (nt) then cls else clear (mac / linux)
def clear():
    _ = os.system('cls' if os.name == 'nt' else 'clear')

def Sleep(t = sleep_time):
    print(f'Going to sleep {t} second(s)')
    time.sleep(t)

# Check for connected device
def ADBCheck():

    return PoGoCLI.Get_List_Of_Devices()

def Connect_Device_Menu(ip = None):
    print('This is the menu for Wireless ADB, if you are using a USB, ADB does not currently see your device.')
    print('1. Connect to a known device')
    print('2. Pair a new device (Only needed for Android 11+)')

    choice = None
    if ip == None:
        choice = int(input('Select an option: '))
    else:
        choice == int(1)

    if choice == 1 or choice == 2:

        if (choice == 1):
            if ip == None:
                ip = input('IP: ')
            newPort = input('What is the connect port? ')
            PoGoCLI.Connect_Device(ip, newPort)
            Main_Menu()

        if (choice == 2):
            ip = input('IP: ')
            port = input('Port: ')
            PoGoCLI.Pair_Device(ip, port)
            newPort = input('What is the connect port? ')
            PoGoCLI.Connect_Device(ip, newPort)
            Main_Menu()
    else:
        print('Please enter an option from the menu.')
        Connect_Device_Menu()

def Check_For_Menu():
    print('Checking...')
    
    # Temp - Using Pixel 5 to figure out process.
    ButtonPressing.Find_Button(menu_button)
    Sleep()
    last_tap = ButtonPressing.Find_Button(appraise_button)
    print(last_tap)
    Sleep()
    input()
    temp = LocateIV.Find_The_IVs(Image.open('phoneScreen.png'))
    PoGoCLI.Click(last_tap[0], last_tap[1])
    Sleep()
    PoGoCLI.Flask_Page(temp[0], temp[1], temp[2])
    Sleep()
    PoGoCLI.Device_Input('Copy')
    Sleep()
    PoGoCLI.Device_Input('Back')
    Sleep()
    ButtonPressing.Find_Button(rename_button)
    Sleep()
    PoGoCLI.Device_Input('Paste')
    Sleep()
    ButtonPressing.Find_Button(ok_button)
    Sleep()
    ButtonPressing.Find_Button(okay_button)
    Sleep()
    PoGoCLI.Swipe_Right_To_Left()
    

def Main_Menu():

    listOfDevices = ADBCheck()

    if len(listOfDevices) == 0:
        print('Need to add a device')
        Connect_Device_Menu()
    else:
        input('Please make sure PoGo is open. Press enter when ready.')
        
        # Update the current screenshot screen
        PoGoCLI.Update_Screenshot()

        # Look for IV's
        # If we can't find any IV's, check for menu button.
        #if len(LocateIV.Find_The_IVs(Image.open('phoneScreen.png'))) == 3:
            # If it returns 3 that is the 3 IVs. 
        temp = LocateIV.Find_The_IVs(Image.open('phoneScreen.png'))
        if not (temp[0] == -1 or temp[1] == -1 or temp[2] == -1):
            print(f"Attack: {list_of_iv_numbers[temp[0]]}  Defense: {list_of_iv_numbers[temp[1]]}  HP: {list_of_iv_numbers[temp[2]]}")
        else:
            # Check if we can find the menu
            Check_For_Menu()

    Main_Menu()

def Web_Server():
    app.run(host='0.0.0.0')

Start_Web = threading.Thread(target = Web_Server)
Start_Web.start()

Main_Menu()