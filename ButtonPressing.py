import os
import time
import PoGoCLI
import LocateIV
from PIL import Image
import pyautogui as pg

menu_button = "images/Menu_Button.png"
appraise_button = 'images/Appraise_Button.png'
rename_button = 'images/Rename_Button.png'
name_box = 'images/Name_Box.png'
ok_button = 'images/Ok_Button.png'
okay_button = 'images/Okay_Button.png'

def Find_Button(button):

    PoGoCLI.Update_Screenshot()

    img = Image.open('phoneScreen.png')

    orginal_width = img.width

    # First Find Menu Button
    base_width = 1080
    wpercent = (base_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    pil_image = img.resize((base_width,hsize), Image.ANTIALIAS)

    width_dif = abs(orginal_width - pil_image.width)

    button_pos = pg.locate(button, pil_image, confidence = .7)

    button_center = pg.center(button_pos)

    button_x, button_y = button_center

    PoGoCLI.Click(button_x + width_dif, button_y)

    return (button_x + width_dif, button_y)

def Test():
    Find_Button(menu_button)
    time.sleep(2)
    last_tap = Find_Button(appraise_button)
    time.sleep(2)
    # After Appraise, you need to tap again
    PoGoCLI.Click(last_tap[0], last_tap[1])
    time.sleep(2)
    PoGoCLI.Update_Screenshot()
    temp = LocateIV.Find_The_IVs(Image.open('phoneScreen.png'))
    PoGoCLI.Click(last_tap[0], last_tap[1])
    time.sleep(2)
    os.popen(f'adb shell am start -a android.intent.action.VIEW -d http://192.168.9.109:5000/?iv={temp[0]}-{temp[1]}-{temp[2]}')
    time.sleep(2)
    os.popen(f'adb shell input keyevent 278') # Copy
    time.sleep(2)
    os.popen('adb shell input keyevent 4') # Back
    time.sleep(2)
    Find_Button(rename_button)
    time.sleep(2)
    os.popen(f'adb shell input keyevent 279') # Paste
    time.sleep(2)
    Find_Button(ok_button)
    time.sleep(2)
    Find_Button(okay_button)