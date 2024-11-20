class IOmanagement:
    def __init__(self, myASCCI, ioregister, kbd, plotbuff):
        self.ioregister = ioregister
        self.plotbuff = plotbuff
        self.kbdbuff  = kbd
        self.myASCCI  = myASCCI
        self.terminalmode = None

    def do(self, IOaddress):
        if IOaddress == False:      # No device selected
            return(False)
        
        elif IOaddress == 1:        # input device: kbd = 1
            if self.kbdbuff.do("size") == 0:
                #self.kbdbuff.do("write", self.keyboard())
                self.keyboard()

            self.ioregister.do("write", self.kbdbuff.do("read"))
            print("Devicebuffer        :",IOaddress, self.kbdbuff.dump())
            return(True)
        
        elif IOaddress == 2:        # Plotter device = 2
            self.plotbuff.do("write", self.ioregister.do("read"))
            print("Devicebuffer        :",IOaddress, self.plotbuff.do("size"), self.plotbuff.dump())
            return(False)
        
        elif IOaddress == 3:        # terminal device = 3
            #self.plotbuff.do("write", self.ioregister.do("read"))
            print("terminal            :",IOaddress, self.ioregister.do("read"))
            self.terminal(self.ioregister.do("read"))
            return(False)
        else:                       #Wrong device 
            exit("ERROR: invalid IO device")

    def keyboard(self):
        inputChars = list(input("I need input> "))
        #print(inputChars)
        for char in inputChars:
            if char in self.myASCCI.keys():
                if char.isnumeric():
                    self.kbdbuff.do("write", 0)
                    self.kbdbuff.do("write", self.myASCCI[str(char)])
                else:
                    self.kbdbuff.do("write", 1)
                    self.kbdbuff.do("write", self.myASCCI[char])
            else:
                self.kbdbuff.do("write", 1)
                self.kbdbuff.do("write", self.myASCCI["#"]) 

        self.kbdbuff.do("write", 1)
        self.kbdbuff.do("write", self.myASCCI["null"])  

    def terminal(self, inputvalue):
        if self.terminalmode == None:
            self.terminalmode = inputvalue
        else:
            if self.terminalmode == 0:
                print(inputvalue)
            elif self.terminalmode == 1:
                pass
            else:
                exit("ERROR: invalid Terminal mode")
            self.terminalmode = None
        

        return()
        