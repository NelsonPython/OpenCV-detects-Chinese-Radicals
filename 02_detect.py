'''
Reads an input file and looks for the radicals:  kou, ri, mu
'''

import re
import numpy as np
import argparse
import imutils
import cv2
from os import listdir
from os.path import isfile, join

class bcolors:
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'


def showImage(imgFile, txt):
	''' shows an image along with embedded txt '''
	img = cv2.imread(imgFile)
	cv2.putText(img, txt, (10, 10),
	        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.imshow("Image", img)
	cv2.waitKey(0)
	return img


def findShapes(arr, hanziFilename):
	''' loads the array from the hanzi .npy file
	finds the minimum X,Y and max X,Y (corners of the rectangle containing kou, ri, mu)
	finds white boxes inside the ROI to determine whether the image is kou, ri, or mu
	'''

	roiArr = np.load(arr)

	# if the array has four points then it may be a rectangle
	if len(roiArr) == 4:
		# if the first and last y coordinates are the same then the shape may be a rectangle
		if int(roiArr[0][0][1]) == int(roiArr[-1][0][1]):

			topLeft = np.min(np.min(roiArr, axis=1), axis=0)
			botRite = np.max(np.max(roiArr, axis=1), axis=0)

			# roi = image[minY:maxY, minX:maxX]
			#print("minY:maxY, minX:maxX", topLeft[1], ":", botRite[1], topLeft[0], ":", botRite[0])
			roi = image[int(topLeft[1]):int(botRite[1]), int(topLeft[0]):int(botRite[0])]

			# find white images inside the ROI
			lower = np.array([240, 240, 240])
			upper = np.array([255, 255, 255])
			shapeMask = cv2.inRange(roi, lower, upper)

			# find the contours in the mask
			cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
			    cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)
			if len(cnts) == 1:
			    print(bcolors.OKGREEN + "\nI found kou3 in " + bcolors.OKGREEN, hanziFilename)
			elif len(cnts) == 2:
			    print(bcolors.OKGREEN + "\nI found ri2 in " + bcolors.OKGREEN, hanziFilename)
			elif len(cnts) ==3:
			    print(bcolors.OKGREEN + "\nI found mu4 in " + bcolors.OKGREEN, hanziFilename)
			else:
			    print(bcolors.WARNING + "\nI found a shape with {} contours in {}".format(len(cnts), hanziFilename) + bcolors.WARNING)

			# loop over the contours
			for c in cnts:
			# draw the contour and show it
			    cv2.drawContours(roi, [c], -1, (0, 255, 0), 2)
			    cv2.imshow("Image", roi)
			    cv2.waitKey(0)
	else:
		print(bcolors.FAIL + "\nIn {}, I found shapes that are most likely not rectangles".format(hanziFilename) + bcolors.FAIL)


###################### get input
ap = argparse.ArgumentParser()
ap.add_argument("-c","--hanzi",required=True, help="Hanzi filename")
args = vars(ap.parse_args())

hanziFilename = "characters/"+args["hanzi"]+".png"
hanziArray = "radicals/processed/"+args["hanzi"]+".npy"

image = showImage(hanziFilename,"Hanzi")
#kou3 = showImage("characters/kou3.png", "kou3")
#ri2 = showImage("characters/ri2.png","ri2")
#mu4 = showImage("characters/mu4.png","mu4")

# three different rectangular radicals labeled with pinyin where kou3=mouth, ri2=sun, mu4=eye
kou = np.load("radicals/kou3.npy")
ri = np.load("radicals/ri2.npy")
mu = np.load("radicals/mu4.npy")

# get all the files with the hanzi filename in it
mypath = "/home/pyimagesearch/Chinese/radicals/processed"
arrFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# compare the length of the arrays and determine if the arrays of same length are both rectangles
# look inside each rectangle to determine how many white boxes are inside

for arr in arrFiles:
	if args["hanzi"]  in arr:
		# bi.npy is in bie.npy  "bi" is the first 2 letters of both names so you get a false match
		# thus you must check that the character after the name is a number then you know the filename matches
		isNum = len(args["hanzi"]) + 1
		if arr[isNum] == ".":
			arr = "radicals/processed/"+arr
			findShapes(arr, hanziFilename)

print("\n")
