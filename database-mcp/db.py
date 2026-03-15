import sqlite3
connection = sqlite3.connect(database="sales.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        month TEXT,
        revenue INTEGER
    )
""")

cursor.execute("INSERT INTO sales VALUES ('January', 10000)")
cursor.execute("INSERT INTO sales VALUES ('February', 8500)")
cursor.execute("INSERT INTO sales VALUES ('March', 12000)")
cursor.execute("INSERT INTO sales VALUES ('April', 9700)")
cursor.execute("INSERT INTO sales VALUES ('May', 11200)")
cursor.execute("INSERT INTO sales VALUES ('June', 10000)")

connection.commit()

res = cursor.execute("SELECT * FROM sales")
db_data = res.fetchall()
print(db_data)