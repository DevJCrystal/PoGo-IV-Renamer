import PoGoCLI
from PIL import Image
import pyautogui as pg

def Find_Button(button):

    PoGoCLI.Update_Screenshot()

    img = Image.open('phoneScreen.png')

    # First Find Menu Button
    base_width = 1080
    wpercent = (base_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    pil_image = img.resize((base_width,hsize), Image.ANTIALIAS)

    button_pos = pg.locate(button, pil_image, grayscale = False, confidence = .7)

    button_center = pg.center(button_pos)

    button_x, button_y = button_center

    # We downsized wpercent
    # Now we got to correct for that
    corrected_x = button_x / wpercent
    corrected_y = button_y / wpercent

    PoGoCLI.Click(corrected_x, corrected_y)

    return (corrected_x, corrected_y)