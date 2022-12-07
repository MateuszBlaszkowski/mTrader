import tkinter as tk
from tkinter.ttk import Label, Entry, Button, Checkbutton
from tkinter import messagebox, Toplevel
import db
import main

def restiger():
    #root.destroy()
    global restigerWindow
    restigerWindow = tk.Toplevel()
    restigerWindow.grab_set()
    restigerWindow.title("Zarejestruj się!")
    restigerWindow.resizable(0,0)
    restigerWindow.columnconfigure(0,weight=1)
    restigerWindow.columnconfigure(1,weight=3)
    restigerWindow.geometry('300x350')
   
    global entryName
    global entryLogin
    global entrySurName
    global entryPass
    global entryRptPass
    global chk
   
    header = Label(restigerWindow, text="Zarejestruj się!")
    header.config(font=("Century Gothic", 22, "bold"))
    labelName = Label(restigerWindow, text="Imię:")
    entryName = Entry(restigerWindow, width=25)
    labelSurName = Label(restigerWindow, text="Nazwisko:")
    entrySurName = Entry(restigerWindow, width=25)
    labelLogin = Label(restigerWindow, text="Login:")
    entryLogin = Entry(restigerWindow, width=25)
    labelPass = Label(restigerWindow, text="Hasło:")
    entryPass = Entry(restigerWindow, width=25, show="*")
    labelRptPass = Label(restigerWindow, text="Powtórz Hasło:")
    entryRptPass = Entry(restigerWindow, width=25, show="*")
    chk = Checkbutton(restigerWindow, text="Akceptuje regulamin")
    submitR = Button(restigerWindow, text="Rejestracja", width=45, command=restigerFun)
    
    header.grid(columnspan=2, row=0, pady=10, sticky=tk.N)
    labelName.grid(column=0, row=1, pady=10, padx=10, sticky=tk.W)
    entryName.grid(column=1, row=1, pady=10, sticky=tk.N)
    labelSurName.grid(column=0, row=2, pady=10, padx=10, sticky=tk.W)
    entrySurName.grid(column=1, row=2, pady=10, sticky=tk.N)
    labelLogin.grid(column=0, row=3, pady=10, padx=10, sticky=tk.W)
    entryLogin.grid(column=1, row=3, pady=10, sticky=tk.N)
    labelPass.grid(column=0, row=4, pady=10, padx=10, sticky=tk.W)
    entryPass.grid(column=1, row=4, pady=10, sticky=tk.N)
    labelRptPass.grid(column=0, row=5, pady=10, padx=10, sticky=tk.W)
    entryRptPass.grid(column=1, row=5, pady=10, sticky=tk.N)
    chk.grid(column=1, row=6, pady=10, sticky=tk.N)
    submitR.grid(columnspan=2, row=7)
    
    restigerWindow.mainloop()

def restigerFun():
    
    if entryName.get() != '' and entrySurName.get() != '' and entryLogin.get() != '' and entryPass.get() != '' and entryRptPass.get() !='':
      if len(entryPass.get()) < 7:
            messagebox.showwarning("Błąd", "Hasło musi mieć minimum 8 znaków!")            
      else:
            if entryPass.get() == entryRptPass.get():
                if "'" in entryLogin.get():
                    messagebox.showerror("Niedozwolony znak", "Nie można używać znkau ' ")
                else:
                    db.cursor.execute(f"SELECT login FROM users WHERE login='{entryLogin.get()}'")
                    result = db.cursor.fetchall()
                    if len(result)>0:
                        messagebox.showwarning("OK", "Podany login jest zajęty. Wypróbuj inny")
                    else:
                        if "'" in entryName.get() or "'" in entrySurName.get() or "'" in entryLogin.get() or "'" in entryPass.get():
                            messagebox.showerror("Niedozwolony znak", "Nie można używać znkau ' ")
                        else:
                            db.cursor.execute(f"INSERT INTO `users`(`user_id`, `name`, `surname`, `login`, `password`) VALUES ('null','{entryName.get()}','{entrySurName.get()}','{entryLogin.get()}','{entryPass.get()}')")
                            db.mTrader_db.commit()
                            messagebox.showinfo("OK", "Konto zostało utworzone")
                            restigerWindow.destroy()
            else:
                messagebox.showwarning("Błąd", "Hasła nie zgadzają się!")
    else:
        messagebox.showwarning("Błąd", "wpisz wszystkie informacje", parent=restigerWindow)

def login():
    if loginBox.get() == '' or passBox.get() == '':
        messagebox.showinfo("Błąd", "Wprowadź login i hasło!")
    else:
        login = loginBox.get()
        password = passBox.get()
        password = password.replace("'", "")
        login = login.replace("'", "")
        db.cursor.execute(f"SELECT * FROM users WHERE login='{login}' AND password='{password}'")
        result = db.cursor.fetchall()
        if len(result)>0:
            root.destroy()
            main.f1(login)
        else:
            messagebox.showwarning("NIE","Login lub hasło niepoprawne")
print(db.mTrader_db)
root = tk.Tk()
root.title("Zaloguj się")
root.geometry('250x100')
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.resizable(0,0)

loginLabel = Label(root, text="Login:")
loginBox = Entry(root, width=25)
passLabel = Label(root, text="Hasło:")
passBox = Entry(root, show="*", width=25)
restigerLbl = Label(root, text="Zarejestruj się!", cursor="hand2", foreground="blue")
submitBtn = Button(root, text="OK", command=login)
root.bind("<Return>", lambda e: login())

loginLabel.grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)
loginBox.grid(column=1, row=0, sticky=tk.E,  pady=5, padx=5)
passLabel.grid(column=0, row=1, sticky=tk.W, padx=10, pady=5)
passBox.grid(column=1, row=1, sticky=tk.E,  pady=5, padx=5)
restigerLbl.grid(column= 0, row=2,sticky=tk.W, padx=10, pady=5, columnspan=2)
restigerLbl.bind("<Button-1>", lambda e: restiger())
submitBtn.grid(column=1, row=2, sticky=tk.E, pady=5, padx=5)
root.mainloop()

"""
canvas = tk.Canvas(restigerWindow, width=20, height=200, bg='white')
canvas.pack(anchor=tk.CENTER, expand=True)
canvas.create_rectangle((0, 200),(21,170),fill='blue', outline='white')
canvas.create_rectangle((0, 170),(21,150),fill='red', outline='white')
canvas.create_rectangle((0, 150),(21,120),fill='green', outline='white')
"""