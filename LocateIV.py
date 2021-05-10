import cv2 as cv
from PIL import Image

listOfPixels = [0, 20, 43, 67, 91, 115, 133, 157, 181, 205, 229, 248, 272, 296, 320, 344]

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

    # Save the PIL image as temp.png so we can OPEN it again in CV2....
    # I really just want to change it but the person typing this is a caveman.
    # # img = cv.cvtColor(np.asarray(pilImage),cv.COLOR_RGB2BGR) - RIP
    pilImage.save('temp.png')
    img = cv.imread('temp.png', 0)

    template = cv.imread('IV_Zero.png',0)
    w, h = template.shape[::-1]

    method = eval('cv.TM_CCOEFF_NORMED')

    # Apply template Matching
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img,top_left, bottom_right, 0, 2)

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

        # Hmm, I should probably remove congress. 
        # I don't remember what I was going to do with it. 
        progress = 0
        congress = 1000

        while x < Max_X:

            # IF not whiteish then IV!
            if (abs(pix[x,y][0] - 226) <= 50 and abs(pix[x,y][1] - 226) <= 50 and abs(pix[x,y][2] - 226) <= 50):
                congress-=1
            else:
                progress+=1
            
            x+=1

        AllTheIV.append(Pixel_To_IV(progress))

    return AllTheIV


# This was just a fun benchmark of 3000+ screenshots from my PoGO and r/pokemongobrag
# path = 'unsorted'

# listOfImages = (glob.glob(f"{path}/*.*"))

# timeStart = time.time()
# for imgFile in listOfImages:
#     img = Image.open(imgFile)
#     print(Find_The_IVs(img))