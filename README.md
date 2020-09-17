# ColorTracker
Implemented this Color Tracker tool using a project of :point_right: **PyImagesearch** in which **Adrian** has created a script explaining how to track object on the basis of their color. 
I have added complete GUI to the Python script available at PyImageSearch.com

## Tkinter
Used Python's GUI library **Tkinter** to track four different colors ( red, green , blue, yellow ) one at a time. 

## How To Use:

- The user will first select a color from the given color options and then press **Start Tracking**.
- Then bring an object of the same color and move it infront of the camera .
- As the object is moved , its trail can be seen on the screen.

## Other colors:

A color is detected only if its HSV value matches with the HSV range defined in the code.
To track color other than these, you can get the appropriate HSV range of desired color through its RGB value. The ```find_hsv_ranges.py``` file is made for this purpose.


