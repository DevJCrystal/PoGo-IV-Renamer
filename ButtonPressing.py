import PoGoCLI
from PIL import Image
import pyautogui as pg

def Find_Button(button):

    PoGoCLI.Update_Screenshot()

    img = Image.open('phoneScreen.png')

    orginal_width = img.width
    orginal_height = img.height

    # First Find Menu Button
    base_width = 1080
    wpercent = (base_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    pil_image = img.resize((base_width,hsize), Image.ANTIALIAS)
    pil_image.save('temp.png')

    width_dif = abs(orginal_width - pil_image.width)
    height_dif = abs(orginal_height - pil_image.height)
    print(width_dif)
    print(height_dif)

    button_pos = pg.locate(button, pil_image, grayscale = False, confidence = .8)

    button_center = pg.center(button_pos)

    button_x, button_y = button_center

    PoGoCLI.Click(button_x + width_dif, button_y + height_dif)

    return (button_x + width_dif, button_y)