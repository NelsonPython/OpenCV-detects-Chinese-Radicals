# USAGE
#python 01_find_chars.py -i characters/bi.png -f y

import numpy as np
import argparse
import imutils
import cv2

print("01_find_chars.py --images images/imageName.png --saveFile y or n")

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "Where is the image file?  path/filename")
ap.add_argument("-f", "--saveFile", help = "Save contour points to file? y or n")
args = vars(ap.parse_args())
outFilename = args["image"].split("/")

image = cv2.imread(args["image"])

# find all the 'black' shapes in the image
lower = np.array([0, 0, 0])
upper = np.array([15, 15, 15])
shapeMask = cv2.inRange(image, lower, upper)

cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

print("I found {} black shapes".format(len(cnts)))
#cv2.imshow("Mask", shapeMask)

# loop over the contours
k=1
for c in cnts:
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.imshow("Image", image)
	cv2.waitKey(0)
	if args["saveFile"] == "y":
		filename = "radicals/processed/"+outFilename[1][:-4]+str(k)
		np.save(filename, c)
		k+=1

