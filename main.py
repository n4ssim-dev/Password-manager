import tkinter
import pyperclip
from tkinter import messagebox
import random
import pandas
import json

"""
Prend le champ website renseigné et mentionne ses champs associés
ou fourni un message d'erreur
"""
def search_website():
    website_selected = website_entry.get()
    website_file = pandas.read_csv('password_list.csv')
    website_found = [[row["Email"], row["Password"]] for _, row in website_file.iterrows() if row["Website"] == website_selected]

    try:
        check_index = website_found[0][0]
    except IndexError as index_error:
        messagebox.showinfo(title="Error",message=f"You have provided an incorrect website, here's the error : \n\n {index_error}")
    else:
        messagebox.showinfo(title=website_selected,message=f"Email: {website_found[0][0]}\nPassword: {website_found[0][0]}")

"""
Génère un MDP alétoire
"""
def generate_password():
    password_entry.delete(0,tkinter.END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8,10)
    nr_symbols = random.randint(2,4)
    nr_numbers = random.randint(2,4)

    password_list = []
    [password_list.append(random.choice(letters)) for i in range(0, nr_letters)]
    [password_list.append(random.choice(symbols)) for i in range(0, nr_symbols)]
    [password_list.append(random.choice(numbers)) for i in range(0,nr_numbers)]
    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)
    password_entry.insert(0,password)

"""
Enregistre dans le .csv et le .json avec les informations renseignées
dans le formulaire
"""
def save_credentials():
    website_selected = website_entry.get()
    email_selected = email_entry.get()
    password_selected = password_entry.get()

    if not website_selected or not email_selected or not password_selected:
        messagebox.showinfo(title="Oops :/", message="You haven't provided the required credentials..")
    else:
        ok_or_cancel = messagebox.askokcancel(title=website_selected,
                                            message=f"These are your details : \n\nWebsite: {website_selected}\nEmail: {email_selected}\nPassword: {password_selected}\n\nAre you sure ?")
        if ok_or_cancel:
            new_data = {
                'Website': [website_selected],
                'Email': [email_selected],
                'Password': [password_selected]
            }

            json_data = {
                website_selected: {
                    "Email": email_selected,
                    "Password": password_selected
                }
            }

            try:
                # Créé ou modifie le password_list.csv
                try:
                    df = pandas.read_csv("password_list.csv")
                    df = pandas.concat([df, pandas.DataFrame(new_data)], ignore_index=True)
                except FileNotFoundError:
                    df = pandas.DataFrame(new_data)

                # Créé ou modifie le password_list.csv
                try:
                    with open("data.json", "r") as j_df:
                        existing_data = json.load(j_df)
                        existing_data.update(json_data)  # This merges the new data with existing
                except FileNotFoundError:
                    existing_data = json_data  # If file doesn't exist, use new data as base

                # Enregistre les deux fichiers
                df.to_csv('password_list.csv', index=False)
                with open("data.json", "w") as j_df:
                    json.dump(existing_data, j_df, indent=4)  # Save the merged data

            except Exception as e:
                messagebox.showerror(title="Error", message=f"Failed to save data: {str(e)}")
            else:
                website_entry.delete(0, tkinter.END)
                password_entry.delete(0, tkinter.END)
                messagebox.showinfo(title="Success", message="Password saved successfully!")



# Window
window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=50, pady=20)

# Image
canvas = tkinter.Canvas(width=200, height=200, highlightthickness=0)
lock_img = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)  # Centered at (100,100) in 200x200 canvas
canvas.grid(column=1, row=0)

# Labels
website_label = tkinter.Label(text="Website/App:", pady=5)
email_label = tkinter.Label(text="Email/Username:", pady=5)
password_label = tkinter.Label(text="Password:", pady=5)

# Entries
website_entry = tkinter.Entry(width=35)
website_entry.focus()
email_entry = tkinter.Entry(width=35)
email_entry.insert(0,"my-email-adress@outlook.com")
password_entry = tkinter.Entry(width=21)

# Buttons
search_button = tkinter.Button(text="Search", command=search_website,width=14)
generate_button = tkinter.Button(text="Generate Password",command=generate_password)
add_button = tkinter.Button(text="Add", command=save_credentials, width=36)

# UI Grid
website_label.grid(column=0, row=1, sticky="e")
website_entry.grid(column=1, row=1, sticky="ew")
search_button.grid(column=2,row=1)

email_label.grid(column=0, row=2, sticky="e")
email_entry.grid(column=1, row=2, columnspan=2, sticky="ew")

password_label.grid(column=0, row=3, sticky="e")
password_entry.grid(column=1, row=3, sticky="ew")
generate_button.grid(column=2, row=3, sticky="ew")

add_button.grid(column=1, row=4, columnspan=2, sticky="ew")

window.mainloop()