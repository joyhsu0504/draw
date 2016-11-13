#!/usr/bin/python

import os,sys
from PIL import Image
from PIL import ImageFilter
from pprint import pprint as pp
img = Image.open("thisthisthis.jpg")
img = img.convert("RGBA")
pic = img.load()
datas = img.getdata()

C_BLACK = 0
C_WHITE = 1

def _isbw(col):
	c = 240 
	if col[0] < c and col[1] < c and col[2] < c:
		col = C_BLACK
	else:
		col = C_WHITE

	return col

def _getcoord( size, pos ):
	x,y = pos
	w,h = size
	i = (y * w) + x
	return i

def _getbw( imgdata, size, pos ):
	return imgdata[ _getcoord(size,pos) ]

def _setbw( imgdata, size, pos, col ):
	imgdata[ _getcoord(size,pos) ] = col

def _getbwdata( img ):
	d = list(img.getdata())
	for i, c in enumerate(d):
		d[ i ] = _isbw( c )
		# print i, c, d[ i ]
	return d


step1_func = lambda parr: parr[0] + parr[2] + parr[4] > 0 and parr[2] + parr[4] + parr[6] > 0
step2_func = lambda parr: parr[0] + parr[2] + parr[6] > 0 and parr[0] + parr[4] + parr[6] > 0

def do_step(imgdata, size, func):
	was_modified = False
	for j in range(1,h-1):
		for i in range(1,w-1):
			p1 = _getbw( imgdata, size, ( i,  j   ) )
			p2 = _getbw( imgdata, size, ( i,  j-1 ) )
			p3 = _getbw( imgdata, size, ( i+1,j-1 ) )
			p4 = _getbw( imgdata, size, ( i+1,j   ) )
			p5 = _getbw( imgdata, size, ( i+1,j+1 ) )
			p6 = _getbw( imgdata, size, ( i,  j+1 ) )
			p7 = _getbw( imgdata, size, ( i,  j+1 ) )
			p8 = _getbw( imgdata, size, ( i-1,j   ) )
			p9 = _getbw( imgdata, size, ( i-1,j-1 ) )

			A_Val  = (p2 == 0 and p3 == 1) + (p3 == 0 and p4 == 1) 
			A_Val += (p4 == 0 and p5 == 1) + (p5 == 0 and p6 == 1) 
			A_Val += (p6 == 0 and p7 == 1) + (p7 == 0 and p8 == 1)
			A_Val += (p8 == 0 and p9 == 1) + (p9 == 0 and p2 == 1)

			B_Val = sum([p2,p3,p4,p5,p6,p7,p8,p9])
			parr = [p2,p3,p4,p5,p6,p7,p8,p9,p2]

			if p1 == C_BLACK:
				if 2 <= B_Val <= 6:
					if A_Val == 1:
						if func(parr):
							_setbw( imgdata, size, (i,j), C_WHITE )
							was_modified = True
	return (imgdata, was_modified)

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
imageFin = newImage.filter(ImageFilter.SMOOTH_MORE)
imageFin = imageFin.filter(ImageFilter.SMOOTH_MORE)
imageFin = imageFin.filter(ImageFilter.SMOOTH_MORE)
imageFin.thumbnail(size, Image.ANTIALIAS)
			
imageFin = imageFin.filter(ImageFilter.SMOOTH_MORE)
imageFin = imageFin.filter(ImageFilter.SMOOTH_MORE)
#imageFin = imageFin.filter(ImageFilter.BLUR)


#imageFin.show()
imageFin.save("hahah.png")
imageFin.show()

#newImage.show()
#newImage.save("hahah", "PNG")

'''if __name__ == '__main__':
	imgname = 'hahah.png'
	img = Image.open(imgname)
	w, h = img.size

	""" The data is returned as a single array """
	pixels = list(img.getdata())

	# Create black and white pixel bitmap image
	nimg = Image.new('1', img.size, -1 )

	# Convert source image to black and white pixels
	bwdata = _getbwdata( img )

	# Run the algorithm until no further modifications are required
	is_modified = True
	while is_modified:

		bwdata, modified1 = do_step(bwdata,img.size,step1_func)
		bwdata, modified2 = do_step(bwdata,img.size,step2_func)

		is_modified = modified1 | modified2

		print is_modified, modified1, modified2

	# Push the data to image
	nimg.putdata( bwdata )
	nimg.show()

	## And save
	fp = open('.abcd_output.jpg','w')
	nimg.save(fp)
	fp.close()'''

