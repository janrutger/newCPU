from tkinter import *
import time

class Display():
    def __init__(self, width, height, scale):
        self.width  = width
        self.height = height
        self.scale  = scale

        self.display = Tk()

        self.canvas = Canvas(self.display, width=self.width*self.scale, height=self.height*self.scale)
        self.canvas.pack()
        self.canvas.config(bg="black")

    def draw_pixel(self, x, y):
        x1 =  x * self.scale
        y1 =  y * self.scale 
        x2 = x1 + self.scale
        y2 = y1 + self.scale

        self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")

    def refresh(self):
        self.display.update()
        self.display.after(10, self.refresh)  # Schedule the next update after 10ms

if __name__ == "__main__":
    display = Display(64, 32, 10)
    input = [(15,10), (40,15)]
    for pixel in input:
        display.draw_pixel(pixel[0], pixel[1])
    
    display.refresh()  # Start the refresh loop
    #display.display.mainloop()  # Start the Tkinter main loop