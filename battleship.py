# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 20:05:56 2023

@author: oawar
"""

import time
import numpy as np
import random
import tkinter as tk

def additionMult(a,b,x):#need this for map
    return a + (b*x)

class timer():
    def __init__(self,msg = ""):
        self._msg = msg

    def start(self):
        self.start = time.perf_counter()
        
    def stop(self,print_time = False):
        self.stop = time.perf_counter()
        if print_time:
            print(self._msg,self.__str__())
        return self.stop - self.start
            
    def __str__(self):
        assert (self.stop > self.start), "Must start before end"
        t = self.stop - self.start
        s = str(t)+"s"
        return s


class board():
    def __init__(self,size = "medium"):
        self.size = size
        self.ships = []
        self.board_dimensions= 0
        if self.size == "big":
            self.board_dimensions= 25
            self.num_ships = 10
        elif self.size == "medium":
            self.board_dimensions= 10
            self.num_ships = 5
        elif self.size == "small":
            self.board_dimensions = 5
            self.num_ships = 3
        self.info_board = np.full((self.board_dimensions,self.board_dimensions),"#")
        self.play_board = np.full((self.board_dimensions,self.board_dimensions),"#")
    
    def __str__(self):
        s = str(self.info_board) +"\n"
        for i in range(len(self.ships)):
            s  = s + str(self.ships[i])+"\n"
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                if any(x in self.ships[i][1] for x in self.ships[j][1]):
                    s = s + "Overlapping Ships" + "\n"
        return s

    def checker(self,randPoint,direction,x):
        mult = np.full(2,x)
        check = map(additionMult,randPoint,direction,mult)
        return list(check)
    
    def ship_store(self,ship):
        self.ships.append(ship)
        
    def place_ships(self):
        ship_types = {"Destroyer":2,"Submarine":3,"Cruiser":3,"Battleship":4,"Carrier":5}
        ship_list = ("Destroyer","Submarine","Cruiser","Battleship","Carrier")
        stop = True
        while stop:
            i = 0
            while i < len(ship_list):
                direction = random.choice(([0,1],[0,-1],[-1,0],[1,0]))
                randPoint = np.random.randint(0,self.board_dimensions,2)
                ship_size = ship_types[ship_list[i]]
                boardCheck = self.checker(randPoint,direction,ship_size-1)
                if (True == any((x<0) or (x>self.board_dimensions-1) for x in boardCheck)):
                    continue
                location = []
                open = True
                for r in range(ship_size):
                    interCheck = self.checker(randPoint,direction,r)
                    open = (not self.info_board[interCheck[0]][interCheck[1]] == "X")
                    if open == False:
                        break
                if open:
                    for r in range(ship_size):
                        change = self.checker(randPoint,direction,r)
                        self.info_board[change[0]][change[1]] = "X"
                        location.append([change[0],change[1]])
                    self.ship_store([ship_list[i],location])
                    i += 1
            if len(self.ships) == self.num_ships:
                stop = False
                break
    
    def play(self,row,col):
        return self.info_board[row][col]

class BattleshipGUI():
    def __init__(self,master,player):
        self.player = player
        self.master = master
        self.count = 0
        self.winCon = 0
        self.master.title("Battleship Turn "+str(self.count))
        #always using medium so board dimensions = 10
        self.buttons = [[None for i in range(10)] for j in range(10)]
        for i in range(10):
            for j in range(10):
                button = tk.Button(master,width = 3,height =2,command = lambda row = i,col = j: self.buttonClick(row,col))
                button.grid(row=i,column=j)
                self.buttons[i][j] = button

    def buttonClick(self,row,col):
        self.buttons[row][col]["text"] = self.player.play(row,col)
        if self.player.play(row,col) == "X":
            self.buttons[row][col]["disabledforeground"] = "red"
            self.winCon += 1
        self.buttons[row][col]["state"] = tk.DISABLED
        self.count += 1
        self.master.title("Battleship Turn "+str(self.count))
        if self.winCon == 17:
            self.master.title(f"You Won! in {self.count} turns")
            for i in self.buttons:
                for j in i:
                    j["state"] = tk.DISABLED


def main(flag=True):
    player1 = board("medium")
    player1.place_ships()
    if flag:
        print(player1)
        root = tk.Tk()
        p1GUI = BattleshipGUI(root,player1)
        root.mainloop()
    
main()
