def mainFunction():
    import tkinter as tk
    from tkinter.ttk import Label, Notebook
    from tkinter import messagebox, Frame



    createWin = tk.Tk()
    createWin.grab_set()
    createWin.title("Ustawienia")
    createWin.resizable(0,0)
    """createWin.columnconfigure(0,weight=1)
    createWin.columnconfigure(1,weight=3)"""
    createWin.geometry('300x300')
    notebook = Notebook(createWin)
    notebook.pack(pady=10, expand=True)
    
    # create frames
    frame1 = Frame(notebook, width=400, height=280)
    frame2 = Frame(notebook, width=400, height=280)
    frame1.config(background="white")

    frame1.pack(fill='both', expand=True)
    frame2.pack(fill='both', expand=True)

    # add frames to notebook

    notebook.add(frame1, text='Portfel')
    notebook.add(frame2, text='Profile')



   

    createWin.mainloop()
mainFunction()