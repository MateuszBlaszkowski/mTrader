import tkinter as tk
from tkinter.ttk import Label, Frame, Style
from tkinter import messagebox, LabelFrame
import db
def f1(login):

    def createWalletF():
        import createWallet
        db.cursor.execute(f"SELECT user_id FROM users WHERE login = '{login}'")
        global id
        id = db.cursor.fetchone()
        createWallet.mainFunction(id[0])

    db.cursor.execute(f"SELECT name FROM users WHERE login = '{login}'")
    imie = db.cursor.fetchone()
    mainWin = tk.Tk()
    mainWin.configure(background="white")
    mainWin.title("Panel mTrader")
    mainWin.geometry("900x500")
    mainWin.resizable(800, 500)
    mainWin.columnconfigure(0,weight=1)
    mainWin.columnconfigure(1,weight=2)
    mainWin.columnconfigure(2,weight=3)
    headerText = "Witaj, "+imie[0]
    header = Label(mainWin, text=headerText, font=("Century Gothic", 22), background='white')
    addWallet = tk.Button(mainWin, text="Dodaj portfel", width=20, height=2, border=0, font=("Century Gothic", 12), activebackground="#e0e0e0", command=createWalletF)
    


    
    header.grid(columnspan=2, row=0, sticky=tk.W, padx=15, pady=15)
    addWallet.grid(column=2, row=0, sticky=tk.E, pady=15, padx=15)

    def closing():
        if messagebox.askokcancel("Wyjście", "Zamknąć program?"):
            mainWin.destroy()
    mainWin.protocol('WM_DELETE_WINDOW', closing)
    
    #wallet()         
    def wallet():
        lf = tk.LabelFrame(mainWin, text="Dane o portfelu", width=300, height=300, background='white', font=("Century Gothic", 12))
        canvas = tk.Canvas(mainWin, width=40, height=300, bg='white', highlightbackground='white')
        canvas.create_rectangle((0,300),(40,150), fill='#9edc13', outline='#9edc13')
        label1 = Label(mainWin, text="Alior", font=("Century Gothic", 16), background="white")
        label2 = Label(mainWin, text="Kruk", font=("Century Gothic", 16), background="white")
        label3 = Label(mainWin, text="Orlen", font=("Century Gothic", 16), background="white")
        label4 = Label(mainWin, text="Inne", font=("Century Gothic", 16), background="white")
        canvas.create_rectangle((0,150),(40,100), fill='#2ab7ed', outline='#2ab7ed')
        canvas.create_rectangle((0,100),(40,50), fill='#ed8f2a', outline='#ed8f2a')
        canvas.create_rectangle((0,50),(40,0), fill='#fff035', outline='#fff035')
        lf.grid(column=1, row=1, sticky=tk.E)
        label1.place(x=80, y=300)
        label2.place(x=80, y=210)
        label3.place(x=80, y=160)
        label4.place(x=80, y=110)
        canvas.grid(column=0, row=1, sticky=tk.W, padx=25, pady=15)
    global showWallets
    def showWallets():
        db.cursor.execute(f"SELECT * FROM `wallets` INNER Join users ON users.user_id = wallets.user_id WHERE login = '{login}';")
        result = db.cursor.fetchall()
        if len(result)>0:
            global lf
            lf = tk.LabelFrame(mainWin, text="Portfele", width=870, height=400, font=("Century Gothic", 12), background='white')
            lf.columnconfigure(0, weight=1)
            lf.columnconfigure(1, weight=1)
            lf.columnconfigure(2, weight=1)
            lf.grid(columnspan=3, row=1, sticky=tk.N)
            buttons = []
            a=0
            db.cursor.execute(f"SELECT wallet_name FROM `wallets` INNER Join users ON users.user_id = wallets.user_id WHERE login = '{login}';")
            walletsNames = db.cursor.fetchall()
            for i in range(len(result)):    
                buttons.append(tk.Button(lf, width=11, height=5,  wraplength=100,text=walletsNames[i],border=0, font=("Century Gothic", 12), activebackground="#e0e0e0", command=ok))
                if i<6:
                    buttons[i].grid(column=0+i, row=0, sticky=tk.W, padx=15, pady=15)
                elif i<12:
                    buttons[i].grid(column=0+a, row=1, sticky=tk.W, padx=15, pady=15)
                    a+=1
        else:
           if messagebox.askyesno("brak portfela", "Nie masz jeszcze żadnego portfela.\n\n Chcesz utworzyć nowy portfel?", parent=mainWin):
            createWalletF()
    def ok():
        lf.destroy()
        wallet()

    



       
       

    showWallets()
    mainWin.mainloop()


#f1()

