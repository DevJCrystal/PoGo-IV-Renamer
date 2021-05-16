import os
import socket

hostname = socket.gethostname()

def Update_Screenshot():
    os.system("adb exec-out screencap -p > phoneScreen.png")

def Pair_Device(ip, port):
    os.system(f'adb pair {ip}:{port}')

def Connect_Device(ip, port):
    os.system(f'adb connect {ip}:{port}')

def Device_Input(action):

    if action.lower() == "back":
        os.popen('adb shell input keyevent 4') # Back
    elif action.lower() == "copy":
        os.popen(f'adb shell input keyevent 278') # Copy
    elif action.lower() == "paste":
        os.popen(f'adb shell input keyevent 279') # Paste

def Get_List_Of_Devices():
    output = os.popen(f'adb devices')
    temp = output.read()
    output.close()

    listOfDevices = []
    temp = temp.split('\n')
    temp[0] = ""
    temp = list(filter(None, temp))

    for device in temp:
        try:
            print(device)
            #int(device[0])
            # Orginally I was going to remove anything after the \t
            # but it is useful to see if a device is offline
            tempDevice = device.split('\n')[0]
            tempDevice2 = tempDevice.split('\t')
            if tempDevice2[1] == 'offline':
                # Connect the device and then add it. 
                #Connect_Device_Menu(tempDevice2[0])
                print('Offline')
            else:
                listOfDevices.append(device.split('\n')[0])

        except ValueError:
            pass

    return listOfDevices

def Click(x, y):
    os.system(f'adb shell input tap {x} {y}')

def Flask_Page(a,d,h):
    # This fancy crazy call will reuse tabs so it don't create thosands of tabs. 
    os.popen(f'adb shell am start -a "android.intent.action.VIEW" -d "http://{hostname}:5000/?iv={a}+{d}+{h}" --es "com.android.browser.application_id" "com.android.browser"')
    
def Swipe_Right_To_Left():
    os.popen('adb shell input swipe 500 1000 200 1000 500')

def Swipe_Left_To_Right():
    os.popen('adb shell input swipe 200 1000 500 1000 500')