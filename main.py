from tkinter import Tk, Canvas, PhotoImage, Button, Listbox
import pandas
from random import choice
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"
file = ""
current_card = {}


# Functions
def listbox_used(event):
    global current_card, file
    print(listbox.get(listbox.curselection()))
    try:
        file = pandas.read_csv(f"data/updated_{listbox.get(listbox.curselection())}_words.csv").to_dict(
            orient="records")
    except FileNotFoundError:
        file = pandas.read_csv(f"data/{listbox.get(listbox.curselection())}_words.csv").to_dict(orient="records")
    current_card = choice(file)
    window.after(0, func=next_card)


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(file)
    canvas.itemconfig(upper_text, text=f"{listbox.get(listbox.curselection())}", fill="black")
    canvas.itemconfig(lower_text, text=current_card["English"], fill="black")
    canvas.itemconfig(backgroud_image, image=front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(upper_text, text=f"English", fill="purple")
    canvas.itemconfig(lower_text, text=current_card["English"], fill="purple")
    canvas.itemconfig(backgroud_image, image=back_image)


def known():
    try:
        file.remove(current_card)
        new_file = pandas.DataFrame(file)
        new_file.to_csv(f"data/updated_{listbox.get(listbox.curselection())}_words.csv", index=False)
        print(len(new_file))
        next_card()
        print(listbox.get(listbox.curselection()))
    except IndexError:
        messagebox.showinfo("Completed", "You've Memorized Everything, Congrats!")


window = Tk()
window.title("Flashipy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

listbox = Listbox(height=4)
fruits = ["English", "Urdu", "Pashto", "French"]
listbox.selection_set("end")
for item in fruits:
    listbox.insert(fruits.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.grid(row=1, column=2)
listbox.selection_set("end")

# CSV
listbox_used(1)

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
backgroud_image = canvas.create_image(400, 263, image=front_image)
upper_text = canvas.create_text(400, 130, text="Title", font=("Ariel", 35, "italic"))
lower_text = canvas.create_text(400, 283, text="Word", font=("Ariel", 70, "bold"))
canvas.grid(row=0, column=0, columnspan=3)

# Buttons
cross_image = PhotoImage(file="images/wrong.png")
cross_button = Button(image=cross_image, highlightthickness=0, command=next_card)
cross_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
tick_button = Button(image=right_image, highlightthickness=0, command=known)
tick_button.grid(row=1, column=1)

next_card()

window.mainloop()
