import sqlite3

print("=" * 60)
print("DATABASE SETUP")
print("=" * 60)

conn = sqlite3.connect("mutual_fund.db")

with open("sql/schema.sql", "r") as file:
    schema = file.read()

conn.executescript(schema)

print("\nSUCCESS")
print("Database Created : mutual_fund.db")

conn.close()