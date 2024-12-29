from tkinter import Tk, Canvas
import random

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


class DisplayMemory():
    def __init__(self):
        self.memory = [0] * (32*64)

    def fill(self):
        self.memory = []
        for y in range(32):
            for x in range(64):
                self.memory.append(random.randint(0, 1))

    def draw(self,x, y, sprite):
        for i in range(8):
            mem_pointer = (y+i) * 64 + x
            for n in range(8):
                self.memory[mem_pointer+n] = sprite[n + (i*8)]

    def get(self):
        return self.memory


if __name__ == "__main__":

    sprite1 = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,]
    sprite2 = [1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1]
    sprite3 = [1] *64


    display = Display(64, 32, 10)
    mem = DisplayMemory()
    display.draw_screen(mem.get())
    mem = DisplayMemory()
    display.draw_screen(mem.get())
    mem.draw(10,10,sprite1)
    display.draw_screen(mem.get())
    mem.draw(10,10,sprite2)
    display.draw_screen(mem.get())
    mem.draw(10,10,sprite3)
    display.draw_screen(mem.get())

    while True:
        display.refresh()
