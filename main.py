import psycopg2 as ps
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    # Connecting to DB
    connection = ps.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    # Creating cursor and testing if it works properly
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH to kurs")
    cursor.execute("SELECT * FROM uczestnik")
    dataset = cursor.fetchall()
    for data in dataset:
        print(data)
