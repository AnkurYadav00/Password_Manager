import string
from tkinter import *
from tkinter import messagebox
import pandas as pd
from random import randint, choices
import pyperclip

UPPERCASE_CHARACTERS = randint(3, 4)
LOWERCASE_CHARACTERS = randint(4, 7)
SYMBOLS = randint(3, 4)
NUMBERS = randint(3, 6)

data_container = {
    "website": [],
    "username": [],
    "password": [],
}


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def pwd_generator():
    pass_entry.delete(0, END)
    alphaLowerString = string.ascii_lowercase
    alphaUpperString = string.ascii_uppercase
    numericString = ''.join([str(i) for i in range(10)])
    symbolsString = '!@#$%^&*()<>?'
    passwordString = (choices(alphaLowerString, k=LOWERCASE_CHARACTERS) +
                      choices(alphaUpperString, k=UPPERCASE_CHARACTERS) +
                      choices(numericString, k=NUMBERS) +
                      choices(symbolsString, k=SYMBOLS))

    # generating random string
    generated_string = ''.join(passwordString)
    # inserting it to entry for user to see
    pass_entry.insert(0, generated_string)
    # copy pwd
    pyperclip.copy(generated_string)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    global data_container
    website = web_entry.get()
    user = email_entry.get()
    password = pass_entry.get()

    if not (len(website) > 0 and len(password) > 0):
        messagebox.showerror(title="Oops!!", message="Don't leave any field empty!!")
        return None

    is_ok = messagebox.askokcancel(title=website, message=f"Do you want to proceed with the details entered?"
                                                          f" \nWebsite: {website}\nUsername: {user}\nPassword: {password}")
    if not is_ok:
        return None

    # save into csv file
    df_csv = pd.read_csv("data.csv")
    data_container["website"].append(website)
    data_container["username"].append(user)
    data_container["password"].append(password)
    df = pd.DataFrame(data_container, )
    df_new = pd.concat([df_csv, df])
    df_new.to_csv("data.csv", index=False)

    # save into text file
    with open('./data.txt', "a") as file:
        file.write(f"{website} | {user} | {password}\n")

    # TODO : deletes entered text once add button is clicked
    web_entry.delete(0, END)
    # email_entry.delete(0, END)
    pass_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.minsize(width=200, height=200)
window.title("Password Manager")
window.config(padx=50, pady=50)

# ----------------- Canvas ------------------- #
img = PhotoImage(file="./logo.png")
canvas = Canvas(width=200, height=190)
canvas.create_image(100, 85, image=img)
canvas.grid(row=0, column=1)

# ------------------ Label ------------------- #
web_label = Label(text="Website:")
web_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

pass_label = Label(text="Password:")
pass_label.grid(row=3, column=0)

# ------------------ Entry -------------------- #

web_entry = Entry(width=52)
web_entry.focus()
web_entry.grid(row=1, column=1, columnspan=2)

email_entry = Entry(width=52)
email_entry.insert(END, "@mail.com")
email_entry.grid(row=2, column=1, columnspan=2)

pass_entry = Entry(width=33)
pass_entry.grid(row=3, column=1)

# ----------------- Button -------------------- #

generate_pd_button = Button(text="Generate Password", bg="grey", fg="white", command=pwd_generator, border=0)
generate_pd_button.grid(row=3, column=2)

add_button = Button(text="Add", width=44, bg="#F3FDE8", fg="blue", command=save_data, border=0)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
