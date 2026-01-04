import pyodbc

# Základní připojovací skript podle zadání
# Poznámka: Místo PC000 je třeba doplnit skutečné jméno databázového serveru

connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=PC000;DATABASE=app1;UID=app1user;PWD=student')

print("Připojeno.")

connection.close()