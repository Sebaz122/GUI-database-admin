import psycopg2 as ps
import os
from tkinter import *  
from tkinter import ttk
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
    top=Toplevel(root)
    cursor.execute(f"SELECT * FROM  {table_name}")
    dataset = cursor.fetchall()
    total_rows = len(dataset)
    total_cols = len(dataset[0])
    top.geometry=(f"{total_cols*80}x{root.winfo_screenheight()}")
    canvas = Canvas(top, borderwidth=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    h=Scrollbar(top, orient="vertical", command=canvas.yview)
    h.pack(side=RIGHT, fill=Y)
    table_frame=Frame(canvas)
    canvas.create_window((0, 0), window=table_frame, anchor="nw")
    column_names=fetch_table_columns(cursor, table_name)

    for j in range(total_cols):
        header = Label(table_frame, text=f"{column_names[j]}", font=('Arial', 12, 'bold'), background="lightblue")
        header.grid(row=0, column=j, sticky="NEWS")
        
    for i in range(total_rows):
        for j in range(total_cols):
            e = Entry(table_frame, width=20, fg='blue',
                      background="lightblue", font=('Arial', 12))
            e.grid(row=i+1, column=j, sticky="NEWS")
            e.insert(END, dataset[i][j])
    table_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.configure(yscrollcommand=h.set)


def edit_record(root,cursor, conn):

    def create_form(selected_table):
        for widget in top.winfo_children():
            widget.destroy()
        columns = fetch_table_columns(cursor, selected_table)
        Label(top, text=f"Podaj id rekordu który chcesz edytować z tabeli: {selected_table}", font=("Arial", 12, "bold")).pack()
        entries.clear()
        Label(top, text=columns[0]).place(x=10,y=30)
        entry_id=Entry(top)
        entry_id.place(x=140,y=30)
        button_id=Button(top, text="Wyszukaj rekord", command=lambda: clear_and_create(top, columns, entry_id.get(), selected_table))
        button_id.place(x=10,y=70)

    def clear_and_create(top, columns, entry_id, selected_table):
        for widget in top.winfo_children():
            widget.destroy()
        if entry_id:
            cursor.execute(f"SELECT * FROM {selected_table} WHERE {columns[0]} = {entry_id}")
            record=cursor.fetchone()
            if record:
                for idx, column in enumerate(columns[1:]):
                    Label(top, text=column).place(x=10, y=10 + idx * 40 + 20)
                    entry = Entry(top)
                    entry.place(x=140, y=10 + idx * 40 + 20)
                    entry.insert(END, record[idx+1])
                    entries[column] = entry
                button_add = Button(top, text="Edytuj rekord", command= lambda: save_record(top, selected_table, columns, entry_id))
                button_add.place(x=10, y=10 + len(columns) * 30 + 70)
            else:
                Label(top, text="Rekord nie został znaleziony")
        else:
            Label(top, text="Podaj ID rekordu")

    def save_record(top, table_name, columns, record_id):
        data = {col: entries[col].get() for col in columns[1:]}  
        updates = ', '.join([f"{col} = %s" for col in columns[1:]]) 
        values = list(data.values()) + [record_id] 
        try:
            cursor.execute(f"UPDATE {table_name} SET {updates} WHERE {columns[0]} = %s;", values)
            conn.commit()
            Label(top, text="Rekord zaktualizowany pomyślnie!", fg="green").place(x=10, y=10 + len(columns) * 40 + 70)
        except Exception as e:
            Label(top, text=f"Błąd: {str(e)}", fg="red").place(x=10, y=10 + len(columns) * 40 + 70)
    
        

    def select_table():
        selected_table = table_name_var.get()
        if selected_table:
            create_form(selected_table)

    top = Toplevel(root)
    top.geometry("400x400")
    top.attributes('-topmost')
    cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
    tables = [row[0] for row in cursor.fetchall()]
    Label(top, text="Wybierz tabelę:").pack()
    table_name_var = StringVar()
    table_menu = OptionMenu(top, table_name_var, "", *tables)
    table_menu.pack()
    Button(top, text="Wybierz tabelę", command=select_table).pack()
    entries={}

def delete_record(root, cursor,conn):
    ...

def print_any_table(root, cursor):
    def select_table():
        selected_table = table_name_var.get()
        if selected_table:
            print_table(top, cursor, selected_table)
    top = Toplevel(root)
    top.geometry("400x400")
    top.attributes('-topmost')
    cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
    tables = [row[0] for row in cursor.fetchall()]
    Label(top, text="Wybierz tabelę:").pack()
    table_name_var = StringVar()
    table_menu = OptionMenu(top, table_name_var, "", *tables)
    table_menu.pack()
    Button(top, text="Wybierz tabelę", command=select_table).pack()




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

def sum_costs(root,cursor):
    cursor.execute("SELECT suma_ceny_zamowien();")
    data=cursor.fetchall()
    Label(root, text=f"{data}").place(x=300,y=300)
    print(str(data[0]))

if __name__ == "__main__":
    load_dotenv()
    # Simple window
    root = Tk()
    root.title("Database GUI")
    root.configure(bg="lightgray")
    window_center(root)
    ###
    connection = load_database()
    cursor = connection.cursor()
    set_path(cursor)
    # Dividing root frame to parts and placing them
    left_frame = Frame(root, width=root.winfo_screenwidth(), height=400, background="crimson")
    left_frame.place(x=0,y=0)
    bottom_frame = Frame(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), background="gray")
    bottom_frame.place(x=0,y=420)
    # Table_test

    
    button1=Button(left_frame, text="Pokaż tabelę", command=lambda: print_any_table(root,cursor))
    button2 = Button(left_frame, text="Dodaj rekord", command=lambda: add_record(root, cursor, connection))
    button3 = Button(left_frame, text="Pokaż widok(td)", command=lambda: print_table(root,cursor,"zamowienie_szczegoly"))
    button4=Button(left_frame, text="Suma kosztow wszystkich zamowien", command=lambda: sum_costs(root,cursor))
    button5 = Button(left_frame, text="Edytuj rekord",command=lambda: edit_record(root, cursor, connection))
    button6=Button(left_frame, text="Usuń rekord", command=lambda: delete_record(root, cursor, connection))
    button1.place(x=50,y=25)
    button2.place(x=50, y=75)
    button3.place(x=50,y=125)
    button4.place(x=50,y=175)
    button5.place(x=50,y=225)
    button6.place(x=50,y=275)
    root.mainloop()
