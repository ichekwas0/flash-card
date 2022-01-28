import pandas
from tkinter import *
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_img, image=card_front_img)
    canvas.itemconfig(french_title, text="French", fill="black")
    canvas.itemconfig(french_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_img, image=card_back_img)
    canvas.itemconfig(french_title, text='English', fill="white")
    canvas.itemconfig(french_word, text=current_card["English"], fill="white")


def known_cards():
    global current_card
    to_learn.remove(current_card)
    next_card()
    df = pandas.DataFrame(to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(height=526, width=800)
card_front_img = PhotoImage(file="images/card_front.png")
canvas_img = canvas.create_image(400, 263, image=card_front_img)
french_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
french_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

card_back_img = PhotoImage(file="images/card_back.png")

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

left_img = PhotoImage(file="images/wrong.png")
left_button = Button(image=left_img, command=next_card)
left_button.grid(column=0, row=1)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, command=known_cards)
right_button.grid(column=1, row=1)

next_card()
window.mainloop()
