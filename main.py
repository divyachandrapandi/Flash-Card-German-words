from tkinter import *
import pandas
from random import choice
import messagebox

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = 'Arial'
CURRENT_CARDS = {}
timer = None  # timer initialised as none variable

# ------------------CSV DATA EXTRACTION------------#
# TODO -2 Pandas used to read_csv --> dataframe ---> dictionary
#  orient specified as records ---> [{element : {'sub-element1':"abc",'sub-element2':"def}}]
#  Documentation: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html

# TODO - 7 try to open word_to_learn.csv if exist, if not read original data
try:
    data_csv = pandas.read_csv(r"data/word_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv(r"data/words.csv")
    data_dict = original_data.to_dict(orient='records')
except pandas.errors.EmptyDataError:
    original_data = pandas.read_csv(r"data/words.csv")
    data_dict = original_data.to_dict(orient='records')

else:
    data_dict = data_csv.to_dict(orient='records')


# TODO - 3 random card is drawn using choice
#  German words are retrieved using current_card['German']
#  title changed to German using item config
#  timer is set to create 3s delay and execute flip card function
#  To remove element from records, use remove method for list

def random_cards():
    global CURRENT_CARDS
    global timer

    CURRENT_CARDS = choice(data_dict)
    canvas.itemconfig(word_text, text=CURRENT_CARDS['German'])
    canvas.itemconfig(title_text, text='German')
    timer = window.after(3000, flip_card)


# TODO - 6 To create words_to_learn.csv
#  to remove the known words from the dictioanry and create a csv
#  index is False to avoid reductant in data

def is_known():
    try:
        data_dict.remove(CURRENT_CARDS)
        print(len(data_dict))
        df = pandas.DataFrame(data_dict)
        df.to_csv("data/word_to_learn.csv", index=False)

        print(data_dict)
        random_cards()

    except IndexError:
        print("You learned all the words!!!!!!!!")
        messagebox.showinfo(title="Completed!", message="You have successfully learned\n all 50 frequent words")
    except ValueError:
        print("You learned all the words!!!!!!!!")
        messagebox.showinfo(title="Completed!", message="You have successfully learned\n all first 50 frequent words")


# TODO - 4 flip card function gives English translated words
#  change canvas image, word to 'English', title to 'English' also change fill color od the character as white
#  cancelling the after method delay and executing another random choice for a next button click

def flip_card():
    global timer
    canvas.itemconfig(canvas_bg, image=english_bg)
    canvas.itemconfig(word_text, text=CURRENT_CARDS['English'], fill='white')
    canvas.itemconfig(title_text, text='English', fill='white')
    window.after_cancel(timer)


# -------------------UI SETUP-----------------------#
# TODO - 1 Set up canvas - 1 image, 2 text, 2 button widget
#  2 button

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

german_bg = PhotoImage(file=r"images/card_front.png")
english_bg = PhotoImage(file=r"images/card_back.png")
canvas_bg = canvas.create_image(400, 263, image=german_bg)

title_text = canvas.create_text(400, 150, text="title", font=(FONT_NAME, 40, 'italic'))
word_text = canvas.create_text(400, 263, text="word", font=(FONT_NAME, 60, 'italic'))

canvas.grid(row=0, column=0, columnspan=2)
# TODO - 5 Add the command line passing random_cards as function
check_image = PhotoImage(file=r"images/right.png")
r_button = Button(image=check_image, command=is_known)
r_button.grid(row=1, column=1)

wrong_image = PhotoImage(file=r"images/wrong.png")
w_button = Button(image=wrong_image, command=random_cards)
w_button.grid(row=1, column=0)
random_cards()
window.mainloop()
