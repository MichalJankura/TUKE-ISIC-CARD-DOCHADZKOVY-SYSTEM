# PREZENČNÝ SYSTÉM TUKE
Tento Python skript slúži na evidenciu prítomnosti študentov na prednáškach pomocou NFC kariet. Skript komunikuje 
s NFC čítačkou a zapisuje prítomnosť do textového súboru typu CSC.
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

