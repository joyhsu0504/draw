from path import Path 
import pyautogui as gui
import time

while True: 

    # wait for file to appear
    d = Path('/Users/rtaori/Dropbox/CalHacks2016/processed')
    while len(d.files()) == 0:
        print('num files:' + str(len(d.files())))
        time.sleep(3)
    img = d.files()[0]

    gui.click(1147, 589) # set home
    time.sleep(1)
    gui.click(70, 52) # hit file
    time.sleep(1)
    gui.click(101, 81) # hit open file
    time.sleep(1)
    gui.click(721, 278) # hit date modified
    time.sleep(1)
    gui.click(721, 278) # hit date modified
    time.sleep(1)
    gui.click(478, 297) # hit first image
    time.sleep(1)
    gui.click(876, 594) # hit open
    time.sleep(25)
    gui.click(191, 53) # hit draw
    time.sleep(1)
    gui.click(200, 81) # hit start
    time.sleep(1)
    gui.click(785, 463) # hit ok
    time.sleep(1)

    # remove the image otherwise next iterations will mess up
    img.remove()