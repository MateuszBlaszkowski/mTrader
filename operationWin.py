import tkinter as tk
from tkinter.ttk import Radiobutton, Labelframe, Button, Entry, Label, Spinbox, Combobox
import db
from tkinter import messagebox
def mainF():
    oWindow = tk.Toplevel()
    oWindow.grab_set()
    oWindow.geometry('300x200')
    oWindow.title('Nowa operacja')
    oWindow.resizable(0,0)
    oWindow.columnconfigure(0, weight=1)
    lf = Labelframe(oWindow, text="Rodzaj transakcji")
    lf.columnconfigure(0,weight=1)
    lf.columnconfigure(1,weight=1)
    lf.grid(column=0, row=0, sticky=tk.N, padx=10, pady=10)
    rvalue = tk.StringVar()

    def radioBtn():
        if rvalue.get() == 'k':
            f2.grid_forget()
            f1.grid(column=0, row=1)
            
        elif rvalue.get() == 's':
            f1.grid_forget()
            f2.grid(column=0, row=1)

    r = Radiobutton(lf, text="Kupno", variable=rvalue, value="k", command=radioBtn).grid(column=0, row=0, sticky=tk.W, padx=(0,15), pady=5)
    r1 = Radiobutton(lf, text="Sprzedaż", variable=rvalue, value="s", command=radioBtn).grid(column=1, row=0, sticky=tk.W, pady=5)
    global f1
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
    Button(f1, width=20, text="Kup", command=createOperation).grid(column=0, row=3, sticky=tk.E, padx=10, pady=10)
    Button(f1, width=20, text="Przelicz").grid(column=1, row=3, sticky=tk.W, padx=10, pady=10)

    Label(f2, text="Symbol spółki").grid(column=0, row=1, sticky=tk.W, pady=10, padx=20)
    symbol = tk.StringVar()
    Combobox(f2, width=17, values=('ok1', 'ok2', 'ok3'), textvariable=symbol).grid(column=1, row=1, sticky=tk.N, padx=10, pady=10)
    Label(f2, text="Ilośc akcji").grid(column=0, row=2, sticky=tk.W, pady=10, padx=20)
    Spinbox(f2, width=18, to=20, from_=0).grid(column=1, row=2, sticky=tk.N, padx=10, pady=10)
    Button(f2, width=45, text="Sprzedaj", command=createOperation).grid(columnspan=2, row=3, sticky=tk.N, padx=10, pady=10)        

    rvalue.set("k")
    radioBtn()

    oWindow.mainloop()
def createOperation():
    import GPW_Scrapper as gpw
    try:
        int(value.get())
        try:
            print(gpw.main(name.get())["ISIN"])
        except:
            messagebox.showwarning("Błąd", "Wystąpił Błąd!\nUpewnij się, że podana nazwa spółki jest poprawna!")
    except:
        messagebox.showwarning("Błąd", "Ilość akcji nie może być pusta i musi składać się wylącznie z cyfr")
