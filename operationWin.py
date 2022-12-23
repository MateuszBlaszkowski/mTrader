import tkinter as tk
from tkinter.ttk import Radiobutton, Labelframe, Button, Entry, Label, Combobox, Progressbar
import db
import threading
from tkinter import messagebox
def mainF(walletid):

    global oWindow
    global walletId
    walletId = walletid
    oWindow = tk.Toplevel()
    oWindow.grab_set()
    oWindow.geometry('300x200')
    oWindow.title('Nowa operacja')
    oWindow.resizable(0,0)
    oWindow.columnconfigure(0, weight=1)
    global lf
    lf = Labelframe(oWindow, text="Rodzaj transakcji")
    lf.columnconfigure(0,weight=1)
    lf.columnconfigure(1,weight=1)
    lf.grid(column=0, row=0, sticky=tk.N, padx=10, pady=10)
    rvalue = tk.StringVar()

    def radioBtn():
        if rvalue.get() == 'k':
            f2.grid_forget()
            f1.grid(column=0, row=1)
            oWindow.geometry('300x200')
            oWindow.update()
        elif rvalue.get() == 's':
            f1.grid_forget()
            f2.grid(column=0, row=1)
            oWindow.geometry('300x240')
            oWindow.update()

    r = Radiobutton(lf, text="Kupno", variable=rvalue, value="k", command=radioBtn).grid(column=0, row=0, sticky=tk.W, padx=(0,15), pady=5)
    r1 = Radiobutton(lf, text="Sprzedaż", variable=rvalue, value="s", command=radioBtn).grid(column=1, row=0, sticky=tk.W, pady=5)
    global f1
    global f2
    f1 = tk.Frame(oWindow)
    f2 = tk.Frame(oWindow)
    f1.columnconfigure(0,weight=1)
    f1.columnconfigure(1,weight=1)

    Label(f1, text="Symbol spółki").grid(column=0, row=1, sticky=tk.W, pady=10, padx=20)
    global name
    name = Entry(f1, width=20)
    name.grid(column=1, row=1, sticky=tk.N, padx=10, pady=10)
    Label(f1, text="Ilośc akcji").grid(column=0, row=2, sticky=tk.W, pady=10, padx=20)
    global value
    value = Entry(f1, width=20)
    value.grid(column=1, row=2, sticky=tk.N, padx=10, pady=10)
    Button(f1, width=20, text="Kup", command=buyBtn).grid(column=0, row=3, sticky=tk.E, padx=10, pady=10)
    Button(f1, width=20, text="Przelicz", command=calculateBtn).grid(column=1, row=3, sticky=tk.W, padx=10, pady=10)

    shares = []
    db.cursor.execute(f"SELECT `SYMBOL` FROM `shares` WHERE WALLET_ID = {walletId}")
    result = db.cursor.fetchall()
    if len(result) > 0:
        for i in range(len(result)):
            if result[i] in shares:
                continue
            else:
                shares.append(result[i])
    Label(f2, text="Symbol spółki").grid(column=0, row=1, sticky=tk.W, pady=10, padx=20)
    global symbol
    symbol = tk.StringVar()
    combo = Combobox(f2, width=17, values=shares, textvariable=symbol, state="readonly")
    combo.grid(column=1, row=1, sticky=tk.N, padx=10, pady=10)
    
    Label(f2, text="Obecna Ilośc akcji").grid(column=0, row=2, sticky=tk.W, pady=10, padx=20)
    
    l = Label(f2, text="")
    l.grid(column=1, row=2, sticky=tk.N, padx=10, pady=10)
    def presentSharesCount(e):
        db.cursor.execute(f"SELECT SUM(`COUNT`) FROM `shares` WHERE WALLET_ID = {walletId} AND SYMBOL = '{symbol.get()}';")
        result = db.cursor.fetchone()
        l.config(text=result[0])
    Label(f2, text="Ilośc akcji").grid(column=0, row=3, sticky=tk.W, pady=10, padx=20)
    global sharesCount
    sharesCount = Entry(f2, width=20)
    sharesCount.grid(column=1, row=3, sticky=tk.N, padx=10, pady=10)
    Button(f2, width=45, text="Sprzedaj", command=sellBtn).grid(columnspan=2, row=4, sticky=tk.N, padx=10, pady=10)        
    combo.bind("<<ComboboxSelected>>", presentSharesCount)
    rvalue.set("k")
    radioBtn()
    
def createOperation():
    import GPW_Scrapper as gpw
    try:
        count = int(value.get())
        try:
            gpwDict = gpw.main(name.get())
            symbol = gpwDict["symbol"]
            price = gpwDict["price"].replace(",", ".")
            price = float(price)
            isin = gpwDict["ISIN"]
            db.cursor.execute(f"SELECT free_funds FROM wallets WHERE wallet_id = {walletId}")
            walletsize = db.cursor.fetchone()
            walletsize = walletsize[0]
            if price*count<=walletsize:
                db.cursor.execute(f"INSERT INTO `shares`(`WALLET_ID`, `PRICE`, `DATE`, `SYMBOL`, `ISIN`, `COUNT`) VALUES ({walletId},'{price}',CURRENT_TIMESTAMP(),'{symbol}','{isin}', {count})")
                db.mTrader_db.commit()
                db.cursor.execute(f"UPDATE `wallets` SET `free_funds`=`free_funds`-{price*count} WHERE wallet_id = {walletId};")
                db.mTrader_db.commit()
                messagebox.showinfo("OK", "Akcje zostały kupione")
                oWindow.destroy()
            else:
                messagebox.showwarning("Za mało pienędzy", "Masz za mało pieniędzy w portfelu aby kupić określoną ilość akcji!")
                pb.grid_forget()
                lf.grid(column=0, row=0, sticky=tk.N, padx=10, pady=10)
                f1.grid(column=0, row=1)
        except:
            messagebox.showwarning("Błąd", "Wystąpił Błąd!\nUpewnij się, że podana nazwa spółki jest poprawna!")
            pb.grid_forget()
            lf.grid(column=0, row=0, sticky=tk.N, padx=10, pady=10)
            f1.grid(column=0, row=1)
    except:
        messagebox.showwarning("Błąd", "Ilość akcji nie może być pusta i musi składać się wylącznie z cyfr")
        pb.grid_forget()
        lf.grid(column=0, row=0, sticky=tk.N, padx=10, pady=10)
        f1.grid(column=0, row=1)
def calculatePrice():
    import GPW_Scrapper as gpw
    try:
        count = int(value.get())
        try:
            gpwDict = gpw.main(name.get())
            symbol = gpwDict["symbol"]
            price = gpwDict["price"].replace(",", ".")
            price = float(price)
            pb.grid_forget()
            lf.grid(column=0, row=0, sticky=tk.N, padx=10, pady=10)
            f1.grid(column=0, row=1)
            messagebox.showinfo("Przelicz", f"{count} Akcji {symbol} = {round(price*count, 2)}\n\nCena jednej akcji = {price}")

        except:
            messagebox.showwarning("Błąd", "Wystąpił Błąd!\nUpewnij się, że podana nazwa spółki jest poprawna!")
            pb.grid_forget()
            lf.grid(column=0, row=0, sticky=tk.N, padx=10, pady=10)
            f1.grid(column=0, row=1)
    except:
        messagebox.showwarning("Błąd", "Ilość akcji nie może być pusta i musi składać się wylącznie z cyfr")
def sell():
    db.cursor.execute(f"SELECT SUM(`COUNT`) FROM `shares` WHERE WALLET_ID = {walletId} AND SYMBOL = '{symbol.get()}';")
    result = db.cursor.fetchone()
    try:
        sharesCount1 = int(sharesCount.get())
    except:
        messagebox.showerror("Błąd","Ilość akcji nie może być pusta i musi zawierać wyłącznie cyfry!")
        pb.grid_forget()
        lf.grid(column=0, row=0, sticky=tk.N, padx=10, pady=10)
        f2.grid(column=0, row=1)
        return
    if result[0] >= sharesCount1:
        import GPW_Scrapper as gpw
        gpwDict = gpw.main(symbol.get())
        price =  gpwDict["price"]
        price = gpwDict["price"].replace(",", ".")
        price = float(price)
        db.cursor.execute(f"UPDATE wallets SET free_funds=free_funds + {sharesCount1*price} WHERE wallet_id = {walletId};")
        db.mTrader_db.commit()
        if result[0] == sharesCount1:
            db.cursor.execute(f"DELETE FROM `shares` WHERE SYMBOL = '{symbol.get()}' AND WALLET_ID = {walletId}")
            db.mTrader_db.commit()
        else:
            db.cursor.execute(f"UPDATE `shares` SET `COUNT`=`COUNT` - {sharesCount1} WHERE WALLET_ID = '{walletId}' AND SYMBOL = '{symbol.get()}'")
            db.mTrader_db.commit()
        oWindow.destroy()
        messagebox.showinfo("Akcje zostały sprzedane", f"Akcje spółki {symbol.get()} zostały sprzedane po cenie: {price} zł.")
        
    else:
        messagebox.showerror("Błąd",f"Za duża ilość akcji\nTwoja liczba akcji {symbol.get()} to: {result[0]}")
        pb.grid_forget()
        lf.grid(column=0, row=0, sticky=tk.N, padx=10, pady=10)
        f2.grid(column=0, row=1)
def pbF():
    f1.grid_forget()
    f2.grid_forget()
    lf.grid_forget()
    global pb
    pb = Progressbar(oWindow, mode="indeterminate", length=200, orient="horizontal")
    pb.grid(column=0, row=0, pady=80)
    pb.start(20)
    
def calculateBtn():
    t1 = threading.Thread(target=pbF)
    t2 = threading.Thread(target=calculatePrice)
    t1.start()
    t2.start()
def buyBtn():
    t1 = threading.Thread(target=pbF)
    t2 = threading.Thread(target=createOperation)
    t1.start()
    t2.start()
def sellBtn():
    t1 = threading.Thread(target=pbF)
    t2 = threading.Thread(target=sell)
    t1.start()
    t2.start()