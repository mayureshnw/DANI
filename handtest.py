import cv2
import numpy as np
cap = cv2.VideoCapture(0)

while( cap.isOpened() ) :
    # Checks if the capturing is on
    ret,image = cap.read()
    # returns true and value of captured frame
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #converts image to gray scale
    blur = cv2.GaussianBlur(gray,(5,5),0)
    #gaussian blur with pixel radius 5    
    ret,thresh1 = cv2.threshold(blur,110,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) # thresholding values maybe changed
    # Binary thresholds the image, threshold vaue is 110
    contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #finds the contours. the three parameters are input image, contour retrieval methos and approxiamtion method
    #Simple approximation gives only the corners instad of the whole shape

    drawing = np.zeros(image.shape,np.uint8)
    #creates an array of image size and all pixels 0

    max_area=0
   
    for i in range(len(contours)):
            cnt=contours[i]
                                               # remove this print. Debug stuff
            area = cv2.contourArea(cnt)
            #gives the area of each contour
            if(area>max_area):
                max_area=area
                ci=i
                #gives the i value when area is maximum
    cnt=contours[ci]
    hull = cv2.convexHull(cnt)
    #finds convex hull of all the points representing each
    moments = cv2.moments(cnt)
    # finds the moments of the given contours
    if moments['m00']!=0:
                # 'm00' generally represnts the area when referring to binary images.
                # cx,cy are coordinates of the centroid of the contours
                cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                cy = int(moments['m01']/moments['m00']) # cy = M01/M00
              
    #below the null matrix is modified to add contours and a circle at the median
    centr=(cx,cy)       
    cv2.circle(image,centr,5,[0,0,255],2)       
    cv2.drawContours(drawing,[cnt],0,(0,255,0),2)   # green for contours
    cv2.drawContours(drawing,[hull],0,(0,0,255),2)  #red for the convex hull
          
    # a polygon curve is approximated with specified precision.      
    cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)  # value can be changed for calibration
    
    if(1):
               defects = cv2.convexityDefects(cnt,hull)
               mind=0
               maxd=0
               for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    #dist = cv2.pointPolygonTest(cnt,centr,True)
                    cv2.line(image,start,end,[0,255,0],2)
                    
                    cv2.circle(image,far,5,[0,0,255],-1)
               print(i)
               i=0
    cv2.imshow('output',drawing)
    cv2.imshow('input',image)
                
    k = cv2.waitKey(10)
    if k == 27:
        break