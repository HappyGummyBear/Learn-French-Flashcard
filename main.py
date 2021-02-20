from tkinter import *
import pandas
import random
import time

BACKGROUND_COLOR = "#B1DDC6"
chosen_word = {}
to_learn = []

#Check if program was run before so it can use old list of words left to learn or start all over again
try:
    word_dataframe = pandas.read_csv("data/french_words.csv")
except FileNotFoundError:
    old_word_dataframe = pandas.read_csv("data/words_to_learn.csv")
    to_learn = old_word_dataframe.to_dict(orient="records")
else:
    to_learn = word_dataframe.to_dict(orient="records")


def next_word():
    '''Function to get the next word in the csv file'''
    global chosen_word, times_up
    window.after_cancel(times_up) #Cancel the old timer to allow a new timer to start
    #Change the canvas to the new word
    canvas.itemconfig(bg_card, image=bg_image)
    chosen_word = random.choice(to_learn)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=chosen_word["French"], fill="black")
    #Start a new timer for the new word
    times_up = window.after(3000, flip_card)


def know_word():
    '''Fuction to remove the known word from the list of choices that can come up. Also adds it to a csv of
    words that the user knows'''
    to_learn.remove(chosen_word) #Remove word from list of possible words
    new_words = pandas.DataFrame(to_learn) #Creates data frame of words left on the list
    new_words.to_csv("data/words_to_learn.csv", index=False) #Creates csv of the new list of words
    next_word() #Calls next word function


def flip_card():
    '''Function to flip the card to the English translation of the word on the screen'''
    global chosen_word
    canvas.itemconfig(word_text, text=chosen_word["English"], fill="white") #Changes the label to 'English'
    canvas.itemconfig(title_text, text="English", fill="white") #Change text color
    canvas.itemconfig(bg_card, image=new_bg) #Change the background image


window = Tk() #Create the window
window.title("French Flash Cards") #Add a title to the window
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR) #Padding to the window to make it look cleaner

times_up = window.after(3000, flip_card) #Start timer as soon as program starts

canvas = Canvas(width=800, height=576) #Create canvas and add images to it on the window
new_bg = PhotoImage(file="images/card_back.png") #Images that will be used created with PhotoImage
bg_image = PhotoImage(file="images/card_front.png")
bg_card = canvas.create_image(400,263, image=bg_image)
word_text = canvas.create_text(400, 263, text="word", font=("Times New Roman", 50, "bold"))
title_text = canvas.create_text(400, 173, text="title", font=("Times New Roman", 25, "normal"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2) #Use grid to add all the parts to the canvas

correct_image = PhotoImage(file="images/right.png") #Correct choice image
correct_button = Button(image=correct_image, highlightthickness=0, command= know_word) #Button to choose correct guess
correct_button.grid(column=1, row=1) #Add it to the canvas

wrong_image = PhotoImage(file="images/wrong.png") #Wrong choice image
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_word) #Button for wrong choice
wrong_button.grid(column=0, row=1) #Add it to the canvas

next_word() #Call next word when program starts

window.mainloop() #Keep window open and updating
