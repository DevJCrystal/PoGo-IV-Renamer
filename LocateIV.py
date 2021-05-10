import cv2 as cv
import numpy as np
from PIL import Image

listOfPixels = [0, 20, 43, 67, 91, 115, 133, 157, 181, 205, 229, 248, 272, 296, 320, 344]

debugging = False

# The y coords
IV_Bar_Pos = [57, 160, 264]

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

    template = cv.imread('images/IV_Zero.png',0)
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

        while x < Max_X:

            # IF not whiteish then IV!
            if (abs(pix[x,y][0] - 226) <= 50 and abs(pix[x,y][1] - 226) <= 50 and abs(pix[x,y][2] - 226) <= 50):
                progress+=0
            else:
                progress+=1
            
            x+=1

        AllTheIV.append(Pixel_To_IV(progress))

    return AllTheIV


# This was just a fun benchmark of 3000+ screenshots from my PoGo and r/pokemongobrag
if debugging:
    import glob
    path = 'unsorted'

    listOfImages = (glob.glob(f"{path}/*.*"))

    for imgFile in listOfImages:
        img = Image.open(imgFile)
        print(Find_The_IVs(img))

# BE WARY NOT TO PASS THIS POINT. DEV RAMBLINGS HAVE BEEN SEEN. UNTOLD HORRORS CAN COME TO ANYONE THAT READS THEM.

# You know.. I was orginally going to try and make this program so I can create a model for machine learning to look at your phone screen.
# I am not sure how Calcy (Is that how it is spelt?) can figure out the IV from just look at the Pokemon in the eyes. I think it is something with CP and weight but
# that sounds like a lot of work. So did the using machine learning for this. I even made a script to automate labeling images. I do have a model but I believe this way makes more sense. 