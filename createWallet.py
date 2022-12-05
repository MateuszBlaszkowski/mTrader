def mainFunction(id):
    import tkinter as tk
    from tkinter.ttk import Label, Entry, Button
    from tkinter import messagebox
    import db
    import main

    def create():
        try:
            int(entryValue.get())
        except:
            messagebox.showerror("Złe dane!","Wielkość portfela musi składać się wyłącznie z cyfr!")
        else:
            if len(str(entryName.get()))<22:
                size = entryValue.get().replace("'","")
                name = entryName.get().replace("'", "")
                db.cursor.execute(f"INSERT INTO `wallets`(`wallet_id`, `user_id`, `wallet_name`, `wallet_size`) VALUES (NULL,'{id}','{name}','{size}')")
                db.mTrader_db.commit()
                try:
                    main.walletsLf.destroy()
                except:
                    pass
                try:
                    main.mainLf.destroy() 
                except:
                    pass
                main.showWallets()
                createWin.destroy()
            else:
                messagebox.showwarning("NIE", "Nazwa nie może mieć więcej niz 21 znakow!")


    createWin = tk.Toplevel()
    createWin.grab_set()
    createWin.title("Nowy portfel")
    createWin.resizable(0,0)
    createWin.columnconfigure(0,weight=1)
    createWin.columnconfigure(1,weight=3)
    createWin.geometry('300x200')

    header = Label(createWin, text="Nowy portfel")
    header.config(font=("Century Gothic", 22, "bold"))
    labelName = Label(createWin, text="Nazwa portfela:")
    entryName = Entry(createWin, width=25)
    labelValue = Label(createWin, text="Wielkość portfela:")
    entryValue = Entry(createWin, width=25)
    submit = Button(createWin, text="Utwórz portfel", width=45, command=create)

    header.grid(columnspan=2, row=0, pady=10, sticky=tk.N)
    labelName.grid(column=0, row=1, pady=10, padx=10, sticky=tk.W)
    entryName.grid(column=1, row=1, pady=10, sticky=tk.N)
    labelValue.grid(column=0, row=2, pady=10, padx=10, sticky=tk.W)
    entryValue.grid(column=1, row=2, pady=20, sticky=tk.N)
    submit.grid(columnspan=2, row=3)

    createWin.mainloop()