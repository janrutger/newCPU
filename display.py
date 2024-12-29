from tkinter import *
import random
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

        

    def draw_pixel(self, x, y, s):
        x1 =  x * self.scale
        y1 =  y * self.scale 
        x2 = x1 + self.scale
        y2 = y1 + self.scale

        if s == 1:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
        else:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

    def draw_screen(self, memory):
        mem_pointer = 0
        for y in range(self.height):
            for x in  range(self.width):
                self.draw_pixel(x, y, memory[mem_pointer])
                mem_pointer = mem_pointer + 1
                self.display.update()
        

    def refresh(self):
        self.display.update()
        



if __name__ == "__main__":
    
    memory = []
    for y in range(32):
        for x in range(64):
            memory.append(random.randint(0, 1))

    display = Display(64, 32, 10)
    display.draw_screen(memory)

    # input = [(15,10), (40,15)]
    # for pixel in input:
    #     display.draw_pixel(pixel[0], pixel[1], 1)
    #     display.refresh()
    
    while True:
        display.refresh()

