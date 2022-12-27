import tkinter as tk
from tkinter.ttk import Label, Treeview, Scrollbar, Progressbar
from tkinter import messagebox
import db
import threading
import os

def f1(login):

    def createWalletF():
        import createWallet
        db.cursor.execute(f"SELECT user_id FROM users WHERE login = '{login}'")
        global id
        id = db.cursor.fetchone()
        createWallet.mainFunction(id[0])
    
    def changeWalletF():
        mainLf.destroy()
        showWallets()
        changeWallet.grid_remove()
    def logOff():
        mainWin.destroy()
        if os.path.exists("cache//login_temp.txt"):
            os.remove("cache//login_temp.txt")
            db.cursor.execute(f"DELETE FROM remembered_users WHERE user_login='{login}'")
            db.mTrader_db.commit()
        os.system('python login.py')
    db.cursor.execute(f"SELECT name FROM users WHERE login = '{login}'")
    imie = db.cursor.fetchone()
    mainWin = tk.Tk()
    mainWin.configure(background="white")
    mainWin.title("Panel mTrader")
    mainWin.geometry("900x500")
    mainWin.iconbitmap("images//icon.ico")
    mainWin.resizable(0,0)
    mainWin.columnconfigure(0,weight=1)
    mainWin.columnconfigure(1,weight=11)
    mainWin.columnconfigure(2,weight=1)
    mainWin.columnconfigure(3,weight=1)
    """ menuBar = tk.Menu(mainWin, background="#000000", borderwidth=0)
        mainWin.config(menu=menuBar)
        walletMenu = tk.Menu(menuBar, tearoff=False, background='#000000')
        walletMenu.add_command(label="WXIT")
        menuBar.add_cascade(label="ok", menu=walletMenu, background="#000000")"""
    headerText = "Witaj, "+imie[0]
    header = Label(mainWin, text=headerText, font=("Century Gothic", 22), background='white')
    addWallet = tk.Button(mainWin, text="Wyloguj się", width=15, height=2, border=0, font=("Century Gothic", 12), activebackground="#e0e0e0", command=logOff, foreground="red")
    changeWallet = tk.Button(mainWin, text="Zmień portfel", width=15, height=2, border=0, font=("Century Gothic", 12), activebackground="#e0e0e0", command=changeWalletF)
    settingsWallet = tk.Button(mainWin,text="+", width=5, height=2, border=0, font=("Century Gothic", 12), activebackground="#e0e0e0", command=createWalletF)
    
    header.grid(column=0, row=0, sticky=tk.W, padx=15, pady=15)
    addWallet.grid(column=3, row=0, sticky=tk.W, pady=15)
    settingsWallet.grid(column=2, row=0, sticky=tk.N, pady=15)

    """def closing():
        if messagebox.askokcancel("Wyjście", "Zamknąć program?"):
            mainWin.destroy()
    mainWin.protocol('WM_DELETE_WINDOW', closing)"""
    
    #wallet()         
    def wallet(walletName):
        global mainLf
        mainLf = tk.LabelFrame(mainWin, text=walletName, width=mainWin.winfo_width()-50, height=400, background='white', font=("Century Gothic", 12))
        
        mainLf.columnconfigure(0, weight=1)
        mainLf.columnconfigure(1, weight=2)
        mainLf.columnconfigure(2, weight=3)
        
        global walletId
        db.cursor.execute(f"SELECT `wallet_id` FROM `wallets` INNER JOIN users on wallets.user_id = users.user_id WHERE users.login = '{login}' and wallet_name = '{walletName[0]}';")
        walletId = db.cursor.fetchone()
        walletId = walletId[0]

        lf = tk.LabelFrame(mainLf, text="Dane o portfelu", width=300, height=300, background='white', font=("Century Gothic", 12))
        
        canvas = tk.Canvas(mainLf, width=40, height=300, bg='white', highlightbackground='white')
        
        def refresh():
            mainLf.grid_forget()
            walletBtnClick(walletName)
        
        def newOperationBtn():
            operationWin.mainF(walletId)
            
        """
        
        label1 = Label(mainLf, text="Alior", font=("Century Gothic", 16), background="white")
        label2 = Label(mainLf, text="Kruk", font=("Century Gothic", 16), background="white")
        label3 = Label(mainLf, text="Orlen", font=("Century Gothic", 16), background="white")
        label4 = Label(mainLf, text="Inne", font=("Century Gothic", 16), background="white")"""
        def makeColumn(prc):
            tab = []
            tab2 = []
            for i in range(3):
                dict1 = {"a" : int((prc[i]/100)*300)}
                if i > 0:
                    dict1["a"] += tab[i-1]["a"]
                tab.append(dict1)
            for i in range(len(tab)): 
                if i > 0:
                    x1 = tab[i-1]["a"]
                elif i == 0:
                    x1 = 0 
                x2 = tab[i]["a"]
                dict2 = {
                    0 : x1,
                    1 : x2
                }
                tab2.append(dict2)
            return tab2
        
        db.cursor.execute(f"SELECT DISTINCT `ISIN` FROM `shares` WHERE WALLET_ID = {walletId}")
        result = db.cursor.fetchall()
        count = {}
        import GPW_Scrapper_ISIN as gpw
        shares = []
        for i in result:
            db.cursor.execute(f"SELECT SUM(COUNT) FROM `shares` WHERE WALLET_ID = {walletId} AND ISIN = '{i[0]}'")
            sumCount = db.cursor.fetchone()
            count[i[0]] = sumCount[0]
            price = gpw.main(i[0])["price"].replace(",",".")
            price = float(price)
            shares.append(int(count[i[0]]) * price)
        db.cursor.execute(f"SELECT free_funds FROM wallets WHERE wallet_id = {walletId}")
        freeFunds = db.cursor.fetchone()
        walletFunds = round(sum(shares) + int(freeFunds[0]),2)
        pb.destroy()
        mainLf.grid(columnspan=4, row=1)
        percent = [0,0]
        colors = ['#9edc13', '#2ab7ed', '#ed8f2a', '#fff035']
        componets = ['', '', 'Wolne\nśrodki']
        a = percent[0]
        b = percent[1]
        c = freeFunds[0]/walletFunds*100
        db.cursor.execute(f"SELECT DISTINCT SYMBOL ,  price*count as p FROM shares WHERE WALLET_ID = {walletId} ORDER BY PRICE*COUNT DESC LIMIT 2;")
        result = db.cursor.fetchall()
        #for i in result:
            #print(i[0])
        labels = []
        for i in range(3):
            #print(makeColumn([a,b,c])[i][1], makeColumn([a,b,c])[i][0])
            canvas.create_rectangle((0,makeColumn([a,b,c])[i][1]),(40,makeColumn([a,b,c])[i][0]), fill=colors[i], outline=colors[i])
            labels.append(Label(mainLf, text=componets[i], font=("Century Gothic", 16), background="white"))
            labels[i].place(x=70, y=makeColumn([a,b,c])[i][0] + (makeColumn([a,b,c])[i][1] - makeColumn([a,b,c])[i][0])/2+5)
        if 300 - makeColumn([a,b,c])[2][1] > 5:
            canvas.create_rectangle((0,300),(40,makeColumn([a,b,c])[2][1]), fill=colors[3], outline=colors[3])
            labels.append(Label(mainLf, text="Akcje", font=("Century Gothic", 16), background="white"))
            labels[3].place(x=70, y=makeColumn([a,b,c])[2][1] + (300-makeColumn([a,b,c])[2][1])/2 + 5)
        
        lf.place(relx=0.2, y=25)
        lf.columnconfigure(0, weight=1)
        lf.columnconfigure(1, weight=1)
        db.cursor.execute(f"SELECT wallet_size FROM wallets WHERE wallet_id = {walletId}")
        walletSize = db.cursor.fetchone()
        walletSize = walletSize[0]
        fr = []
        frLabels = []
        frLabelsT = [str(walletFunds)+"zł", str(walletSize)+"zł", str(round((walletFunds - walletSize)/walletSize*100, 2))+"%", str(round(walletFunds - walletSize, 2))+"zł"]
        walletDataLabels = []
        walletDataLabelsT = ['Wartość\nobecna', 'Wartość\npoczątkowa', 'Stopa zwrotu', 'Zysk/strata']
        for i in range(4):
            fr.append(tk.Frame(lf, width=80, height=80))
            frLabels.append(Label(fr[i], text=frLabelsT[i], anchor="center", font=("Century Gothic", 12)))
            frLabels[i].place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            walletDataLabels.append(Label(lf, text=walletDataLabelsT[i], font=("Century Gothic", 10), background="white"))

        if frLabelsT[0]>frLabelsT[1]:
            frLabels[0].config(foreground="#45e43a")
            frLabels[2].config(foreground="#45e43a")
            frLabels[3].config(foreground="#45e43a")
        elif frLabelsT[0]<frLabelsT[1]:
            frLabels[0].config(foreground="red")
            frLabels[2].config(foreground="red")
            frLabels[3].config(foreground="red")
        walletDataLabels[0].grid(column=0, row=0, sticky=tk.N, pady=15)
        fr[0].grid(column=0, row=1, sticky=tk.N, padx=20)
        walletDataLabels[1].grid(column=1, row=0, sticky=tk.N, pady=15)
        fr[1].grid(column=1, row=1, sticky=tk.N, padx=20)
        walletDataLabels[2].grid(column=0, row=2, sticky=tk.N, pady=15)
        fr[2].grid(column=0, row=3, sticky=tk.N, padx=20, pady=(0, 15))
        walletDataLabels[3].grid(column=1, row=2, sticky=tk.N, pady=15)
        fr[3].grid(column=1, row=3, sticky=tk.N, padx=20, pady=(0, 15))
        import operationWin
        newOperation = tk.Button(mainLf, text="Nowa operacja", border=0, font=("Century Gothic", 12), activebackground="#e0e0e0", command=newOperationBtn).place(relx=0.82, rely=0.02, relwidth=0.16, relheight=0.10)
        walletSettings = tk.Button(mainLf, text="Odśwież", border=0, font=("Century Gothic", 12), activebackground="#e0e0e0", command=refresh).place(relx=0.64, rely=0.02, relwidth=0.16, relheight=0.10)
        Label(mainLf, text="Historia operacji", background="white", font=("Century Gothic", 12)).place(relx=0.51, rely=0.215)
        treeview = Treeview(mainLf, columns=('column1', 'column2','column3', 'column4', 'column5', 'column6'), show='headings')
        treeview.column('column1', width=60, stretch=tk.NO)
        treeview.column('column2', width=36, stretch=tk.NO)
        treeview.column('column3', width=65, stretch=tk.NO)
        treeview.column('column4', width=90, stretch=tk.NO)
        treeview.column('column5', width=63, stretch=tk.NO)
        treeview.column('column6', width=68, stretch=tk.NO)
        treeview.heading('column1', text='Symbol')
        treeview.heading('column2', text='K/S')
        treeview.heading('column3', text='Cena')
        treeview.heading('column4', text='Cena Aktualna')
        treeview.heading('column5', text='Ilośc akcji')
        treeview.heading('column6', text='Data')
        for i in range(2):
            treeview.insert('', tk.END,values=(i, i, i, i, i))
        scrollbar = Scrollbar(mainLf, orient=tk.VERTICAL, command=treeview.yview)
        scrollbar.place(relx=0.961, rely=0.320, relheight=0.59)
        treeview.configure(yscroll=scrollbar.set)
        treeview.place(relx=0.51, rely=0.315, width=400, relheight=0.6)
        
        """ label1.place(x=70, y=230)
            label2.place(x=70, y=130)
            label3.place(x=70, y=80)
            label4.place(x=70, y=30)"""
        changeWallet.grid(column=1, row=0, sticky=tk.E, pady=15)
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
            walletsLf.grid(columnspan=4, row=1, sticky=tk.N)
            buttons = []
            a=0
            db.cursor.execute(f"SELECT wallet_name FROM `wallets` INNER Join users ON users.user_id = wallets.user_id WHERE login = '{login}';")
            walletsNames = db.cursor.fetchall()
            
            for i in range(len(result)):
                buttons.append(tk.Button(walletsLf, width=11, height=5,  wraplength=100,text=walletsNames[i],border=0, font=("Century Gothic", 12), activebackground="#e0e0e0", command=lambda m=walletsNames[i]:walletBtnClick(m)))
                
                if i<6:
                    buttons[i].grid(column=0+i, row=0, sticky=tk.W, padx=15, pady=15)
                elif i<12:
                    buttons[i].grid(column=0+a, row=1, sticky=tk.W, padx=15, pady=15)
                    a+=1
        else:
         if messagebox.askyesno("brak portfela", "Nie masz jeszcze żadnego portfela.\n\n Chcesz utworzyć nowy portfel?", parent=mainWin):
            createWalletF()
    def pbFunction():
        global pb
        pb = Progressbar(mainWin, orient="horizontal", length=200, mode="indeterminate")
        pb.grid(columnspan=4,sticky=tk.N, pady=150, row=2)
        pb.start(20)
    
    def walletBtnClick(walletName):
        walletsLf.destroy()
        t1 = threading.Thread(target=pbFunction)
        t2 = threading.Thread(target=wallet, args=(walletName,))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()

    showWallets()
    mainWin.mainloop()

#f1()

