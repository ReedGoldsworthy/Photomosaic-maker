import pathlib
import json
import os
import math
import random

import numpy as np
import cv2

#Set images_folder to be whatever images folder you want to use
images_folder = "animals"

#set main_image to be the name of the photo you want to use
# change photo type depending on if photo is jpg, png, etc...
main_image = "input"
photo_type = ".jpg"

# define tile size for each sub image
TILE_HEIGHT, TILE_WIDTH = 50, 50

#function to get average color of an rgb numpy matrix
def get_average_color(img):
    
    avg_color = np.average(np.average(img, axis=0), axis=0)
    avg_color = np.around(avg_color, decimals=-1)
    avg_color = tuple(int(i) for i in avg_color)
    return avg_color



# loops through colors and finds the closest rgb tuple to color
def get_closest_color(color, colors):
    cr, cg, cb = color
    min_difference = float("inf")
    closest_color = None
    for c in colors:
        r,g,b = eval(c)
        difference = math.sqrt((r - cr) ** 2 + (g - cg ) ** 2 + (b - cb) ** 2)
        if difference < min_difference:
            min_difference = difference
            closest_color = eval(c)
    return closest_color


#use this if folder of sub images does not contain sub folders
# png_files = []
# for root, dirs, files in os.walk("Humans"):
#     for file in files:
#         if file.lower().endswith(".png") or file.lower().endswith(".jpg"):
#             png_files.append(os.path.join(root, file))




# If cache.json is not present, this section creates a new cache from a dictionary that maps [tuple of rgb values] -------> [a list of file paths with that average rgb value]
if "cache.json" not in os.listdir():

    #gets path of animals folder
    imgs_dir = pathlib.Path(images_folder)

    #creates a list of file paths from the subfolders inside the animals folder
    images = list(imgs_dir.glob("*\\*.jpg"))

    data = {}


    #add each image to dictionary
    for img_path in images:

        #converts photo file path into a numpy matrix storing the images rgb values
        img = cv2.imread(str(img_path))

        #calculates the average color of the rgb matrix
        avg_color = get_average_color(img)

        if str(tuple(avg_color)) in data:
            data[str(tuple(avg_color))].append(str(img_path))
        else:
            data[str(tuple(avg_color))] = [str(img_path)]

    #stores the data dictionary into a cache json file
    with open("cache.json", "w") as file:
        json.dump(data, file, indent=2, sort_keys=True)

    print("finished caching")

# stores the cache into data dictionary
with open("cache.json", "r") as file:
    data = json.load(file)


# converts main image into rgb numpy array
img = cv2.imread(main_image + photo_type)

img_height, img_width, _ = img.shape


# # this section pixelates the main image
# pixel_size = 12

# if img is not None:
#         # Get the original dimensions of the image
#         height, width = img.shape[:2]

#         # Calculate the number of blocks in both dimensions
#         block_count_x = width // pixel_size
#         block_count_y = height // pixel_size

#         # Resize the image to pixelate it
#         small_image = cv2.resize(img, (block_count_x, block_count_y), interpolation=cv2.INTER_NEAREST)

#         # Resize the image back to its original dimensions
#         img = cv2.resize(small_image, (width, height), interpolation=cv2.INTER_NEAREST)


# crop the main image so tiles all fit perfectly
num_tiles_h, num_tiles_w = img_height // TILE_HEIGHT, img_width // TILE_WIDTH

img = img[:TILE_HEIGHT * num_tiles_h, :TILE_WIDTH * num_tiles_w]


# loop through tiles in the main image
for y in range(0, img_height, TILE_HEIGHT):
    for x in range(0, img_width, TILE_WIDTH):

        y0,y1, x0, x1 = y, y + TILE_HEIGHT, x, x + TILE_WIDTH

        try:
            #get average color of tile
            avg_color = get_average_color(img[y0:y1, x0:x1])

            #get the color from our cache closest to to avg tile color
            closest_color = get_closest_color(avg_color, data.keys())

            # select a random photo path from the values in our dictionary for the closest_color value
            i_path = random.choice(data[str(closest_color)])
            i = cv2.imread(i_path)

            #resize sub-image
            i = cv2.resize(i, (TILE_WIDTH, TILE_HEIGHT))

            #replace original images tile with this sub-image
            img[y0:y1, x0:x1] = i

        except Exception:
            continue

        # cv2.imshow(main_image, img)
        # cv2.waitKey(1)

    

cv2.imwrite("output.jpg", img)