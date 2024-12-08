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
    cursor.execute("SET SEARCH_PATH to public")


def window_center(root):
    window_width = 1280
    window_height = 720
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width-window_width)/2)
    center_y = int((screen_height-window_height)/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


def print_table(root, cursor, table_name):
    cursor.execute(f"SELECT * FROM  {table_name}")
    dataset = cursor.fetchall()
    total_rows = len(dataset)
    total_cols = len(dataset[0])
    for i in range(total_rows):
        for j in range(total_cols):
            e = Entry(root, width=20, fg='blue',
                      background="lightblue", font=('Arial', 16, 'bold'))
            e.grid(row=i, column=j, sticky="NEWS")
            e.insert(END, dataset[i][j])




def fetch_table_columns(cursor, table_name, schema='public'):
    # return - Lista nazw kolumn
    query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s AND table_schema = %s;
    """
    cursor.execute(query, (table_name, schema))
    return [row[0] for row in cursor.fetchall()]


def add_record(root, cursor, conn):

    def select_table():
        selected_table = table_name_var.get()
        if selected_table:
            create_form(selected_table)

    def create_form(selected_table):
        for widget in top.winfo_children():
            widget.destroy()
        columns = fetch_table_columns(cursor, selected_table)
        Label(top, text=f"Adding to table: {selected_table}", font=("Arial", 12, "bold")).pack()

        entries.clear()
        for idx, column in enumerate(columns):
            Label(top, text=column).place(x=10, y=10 + idx * 40 + 20)
            entry = Entry(top)
            entry.place(x=140, y=10 + idx * 40 + 20)
            entries[column] = entry

        button_add = Button(top, text="Dodaj rekord", command=lambda: save_record(selected_table, columns))
        button_add.place(x=10, y=10 + len(columns) * 30 + 40)

    def save_record(table_name, columns):
        data = {col: entries[col].get() for col in columns}
        columns_str = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())
        try:
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders});", values)
            conn.commit()
            Label(top, text="Record added successfully!", fg="green").place(x=10, y=10 + len(columns) * 40 + 40)
        except Exception as e:
            Label(top, text=f"Error: {str(e)}", fg="red").place(x=10, y=10 + len(columns) * 40 + 40)

    top = Toplevel(root)
    top.geometry("400x400")
    top.attributes('-topmost', True)
    cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
    tables = [row[0] for row in cursor.fetchall()]
    Label(top, text="Wybierz tabelę:").pack()
    table_name_var = StringVar()
    table_menu = OptionMenu(top, table_name_var, "", *tables)
    table_menu.pack()
    Button(top, text="Wybierz tabelę", command=select_table).pack()
    entries = {}

if __name__ == "__main__":
    load_dotenv()
    # Simple window
    root = Tk()
    root.title("Database GUI")
    root.configure(bg="lightblue")
    window_center(root)
    ###
    connection = load_database()
    cursor = connection.cursor()
    set_path(cursor)
    # Dividing root frame to parts and placing them
    left_frame = Frame(root, width=200, height=200, background="crimson")
    left_frame.pack(side=LEFT)
    right_frame = Frame(root, width=800, height=500, background="lightgreen")
    right_frame.pack(side=RIGHT)
    # Table_test

    button1 = Button(left_frame, text="Wyprintuj uczestników kursu",command=lambda: print_table(right_frame, cursor, "pracownicy"))
    button2 = Button(left_frame, text="Dodaj rekord", command=lambda: add_record(root, cursor, connection))  
    button1.place(x=50, y=50)
    button2.place(x=100, y=100)
    root.mainloop()



    #printowanie tabeli i dodawanie rekordów dziala
