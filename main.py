import psycopg2 as ps
import os
from tkinter import *  
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import src.functions as f
import src.database_and_window as dw
import src.reports as r

def sum_costs(root,cursor):
    cursor.execute("SELECT suma_ceny_zamowien();")
    data=cursor.fetchall()
    Label(root, text=f"{data}").place(x=300,y=300)
    print(str(data[0]))



if __name__ == "__main__":

    root = Tk()
    root.title("Database GUI")
    root.configure(bg="lightgray")
    dw.window_center(root)
    connection = dw.load_database()
    cursor = connection.cursor()
    dw.set_path(cursor)
    left_frame = Frame(root, width=root.winfo_screenwidth(), height=400, background="crimson")
    left_frame.place(x=0,y=0)
    bottom_frame = Frame(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), background="gray")
    bottom_frame.place(x=0,y=420)

    
    button1=Button(left_frame, text="Pokaż tabelę", command=lambda: f.print_any_table(root,cursor))
    button2 = Button(left_frame, text="Dodaj rekord", command=lambda: f.add_record(root, cursor, connection))
    button3 = Button(left_frame, text="Edytuj rekord",command=lambda: f.edit_record(root, cursor, connection))
    button4=Button(left_frame, text="Usuń rekord", command=lambda: f.delete_record(root, cursor, connection))
    button5=Button(left_frame, text="Ilość opłaconych zamówień (procentowo)", command=lambda: r.generate_payment_status_report(cursor))
    button6=Button(left_frame, text="Ilość zamówień danego produktu", command=lambda: r.generate_sales_report(cursor))
    button7=Button(left_frame, text="Ilość zamówień na miesiąc", command=lambda: r.plot_sales_per_month(cursor))
    button9 = Button(left_frame, text="Zamowienia i szczegóły (widok)", command=lambda: f.print_table(root,cursor,"zamowienie_szczegoly"))
    button10 = Button(left_frame, text="Klienci i zamówienia (widok)", command=lambda: f.print_table(root,cursor,"klienci_i_ich_zamowienia"))
    button11 = Button(left_frame, text="Dostawcy i nadawcy (widok)", command=lambda: f.print_table(root,cursor,"dostawcy_i_nadawcy"))
    button1.place(x=50,y=25)
    button2.place(x=50, y=75)
    button3.place(x=50,y=125)
    button4.place(x=50,y=175)
    button5.place(x=50,y=225)
    button6.place(x=50,y=275)
    button7.place(x=250,y=25)
    button9.place(x=250,y=125)
    button10.place(x=250,y=175)
    button11.place(x=300,y=225)
    root.mainloop()
