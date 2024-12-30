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
        print("draw screen")
        self.canvas.delete("all")
        mem_pointer = 0
        for y in range(self.height):
            for x in  range(self.width):
                self.draw_pixel(x, y, memory[mem_pointer])
                mem_pointer = mem_pointer + 1
        self.display.update()
    

        

    def refresh(self):
        self.display.update()
        



if __name__ == "__main__":
    
    sprite1 = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,]
    sprite2 = [1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1]
    sprite3 = [1] *64

    #0xF0, 0x90, 0xF0, 0x90, 0x90, # A
    spriteA = [1,1,1,1,0,0,0,0,
               1,0,0,1,0,0,0,0,
               1,1,1,1,0,0,0,0,
               1,0,0,1,0,0,0,0,
               1,0,0,1,0,0,0,0]

    #0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
    spriteB = [1,1,1,0,0,0,0,0,
               1,0,0,1,0,0,0,0,
               1,1,1,0,0,0,0,0,
               1,0,0,1,0,0,0,0,
               1,1,1,0,0,0,0,0]
    
    #0xF0, 0x80, 0x80, 0x80, 0xF0, # C
    spriteC = [1,1,1,1,0,0,0,0,
               1,0,0,0,0,0,0,0,
               1,0,0,0,0,0,0,0,
               1,0,0,0,0,0,0,0,
               1,1,1,1,0,0,0,0]


	#0xE0, 0x90, 0x90, 0x90, 0xE0, # D
    spriteD = [1,1,1,0,0,0,0,0,
               1,0,0,1,0,0,0,0,
               1,0,0,1,0,0,0,0,
               1,0,0,1,0,0,0,0,
               1,1,1,0,0,0,0,0]
        
    #'W': [0x9, 0x9, 0xf, 0xf, 0x9],
    spriteW = [1,0,0,1,0,0,0,0,
               1,0,0,1,0,0,0,0,
               1,1,1,1,0,0,0,0,
               1,1,1,1,0,0,0,0,
               1,0,0,1,0,0,0,0]

    def fill_mem():
        memory = []
        for _ in range(32*64):
            memory.append(random.randint(0, 1))
        return(memory)
    
    def clear_mem():
        memory = [0] * (32*64)
        return(memory)
    
    def draw_mem(x, y, sprite, memory, rows):
        print("Draw Sprite in memory")
        for i in range(rows):
            mem_pointer = (y+i) * 64 + x
            for n in range(8):
                memory[mem_pointer+n] = sprite[n + (i*8)]
        return(memory)






    display = Display(64, 32, 10)
    mem = fill_mem()
    display.draw_screen(mem)
    # mem = clear_mem()
    # display.draw_screen(mem)
    # mem = draw_mem(10,10,sprite1,mem,8)
    # display.draw_screen(mem)
    # mem = draw_mem(10,10,sprite2,mem,8)
    # display.draw_screen(mem)
    # mem = draw_mem(10,10,sprite3,mem,8)
    # display.draw_screen(mem)

    mem = clear_mem()
    #display.draw_screen(mem)
    mem = draw_mem(10,10,spriteA,mem,5)
    display.draw_screen(mem)
    mem = draw_mem(15,10,spriteB,mem,5)
    display.draw_screen(mem)
    mem = draw_mem(10,16,spriteC,mem,5)
    # display.draw_screen(mem)
    mem = draw_mem(20,10,spriteW,mem,5)
    mem = draw_mem(16,16,spriteD,mem,5)
    display.draw_screen(mem)
    
    while True:
        display.refresh()
        time.sleep(0.001)


