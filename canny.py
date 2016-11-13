import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from path import Path
import time

d = Path("../../../Dropbox/CalHacks2016/faces/
print(len(d.files()))
while len(d.files()) == 0:
    time.sleep(20)
imgpath = d.files()[0]
img = cv2.imread(imgpath,0)
print(img.shape)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.resize(img, (img.shape[1] / 8, img.shape[0] / 8))
img = img[img.shape[0]/4:3 * img.shape[0]/4].T
img = cv2.GaussianBlur(img, (5, 5), 0)
edges = cv2.Canny(img,50,200)
edges = (255-edges)



cv2.imwrite("../../../Dropbox/CalHacks2016/processed/cannyout.jpg", edges)
imgpath.remove()

