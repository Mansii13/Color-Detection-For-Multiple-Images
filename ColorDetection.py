#I Build The Project Based On Color Detection 
#In My Project To Detect Color Name For Sequentially Change Image
#Author 19BCE510

import numpy as np 
import pandas as pd
import tkinter
import cv2
import matplotlib.pyplot as plt
from PIL import ImageTk

window = tkinter.Tk()
window.title("Color Detection") # title for open window
window.configure(background="black") # set black background on open window
	
A = ImageTk.PhotoImage(file="1.jpg")
B = ImageTk.PhotoImage(file="2.jpg")
C = ImageTk.PhotoImage(file="3.jpg")
D = ImageTk.PhotoImage(file="4.jpg")
E = ImageTk.PhotoImage(file="5.jpeg")

listOfImages = np.array([A,B,C,D,E]) # collection of images with use of Pillow
Images = ["1.jpg","2.jpg","3.jpg","4.jpg","5.jpeg"] # name of all images to open image sequentially

ln=len(Images)
i=0
count=0
CodeR = []
CodeG = []
CodeB = []

def changeImage():
    global listOfImages,i
    im = listOfImages[i] # to display image on label with use of PIL of ImageTk
    lblImg.configure(image=im) # particular change image display on label 
	
def mouseClick(event):
	global i,count,CodeB,CodeG,CodeR
	im = Images[i] 
	img = cv2.imread(im) # open particular image with use of openCV

	width = np.size(img,1) # width of particular image
	height = np.size(img,0) # height of particular image
	
	clicked = False
	r = g = b = xpos = ypos = 0

	index=["color_name","hex","R","G","B"]
	csv = pd.read_csv('ColorDetectName.csv', names=index, header=None)# all value of csv file store into csv variable

	def FindColorName(R,G,B): # this function return color name from csv file depend on r,g,b
		min = 10000
		
		for i in range(len(csv)):
		
			r = int(csv.loc[i,"R"])
			g = int(csv.loc[i,"G"])
			b = int(csv.loc[i,"B"])
			Cname = csv.loc[i,"color_name"]
			result = abs(R-r) + abs(G-g)+ abs(B-b)
			
			if result<=min:
				min = result
				color_name = Cname
		return color_name

	def FindRGB(event, x,y,flag,param): #this function return R,G,B color depend on x and y position
		if event == cv2.EVENT_LBUTTONDBLCLK:
			global b,g,r,xpos,ypos, clicked
			clicked = True
			xpos = x
			ypos = y
			b,g,r = img[y,x]
			b = int(b)
			g = int(g)
			r = int(r)
			return clicked,xpos,ypos,r,g,b
	
	click,x,y,r,g,b = FindRGB(cv2.EVENT_LBUTTONDBLCLK,event.x,event.y,True,'Param')
	
	while(1):
		cv2.imshow("Color Name",img)
		
		if (click):
		
			CodeR.append(r); CodeG.append(g); CodeB.append(b) # this lists store rgb color code to display graph
			
			ColorName = FindColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b) # get color name with use of FindColorName function
			
			cv2.rectangle(img,((width-(width-25)),15), ((width-25),65), (255,255,255), -1) # draw outside rectangle for border of inside rectangle
			cv2.rectangle(img,((width-(width-30)),20), ((width-30),60), (b,g,r), -1) #draw inside rectangle to display color name with its RGB
			
			if(r+g+b>=600):
				cv2.putText(img, ColorName,(40,50),2,0.8,(0,0,0),2,cv2.LINE_AA) #Set Color of the colorname is black when light color occur
			else:
				cv2.putText(img, ColorName,(40,50),2,0.8,(255,255,255),2,cv2.LINE_AA) #Set Color of the colorname is white when dark color occur
				
			click=False
 
		if cv2.waitKey(20) & 0xFF ==27: # press Esc key and close the open image
			break
		
	cv2.destroyAllWindows()
	
	if i!=(ln-1): # this condition use for change image on window
		i=i+1
	else: 
		i=0
	count=count+1
	changeImage()

def quit(): #This function use to distroy(exit) window
	window.destroy()
	
def doNothing(): #This function use to disable close icon
	pass

def ShowGraph():
	global CodeB,CodeG,CodeR,count
	plt.title("Color Detection")
	plt.xlabel("Clickable Count")
	plt.ylabel("Color Code")
	plt.plot(CodeR,label="Red",marker='o', linewidth=3)
	plt.plot(CodeG,label="Green",marker='o', linewidth=3)
	plt.plot(CodeB,label="Blue",marker='o', linewidth=3)
	plt.legend(loc='upper left')
	plt.xticks(np.arange(0,count))
	plt.show()
	
lblImg = tkinter.Label(window,image = A) #This Label Show the image
lblImg.bind("<Button>",mouseClick)
lblImg.grid(row=1,column=1,padx=15,pady=15)

bntGraph = tkinter.Button(window,text="Show Graph",command=ShowGraph,height = 2 , width = 35) #This button use for show graph
bntGraph.grid(row=2,column=1,padx=10,pady=10)

btnExit = tkinter.Button(window,text="Exit",command=quit,height = 2, width = 35)#This button use for exit current window
btnExit.grid(row=3,column=1,padx=10,pady=10)

window.protocol('WM_DELETE_WINDOW',doNothing) #It use to disable the close button
tkinter.mainloop()