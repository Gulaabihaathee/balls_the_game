# very much based on : Trevor Payne https://www.youtube.com/watch?v=fInYh90YMJU&noredirect=1
from sys import maxsize
import numpy as np
import pickle
import random
import datetime
from time import sleep
from itertools import combinations


#board is an array n x n where True values are not crossed balls and False values are crossed balls
#move is an array n x n where True values are not touched balls and False values are balls to be crossed

def createboard(n):
    return np.ones((n, n), dtype = bool)

def makeMove(move,board):
    return np.logical_and(board, move)

def spider(board):
    #returns all possible moves (not boards!)
    
    #vertical
    listofallmoves = []
    for n in range (len(board)):
        for m in range (len(board)):
            if board[n,m] == True:
                for k in range (len(board)):
                    if (m < (len(board)-k)):
                        if board[n,(len(board)-k-1)] == True:
                            boardx = np.ones((len(board), len(board)), dtype = bool)
                            boardx[n,m:(len(board)-k)] = False
                            listofallmoves.append(boardx)
    
    #horizontal
    for n in range (len(board)):
        for m in range (len(board)):
            if board[m,n] == True:
                for k in range (len(board)):
                    if (m < (len(board)-k-1)): #-1 due to repeate ones
                        if board[(len(board)-k-1),n] == True:
                            boardx = np.ones((len(board), len(board)), dtype = bool)
                            boardx[m:len(board)-k,n] = False
                            listofallmoves.append(boardx)
    #diagonal backward 
    for n in range (len(board)-1):
        for m in range (len(board)-1):
            if board[n,m] == True:
                #boardx = np.ones((len(board), len(board)), dtype = bool)
                for k in range (1,len(board)):
                    #boardx = np.ones((len(board), len(board)), dtype = bool)
                    if (n < (len(board)-k)) & (m < (len(board)-k)) :
                            if board[n+k,m+k] == True: # move?
                                    boardx = np.ones((len(board), len(board)), dtype = bool)
                                    for x in range(k+1):
                                    #boardx = np.ones((len(board), len(board)), dtype = bool)
                                            boardx[n+x,m+x] = False
                                    listofallmoves.append(boardx)

    #diagonal forward 
    for n in range (len(board)-1,0,-1):
        for m in range (len(board)-1):
            if board[n,m] == True:
                #boardx = np.ones((len(board), len(board)), dtype = bool)
                for k in range (1,len(board)):
                    #boardx = np.ones((len(board), len(board)), dtype = bool)
                    if (n-k >= 0) & (m < (len(board)-k)) :
                            if board[n-k,m+k] == True:
                                    boardx = np.ones((len(board), len(board)), dtype = bool)
                                    for x in range(k+1):
                                    #boardx = np.ones((len(board), len(board)), dtype = bool)
                                            boardx[n-x,m+x] = False
                                    listofallmoves.append(boardx) 

    return listofallmoves


def combs(k):
    ile_kulek = k 
    combs = np.sum(np.array(list(combinations(2**np.arange(n*n), ile_kulek))), axis=1)
    binary_repr_vec = np.vectorize(np.binary_repr)
    all_binaries = binary_repr_vec(combs, width=n*n)
    boards = []

    for binary in all_binaries:
        board = np.array([bit for bit in binary]).astype(bool).reshape(n,n)
        boards.append(board)
    #boards = np.array(boards)
    return boards

def iswin(board,list4):
    for move in spider(board):
        if np.any([np.array_equal(makeMove(move,board), x) for x in list4]):
            return False
    return True

def iswin2(board,list4):
    moves = spider(board)
    boards = []
    for m in moves:
        boards.append(makeMove(m, board))
                      
    for b in boards:
        if np.any([np.array_equal(b, x) for x in list4]):
            return False
    return True
def iswin3(board,list4):
    moves = spider(board)
    boards = []
    for m in moves:
        boards.append(makeMove(m, board))
                      
    for b in boards:
        if boardnum(b) in list4:
            return False
    return True
def boardnum(board):
    k = len(board)
    num = 0
    i=1
                               
    for n in range (k):
        for m in range (k):
            if board[n,m] == False:
                num = num+i
            i=i*2
    return num
                               
def numboard(num):
    board = createboard(n)
    ind = 2**(n**2-1)
    while ind >= 1:
        if num // ind > 0:
            i = 0
            for x in range (n):
                for y in range (n):
                    if i == np.log2(ind):
                        board[x,y] = False
                    i = i + 1
        num=num%ind
        ind = ind / 2
    return board
def drawBoard(board):
    n = len(board)
    for x in range (n):
        for y in range (n):
            if board[x,y]: print('O',end=' ')
            else: print('X',end=' ')
        print('')

def saveList(set2save):
    with open('list_4x.bin','wb') as output:
        pickle.dump(set2save, output, -1)
    return 1

def genList(n):
    list4 = combs(1)    
    tt = datetime.datetime.now()
    print(datetime.datetime.now().time())
    t = datetime.datetime.now()
    for k in range(3,n**2+1):
        print(k)
        #print(datetime.datetime.now().time())
        for board in combs(k):
            if iswin(board,list4): #np.append(list4,board) #
                list4.append(board)#
        diff = datetime.datetime.now()-t
        print(diff)
        print('..................')
              
        t = datetime.datetime.now()
              
    diff = datetime.datetime.now()-tt
    print(diff)
    return(list4)
def genList2(n):
    list4 = set()
    for x in combs(1):
        list4.add(boardnum(x))
           
    tt = datetime.datetime.now()
    print(datetime.datetime.now().time())
    t = datetime.datetime.now()
    for k in range(3,n**2+1):
        print(k)
        #print(datetime.datetime.now().time())
        for board in combs(k):
            if iswin3(board,list4): #np.append(list4,board) #
                list4.add(boardnum(board))#
        diff = datetime.datetime.now()-t
        print(diff)
        print('..................')
              
        t = datetime.datetime.now()
              
    diff = datetime.datetime.now()-tt
    print(diff)
    return(list4)
if __name__ == '__main__':
    n=3
    set3 = genList2(n)
    list3 = list(set3)
    print('list of all lost boards 3x3')
    for l in list3:
        drawBoard(numboard(l))
        print('------------')
    '''
    #dict4 = set()
    dict4 = allboards(n)
    t = datetime.datetime.now()
    for k in range(3,n**n+1):
        print(datetime.datetime.now().time())
        print(k)
        for board in combs2(k):
            if iswin(numboard(board)): dict4.add(board)
        print('..................')
    #saveSet1(dict4)'''
