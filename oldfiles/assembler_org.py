def compile(memsize, progstart):
    ASMfile = []
    file = open("program.asm", "r")
    for line in file:
        ASMfile.append(line.strip())
    file.close()

    newProgram = []
    for line in ASMfile:
        if line == "" or line[0] == "#" or line[0] == ";":
            pass
        else:
            newProgram.append(line)

    print(newProgram)

    labels = {}
    varcount = 0
    pc = progstart
    vars = memsize // 2


    for line in newProgram:
        if line[0] == "@":
            labels[line] = pc
        elif line[0] == ".":
            _line = line.split()
            labels[_line[1]] = (vars + varcount)
            varcount = varcount + int(_line[2])
        else:
            pc = pc +1

    print(labels)

    pc = progstart
    binProgram = []
    for line in newProgram:
        instruction = line.split()
        #print(instruction)

        if instruction[0][0] in ["@", "."]:
            pass

        elif instruction[0] in ['lda', 'ldb', 'out', 'in']:
            newLine = (pc, instruction[0], int(instruction[1]))
            binProgram.append(newLine)
            pc = pc +1

        elif instruction[0] in ['stx', 'lxa', 'lxb', 'sto', 'sta', 'stb', 'lma', 'lmb']:
            if instruction[1][0] == "$":
                newLine = (pc, instruction[0], int(labels[instruction[1]]))
            else:
                newLine = (pc, instruction[0], int(instruction[1]))
            binProgram.append(newLine)
            pc = pc +1

        elif instruction[0] in ['call', 'jmp', 'jmpt', 'jmpf']:
            if instruction[1] in labels.keys():
                newLine = (pc, instruction[0], labels[instruction[1]])
            else:
                newLine = (pc, instruction[0], int(instruction[1]))
            binProgram.append(newLine)
            pc = pc +1
        elif instruction[0] in [ 'test']:
            newLine = (pc, instruction[0], (instruction[1]))
            binProgram.append(newLine)
            pc = pc +1
        elif instruction[0] in ['halt', 'idx','push', 'pop', 'ret', 'add', 'sub', 'mul', 'div']:
            newLine = (pc, instruction[0], None)
            binProgram.append(newLine)
            pc = pc +1
        else:
            exit("ERROR: Unkown instruction: " + instruction[0])


    return(binProgram)       


