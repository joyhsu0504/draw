#!/usr/bin/python

import os,sys
from PIL import Image
from PIL import ImageFilter
import numpy as np
from scipy.misc import imsave

img = Image.open("rohan.jpg")
img = img.convert("RGBA")
pic = img.load()
width, height = img.size

test = np.zeros((width, height))

for i in range(width):
	for j in range(height):
		v = pic[i, j][1]
		left_max = 0
		right_max = 0
		top_max = 0
		bottom_max = 0
		for a in range(0, i):
			if abs(pic[a, j][1]) > abs(left_max):
				left_max = pic[a, j][1]
			else:
				break
		for b in range(i, width):
			if abs(pic[b, j][1]) > abs(right_max):
					right_max = pic[b, j][1]
			else:
				break
		for c in range(0, j):
			if abs(pic[i, c][1]) > abs(top_max):
					top_max = pic[i, c][1]
			else:
				break
		for d in range(j, height):
			if abs(pic[i, d][1]) > abs(bottom_max):
				bottom_max = pic[i, d][1]
			else:
				break
		dx = left_max + right_max
		dy = bottom_max + top_max
		v = max(abs(dx), abs(dy))
		test[i][j] = v
imsave('weird1.jpg', test)
