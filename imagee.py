#!/usr/bin/python

import os,sys
from PIL import Image
img = Image.open("leel.jpg")
img = img.convert("RGBA")
pic = img.load()
datas = img.getdata()

#difference function to calculate between two pixels
def difference(item, item2):
	reddif = abs(item[0] - item2[0])
	greendif = abs(item[1] - item2[1])
	bluedif = abs(item[2] - item2[2])
	maxdif = max(reddif, greendif, bluedif)
	return maxdif

#check if pixel is in bounds of image
def inBounds(x, y, width, height):
	if x < 0 or x > width-1 or y < 0 or y > height-1:
		return False
	return True

#get list of neighbors in a 5 x 5 block
def getSquareNeighbors(x, y, width, height):
	ans = []
	for i in range(x, x+6):
		for j in range(y, y+6):
			if(inBounds(i, j, width, height)):
				ans.append(newPic[i, j])
	return ans

#get list of specifically adjacent neighbors
def getSpecNeighbors(x, y, width, height):
	ans = []
	if(inBounds(x + 1, y, width, height)):
		ans.append(newPic[x + 1, y])
	if(inBounds(x, y + 1, width, height)):
		ans.append(newPic[x, y + 1])
	if(inBounds(x - 1, y, width, height)):
		ans.append(newPic[x - 1, y])
	if(inBounds(x, y - 1, width, height)):
		ans.append(newPic[x, y - 1])
	return ans

#get list of surrounding pixels
def getNeighbors(x, y, width, height):
	ans = []
	for i in range(x-1, x+2):
		for j in range(y-1, y+2):
			if(inBounds(i, j, width, height)):
				ans.append(pic[i, j])
	return ans


newData = []
threshold = 10
width, height = img.size

newImage = Image.new("RGBA", img.size)

#change to black and white based on difference and threshold
for i in range(width):
    for j in range(height):
		temp = getNeighbors(i, j, width, height)
		found = False
		for n in range(0, len(temp)):
			diff = difference(pic[i, j], temp[n])
			if diff > threshold:
				newImage.putpixel((i, j), (0, 0, 0, 255))
				found = True
				break
		if not found:
			newImage.putpixel((i, j), (255, 255, 255, 255))

#take out small colored pixels
tempVar = False
newPic = newImage.load()
for i in range(width):
	for j in range(height):	
		temp = getSpecNeighbors(i, j, width, height)
		for n in range(len(temp)):
			if newPic[i, j][1] == temp[n][1]:
				tempVar = True
		if not tempVar:
			newImage.putpixel((i, j), (255, 255, 255, 255))
		tempVar = False

#take out random splotches of black
for i in range(0, width, 5):
	for j in range(0, height, 5):	
		count = 0
		temp2 = getSquareNeighbors(i, j, width, height)
		for n in range(len(temp2)):
			if temp2[n][1] == 0:
				count+=1
		if count <= 15:
			for q in range(i, i+6):
				for a in range(j, j+6):
					if(inBounds(q, a, width, height)):
						newImage.putpixel((q, a), (255, 255, 255, 255))

size = width *2, height *2
newImage.thumbnail(size, Image.ANTIALIAS)
newImage.show()
newImage.save("hahah", "PNG")

