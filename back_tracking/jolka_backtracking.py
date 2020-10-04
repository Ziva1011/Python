import numpy as np
import copy

def read_puzzle(input_file):
    file = open(input_file,"r")

    board=[]
    line=[]

    while (1):
        line=file.readline().strip("\n")
        if line:
            board.append(list(line))
        else:
            break
    return board

def read_words(input_file):
    file = open(input_file,"r")

    dict={}
    line=[]
    lenght=2
    while (1):
        line=file.readline().strip("\n")
        if line:
            if len(line) in dict:
                dict[len(line)].append(line)
            else:
                dict[len(line)]=[]
                dict[len(line)].append(line)
        else:
            break
    return dict

def complete(board):
    for i in range(len(board)):
        if '_' in board[i]:
            return 0;
    return 1

def word_lenght(board, line,pos):
    word_lenght=0
    line_cpy = ''.join(board[line][pos:])
    for i in range(line_cpy.find('_')+pos, len(board[line])):
        if board[line][i]=='#':
            break
        word_lenght+=1;

    return word_lenght,line_cpy.find('_')+pos


def check_letter(board,dict,line,pos):
    i=line
    word=""

    while i>-1 and board[i][pos]!='#':
        word= str(board[i][pos])+word
        i-=1

    lenght=len(word)
    line+=1


    while line<len(board) and board[line][pos]!='#':
        lenght+=1
        line+=1

    if (lenght==1):
        return 1;

    for w in dict[lenght]:
        if w.startswith(word,0,lenght):
            return 1

    return 0


def check_vertical(board,dict,line,start_p,lenght):
    word=board[line][start_p:start_p+lenght]
    for i in word:
        if not check_letter(board,dict,line,start_p):
            return 0
        start_p+=1
    return 1


def back_tracking(board, dict,line,pos):
    solved=0

    if line == len(board):
        return 1;

    lenght, start_p = word_lenght(board,line,pos)

    for word in dict[lenght]:
        board[line][start_p:start_p+lenght]=list(word)
        c1=check_vertical(board,dict,line,start_p,lenght)

        if (c1):
            dict[lenght].remove(word)

            #If at the end of the line or no more blank spaces exists to fill, we increment the line
            if len(board[line])==start_p+lenght or not '_' in board[line]:
                solved=back_tracking(board,dict,line+1,0)

            #Otherwise we increment the position in the line
            else:
                solved=back_tracking(board,dict,line,start_p+lenght)

            if solved:
                break
            dict[lenght].append(word)

        #To reset the space where we tested a word
        board[line][start_p:start_p+lenght]=['_']*lenght
    return solved;


board= read_puzzle("puzzle4")
dict= read_words("words4")

back_tracking(board,dict,0,0)

for i in range (len(board)):
    print(board[i])
