
def maketable():
    table = {}

    table["null"] = 0
    table["."] = 1
    table["!"] = 2
    table["="] = 3
    table["<"] = 4
    table[">"] = 5
    table["+"] = 6
    table["-"] = 7
    table["*"] = 9

    table["0"] = 10
    table["1"] = 11
    table["2"] = 12
    table["3"] = 13
    table["4"] = 14
    table["5"] = 15  
    table["6"] = 16
    table["7"] = 17
    table["8"] = 18
    table["9"] = 19

    table["$"] = 20
    table["#"] = 21
    table["/"] = 22
    table["%"] = 23

    table[" "] = 30
    table["a"] = 31
    table["b"] = 32
    table["c"] = 33
    table["d"] = 34
    table["e"] = 35
    table["f"] = 36
    table["g"] = 37
    table["h"] = 38


    table["nl"] = 99    # newline

    return table
