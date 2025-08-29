import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

print("Contacts table:")
for row in cursor.execute("SELECT * FROM contacts"):
    print(row)

print("\nChat history table:")
for row in cursor.execute("SELECT * FROM chat_history"):
    print(row)

conn.close()
