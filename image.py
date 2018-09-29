from selenium import webdriver
import numpy as np
import time
import cv2

def screenshot():
    DRIVER = './chromedriver'
    driver = webdriver.Chrome(DRIVER)
    driver.get('http://codebb.cloudapp.net/BaseInvaders.html')
    driver.set_window_size(1920, 1080)
    time.sleep(2)
    screenshot = driver.save_screenshot('image.png')
    driver.quit()

def find_corner():
    im = cv2.imread("/home/dodo/Projects/HackBloomberg2018/image.jpg")
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    _, bin = cv2.threshold(gray,120,255,1) # inverted threshold (light obj on dark bg)
    bin = cv2.dilate(bin, None)  # fill some holes
    bin = cv2.dilate(bin, None)
    bin = cv2.erode(bin, None)   # dilate made our shape larger, revert that
    bin = cv2.erode(bin, None)
    bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    rc = cv2.minAreaRect(contours[0])
    box = cv2.boxPoints(rc)
    for p in box:
        pt = (p[0],p[1])
        cv2.circle(im,pt,5,(200,0,0),2)
        print(p)

def white_contour():
    gray = cv2.imread("image.png", 0)
    th, threshed = cv2.threshold(gray, 100, 255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    _,cnts,_ = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    s1 = 15
    s2 = 20
    xcnts = []
    for cnt in cnts:
        if s1<cv2.contourArea(cnt) <s2:
            xcnts.append(cnt)

    print("Dots number: {}".format(len(xcnts)))

#screenshot()
#white_contour()
find_corner()