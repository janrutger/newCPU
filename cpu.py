from register import Register
from buffer import Buffer
from memory import Memory
from controller import controller
from IOmanagement import IOmanagement
from assembler import compile
from stringtable import maketable


#####################################
pc    = Register()
ix    = Register()
sp    = Register()
regA  = Register()
regB  = Register()
regR  = Register()
regIO = Register()

plotter = Buffer("plotter")
kbd     = Buffer("kbd")

myASCII = maketable()

memsize  = 128 * 5
MEMORY   = Memory(memsize)

CONTROLLER = controller(pc, ix, sp, regA, regB, regR, regIO, MEMORY)
IO_MANAGER = IOmanagement(myASCII, regIO, kbd, plotter)

loaderstart = 0
progstart   = loaderstart +64

varaddress  = memsize -192
symbols     = {}
files       = [('loader.asm', loaderstart), ('program2.asm', progstart)]

for file in files:
    bin, varaddress, symbols = compile(file[0], file[1], varaddress, symbols, myASCII)
    for line in bin:
        # print(line)
        MEMORY.write(line[0], line[1])


halted = False
IOack  = False

while not halted:
    halted, zero, IOadr = CONTROLLER.do(progstart, IOack)
    IOack = IO_MANAGER.do(IOadr)
