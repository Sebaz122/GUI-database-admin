import matplotlib.pyplot as plt
from tkinter import *
import psycopg2 as ps

def plot_sales_per_month(cursor):
    query = """
        SELECT 
            DATE_TRUNC('month', data_zamowienia) AS sale_month,
            COUNT(*) AS sales_count
        FROM zamowienia
        GROUP BY sale_month
        ORDER BY sale_month;
    """
    cursor.execute(query)
    data=cursor.fetchall()
    months = [row[0].strftime('%Y-%m') for row in data]
    sales_counts = [row[1] for row in data]
    plt.figure(figsize=(10, 6))
    plt.bar(months, sales_counts, color='skyblue', edgecolor='black')
    plt.title('Ilość zamówień na miesiąc i rok')
    plt.xlabel('Miesiąc i rok')
    plt.ylabel('Ilość zamówień')
    plt.show()

def generate_sales_report(cursor):
    query = """
        SELECT 
            p.nazwa_produktu, 
            COUNT(d.id_produktu) AS liczba_sprzedazy
        FROM produkty p
        JOIN dane_zamowien d ON p.produkt_id = d.id_produktu
        GROUP BY p.nazwa_produktu
        ORDER BY liczba_sprzedazy DESC;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    product_names = [row[0] for row in data]
    sales_counts = [row[1] for row in data]
    plt.figure(figsize=(12, 6))
    plt.bar(product_names, sales_counts, color='skyblue')
    plt.xlabel('Nazwa produktu')
    plt.ylabel('Ilość zamówień')
    plt.title('Ilość zamówień danego produktu')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.show()

def generate_payment_status_report(cursor):
    cursor.execute("SELECT procent_oplaconych_zamowien();")
    result = cursor.fetchone()
    percent_paid = float(result[0]) 
    percent_unpaid = 100 - percent_paid
    labels = ['Opłacone zamówienia', 'Nieopłacone zamówienia']
    sizes = [percent_paid, percent_unpaid]
    colors = ['green', 'crimson']
    plt.figure(figsize=(8, 6))
    plt.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors,
    )
    plt.title('Procent zamówień opłaconych i nieopłaconych', fontsize=14)
    plt.show()