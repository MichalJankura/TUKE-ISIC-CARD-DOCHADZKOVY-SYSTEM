import pandas as pd
import time
from datetime import datetime, timedelta
from smartcard.System import readers
from smartcard.util import toHexString
from tabulate import tabulate
import msvcrt

# Banner to be printed at program start
banner = '''
██╗███████╗██╗ ██████╗    ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗    ████████╗██╗   ██╗██╗  ██╗███████╗
██║██╔════╝██║██╔════╝    ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║    ╚══██╔══╝██║   ██║██║ ██╔╝██╔════╝
██║███████╗██║██║         ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║       ██║   ██║   ██║█████╔╝ █████╗  
██║╚════██║██║██║         ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║       ██║   ██║   ██║██╔═██╗ ██╔══╝  
██║███████║██║╚██████╗    ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║       ██║   ╚██████╔╝██║  ██╗███████╗
╚═╝╚══════╝╚═╝ ╚═════╝    ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝       ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝
'''
print(banner)

banner_zapis = r'''
███████╗ █████╗ ██████╗ ██╗███████╗    ██╗███████╗██╗ ██████╗ ██████╗ ██╗   ██╗
╚══███╔╝██╔══██╗██╔══██╗██║██╔════╝    ██║██╔════╝██║██╔════╝██╔═══██╗██║   ██║
  ███╔╝ ███████║██████╔╝██║███████╗    ██║███████╗██║██║     ██║   ██║██║   ██║
 ███╔╝  ██╔══██║██╔═══╝ ██║╚════██║    ██║╚════██║██║██║     ██║   ██║╚██╗ ██╔╝
███████╗██║  ██║██║     ██║███████║    ██║███████║██║╚██████╗╚██████╔╝ ╚████╔╝ 
╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═════╝   ╚═══╝  
'''

banner_prezencka = r'''
██████╗ ██████╗ ███████╗███████╗███████╗███╗   ██╗ ██████╗██╗  ██╗ █████╗ 
██╔══██╗██╔══██╗██╔════╝╚══███╔╝██╔════╝████╗  ██║██╔════╝██║ ██╔╝██╔══██╗
██████╔╝██████╔╝█████╗    ███╔╝ █████╗  ██╔██╗ ██║██║     █████╔╝ ███████║
██╔═══╝ ██╔══██╗██╔══╝   ███╔╝  ██╔══╝  ██║╚██╗██║██║     ██╔═██╗ ██╔══██║
██║     ██║  ██║███████╗███████╗███████╗██║ ╚████║╚██████╗██║  ██╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝
'''

GET_UID_APDU = [0xFF, 0xCA, 0x00, 0x00, 0x00]
POLL_INTERVAL_SEC = 0.5
FIRST_THURSDAY = datetime(2025, 9, 25)
WEEKS = 102

LAST_THURSDAY = FIRST_THURSDAY + timedelta(weeks=WEEKS - 1)


def get_readers():
    try:
        return readers()
    except Exception:
        return []

def read_uid_from_reader(reader):
    try:
        conn = reader.createConnection()
        conn.connect()
        data, sw1, sw2 = conn.transmit(GET_UID_APDU)
        if data and sw1 == 0x90 and sw2 == 0x00:
            return toHexString(data).replace(" ", "")
    except Exception:
        return None
    return None

def get_week_column(date: datetime) -> str | None:
    if date.date() < FIRST_THURSDAY.date() or date.date() > LAST_THURSDAY.date():
        return None
    delta_days = (date.date() - FIRST_THURSDAY.date()).days
    week_number = delta_days // 7 + 1
    if 1 <= week_number <= WEEKS:
        return f"{week_number}-WEEK"
    return None

def select_csv_file():
    print("--- Výber súboru podľa čísla cvika ---")
    print("1 - Cvik A10 (studentiA10.csv)")
    print("2 - Cvik B3 (studentiB3.csv)")
    while True:
        try:
            cviko = int(input("Zadaj číslo cvika : "))
            if cviko == 1:
                print("Používam súbor studentiA10.csv")
                return "studentiA10.csv"
            elif cviko == 2:
                print("Používam súbor studentiB3.csv")
                return "studentiB3.csv"
            else:
                print("Neplatné číslo cvika.")
        except ValueError:
            print("Zadaj číslo cvika (1 alebo 2)")

def load_or_create_df(csv_file):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"⚠ Súbor {csv_file} neexistuje, vytváram nový.")
        df = pd.DataFrame(columns=["Meno Priezvisko", "ID"])
    return df

def print_table(df):
    print("\nAktuálna dochádzka:")
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
    print("\n")

def print_row(df, student_id):
    mask = df["ID"] == student_id
    if not mask.any():
        print(f"⚠ Student with ID {student_id} not found.")
        return
    row = df[mask]
    print(tabulate(row, headers='keys', tablefmt='fancy_grid', showindex=False))

def zapis_mode(df, csv_file):
    print(banner_zapis)
    print_table(df)
    while True:
        print("\nZadajte číslo študenta (poradie v tabuľke) alebo Enter pre meno, alebo 'exit' pre návrat do menu.")
        student_input = input("> ").strip()
        if student_input.lower() == 'exit':
            break
        if student_input.isdigit():
            idx = int(student_input) - 1
            if 0 <= idx < len(df):
                name = df.iloc[idx]["Meno Priezvisko"]
            else:
                print("❌ Študent s daným poradovým číslom sa nenašiel.")
                continue
        else:
            name_input = input("Zadajte Meno Priezvisko študenta: ").strip()
            found = df[df["Meno Priezvisko"].str.lower() == name_input.lower()]
            if not found.empty:
                idx = found.index[0]
                name = found.iloc[0]["Meno Priezvisko"]
            else:
                print(f"❌ Študent s {name_input} sa nenašiel.")
                continue
        print(f"✅ Zvolený študent: {name}")
        print("👉 Priložte k čítačke ISIC (6 seconds)...")
        start_time = time.time()
        card_saved = False
        while time.time() - start_time < 6:
            rdrs = get_readers()
            for rd in rdrs:
                uid_hex = read_uid_from_reader(rd)
                if uid_hex:
                    df.at[idx, "ID"] = uid_hex
                    df.to_csv(csv_file, index=False)
                    print(f"✔ Saved ISIC {uid_hex} for {name}")
                    card_saved = True
                    break
            if card_saved:
                break
            time.sleep(POLL_INTERVAL_SEC)
        if not card_saved:
            print("⏰ Nezaznamenal som kartu v 6 sekundovom intervale.")
        print("--------------------------------------------------")

def prezencka_mode(df, csv_file):
    print(banner_prezencka)
    print_table(df)
    print("Napíš 'exit' pre návrat do menu alebo prilož ISIC kartu.")
    buffer = ''
    while True:
        # Check for card
        rdrs = get_readers()
        if not rdrs:
            print("⚠ No readers found. Is the reader plugged in?")
            time.sleep(2.0)
            continue
        card_found = False
        for rd in rdrs:
            uid_hex = read_uid_from_reader(rd)
            if uid_hex:
                now = datetime.now()
                col = get_week_column(now)
                if col is None:
                    print(f"⚠ Dátum {now.date()} nie je v rozsahu semestra.")
                    # Prompt for exit or continue
                    user_input = input("Pokračovať? (Enter) alebo 'exit': ").strip().lower()
                    if user_input == 'exit':
                        print("Opúšťam prezenčku...")
                        return
                    continue
                if col not in df.columns:
                    df[col] = ""
                mask = df["ID"] == uid_hex
                if not mask.any():
                    print(f"⚠ Študent s ID {uid_hex} sa nenašiel v CSV.")
                    # Prompt for exit or continue
                    user_input = input("Pokračovať? (Enter) alebo 'exit': ").strip().lower()
                    if user_input == 'exit':
                        print("Opúšťam prezenčku...")
                        return
                    continue
                df.loc[mask, col] = "P"
                df.to_csv(csv_file, index=False)
                student_name = df.loc[mask, "Meno Priezvisko"].values[0]
                print(f"✅ {student_name} ({uid_hex}) bol označený ako prítomný v {col} [dátum: {now.date()}].")
                print_row(df, uid_hex)
                card_found = True
                # Wait 5 seconds, but allow exit during this time
                wait_time = 3.0
                interval = 0.1
                elapsed = 0.0
                while elapsed < wait_time:
                    time.sleep(interval)
                    elapsed += interval
                    while msvcrt.kbhit():
                        char = msvcrt.getwch()
                        if char == '\r' or char == '\n':
                            if buffer.strip().lower() == 'exit':
                                print("Opúšťam prezenčku...")
                                return
                            buffer = ''
                        else:
                            buffer += char
                print_table(df)
                # Prompt for exit or continue
                user_input = input("Pokračovať? (Enter) alebo 'exit': ").strip().lower()
                if user_input == 'exit':
                    print("Opúšťam prezenčku...")
                    return
                break
        # Check for user input (non-blocking)
        while msvcrt.kbhit():
            char = msvcrt.getwch()
            if char == '\r' or char == '\n':
                if buffer.strip().lower() == 'exit':
                    print("Opúšťam prezenčku...")
                    return
                buffer = ''
            else:
                buffer += char
        time.sleep(POLL_INTERVAL_SEC)

def main_menu():
    while True:
        print("\n--- HLAVNÉ MENU ---")
        print("1 - Zápis študentov (priradenie ISIC)")
        print("2 - Prezenčka (dochádzka)")
        print("3 - Exit")
        choice = input("Vyber možnosť: ").strip()
        if choice == '1':
            csv_file = select_csv_file()
            df = load_or_create_df(csv_file)
            zapis_mode(df, csv_file)
        elif choice == '2':
            csv_file = select_csv_file()
            df = load_or_create_df(csv_file)
            prezencka_mode(df, csv_file)
        elif choice == '3':
            print("Exiting program. Dovidenia!")
            break
        else:
            print("Neplatná voľba. Skús znova.")

if __name__ == "__main__":
    main_menu()
