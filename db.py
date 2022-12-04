import mariadb
from tkinter import messagebox
try:
  mTrader_db = mariadb.connect(
      host="h26.seohost.pl",
      user="srv50655_mTrader",
      password="H1gHPsjdi0",
      database="srv50655_mTrader"
  )
except:
  messagebox.showerror("Błąd", "Nie można połączyć się z bazą")

cursor = mTrader_db.cursor()
