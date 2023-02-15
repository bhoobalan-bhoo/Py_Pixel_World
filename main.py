import cv2
import random
import pandas as pd
from PIL import Image as PilImage
from tkinter import *
from tkinter.colorchooser import askcolor

# Load image
img_path = 'fruitveg.jpeg'
img = cv2.imread(img_path)

# Set up variables for color picker
clicked = False
r = g = b = xpos = ypos = 0

# Load CSV with color names and values
color_data_columns = ["color", "color_name", "hex", "R", "G", "B"]
color_data = pd.read_csv('colors.csv', names=color_data_columns, header=None)

def getColorName(R, G, B):
    # Get the color name closest to the given RGB values
    minimum = 10000
    for i in range(len(color_data)):
        d = abs(R - int(color_data.loc[i, "R"])) + abs(G - int(color_data.loc[i, "G"])) + abs(B - int(color_data.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = color_data.loc[i, "color_name"]
    return cname

def draw_function(event, x, y, flags, param):
    # Event listener for mouse click on the image
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]  # Get the BGR values at the clicked pixel
        b = int(b)
        g = int(g)
        r = int(r)
        print("-----------------------------------------------------------")
        print("Color you have picked from the image:", b, g, r)

# Set up OpenCV window and mouse click event listener
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

# Convert image to RGB and create a PIL Image object
img_pil = PilImage.open(img_path)
img_pil = img_pil.convert("RGB")

while True:
    # Show the OpenCV image window
    cv2.imshow("image", img)

    if clicked:
        # If the user has clicked on the image, open a color picker dialog
        colors = askcolor(title="Color Chooser")[0]
        print("Color you have chosen to change:", colors)

        # Draw a rectangle in the chosen color to indicate the selected color
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Add text with the color name and RGB values to the image
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # If the selected color is light, use black text instead of white
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        # Change pixels in the PIL Image that match the selected color
        width, height = img_pil.size
        for i in range(width):
            for j in range(height):
                pixel_rgb = img_pil.getpixel((i, j))
                if pixel_rgb[0] in list(range(r-70,r+70,1)):
                    if pixel_rgb[1] in list(range(g-70,g+70,1)):
                        if pixel_rgb[2] in list(range(b-70,b+70,1)):
                            img_pil.putpixel((i,j),(int(colors[0]),int(colors[1]),int(colors[2])))
        img_pil.show("image")
        file_name="name_of_the_img"+str(random.randint(100, 999))+".jpg"
        img_pil.save(file_name)
        print("File Has Been Successfully. Named:",file_name)
        print("-----------------------------------------------------------")
        clicked=False
        if cv2.waitKey(20) & 0xFF ==27:
            break
cv2.destroyAllWindows()
