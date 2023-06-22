import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

HOME = os.getenv("HOME")
BASEPATH = HOME + "/nfs/1914-1926/Bowling_Harbour_1914/"
IMG_WIDTH = 720

def resize_image(img, fixed_width):
    height = img.shape[0]
    width = img.shape[1]
    if height == 0:
        print("ERROR: IMAGE SIZE BAD, PROBABLY FAILED IMAGE LOADING")
        return
    aspect = width / height
    img_resize = cv2.resize(img, (IMG_WIDTH, int(IMG_WIDTH / aspect)))
    return img_resize

# NOTE: images are BGR
def display_image(img):
    plt.imshow(img)
    plt.show()

    
def colour_mask(img, lower_colour, upper_colour):
    mask = cv2.inRange(img, lower_colour, upper_colour)
    masked = cv2.bitwise_and(img,img, mask=mask)
    return masked

def colour_filter(img, lower_colour, upper_colour):
    mask = cv2.inRange(img, lower_colour, upper_colour)
    masked = cv2.bitwise_and(img,img, mask=mask)
    result = img - masked
    return result

def colour_histogram(img):
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    plt.show()
    
def detect_lines(img):
    edges = cv2.Canny(img,50,150,apertureSize = 3)
    display_image(edges)
    
    minLineLength=5
    maxLineGap=5
    lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=200,lines=np.array([]), minLineLength=minLineLength,maxLineGap=maxLineGap)

    a,b,c = lines.shape
    for i in range(a):
        cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
        display_image(edges)

red_colour_lower = (164, 98, 91)
red_colour_higher = (195, 141, 141)
black_colour_lower = (0, 0, 0)
black_colour_higher = (120, 120, 120)

test_file = BASEPATH + "1914_007.tif"

print(test_file + " is file, ", os.path.isfile(test_file))
print(os.listdir(BASEPATH))

# read core image
img = cv2.imread(test_file)
red_filter = colour_filter(img, red_colour_lower, red_colour_higher)
black_filter = colour_filter(img, black_colour_lower, black_colour_higher)

# display_image(red_filter)
# display_image(black_filter)
# display_image(img)
detect_lines(img)




