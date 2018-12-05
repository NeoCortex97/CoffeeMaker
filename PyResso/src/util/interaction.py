# -*- coding: utf-8 -*-
from src.util.decoding import isInteger


def makeChoice():
    while True:
        choice = input("You smiled! Please choose between following options:\n1. Coffee\n2. Espresso\n3. Hot Water\n")
        if isInteger(choice):
            choice = int(choice)
            if 0 < choice < 4:
                return choice
            else:
                print("This is not a valid choice!")
        else:
            print("Your choice has to be numeric!")


def chooseStrength():
    while True:
            strength = input("How strong would you like your drink?\nChoose between 1-5.\n")
            if isInteger(strength):
                strength = int(strength)
                if strength in range(1, 6):
                    return strength
                else:
                    print("The strength has to be inbetween 1 and 5!")
            else:
                print("The strength has to be numeric!")


def enterName():
    name= input("Please enter your full name seperated by one space: \n")
    if name.count(" ") != 1:
        print("This seems wrong.. You need a first and a last name seperated by space.")
        enterName()
    return name
