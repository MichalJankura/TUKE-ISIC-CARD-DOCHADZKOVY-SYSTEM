# PREZENČNÝ SYSTÉM TUKE
Tento Python skript slúži na evidenciu prítomnosti študentov na prednáškach pomocou NFC kariet. Skript komunikuje 
s NFC čítačkou a zapisuje prítomnosť do textového súboru typu CSV.
# Required Hardware - Advanced Card Systems Ltd.
- ACR122
- P/N: ACR122U-A9
- Power: 5VDC 200mA
- S/N: RR1717-149064
- [Advanced Card Systems Ltd.](https://www.acs.com)


You may need drivers for the ACR1252: : https://www.acs.com.hk/en/products/342/acr1252u-usb-nfcreader-iii-nfc-forum-certified-reader/
You may have to put the tag directly on the reader, on some devices the waitforcard() function does not work properly

# pip requirements (pip install):
- pandas
- smartcard
- tabulate
# VIZUALIZÁCIA PROJEKTU

<img width="1280" height="319" alt="Menu" src="https://github.com/user-attachments/assets/bdffdbd8-22a2-4d7a-a3c0-7aacd7c2bc5b" />

<img width="1041" height="762" alt="Zapis_isicov" src="https://github.com/user-attachments/assets/00081254-447a-44b5-90f0-64edeac95699" />

<img width="998" height="157" alt="Prezencka" src="https://github.com/user-attachments/assets/e0cc9f7d-28e2-4e35-8fca-bb32313ce6db" />

<img width="1041" height="719" alt="Prezencka_isic" src="https://github.com/user-attachments/assets/1db15727-df33-4ff8-b718-010c334fcc6a" />
