import cv2 as cv
import numpy as np
from PIL import Image

debugging = False

# Static information
template = cv.imread('images/IV_Zero.png',0)
IV_Bar_Pos = [57, 160, 264] # The y coords once we find the IV bars
listOfPixels = [0, 17, 40, 64, 88, 112, 130, 154, 188, 202, 226, 245, 269, 293, 317, 341] # 0 IV, .., 15 IV

def Pixel_To_IV(pCount):

    abs_diff = lambda list_value : abs(list_value - pCount)
    closest_value = min(listOfPixels, key=abs_diff)

    return listOfPixels.index(closest_value)

def Find_The_IVs(img):

    AllTheIV = []

    basewidth = 1080
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    pilImage = img.resize((basewidth,hsize), Image.ANTIALIAS)

    # Thanks Divakar! https://stackoverflow.com/a/32920586
    adjImg = np.array(pilImage.convert('RGB'))

    w, h = template.shape[::-1]

    # Apply template Matching
    res = cv.matchTemplate(adjImg[:,:,0],template,cv.TM_CCOEFF_NORMED)

    max_loc = cv.minMaxLoc(res)[3]
    top_left = max_loc

    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Set the bounds of the crop
    x = top_left[0]
    y = top_left[1]
    w = abs(top_left[0] - bottom_right[0])
    h = abs(top_left[1] - bottom_right[1])

    IV = (x, y, x + w, y + h)
    ivBar = pilImage.crop(IV)

    # Now we need to measure the color in the
    # This allows us to view the pixels like pixel [x,y]
    pix = ivBar.load()
    Max_X = ivBar.width

    for Bar_pos in IV_Bar_Pos:

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
            AllTheIV.append(-1)
        else:
            AllTheIV.append(Pixel_To_IV(progress))

    return AllTheIV