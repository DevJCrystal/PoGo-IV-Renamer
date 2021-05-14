import os
import PoGoCLI
#import time
import LocateIV
#import pyautogui
from PIL import Image

# Fancy list for renaming
# Might want to make this a csv so more fonts/ascii styling can be used. 
# TODO: Create CSV so it is easy to add and configure style. 
list_of_iv_numbers = ['⓪', '①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '⑪', '⑫', '⑬', '⑭', '⑮', 'Error']

string_finder = 'findstr' if os.name == 'nt' else 'grep'
move = 'move' if os.name == 'nt' else 'mv'

# If window (nt) then cls else clear (mac / linux)
def clear():
    _ = os.system('cls' if os.name == 'nt' else 'clear')

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
        if not (temp[0] == -1):
            print(f"Attack: {list_of_iv_numbers[temp[0]]}  Defense: {list_of_iv_numbers[temp[1]]}  HP: {list_of_iv_numbers[temp[2]]}")
        else:
            # Check if we can find the menu
            Check_For_Menu()

    Main_Menu()


Main_Menu()