import os
#import time
import LocateIV
#import pyautogui
from PIL import Image

# Fancy list for renaming
# Might want to make this a csv so more fonts/ascii styling can be used. 
# TODO: Create CSV so it is easy to add and configure style. 
list_Of_IV_Numbers = ['⓪', '①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '⑪', '⑫', '⑬', '⑭', '⑮', 'Error']

stringFinder = 'findstr' if os.name == 'nt' else 'grep'
move = 'move' if os.name == 'nt' else 'mv'

# If window (nt) then cls else clear (mac / linux)
def clear():
    _ = os.system('cls' if os.name == 'nt' else 'clear')

# Check for connected device
def ADBCheck():

    listOfDevices = []

    # First check if device is connected
    os.system(f'adb devices > temp.txt')
    temp = open('temp.txt').readlines()
    for device in temp:
        try:
            int(device[0])
            # Orginally I was going to remove anything after the \t
            # but it is useful to see if a device is offline
            tempDevice = device.split('\n')[0]
            tempDevice2 = tempDevice.split('\t')
            if tempDevice2[1] == 'offline':
                # Connect the device and then add it. 
                ConnectDeviceMenu(tempDevice2[0])
            else:
                listOfDevices.append(device.split('\n')[0])

        except ValueError:
            pass

    return listOfDevices

def ConnectDeviceMenu(ip = None):
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
            os.system(f'adb connect {ip}:{newPort}')
            MainMenu()

        if (choice == 2):
            ip = input('IP: ')
            port = input('Port: ')
            os.system(f'adb pair {ip}:{port}')
            newPort = input('What is the connect port? ')
            os.system(f'adb connect {ip}:{newPort}')
            MainMenu()
    else:
        print('Please enter an option from the menu.')
        ConnectDeviceMenu()

def MainMenu():

    listOfDevices = ADBCheck()

    if len(listOfDevices) == 0:
        print('Need to add a device')
        ConnectDeviceMenu()
    else:
        input('Please make sure PoGo is open. Press enter when ready.')
        
        # Update the current screenshot screen
        os.system("adb exec-out screencap -p > phoneScreen.png")

        # Look for IV's
        # If we can't find any IV's, check for menu button.
        #if len(LocateIV.Find_The_IVs(Image.open('phoneScreen.png'))) == 3:
            # If it returns 3 that is the 3 IVs. 
        temp = LocateIV.Find_The_IVs(Image.open('phoneScreen.png'))
        print(f"Attack: {list_Of_IV_Numbers[temp[0]]}  Defense: {list_Of_IV_Numbers[temp[1]]}  HP: {list_Of_IV_Numbers[temp[2]]}")

    MainMenu()


MainMenu()