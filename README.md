# D1 - E-COMMERCE APLIKACE

## DŮLEŽITÉ INFORMACE
  
**📚 ŠKOLNÍ PROJEKT - SPLŇUJE VŠECHNA ZADÁNÍ**  

## KLÍČOVÉ CHARAKTERISTIKY (D1 ZADÁNÍ)

✅ **HLAVNÍ ÚKOL D1 SPLNĚN:** Vlastní implementace Repository patternu  
✅ **RELACNI DATABÁZE:** Microsoft SQL Server Express  
✅ **STRUKTURA:** 7 tabulek, 2 pohledy, M:N vazby  
✅ **DATOVÉ TYPY:** Všechny požadované (Real, Boolean, Enum, String, DateTime)  
✅ **MULTI-TABULKOVÉ OPERACE:** Jeden formulář → data do více tabulek  
✅ **TRANSKACE:** Atomické operace nad více tabulkami  
✅ **REPORTY:** Agregovaná data z 3+ tabulek  
✅ **IMPORT:** CSV, XML, JSON do 2+ tabulek  
✅ **KONFIGURACE:** JSON soubor + runtime změny  
✅ **ERROR HANDLING:** Komplexní validace a chybové stavy  

## ARCHITEKTURA (D1 PATTERN)

```
UI VRSTVA (console_ui.py)
    ↓
SERVISNÍ VRSTVA (business logika, transakce, reporty)
    ↓
REPOSITORY VRSTVA (D1 - Repository Pattern)
    ↓
DATABÁZOVÁ VRSTVA (SQL Server)
```

**IMPLEMENTOVANÉ REPOSITORY ROZHRANÍ:**
- `IRepository` - základní CRUD operace
- `ICustomerRepository` - specifické metody pro zákazníky
- `IProductRepository` - specifické metody pro produkty  
- `IOrderRepository` - specifické metody pro objednávky

**KONKRÉTNÍ IMPLEMENTACE:**
- `CustomerRepository`, `ProductRepository`, `OrderRepository`
- `BaseRepository` - společné databázové operace
- `RepositoryFactory` - továrna na repozitáře

## INSTALACE A SPUŠTĚNÍ

### 🔧 POŽADAVKY:
- Microsoft SQL Server Express
- Python 3.8+
- pyodbc knihovna

### ⚡ RYCHLÁ INSTALACE:
```bash
1. Nainstalujte SQL Server Express
2. Vytvořte databázi app1 a uživatele app1user
3. Spusťte database_schema.sql
4. pip install pyodbc
5. Upravte config.json s vaším názvem serveru
6. python console_ui.py
```

### 📖 DETAILNÍ PRŮVODCE:
Kompletní instalační průvodce najdete v: `dokumentace/instalacni_pruvodce_cz.md`

## HLAVNÍ FUNKCE

```
🏪 1. Správa zákazníků     - CRUD operace se zákazníky
📦 2. Správa produktů      - CRUD operace s produkty  
🛒 3. Správa objednávek    - Objednávky (multi-tabulka)
💱 4. Transakce            - Transakce (atomické)
📊 5. Reporty              - Reporty (agregace 3+ tabulek)
📥 6. Import dat           - Import CSV/XML/JSON
⚙️  7. Konfigurace         - Nastavení aplikace
```

## KLÍČOVÉ FUNKCE SPLŇUJÍCÍ ZADÁNÍ

### 🔀 MULTI-TABULKOVÉ OPERACE (Bod 4):
**Vytvoření objednávky = JEDEN FORMULÁŘ → VÍCE TABULEK**
- Validace zákazníka (Customers)
- Validace produktů (Products)  
- Vytvoření objednávky (Orders)
- Vytvoření položek (OrderItems)
- Automatický výpočet celkové částky

### 🔄 TRANSKACE (Bod 5):
**Převod kreditu = ATOMICKÁ OPERACE**
- Odečtení z účtu A (Customers)
- Připsání na účet B (Customers)
- Zalogování transakce (TransactionLog)
- **Vše nebo nic - ACID principy**

### 📊 REPORTY (Bod 6):
**Sales Summary = AGREGACE 3+ TABULEK**
- Customers + Orders + OrderItems
- Produkty + Kategorie + Položky + Objednávky
- Měsíční statistiky z více tabulek

### 📤 IMPORT (Bod 7):
**Podpora všech formátů do 2+ tabulek:**
- CSV → Customers, Products
- XML → Customers, Products  
- JSON → Customers, Products

## DŮKAZY SPLNĚNÍ ZADÁNÍ

| Požadavek | Splněno | Umístění |
|-----------|---------|----------|
| D1 Repository Pattern | ✅ | repositories/, dokumentace/D1_dokumentace.md |
| Relační databáze | ✅ | database_schema.sql |
| 5+ tabulek | ✅ (7 tabulek) | database_schema.sql |
| 2 pohledy | ✅ | database_schema.sql |
| M:N vazby | ✅ | OrderItems, ProductSuppliers tabulky |
| Všechny datové typy | ✅ | database_schema.sql |
| Multi-tabulka operace | ✅ | services/multi_table_services.py |
| Transakce | ✅ | transactions/transaction_manager.py |
| Reporty 3+ tabulek | ✅ | reports/report_service.py |
| Import 2+ tabulek | ✅ | data_import/data_import_service.py |
| Konfigurace | ✅ | config/config_manager.py |
| Error handling | ✅ | error_handling/error_handler.py |

## TECHNICKÉ DETAILY

### 🛡️ BEZPEČNOST:
- Validace všech vstupů
- Parametrizované SQL dotazy
- Oddělení práv uživatelů
- Error handling bez expozice systému

### 🧪 TESTOVÁNÍ:
- 5 komplexních testovacích scénářů
- Automatické testy připojení
- Validace všech chybových stavů



## STATUS PROJEKTU

🟢 **PROJEKT JE PLNĚ FUNKČNÍ A SPLŇUJE VŠECHNA ZADÁNÍ**  
🟢 **PŘIPRAVEN PRO ODEVZDÁNÍ A TESTOVÁNÍ NA ŠKOLNÍM PC**  
🟢 **VŠECHNY DOKUMENTY A TESTY PŘIPRAVENY**

## DOKUMENTACE PROJEKTU

📁 **VSECHNY DOKUMENTY V ADRESARI dokumentace/:**

**Hlavní dokumentace:**
- `D1_dokumentace.md` - Dokumentace Repository patternu (D1)
- `kompletni_dokumentace.md` - Kompletní technická dokumentace

**Průvodci:**
- `instalacni_pruvodce.md` - Detailní instalační průvodce
- `testovaci_scenare.md` - Kompletní testovací scénáře

## FINÁLNÍ KROKY PŘED ODEVZDÁNÍM

1. **Převod dokumentace do PDF:**
   - dokumentace/D1_dokumentace.md → PDF
   - dokumentace/kompletni_dokumentace.md → PDF
   - dokumentace/instalacni_pruvodce.md → PDF
   - dokumentace/testovaci_scenare.md → PDF

2. **Vytvoření ZIP archivu s projektem**

3. **Aktualizace config.json:**
   - Nahraďte "PC000" skutečným názvem vašeho serveru

## PRO TESTERY - NÁVOD K POUŽITÍ

Kompletní návod pro testery najdete v souboru `NAVOD_PRO_TESTERA.md`

---
**⚠️ PŘED SPUŠTĚNÍM:** Aktualizujte "PC000" v config.json na skutečný název vašeho serveru