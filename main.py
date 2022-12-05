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
        global mainLf
        mainLf = tk.LabelFrame(mainWin, text="Portfel 1", width=850, height=400, background='white', font=("Century Gothic", 12))
        mainLf.grid(columnspan=3, row=1)
        mainLf.columnconfigure(0, weight=1)
        mainLf.columnconfigure(1, weight=2)
        mainLf.columnconfigure(2, weight=3)
        
        lf = tk.LabelFrame(mainLf, text="Dane o portfelu", width=300, height=300, background='white', font=("Century Gothic", 12))
        
        canvas = tk.Canvas(mainLf, width=40, height=300, bg='white', highlightbackground='white')
        
        
        label1 = Label(mainLf, text="Alior", font=("Century Gothic", 16), background="white")
    
        label2 = Label(mainLf, text="Kruk", font=("Century Gothic", 16), background="white")
        label3 = Label(mainLf, text="Orlen", font=("Century Gothic", 16), background="white")
        label4 = Label(mainLf, text="Inne", font=("Century Gothic", 16), background="white")
        
        canvas.create_rectangle((0,300),(40,150), fill='#9edc13', outline='#9edc13')# 150 + (300-150)/2 + 5 = 150 + 75 + 5 = 230
        canvas.create_rectangle((0,150),(40,100), fill='#2ab7ed', outline='#2ab7ed')
        canvas.create_rectangle((0,100),(40,50), fill='#ed8f2a', outline='#ed8f2a')
        canvas.create_rectangle((0,50),(40,0), fill='#fff035', outline='#fff035')
        
        lf.place(x=200, y=50)
        
        label1.place(x=70, y=230)
        label2.place(x=70, y=130)
        label3.place(x=70, y=80)
        label4.place(x=70, y=30)
        
        
        canvas.place(x=20, y=20)
    global showWallets
    def showWallets():
        db.cursor.execute(f"SELECT * FROM `wallets` INNER Join users ON users.user_id = wallets.user_id WHERE login = '{login}';")
        result = db.cursor.fetchall()
        if len(result)>0:
            global walletsLf
            walletsLf = tk.LabelFrame(mainWin, text="Portfele", width=870, height=400, font=("Century Gothic", 12), background='white')
            walletsLf.columnconfigure(0, weight=1)
            walletsLf.columnconfigure(1, weight=1)
            walletsLf.columnconfigure(2, weight=1)
            walletsLf.grid(columnspan=3, row=1, sticky=tk.N)
            buttons = []
            a=0
            db.cursor.execute(f"SELECT wallet_name FROM `wallets` INNER Join users ON users.user_id = wallets.user_id WHERE login = '{login}';")
            walletsNames = db.cursor.fetchall()
            for i in range(len(result)):    
                buttons.append(tk.Button(walletsLf, width=11, height=5,  wraplength=100,text=walletsNames[i],border=0, font=("Century Gothic", 12), activebackground="#e0e0e0", command=ok))
                if i<6:
                    buttons[i].grid(column=0+i, row=0, sticky=tk.W, padx=15, pady=15)
                elif i<12:
                    buttons[i].grid(column=0+a, row=1, sticky=tk.W, padx=15, pady=15)
                    a+=1
        else:
           if messagebox.askyesno("brak portfela", "Nie masz jeszcze żadnego portfela.\n\n Chcesz utworzyć nowy portfel?", parent=mainWin):
            createWalletF()
    def ok():
        walletsLf.destroy()
        wallet()

    



       
       

    showWallets()
    mainWin.mainloop()


#f1()

