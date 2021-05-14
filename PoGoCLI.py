import os

def Update_Screenshot():
    os.system("adb exec-out screencap -p > phoneScreen.png")

def Pair_Device(ip, port):
    os.system(f'adb pair {ip}:{port}')

def Connect_Device(ip, port):
    os.system(f'adb connect {ip}:{port}')

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