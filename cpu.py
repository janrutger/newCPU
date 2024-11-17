from register import register, buffer
from memory import memory
from controller import controller
from IOmanagement import IOmanagement
from assembler import compile
from stringtable import maketable


#####################################
pc    = register("PC")
ix    = register("IX")
sp    = register("SP")
regA  = register("regA")
regB  = register("regB")
regR  = register("regR")
regIO = register("regIO")

plotter = buffer("plotter")
kbd     = buffer("kbd")

myASCII = maketable()

memsize  = 128 *3
MEMORY   = memory(memsize)

CONTROLLER = controller(pc, ix, sp, regA, regB, regR, regIO, MEMORY)
IO_MANAGER = IOmanagement(myASCII, regIO, kbd, plotter)

loaderstart = 0
progstart   = loaderstart +64

varaddress  = memsize -48
symbols     = {}
files       = [('loader.asm', loaderstart), ('program2.asm', progstart)]

for file in files:
    bin, varaddress, symbols = compile(file[0], file[1], varaddress, symbols, myASCII)
    for line in bin:
        print(line)
        MEMORY.do("write",line[0], line[1])


halted = False
IOack  = False

while not halted:
    halted, zero, IOadr = CONTROLLER.do(progstart, IOack)
    IOack = IO_MANAGER.do(IOadr)





