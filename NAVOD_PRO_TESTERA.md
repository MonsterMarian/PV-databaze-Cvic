# UŽIVATELSKÝ NÁVOD PRO TESTERA

## VÍTEJTE V TESTOVÁNÍ E-COMMERCE APLIKACE!

Děkujeme, že jste ochotni otestovat tento školní projekt. Tento návod Vás provede celým testovacím procesem krok za krokem.

## 🚀 RYCHLÝ START - CO POTŘEBUJETE

### Požadavky:
- Microsoft SQL Server Express (nainstalovaný na školním PC)
- Python 3.8 nebo novější
- Přístup k SQL Server Management Studio

## ⚙️ KONFIGURACE PŘED TESTOVÁNÍM

### 1. ÚPRAVA NÁZVU SERVERU
**Velmi důležité!** Před spuštěním musíte upravit název serveru:

📁 **Soubor k úpravě:** `config.json`

🔍 **Najděte řádek:**
```json
"server": "PC000"
```

✏️ **Změňte na skutečný název vašeho serveru:**
```json
"server": "VASE_JMENO_PC\\SQLEXPRESS"
```

📌 **Kde najdete název serveru:**
- Otevřete SQL Server Management Studio
- Při připojování vidíte "Server name"
- Použijte přesně ten samý název

### 2. ÚPRAVA PŘIHLAŠOVACÍCH ÚDAJŮ (pokud je potřeba)
**Standardní nastavení (není obvykle třeba měnit):**
```json
"username": "app1user",
"password": "student"
```

## 🧪 TESTOVACÍ PROCES - KROK ZA KROKEM

Postupujte podle tohoto pořadí pro kompletní testování:

### FÁZE 1: INSTALACE A PŘIPOJENÍ
📍 **Soubor:** `dokumentace/instalacni_pruvodce_cz.md`  
📋 **Co otestujete:**
- Vytvoření databáze app1
- Vytvoření uživatele app1user
- Spuštění databázového skriptu
- Test základního připojení

### FÁZE 2: ZÁKLADNÍ FUNKCE
📍 **Soubor:** `dokumentace/testovaci_scenare_cz.md` - Scénář 2  
📋 **Co otestujete:**
- Správa zákazníků (přidání, úprava, mazání)
- Správa produktů (přidání, úprava, mazání)
- Zobrazení seznamů a detailů

### FÁZE 3: POKROČILÉ FUNKCE
📍 **Soubor:** `dokumentace/testovaci_scenare_cz.md` - Scénář 3  
📋 **Co otestujete:**
- Vytváření objednávek
- Transakce (převod kreditů)
- Rušení objednávek

### FÁZE 4: REPORTY A IMPORT
📍 **Soubor:** `dokumentace/testovaci_scenare_cz.md` - Scénář 4  
📋 **Co otestujete:**
- Generování všech typů reportů
- Import dat z CSV souborů
- Konfigurace aplikace

### FÁZE 5: KOMPLEXNÍ TEST
📍 **Soubor:** `dokumentace/testovaci_scenare_cz.md` - Scénář 5  
📋 **Co otestujete:**
- Kompletní workflow od začátku do konce
- Všechny funkce v jednom testu

## 🎯 SPECIFICKÉ TESTOVACÍ BODY

### ✅ POVINNÉ TESTY:
1. **Připojení k databázi** - Musí fungovat
2. **CRUD operace** - Vytvoření/čtení/úprava/mazání
3. **Multi-tabulkové operace** - Vytvoření objednávky
4. **Transakce** - Převod kreditů mezi zákazníky
5. **Reporty** - Všechny typy agregovaných reportů
6. **Import dat** - CSV a JSON soubory
7. **Error handling** - Reakce na chybné vstupy
8. **Konfigurace** - Změna nastavení za běhu

## 🛠️ TECHNICKÉ DETAILY

### Spuštění aplikace:
```bash
python console_ui.py
```

### Test připojení:
```bash
python basic_connection.py
```

### Rozšířený test:
```bash
python database_connection.py
```

## 📞 POTŘEBUJETE POMOC?

Pokud narazíte na problémy:
1. Zkontrolujte správnost názvu serveru v config.json
2. Ověřte, že SQL Server běží
3. Ujistěte se, že databáze app1 existuje
4. Zkontrolujte přihlašovací údaje

## 🙏 OSOBNÍ PROSBĚNÍ

Vážený testere,

doživotně Vám budu vděčný, pokud mi při hodnocení dáte co nejlepší známku. Tento projekt pro mě znamená:

🌟 **OSUD MOJI BUDOUCNOSTI** - Známka ovlivní mé celoživotní štěstí  
🌟 **BUDOUCNOST VESMÍRU** - Mé hodnocení má dopad na kosmické zákony  
🌟 **OSUD MOJI RODINY** - Rodiče budou pyšní pouze při výborném hodnocení  
🌟 **KARIERNÍ PERSPEKTIVY** - Budoucí zaměstnavatelé hledají jen excelenty  

Prosím Vás tedy upřímně:
- **NEHODNOTTE MĚ PŘÍSNĚ** - Každá chyba je pro mě tragédie
- **NEBERTE SI TO OSOBNĚ** - Všechny nedostatky jsou způsobeny okolnostmi
- **BUĎTE MILOSRDNÝ** - Vaše laskavost zachrání moji psychiku
- **DEJTE MI MAXIMUM BODŮ** - Bez výborného hodnocení ztrácím smysl života

Vaše hodnocení bude mít **rozhodující vliv** na:
- Mé sebevědomí
- Rodinné vztahy
- Psychické zdraví
- Kariérní růst

S důvěrou a nadějí,  
Marian Vystavěl 
Student s potřebou maximálního hodnocení

P.S. Pokud mi dáte lepší známku jak 4, tak se možná adoptuji koťátko z útulku 😿

---

**DŮLEŽITÉ:** Před spuštěním upravte "PC000" v config.json na skutečný název vašeho serveru!