import psycopg2 as ps
from tkinter import * 

def print_table(root, cursor, table_name):
    top=Toplevel(root)
    cursor.execute(f"SELECT * FROM  {table_name}")
    top.resizable(True,True)
    dataset = cursor.fetchall()
    total_rows = len(dataset)
    total_cols = len(dataset[0])
    top.geometry(f"{180*total_cols+120}x{20*total_rows}")
    #top.geometry=(f"{600}x{600}")
    canvas = Canvas(top, borderwidth=0)
    # canvas.pack(side=LEFT, fill=BOTH, expand=True)
    canvas.place(x=0, y=0, relwidth=0.9, relheight=0.9)
    h=Scrollbar(top, orient="vertical", command=canvas.yview)
    h.place(relx=0.9, rely=0, relheight=0.94)
    g=Scrollbar(top, orient="horizontal", command=canvas.xview)
    g.place(x=0, rely=0.9, relwidth=0.94)
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
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.configure(yscrollcommand=h.set)
    canvas.configure(xscrollcommand=g.set)

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
        Label(top, text=f"Dodawane rekordu do tabeli: {selected_table}", font=("Arial", 12, "bold")).pack()

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

def delete_record(root, cursor, conn):
    def select_table():
        selected_table = table_name_var.get()
        if selected_table:
            create_form(selected_table)

    def create_form(selected_table):
        for widget in top.winfo_children():
            widget.destroy()
        columns = fetch_table_columns(cursor, selected_table)
        id_col=columns[0]
        Label(top, text=f"Podaj id rekordu który chcesz USUNĄĆ z tabeli: {selected_table}", font=("Arial", 12, "bold")).pack()
        # entries.clear()
        Label(top, text=columns[0]).place(x=10,y=30)
        entry_id=Entry(top)
        entry_id.place(x=140,y=30)
        button_id=Button(top, text="Usuń rekord", command=lambda: delete(top, cursor, id_col,entry_id.get(), selected_table))
        button_id.place(x=10,y=70)
    def delete(top, cursor, id_col, entry_id, selected_table):
        try:
            cursor.execute(f"SELECT 1 FROM {selected_table} WHERE {id_col} = {entry_id}")
            result=cursor.fetchone()
            if not result:
                raise Exception
            cursor.execute(f"DELETE FROM {selected_table} WHERE {id_col} = {entry_id}")
            conn.commit()
            top.update_idletasks()
            success_label=Label(top, text="Rekord został usunięty!", fg="green")
            success_label.pack(side=BOTTOM)
            top.after(3000, success_label.destroy)
        except Exception:
            error_label=Label(top, text=f"Błąd: Nie ma podanego rekordu", fg="red")
            error_label.pack(side=BOTTOM)
            top.after(3000, error_label.destroy)

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
        cursor.execute(f"SELECT 1 FROM {selected_table} WHERE {columns[0]} = {entry_id}")
        result=cursor.fetchone()
        if not result:
            error_label=Label(top, text="Rekord nie został znaleziony", fg="red")
            error_label.pack(side=BOTTOM)
            top.after(3000, error_label.destroy)
        elif result:
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