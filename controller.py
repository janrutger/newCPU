class controller:
    def __init__(self, PC, IX, STACK, regA, regB, regR, regIO, memory):
        self.memory = memory
    
        self.IR = None
        self.halt = True
        self.zero = False
        self.IOadr = False 

        self.PC = PC
        self.IX = IX
        self.STACK = STACK 
        self.STACK.do("write", self.memory.MEMmax())

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
            self.PC.do("write", pc)
            self.halt = False
        # elif self.halt:  #kan dit weg?
        #     self.PC.do("read", 0)
        #     self.halt = False
        
        if INint:
            self.regA.do("write", self.regIO.do("read"))
        
        self.IOadr = False


        
        # fetch
        self.IR = self.memory.do("read", self.PC.do("read"))
        #self.PC.do("write", self.PC.do("inc"))
        self.PC.do("inc")
        
        #decode & execute
        match self.IR[0]:
            case "lda":
                self.regA.do("write", self.IR[1])
            case "ldb":
                self.regB.do("write", self.IR[1])

            case "maa":
                self.regA.do("write", self.IR[1])
            case "mab":
                self.regB.do("write", self.IR[1])

            case "sto":
                self.memory.do("write", self.IR[1], self.regR.do("read"))
            case "sta":
                self.memory.do("write", self.IR[1], self.regA.do("read"))
            case "stb":
                self.memory.do("write", self.IR[1], self.regB.do("read"))
            case "lma":
                self.regA.do("write", self.memory.do("read", self.IR[1]))
            case "lmb":
                self.regB.do("write", self.memory.do("read", self.IR[1]))

            case "idx":
                self.IX.do("write", self.regB.do("read"))
            case "stx":
                self.memory.do("write", self.IR[1] + self.IX.do("read"), self.regR.do("read"))
            case "lxa":
                self.regA.do("write", self.memory.do("read", self.IR[1] + self.IX.do("read")))
            case "lxb":
                self.regB.do("write", self.memory.do("read", self.IR[1] + self.IX.do("read")))

            case "push":
                self.memory.do("write", self.STACK.do("read"), self.regR.do("read"))
                self.STACK.do("write", self.STACK.do("dec"))
            case "pop":
                self.STACK.do("write", self.STACK.do("inc"))
                self.regA.do("write", self.memory.do("read", self.STACK.do("read")))

            case "call":
                self.memory.do("write", self.STACK.do("read"), self.PC.do("read"))
                self.STACK.do("write",  self.STACK.do("dec"))
                self.PC.do("write", self.IR[1])
            case "ret":
                self.STACK.do("write", self.STACK.do("inc"))
                self.PC.do("write", self.memory.do("read", self.STACK.do("read")))
                

            case "add":
                self.regR.do("write", self.regA.do("read") + self.regB.do("read"))
                self.regA.do("write", self.regR.do("read"))
            case "sub":
                self.regR.do("write", self.regA.do("read") - self.regB.do("read"))
                self.regA.do("write", self.regR.do("read"))
            case "mul":
                self.regR.do("write", self.regA.do("read") * self.regB.do("read"))
                self.regA.do("write", self.regR.do("read"))
            case "div":
                self.regR.do("write", self.regA.do("read") // self.regB.do("read"))
                self.regA.do("write", self.regR.do("read"))

            case "jmp":
                self.PC.do("write", self.IR[1])

            case "test":
                self.regR.do("write", 1)
                if self.IR[1] == 'eq':
                    if self.regA.do("read") == self.regB.do("read"):
                        self.regR.do("write", 0)
                elif self.IR[1] == 'gt':
                    if self.regA.do("read") > self.regB.do("read"):
                        self.regR.do("write", 0)
                elif self.IR[1] == 'z':
                    if self.regA.do("read") == 0:
                        self.regR.do("write", 0)
                else:
                    self.fatalerror("TEST ERROR, wrong  place to be")

            case "ise":
                self.regR.do("write", 1)
                if self.memory.do("read", self.regA.do("read")) == self.memory.do("read", self.regB.do("read")):
                    self.regR.do("write", 0)
            case "isz":
                self.regR.do("write", 1)
                if self.memory.do("read", self.regA.do("read")) == 0:
                    self.regR.do("write", 0)

            case "jmpt":
                if self.zero == True:
                    self.PC.do("write", self.IR[1])
            case "jmpf":
                if self.zero == False:
                    self.PC.do("write", self.IR[1])
        
            case "skip":
                if self.zero == False:
                    self.PC.do("inc")

            case "out":
                self.regIO.do("write", self.regR.do("read"))
                self.IOadr = self.IR[1]
            case "in":
                self.IOadr = self.IR[1]

            case "inc":
                if self.IR[1] == 'a':
                    self.regA.do("write", self.regA.do("read") +1)                          
                elif self.IR[1] == 'b':
                    self.regB.do("write", self.regB.do("read") +1) 
                elif self.IR[1] == 'x':
                    self.IX.do("write", self.IX.do("read") +1) 
                else:
                    self.fatalerror("INC ERROR, invalid register")

            case "dec":
                if self.IR[1] == 'a':
                    self.regA.do("write", self.regA.do("read") -1)                          
                elif self.IR[1] == 'b':
                    self.regB.do("write", self.regB.do("read") -1) 
                elif self.IR[1] == 'x':
                    self.IX.do("write", self.IX.do("read") -1) 
                else:
                    self.fatalerror("DEC ERROR, invalid register")


            case "halt":
                self.halt = True
                self.PC.do("write", self.PC.do("dec"))
            case _:
                self.fatalerror("INTRUCTION ERROR, wrong  place to be : " + self.IR[1])
                
        #set controlbits
        if self.regR.do("read") == 0: 
            self.zero = True
        else:
            self.zero = False

        if self.halt == True:
            print("Instruction register: " + self.IR[0])
            print("Program counter     : " + str(self.PC.do("read")))
            print("Stack pointer       : " + str(self.STACK.do("read")))
            print("Index register      : " + str(self.IX.do("read")))
            print("Register A          : " + str(self.regA.do("read")))
            print("Register B          : " + str(self.regB.do("read")))
            print("Result register     : " + str(self.regR.do("read")))
            print("IO register         : " + str(self.regIO.do("read")))
            print(self.halt, self.zero, self.IOadr, INint)
            print(self.memory.dump())
        

        return(self.halt, self.zero, self.IOadr)
