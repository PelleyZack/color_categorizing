#Augmented color_detection that counts the number of colors in the whole picture
#Will impliment the data from the counter into a Matlab graph of some kind 
import cv2
import numpy as np
import pandas as pd
import argparse
import collections 

#argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

#Reading the image with opencv
img = cv2.imread(img_path)

#declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

#Dummy variable that is here to make img.shape allocate the width and height correctly
channel = 0

#empty counter to count all the colors in the picture
cnt = collections.Counter()

#two lists that will take the data from the counter(the colors it finds for one and the amount for the other)
#this is to make working with matlab easier
unique_colors_data = list()
values_for_color_data = list()

#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
#csv = pd.read_csv('colors.csv', names=index, header=None)

#have to use a simplified color csv, will expand after testing
csv = pd.read_csv('simple_colors.csv', names=index, header=None)

#function to calculate minimum distance from all colors and get the most matching color unchanged from origional other then new csv
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

    
#Augmented function that itterates through most pixels of the picture and counts the color at each point
#Currently has to skip 4 pixles every interation in order to avoid overflow in larger pictures
#Will work on making it get to every pixel by either finding a better way to avoid overflow 
def draw_function(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked,channel,cnt
        clicked = True
        xpos, ypos, channel =img.shape
        xpos = int((xpos/4))
        ypos = int((ypos/4))
        for j in range(xpos):
            for k in range(ypos):
                b,g,r = img[((j)*4),(k*4)]
                b = int(b)
                g = int(g)
                r = int(r)
                cnt[getColorName(b,g,r)] +=1
       
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)

#converts the counters data into two simple lists, will be useful when data plotting
def convert_counter(c):
    global unique_colors_data, values_for_color_data
    unique_colors_data = list(c)
    for j in range(len(unique_colors_data)):
            values_for_color_data.append(cnt[unique_colors_data[j]])
    return    unique_colors_data,values_for_color_data


while(1):

    cv2.imshow("image",img)
    if (clicked):
        #currently Just prints out the stored values in cnt, will use this data in later matplots
        
        print(convert_counter(cnt))        
        print(cnt)
        
        clicked=False

       
    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
