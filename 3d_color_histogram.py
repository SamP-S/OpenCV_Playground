import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

HOME = os.getenv("HOME")
BASEPATH = HOME + "/nfs/1914-1926/Bowling_Harbour_1914/"

# NOTE: images are BGR
def display_image(img):
    plt.imshow(img)
    plt.show()
    
def colour_mask(img, lower_colour, upper_colour):
    mask = cv2.inRange(img, lower_colour, upper_colour)
    masked = cv2.bitwise_and(img, img, mask=mask)
    return masked

def sharpen(img):
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    img = cv2.filter2D(img, -1, kernel)
    return img

test_file = BASEPATH + "1914_007.tif"

print(test_file + " is file, ", os.path.isfile(test_file))

# read core image
img = cv2.imread(test_file)

# img = sharpen(img)
display_image(img)


red_lower = np.array([0, 0, 0])
red_higher = np.array([128, 255, 255])
green_lower = np.array([0, 0, 0])
green_higher = np.array([255, 128, 255])
blue_lower = np.array([0, 0, 0])
blue_higher = np.array([255, 255, 128])
low_red_mask = colour_mask(img, red_lower, red_higher)
low_green_mask = colour_mask(img, green_lower, green_higher)
low_blue_mask = colour_mask(img, blue_lower, blue_higher)

red = img - low_red_mask
green = img - low_green_mask
blue = img - low_blue_mask
display_image(red)
display_image(green)
display_image(blue)

exit()

# grey_range = (np.array([255, 255, 255]) * 0.2).astype(int)
# white_higher = np.array([255, 255, 255])
# white_lower = white_higher - grey_range
# black_higher = grey_range
# black_lower = np.array([0, 0, 0])

# white_higher = white_higher.tolist()
# white_lower = white_lower.tolist()
# black_higher = black_higher.tolist()
# black_lower = black_lower.tolist()

# white_mask = colour_mask(img, tuple(white_lower), tuple(white_higher))
# black_mask = colour_mask(img, tuple(black_lower), tuple(black_higher))
# # display_image(white_mask)
# # display_image(black_mask)
# img = img - white_mask
# img = img - black_mask
# display_image(img)

colours, frequency = np.unique(img.reshape(-1, img.shape[-1]), axis=0, return_counts=True)

sort_arr = frequency.argsort()
# sort_arr = np.flip(sort_arr)
colours_sort = colours[sort_arr]
frequency_sort = frequency[sort_arr]

colours_total = len(colours_sort)
print("colours: ", colours_total)
print(colours_sort)
print("frequency: ", colours_total)
print(frequency_sort)

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')

COLOUR_COUNT = 1000
COLOUR_STEP = 4
colours_trunc = colours_sort[:COLOUR_COUNT]
# colours_trunc = colours_sort[::COLOUR_STEP]

x_values = [colour[0] for colour in colours_trunc]
y_values = [colour[1] for colour in colours_trunc]
z_values = [colour[2] for colour in colours_trunc]
scatter_colours = colours_trunc / 255

scatter = ax.scatter(x_values, y_values, z_values, c=scatter_colours)
ax.set_xlabel('R')
ax.set_ylabel('G')
ax.set_zlabel('B')
plt.xlim(0, 255)
plt.ylim(0, 255)
ax.set_zlim(0, 255)

plt.show()
