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
    length=2
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

def word_length(board, line,pos):
    word_length=0
    line_cpy = ''.join(board[line][pos:])
    for i in range(line_cpy.find('_')+pos, len(board[line])):
        if board[line][i]=='#':
            break
        word_length+=1;

    return word_length,line_cpy.find('_')+pos


def check_letter(board,dict,line,pos):
    i=line
    word=""

    while i>-1 and board[i][pos]!='#':
        word= str(board[i][pos])+word
        i-=1

    length=len(word)
    line+=1

    while line<len(board) and board[line][pos]!='#':
        length+=1
        line+=1

    #In case of being just one letter
    if length==1:
        return 1;


    for w in dict[length]:
        if w.startswith(word,0,length):
            return 1

    return 0


def check_vertical(new_board,dict,line,start_p,length,word):
    board[line][start_p:start_p+length]=list(word)

    #For cycle that checks each letter in the word
    for i in word:
        # If one of the letters doesnt form a vertical word that is contained in the dictionary, this function returns 0
        if not check_letter(board,dict,line,start_p):
            return 0
        start_p+=1
    return 1

#Function that takes the words in the dictionary and checks which ones can be put in the blank space that also form words vertically
#Returns a list with all the valid words
def domain(board,dict,line,start_p,length):
    list=dict[length]

    domain=[]

    for i in list:
        if check_vertical(board,dict,line,start_p,length,i):
            domain.append(i)

    if domain==[]:
        board[line][start_p:start_p+length]=['_']*length

    return domain


def back_tracking(board, dict,line,pos):
    solved=0
    global iterations

    if line == len(board):
        return 1;

    length, start_p = word_length(board,line,pos)


    for word in domain(board,dict,line,start_p,length):

        iterations +=1
        board[line][start_p:start_p+length]=list(word)


        dict[length].remove(word)

        #If at the end of the line or no more blank spaces exists to fill, we increment the line
        if len(board[line])==start_p+length or not '_' in board[line]:
            solved=back_tracking(board,dict,line+1,0)

        #Otherwise we increment the position in the line
        else:
            solved=back_tracking(board,dict,line,start_p+length)

        if solved:
            break

        dict[length].append(word)

        #To reset the space where we tested a word
        board[line][start_p:start_p+length]=['_']*length
    return solved;

board= read_puzzle("puzzle4")
dict= read_words("words4")

back_tracking(board,dict,0,0)

#Prints the solved puzzle
for i in range (len(board)):
    print(board[i])
