import cv2 as cv
import numpy as np
from PIL import Image

debugging = False

# Static information
template = cv.imread('images/IV_Zero.png',0)
iv_bar_pos = [57, 160, 264] # The y coords once we find the IV bars
list_of_pixels = [0, 17, 40, 64, 88, 112, 130, 154, 188, 202, 226, 245, 269, 293, 317, 341] # 0 IV, .., 15 IV

def Pixel_To_IV(pCount):

    abs_diff = lambda list_value : abs(list_value - pCount)
    closest_value = min(list_of_pixels, key = abs_diff)

    return list_of_pixels.index(closest_value)

def Find_The_IVs(img):

    all_the_ivs = []

    base_width = 1080
    wpercent = (base_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    pil_image = img.resize((base_width,hsize), Image.ANTIALIAS)

    # Thanks Divakar! https://stackoverflow.com/a/32920586
    adj_img = np.array(pil_image.convert('RGB'))

    w, h = template.shape[::-1]

    # Apply template Matching
    res = cv.matchTemplate(adj_img[:,:,0],template,cv.TM_CCOEFF_NORMED)

    max_loc = cv.minMaxLoc(res)[3]
    top_left = max_loc

    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Set the bounds of the crop
    x = top_left[0]
    y = top_left[1]
    w = abs(top_left[0] - bottom_right[0])
    h = abs(top_left[1] - bottom_right[1])

    iv = (x, y, x + w, y + h)
    iv_bar = pil_image.crop(iv)

    # Now we need to measure the color in the
    # This allows us to view the pixels like pixel [x,y]
    pix = iv_bar.load()
    Max_X = iv_bar.width

    for Bar_pos in iv_bar_pos:

        x = 0
        y = Bar_pos
        progress = 0
        congress = 0

        while x < Max_X:

            # Non-Perfect Color  | Perfect Color
            # R 225              | R 212
            # G 151              | G 133
            # B 60               | B 124
            # I am checking if the difference is less than 15 because I don't have 
            # enough devices to test to see if something weird happens with colors on other devices.

            if (abs(pix[x,y][0] - 225) < 15 and abs(pix[x,y][1] - 151) < 15 and abs(pix[x,y][2] - 60) < 15) or \
                (abs(pix[x,y][0] - 212) < 15 and abs(pix[x,y][1] - 133) < 15 and abs(pix[x,y][2] - 124) < 15):
                progress+=1
            elif (abs(pix[x,y][0] - 226) < 15 and abs(pix[x,y][1] - 226) < 15 and abs(pix[x,y][2] - 226) < 15):
                congress+=1

            if debugging:
                print(f"[{x},{y}] - {pix[x,y]}")
                
            
            x+=1

        if debugging:
            print(f'Congress: {congress} / Progress: {progress}')

        if progress == 0 and congress < 50:
            # Means IV screen is most likely not up. 
            all_the_ivs.append(-1)
        else:
            all_the_ivs.append(Pixel_To_IV(progress))

    return all_the_ivs