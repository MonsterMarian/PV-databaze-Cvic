import pyodbc

def connect_to_database(server_name, database_name='app1', username='app1user', password='student'):
    """
    Funkce pro připojení k databázi Microsoft SQL Server
    
    Args:
        server_name (str): Jméno databázového serveru
        database_name (str): Název databáze (výchozí: app1)
        username (str): Uživatelské jméno (výchozí: app1user)
        password (str): Heslo (výchozí: student)
    
    Returns:
        connection: Připojení k databázi
    """
    try:
        # Vytvoření připojovacího řetězce
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}'
        
        # Připojení k databázi
        connection = pyodbc.connect(connection_string)
        
        print("Připojeno k databázi úspěšně.")
        
        return connection
        
    except pyodbc.Error as e:
        print(f"Chyba při připojení k databázi: {e}")
        return None

def test_crud_operations(connection):
    """
    Funkce pro testování CRUD operací na jednoduché tabulce
    """
    try:
        cursor = connection.cursor()
        
        # Vytvoření testovací tabulky
        create_table_query = """
        IF NOT EXISTS (
            SELECT * FROM sysobjects 
            WHERE name='test_table' AND xtype='U'
        )
        CREATE TABLE test_table (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(50),
            value INT
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabulka vytvořena (nebo již existovala).")
        
        # INSERT operace
        cursor.execute("INSERT INTO test_table (name, value) VALUES (?, ?)", ("Testovací záznam", 123))
        connection.commit()
        print("Záznam vložen.")
        
        # SELECT operace
        cursor.execute("SELECT * FROM test_table")
        rows = cursor.fetchall()
        print("Data z tabulky:")
        for row in rows:
            print(f"  ID: {row.id}, Název: {row.name}, Hodnota: {row.value}")
        
        # UPDATE operace
        cursor.execute("UPDATE test_table SET value = ? WHERE name = ?", (456, "Testovací záznam"))
        connection.commit()
        print("Záznam aktualizován.")
        
        # Opětovné čtení pro ověření
        cursor.execute("SELECT * FROM test_table")
        rows = cursor.fetchall()
        print("Aktualizovaná data:")
        for row in rows:
            print(f"  ID: {row.id}, Název: {row.name}, Hodnota: {row.value}")
        
        # DELETE operace
        cursor.execute("DELETE FROM test_table WHERE name = ?", ("Testovací záznam",))
        connection.commit()
        print("Záznam smazán.")
        
    except pyodbc.Error as e:
        print(f"Chyba při práci s databází: {e}")

if __name__ == "__main__":
    # Zadejte skutečné jméno databázového serveru místo PC000
    server_name = "PC000"  # Toto je potřeba změnit na skutečné jméno serveru
    
    print("Připojuji se k databázi...")
    connection = connect_to_database(server_name)
    
    if connection:
        print("Testuji CRUD operace...")
        test_crud_operations(connection)
        
        # Uzavření připojení
        connection.close()
        print("Připojení uzavřeno.")
    else:
        print("Nepodařilo se připojit k databázi.")