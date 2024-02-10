# Program Cyberpunk 2077 Breach Protocol Solver dengan Brute Force

# M. Hanief Fatkhan Nashrullah
# 13522100
# 09/02/2024

# Desc : Sebuah program untuk mencari solusi dari minigame meretas pada permainan video Cyberpunk 2077. 
#        Minigame ini merupakan simulasi peretasan jaringan local dari ICE 
#        (Intrusion Countermeasures Electronics) pada permainan Cyberpunk 2077.

# Import Function
import random
from os import getcwd
from os import system
from os import name
from datetime import datetime


# Kamus Global
# PATH        = [] # 
# ELPATH      = "" #
# OPT_PATH    = "" #
# OPT_TOKEN   = "" #
# ROWS        = 0  #
# COLS        = 0  #
# MAXPOINT    = 0  #
# MATR        = [] #
# SUBSTRING   = [] #
ALPHANUMERIC = {'a','b','c','d','e','f',
                'A','B','C','D','E','F',
                '0','1','2','3','4','5',
                '6','7','8','9','0'}

NUMBER = {'0','1','2','3','4','5','6','7','8','9','0'}

# Fungsi/Prosedur

# Clear
def clear_terminal():
    if name == "nt":
        system('cls')
    else:
        system('clear')

# Validasi String
def string_validation(alphabet,length,text,equalLength):
    words = text.split(" ")
    for word in words:
        if equalLength:
            if len(word)!=length:
                return False
        for letter in word:
            if letter not in alphabet:
                return False
    return True

# Depth First Search
def dfs(r,c,d,m,horizontal):
    global MATR
    global ROWS
    global COLS
    global PATH
    global ELPATH
    global OPT_PATH
    global OPT_TOKEN
    global SUBSTRING
    global MAXPOINT
    # global CHECKEDPATH
    # CHECKEDPATH += 1
    currentPoint = 0
    if d==m:
        return 
    if(r<0 or c<0 or r>=ROWS or c>=COLS or (r,c) in PATH):
        return 
    PATH.append((r,c))
    ELPATH+=MATR[r][c]+" "
    for element in SUBSTRING:
        if element[0] in ELPATH:
            currentPoint += element[1]

    if currentPoint==MAXPOINT:
        if len(PATH)<len(OPT_PATH):
            OPT_PATH = PATH[:]
            OPT_TOKEN = ELPATH
    elif currentPoint>MAXPOINT:
        MAXPOINT -= MAXPOINT
        MAXPOINT += currentPoint
        OPT_PATH = PATH[:]
        OPT_TOKEN = ELPATH
    # print("Checking path-%d" % (CHECKEDPATH))
    # print ("\033[A                             \033[A")
    if horizontal:
        if  c < len(MATR[0])-c :
            for i in range(len(MATR[0])):
                dfs(r,i,d+1,m,False)
        else:        
            for i in range(len(MATR[0])-1,0,-1):
                dfs(r,i,d+1,m,False)
    else:
        if  r < len(MATR)-r :
            for i in range(len(MATR)):
                dfs(i,c,d+1,m,True)
        else:
            for i in range(len(MATR)-1,0,-1):
                dfs(i,c,d+1,m,True)
    PATH.remove((r,c))
    ELPATH = ELPATH[:-3]
    return

# Input via CLI
def cliInput():
    global ALPHANUMERIC
    global NUMBER
    numberOfUniqueToken = int(input("Masukkan jumlah token unik : "))
    tokenString = ""
    while (not string_validation(ALPHANUMERIC,2,tokenString,True)) or (len(tokenString.split(" "))!=numberOfUniqueToken):
        tokenString = str(input("Masukkan token :\n"))
    bufferSize = int(input("Masukkan ukuran buffer : "))

    matrixSize = ""
    while (not string_validation(NUMBER,0,matrixSize,False)) or (len(matrixSize.split(" "))!=2) or (int(matrixSize.split(" ")[0])==0) or (int(matrixSize.split(" ")[1])==0):
        matrixSize = str(input("Masukkan ukuran matriks :\n"))

    matrixRow = int(matrixSize.split(" ")[0])
    matrixCol = int(matrixSize.split(" ")[1])

    numberOfSequence = int(input("Masukkan jumlah sekuens : "))
    sequenceMaxSize = int(input("Masukkan ukuran maksimal sekuens : "))

    tokenArray = tokenString.upper().split(" ")

    matrix = [[0] * matrixCol for i in range(matrixRow)]
    sequence = [["", 0] for _ in range(numberOfSequence)]

    for i in range(numberOfSequence):
        randomnum = random.randint(2, sequenceMaxSize)
        seq = ""
        for j in range(randomnum):
            seq += random.choice(tokenArray) + " "
        sequence[i] = [seq.strip(), 0]
        sequence[i][1] = random.randint(1,100)
        for k in sequence:
            while sequence[i][0] in k[0] and i!=sequence.index(k):
                sequence[i][0] = sequence[i][0][:3]
                sequence[i][0] += random.choice(tokenArray)

    for i in range(matrixRow):
        for j in range(matrixCol):
            matrix[i][j] = tokenArray[random.randint(0,numberOfUniqueToken-1)]

    return matrix,sequence,bufferSize

# Input via file
def fileInput(filename):
    global ALPHANUMERIC
    file = open(getcwd()+"/testcase/"+filename,"r")
    bufferSize = int(file.readline())
    rowAndCol= file.readline().split(" ")
    matrixRow = int(rowAndCol[0])
    matrixCol = int(rowAndCol[1])
    matrix = [[""]*matrixCol]*matrixRow
    for i in range(matrixRow):
        currInput = file.readline().rstrip()
        if len(currInput.split(" "))!=matrixCol or string_validation(ALPHANUMERIC,0,currInput,False)==False:
            print("Input invalid")
        else:
            matrix[i] = currInput.split(" ")
    numberOfSequence = int(file.readline().rstrip())
    sequence = [["", 0] for _ in range(numberOfSequence)]
    for i in range(numberOfSequence):
        sequence[i][0] = file.readline().rstrip()
        sequence[i][1] = int(file.readline().rstrip())
    file.close()
    
    return matrix,sequence,bufferSize

# Display solution
def displaySolution():
    global SUBSTRING
    global ROWS
    global COLS
    global BUFFERSIZE
    global OPT_PATH
    global MAXPOINT
    global OPT_TOKEN
    global RUNTIME

    start=datetime.now()
    print((f"\033[38;5;227mSEQUENCE : \033[0m"))
    for x in SUBSTRING:
        print(f"\033[38;5;227m{x[0]}\033[0m\033[38;5;87m ({x[1]})\033[0m")

    print("")

    for i in range(COLS):
        dfs(0,i,0,BUFFERSIZE,False)

    print((f"\033[38;5;227mMATRIX : \033[0m"))
    for i in range(ROWS):
        for j in range(COLS):
            if (i,j) in OPT_PATH :
                print(f"\033[38;5;87m{MATR[i][j]}\033[0m", end=" ")
            else:
                print(f"\033[38;5;227m{MATR[i][j]}\033[0m", end=" ")
        print("")


    print(f"\033[38;5;87m{MAXPOINT}\033[0m")
    print(f"\033[38;5;87m{OPT_TOKEN}\033[0m")
    for y,x in OPT_PATH:
        print(f"\033[38;5;227m{x+1},{y+1}\033[0m")

    stop = datetime.now()
    RUNTIME = stop-start
    print(f"\033[38;5;87m{round(RUNTIME.total_seconds()*1000)} ms\033[0m")

def saveFile(filename):
    global RUNTIME
    with open(filename, "w") as f:
        print(f"{MAXPOINT}",file=f)
        print(f"{OPT_TOKEN}",file=f)
        for y,x in OPT_PATH:
            print(f"{x+1},{y+1}",file=f)
        print(f"{round(RUNTIME.total_seconds()*1000)} ms",file=f)


# Algoritma Utama    
while True:
    MATR = 0
    PATH =[]
    ELPATH =""
    OPT_PATH = ()
    OPT_TOKEN = ""
    RUNTIME = 0
    # CHECKEDPATH = 0
    clear_terminal()
    print(f"\033[38;5;87mBREACH PROTOCOL SOLVER\033[0m")
    print(f"\033[38;5;227m1.Input Via CLI\033[0m")
    print(f"\033[38;5;227m2.Input via .txt file\033[0m")
    print(f"\033[38;5;227m3.Exit\033[0m")
    print(f"\033[38;5;87m>>",end=" ")
    choice = int(input())
    print(f"\033[0m",end="")
    if choice==1:
        clear_terminal()
        MATR,SUBSTRING,BUFFERSIZE = cliInput()
    elif choice==2:
        clear_terminal()
        MATR,SUBSTRING,BUFFERSIZE = fileInput(str("/"+input("Nama File : ")))
    elif choice==3:
        exit()
    else:
        pass
    try:
        ROWS = len(MATR)
        COLS = len(MATR[0])
        MAXPOINT = 0
        clear_terminal()
        displaySolution()
        saveChoice=str(input("Save result? (y/n)"))
        if saveChoice.upper()=="Y":
            saveName = str(input("Enter file name :"))
            saveFile(saveName)
    except:
        pass