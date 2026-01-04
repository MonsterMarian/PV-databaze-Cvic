# Příprava připojení do databáze Microsoft SQL Server Express

## Požadavky na absolvování

### 1. Vytvoření databáze a aplikačního uživatelského účtu

Nejprve je třeba si nainstalovat databázi **Microsoft SQL Server Express**. Pokud jste ve škole na cvičení, použijte připravenou instalaci MSSQL.

Připojíte se pomocí programu **Microsoft SQL Server Management Studio** pomocí následujících přístupových údajů, kde PC000 nahradíte skutečným jménem databázového serveru:
- SERVER TYPE: Database engine
- SERVER NAME: PC000
- AUTHENTICATION: SQL Server authentication
- LOGIN: sa
- PASSWORD: student

Následně je třeba vytvořit novou databázi, což nejrychleji uděláte v záložce "Object explorer" v pravém sloupci, kde ve složce "Databases" pravým tlačítkem zvolíte možnost "New database" a následně vytvořte databázi s parametry:
- DATABASE NAME: app1
- A potvrďte tlačítkem "OK".

Dále je třeba vytvořit aplikační uživatelský účet, který vytvoříte ve složce "Security" a podsložce "Logins" kliknutím na pravé tlačítko a zvolením "New login". Nového uživatele vytvořte s těmito parametry:
- LOGIN NAME: app1user
- AUTHENTICATION: SQL Server authentication
- PASSWORD: student
- USER MUST CHANGE PASSWORD: no
- DEFAULT DATABASE: app1

A v záložce vpravo označené jako "User mapping" pak nastavte mapování mezi databází app1 a oprávněním, nejlépe: db_owner. Vše uložíte tlačítkem "OK".

Spojení otestujte tak, že kliknete v Microsoft SQL Server Management Studio v záložce "Object explorer" znovu kliknete na tlačítko "Connect" a vytvoříte druhé připojení pomocí tohoto uživatele.

Doporučujeme vytvořit si pak jednu tabulku a otestovat CRUD nad touto tabulkou.

### 2. Instalace connectoru/driveru pro Python

Název python package: **pyodbc**

Link dokumentace: https://docs.microsoft.com/en-us/sql/connect/python/python-driver-for-sql-server?view=sql-server-ver15

Pro instalaci na driveru na školním PC je nejprve nutné deaktivovat školní proxy server. To lze udělat kliknutím na tlačítko start a následně na nastavení (ozubené kolečko). Do vyhledávání napište "Změnit nastavení proxy serveru" a v části "Ruční nastavení proxy serveru" u volby "Používat proxy server" zvolte vypnuto.

Dále je třeba doinstalovat connector/driver pro MySQL na připojení do databáze pomocí jazyka Python. K tomu slouží instalační manager jazyka Python, který se jmenuje pip.

### 3. Varianta PyCharm
Pokud používáte PyCharm s vlastním venv, stačí si spustit terminal a napsat příkaz:
```
pip install pyodbc
```
Nebo můžete použít variantu pro ostatní níže, ale při vytváření projektu musíte zaškrtnout políčko "Inherit global site packages"

### 4. Varianta VStudio a ostatní:
Pokud používáte Python bez venv, například pomocí Visual Studio Code, nebo z příkazové řádky použijte v příkazové řádce příkaz:
```
pip install --user pyodbc
```

## 5. Testovací skript

V adresáři projektu jsou dva skripty:

1. `basic_connection.py` - Základní připojovací skript podle zadání
2. `database_connection.py` - Rozšířený skript s funkcí pro testování CRUD operací

### Použití:
1. Nahraďte "PC000" ve skriptu skutečným jménem databázového serveru
2. Spusťte skript pomocí Pythonu: `python database_connection.py`

Poznámka: Skripty předpokládají, že:
- Databáze `app1` existuje
- Uživatel `app1user` s heslem `student` má přístup
- Je nainstalován ODBC Driver 17 pro SQL Server

## Důležité informace pro testování:
- Před spuštěním skriptů je třeba mít připravený SQL Server s odpovídající databází a uživatelem
- Pokud se při spuštění objeví chyba spojení, zkontrolujte správnost názvu serveru, přihlašovacích údajů a dostupnost SQL Serveru