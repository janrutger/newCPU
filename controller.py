from register import Register
from memory import Memory

class controller:
    def __init__(self, PC: Register, IX: Register, STACK: Register, regA: Register, regB: Register, regR: Register, regIO: Register, memory: Memory):
        self.memory = memory

        self.IR = None
        self.halt = True
        self.zero = False
        self.IOadr = False

        self.PC = PC
        self.IX = IX
        self.STACK = STACK
        self.STACK.write(self.memory.MEMmax())

        self.regA  = regA
        self.regB  = regB
        self.regR  = regR
        self.regIO = regIO

    def fatalerror(self, text):
        print("FATAL:  " + text)
        self.halt = True


    def do(self, pc=None, INint=False):
        # Handle the input status bits
        if pc and self.halt:
            self.PC.write(pc)
            self.halt = False
        elif self.halt: # start at 0 when pc=None
            self.PC.read()
            self.halt = False

        if INint:
            self.regA.write(self.regIO.read())

        self.IOadr = False

        # fetch
        self.IR = self.memory.read(self.PC.read())
        #self.PC.do(self.PC.do("inc"))
        self.PC.inc()

        #decode & execute
        match self.IR[0]:
            case "lda":
                self.regA.write(self.IR[1])
            case "ldb":
                self.regB.write(self.IR[1])

            case "maa":
                self.regA.write(self.IR[1])
            case "mab":
                self.regB.write(self.IR[1])

            case "sto":
                self.memory.write(self.IR[1], self.regR.read())
            case "sta":
                self.memory.write(self.IR[1], self.regA.read())
            case "stb":
                self.memory.write(self.IR[1], self.regB.read())
            case "lma":
                self.regA.write(self.memory.read(self.IR[1]))
            case "lmb":
                self.regB.write(self.memory.read(self.IR[1]))

            case "lix":
                self.IX.write(self.memory.read(self.IR[1]))
            case "iix":
                self.IX.write(self.memory.read(self.IR[1]))
                # self.IX.do("inc")
                self.memory.write(self.IR[1], self.IX.read() + 1)
            case "dix":
                self.IX.write(self.memory.read(self.IR[1]))
                self.IX.dec()
                self.memory.write(self.IR[1], self.IX.read())

            case "idx":
                self.IX.write(self.regB.read())
            case "stx":
                self.memory.write(self.IR[1] + self.IX.read(), self.regR.read())
               # self.regR.do(self.IX.do())
            case "lxa":
                self.regA.write(self.memory.read(self.IR[1] + self.IX.read()))
            case "lxb":
                self.regB.write(self.memory.read(self.IR[1] + self.IX.read()))

            case "push":
                self.memory.write(self.STACK.read(), self.regR.read())
                self.STACK.write(self.STACK.dec())
            case "pop":
                self.STACK.write(self.STACK.inc())
                self.regA.write(self.memory.read(self.STACK.read()))

            case "call":
                self.memory.write(self.STACK.read(), self.PC.read())
                self.STACK.write( self.STACK.dec())
                self.PC.write(self.IR[1])
            case "ret":
                self.STACK.write(self.STACK.inc())
                self.PC.write(self.memory.read(self.STACK.read()))


            case "add":
                self.regR.write(self.regA.read() + self.regB.read())
                self.regA.write(self.regR.read())
            case "sub":
                self.regR.write(self.regA.read() - self.regB.read())
                self.regA.write(self.regR.read())
            case "mul":
                self.regR.write(self.regA.read() * self.regB.read())
                self.regA.write(self.regR.read())
            case "div":
                self.regR.write(self.regA.read() // self.regB.read())
                self.regA.write(self.regR.read())

            case "jmp":
                self.PC.write(self.IR[1])
            case "jmpx":
                self.PC.write(self.memory.read(self.IR[1] + self.IX.read()))

            case "test":
                self.regR.write(1)
                if self.IR[1] == 'eq':
                    if self.regA.read() == self.regB.read():
                        self.regR.write(0)
                elif self.IR[1] == 'gt':
                    if self.regA.read() > self.regB.read():
                        self.regR.write(0)
                elif self.IR[1] == 'z':
                    if self.regA.read() == 0:
                        self.regR.write(0)
                else:
                    self.fatalerror("TEST ERROR, wrong  place to be")

            case "ise":
                self.regR.write(1)
                if self.memory.read(self.regA.read()) == self.memory.read(self.regB.read()):
                    self.regR.write(0)
            case "isz":
                self.regR.write(1)
                if self.memory.read(self.regA.read()) == 0:
                    self.regR.write(0)

            case "jmpt":
                if self.zero == True:
                    self.PC.write(self.IR[1])
            case "jmpf":
                if self.zero == False:
                    self.PC.write(self.IR[1])

            case "skip":
                if self.zero == False:
                    self.PC.inc()

            case "out":
                self.regIO.write(self.regR.read())
                self.IOadr = self.IR[1]
            case "in":
                self.IOadr = self.IR[1]

            case "inc":
                if self.IR[1] == 'a':
                    self.regA.write(self.regA.read() + 1)
                elif self.IR[1] == 'b':
                    self.regB.write(self.regB.read() + 1)
                elif self.IR[1] == 'x':
                    self.IX.write(self.IX.read() + 1)
                else:
                    self.fatalerror("INC ERROR, invalid register")

            case "dec":
                if self.IR[1] == 'a':
                    self.regA.write(self.regA.read() - 1)
                elif self.IR[1] == 'b':
                    self.regB.write(self.regB.read() - 1)
                elif self.IR[1] == 'x':
                    self.IX.write(self.IX.read() - 1)
                else:
                    self.fatalerror("DEC ERROR, invalid register")


            case "halt":
                self.halt = True
                self.PC.write(self.PC.dec())
            case _:
                self.fatalerror("INTRUCTION ERROR, wrong  place to be : " + self.IR[1])

        #set controlbits
        if self.regR.read() == 0:
            self.zero = True
        else:
            self.zero = False

        if self.halt == True:
            print("Instruction register: " + self.IR[0])
            print("Program counter     : " + str(self.PC.read()))
            print("Stack pointer       : " + str(self.STACK.read()))
            print("Index register      : " + str(self.IX.read()))
            print("Register A          : " + str(self.regA.read()))
            print("Register B          : " + str(self.regB.read()))
            print("Result register     : " + str(self.regR.read()))
            print("IO register         : " + str(self.regIO.read()))
            print(self.halt, self.zero, self.IOadr, INint)
            print(self.memory.dump())


        return(self.halt, self.zero, self.IOadr)
