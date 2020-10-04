import numpy as np



def read(input_file, line):
    file = open(input_file,"r")
    for i in range (line):
        _= file.readline()

    temp=[]
    board=[]
    _,_,temp,_=file.readline().strip("\n").split(";")
    k=0

    for j in range (9):
        line=[]
        for i in range(9):
            if temp[k]==".":
                line.append(0);
            else:
                line.append(int(temp[k]));
            k+=1;
        board.append(line)
    return board

def print_board(board):
    for i in range (9):
        print(board[i]);

def check_row(board,x,y):
    line=board[x].copy();
    line.remove(board[x][y])

    if board[x][y] in line:
        return 0;

    return 1;


def check_column(board, x,y):
    row=[]
    for i in range (9):
        if (i!=x):
            row.append(board[i][y])

    return 0 if board[x][y] in row else 1;


def check_square(board,x,y):
    x_square=int(x//3)
    y_square=int(y//3)
    for i in range(x_square*3,x_square*3+3):
        for j in range(y_square*3,y_square*3+3):
            if board[x][y]==board[i][j] and x!=i and y!=j:
                return 0;
    return 1;

def domain (board,x,y):
    domain=[1,2,3,4,5,6,7,8,9]
    line=[]
    x_square=int(x//3)
    y_square=int(y//3)

    for i in range (9):
            #Appends to list the numbers that are in the same column and row
            if board[x][i]!=0:
                line.append(board[x][i])
            if board[i][y]!=0:
                line.append(board[i][y])

    #Appends to list the numbers that are in the same column and row
    for i in range(x_square*3,x_square*3+3):
        for j in range(y_square*3,y_square*3+3):
            if board[i][j]!=0:
                line.append(board[i][j])

    #If the number already exists in the row, column or square we remove it from the domain
    for i in line:
        if i in domain:
            domain.remove(i)

    return domain


def back_tracking(board,x,y):
    solved=0
    global iterations
    #print_board(board)
    if (x==9):
        return 1

    if (board[x][y]):
        if (y<8):
            solved=back_tracking(board,x,y+1)
        else:
            solved=back_tracking(board,x+1,0)
        return solved

    for i in domain(board,x,y):
        iterations +=1
        board[x][y]=i
        #c1=check_row(board,x,y)
        #c2=check_column(board,x,y)
        #c3=check_square(board,x,y)
        #print(c1,c2,c3,i)
        #if c1 and c2 and c3:
            #print(x,y,i)
        if y<8:
            solved=back_tracking(board,x,y+1)
        else:
            solved=back_tracking(board,x+1,0)
        if solved==1:
            break
        #print(board)
        #print("/n")
        board[x][y]=0

    return solved



input_file= "Sudoku.csv"
start_board = read(input_file,4)
print_board(start_board)

iterations = 0
w, h = 9, 9;
#print(domain(start_board,0,2))
#print(check_row(start_board, 0,2))
#print (check_column(start_board,0,1))
#print (check_square(start_board,0,3))
print(back_tracking(start_board,0,0))
print_board(start_board)
print(iterations)
