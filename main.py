import psycopg2 as ps
import os
from tkinter import *  # To change- import * are bad habit
from dotenv import load_dotenv


def load_database():
    connection = ps.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return connection

def print_uczestnik(cursor):
    cursor.execute("SELECT * FROM uczestnik")
    dataset = cursor.fetchall()
    for data in dataset:
        print(data)

def set_path(cursor):
    cursor.execute("SET SEARCH_PATH to kurs")

def load_window():
    ...
    #May be done in function in future
def window_center(root):
    window_width=1280
    window_height=720
    screen_width=root.winfo_screenwidth()
    screen_height=root.winfo_screenheight()
    center_x=int((screen_width-window_width)/2)
    center_y=int((screen_height-window_height)/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

def print_uczestnik_on_screen(root,cursor):
    cursor.execute("SELECT * FROM uczestnik")
    dataset=cursor.fetchall()
    total_rows=len(dataset)
    total_cols=len(dataset[0])
    for i in range(total_rows):
        for j in range(total_cols):
            e=Entry(root, width=20, fg='blue', background="lightblue", font=('Arial', 16 , 'bold'))
            e.grid(row=i, column=j, sticky="NEWS")
            e.insert(END,dataset[i][j])


if __name__ == "__main__":
    load_dotenv()
    ### Simple window
    root = Tk()
    root.title("Shop simulation")
    root.configure(bg="lightblue")
    window_center(root) 
    ###
    connection = load_database()
    cursor = connection.cursor()
    set_path(cursor)
    #print_uczestnik(cursor)
    button1= Button(root, text="Wyprintuj uczestników kursu", command=lambda:print_uczestnik_on_screen(root,cursor))
    button1.place(x=50,y=50)
    root.mainloop()
    
    
