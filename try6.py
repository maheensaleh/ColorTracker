import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from PIL import Image, ImageTk
from collections import deque
import numpy as np
import argparse
import imutils

selected = None
clicked = 0
Lower = (0, 0, 0)
Upper = (0, 255, 255)
track_color = None

colors={"red":(0,0,255),"green":(0,255,0),"blue":(255,0,0),"yellow":(8,255,251)}


class App:

    def __init__(self, window, window_title, video_source=0):
        self.window = window
        # self.window.configure(background="light pink")
        self.window.title(window_title)
        self.video_source = video_source
        self.switch = False
        self.sx, self.sy = None, None

        name = tkinter.Label(self.window, text="Ball Tracker", font=('Comic Sans MS bold', 35),  fg="blue")
        name.place(x = 600, y= 10)

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=2000, height=600)
        self.canvas.place(x=50,y=85+50)

        # # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 12
        self.update()
        # to hide the balck bars above and below video dispaly
        self.hide1 = tkinter.Label(self.window,width = 500,text ="to hide", font=('Comic Sans MS bold', 38),fg = "#f0f0f0",bg="#f0f0f0")
        self.hide1.place(x =50, y= 85+50)

        self.hide2 = tkinter.Label(self.window,width = 500,text ="to hide", font=('Comic Sans MS bold', 38),fg = "#f0f0f0",bg="#f0f0f0")
        self.hide2.place(x =50, y= 610+50)

        self.detail = tkinter.Label(self.window, text="Try out this interesting tool to track things \n in the color you want !! ",
                               font=('Comic Sans MS bold', 20))
        self.detail.place(x= 200 , y= 110)

        self.tell = tkinter.Label(self.window, text="Just select your color below\n and start tracking it !", font=('Comic Sans MS bold', 20))
        self.tell.place(x=930, y=110)

        self.start = tkinter.Button(self.window, text="Start \nTracking", font=('Comic Sans MS bold', 17), bg="light grey",
                               height=2,width=10,
                               command=self.start_tracking, relief="raised")
        self.start.place(x=850+60, y=550)

        #displaying vdieo display border
        self.img = ImageTk.PhotoImage(Image.open("bh.png"))
        self.imglabel = tkinter.Label(self.window, image=self.img,bg = "#f0f0f0")
        self.imglabel.place(x = 45 ,y = 210)

        self.imglabel2 = tkinter.Label(self.window, image=self.img)
        self.imglabel2.place(x = 45 ,y = 650)

        self.img2 = ImageTk.PhotoImage(Image.open("bv.png"))
        self.imglabel3 = tkinter.Label(self.window, image=self.img2)
        self.imglabel3.place(x = 45 ,y = 210)

        self.imglabel3 = tkinter.Label(self.window, image=self.img2)
        self.imglabel3.place(x = 45+800 ,y = 210)

        self.stop_button = tkinter.Button(self.window, text="Stop \nTracking", font=('Comic Sans MS bold', 17), bg="light grey",
                               height=2,width=10,
                               command=self.stop_tracking, relief="raised")
        self.stop_button.place(x=1050+60, y=550)

        self.this_selected = tkinter.Label(self.window, text="selected", font=('Comic Sans MS bold', 13))

        # button display

        #   for red
        r_pic = Image.open("red.JPG")
        r__pic = ImageTk.PhotoImage(r_pic)
        # label with image
        red = tkinter.Label(self.window, image=r__pic)
        red.place(x=850+60, y=250)
        # bind click event to image
        red.bind('<Button-1>', self.get_red)

        #   for green

        g_pic = Image.open("green.JPG")
        g__pic = ImageTk.PhotoImage(g_pic)
        # label with image
        green = tkinter.Label(self.window, image=g__pic)
        green.place(x=1100+60, y=250)
        # bind click event to image
        green.bind('<Button-1>', self.get_green)

        # for blue

        b_pic = Image.open("blue.JPG")
        b__pic = ImageTk.PhotoImage(b_pic)
        # label with image
        blue = tkinter.Label(self.window, image=b__pic)
        blue.place(x=850+60, y=400)
        # bind click event to image
        blue.bind('<Button-1>', self.get_blue)

        # for yellow

        y_pic = Image.open("yellow.JPG")
        y__pic = ImageTk.PhotoImage(y_pic)
        # label with image
        yellow = tkinter.Label(self.window, image=y__pic)
        yellow.place(x=1100+60, y=400)
        # bind click event to image
        yellow.bind('<Button-1>', self.get_yellow)

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:

            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)

    def get_red(self, event=None):
        global selected
        self.switch = True
        selected = "red"
        self.sx, self.sy = 860+60, 220
        self.this_selected.place(x=self.sx, y=self.sy)

    def get_blue(self, event=None):
        global selected
        self.switch = True
        selected = "blue"
        self.sx, self.sy = 860+60, 370
        self.this_selected.place(x=self.sx, y=self.sy)


    def get_green(self, event=None):
        global selected
        self.switch = True
        selected = "green"
        self.sx, self.sy = 1120+60, 220
        self.this_selected.place(x=self.sx, y=self.sy)


    def get_yellow(self, event=None):
        global selected, Lower, Upper
        selected = "yellow"
        self.sx, self.sy = 1120+60, 370
        self.this_selected.place(x=self.sx, y=self.sy)

    def start_tracking(self):
        global selected,Lower,Upper,clicked,track_color,stop
        stop = False

        clicked=1
        if selected != None:
            print(selected)
            tracking_color = tkinter.Label(self.window, text="                    Tracking ....                ", font=('Comic Sans MS bold', 13),
                                           fg=selected
                                           , bg="light grey", relief="raised")
            tracking_color.place(x=850+60, y=510)

            if clicked==1:
                track_color = colors[selected]

                clicked = 0
                # changing the color range:
                if selected == "red":
                    Lower =(0,120,100)
                    Upper =  (10, 255,255)
                elif selected == "blue":
                    Lower = (110,100,100)
                    Upper = (130,255,255)
                elif selected == "green":
                    Lower = (50, 100,100)
                    Upper = (70, 255, 255)
                elif selected == "yellow":
                    Lower = (20, 100, 100)
                    Upper = (40, 255, 255)

        else:
            tracking_color = tkinter.Label(self.window, text="-             No Color Selected            -", font=('Comic Sans MS bold', 13),
                                           fg="black", bg="light grey")
            print("no selected")
            tracking_color.place(x=850+60, y=510)

        print(selected)

    def stop_tracking(self):
        global track_color
        track_color = None
        no_selected = tkinter.Label(self.window, text="-             No Color Selected             -", font=('Comic Sans MS bold', 13),
                                       fg="black", bg="light grey")
        print("no selected")
        no_selected.place(x=850+60, y=510)


# this class handles the video capture and tracks the color
class MyVideoCapture:

        def __init__(self, video_source=0):
            self.ap = argparse.ArgumentParser()

            self.ap.add_argument("-v", "--video",
                            help="path to the (optional) video file")
            self.ap.add_argument("-b", "--buffer", type=int, default=64,
                            help="max buffer size")
            self.args = vars(self.ap.parse_args())
            self.pts = deque(maxlen=self.args["buffer"])

            self.vs = cv2.VideoCapture(0)

        def get_frame(self):
            global Lower,Upper,track_color,selected

            # grab the current frame
            ret, frame = self.vs.read()
            # handle the frame from VideoCapture or VideoStream
            frame = frame[1] if self.args.get("video", False) else frame

            # resize the frame, blur it, and convert it to the HSV
            frame = imutils.resize(frame, width=800)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            # construct a mask for the color then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, Lower, Upper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None

            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # update the points queue
            self.pts.appendleft(center)

            # loop over the set of tracked points
            for i in range(1, len(self.pts)):

                if self.pts[i - 1] is None or self.pts[i] is None:
                    continue

                thickness = int(np.sqrt(self.args["buffer"] / float(i + 1)) * 2.5)
                if selected is not None and track_color is not None:
                    cv2.line(frame, self.pts[i - 1], self.pts[i], track_color, thickness)
                else:
                    pass

            frame = cv2.flip(frame, 1)
            return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

App(tkinter.Tk(), "Ball Tracker")
