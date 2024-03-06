import serial
import pymysql
import datetime


# Serielle Verbindung zum Arduino herstellen
ser = serial.Serial('COM5', 9600)  # 'COM4' an Ihre Umgebung anpassen

# Verbesserte Fehlerbehandlung bei der MySQL-Verbindung
try:
    db_rfid_cards = pymysql.connect(host='localhost', user='root', password='', database='rfid_cards')
    cursor = db_rfid_cards.cursor()

except pymysql.Error as e:
    print(f"Fehler bei der MySQL-Verbindung: {e}")
    exit(1)

# Daten in geeignete Datentypen konvertieren

Zeitstempel = str(datetime.datetime.now())  # Zeitstempel als String im aktuellen Format,


try:
    while True:
        # Daten vom Arduino lesen und leere Zeilen ignorieren
        line1 = ''
        line2 = ''

        while not line1:
            line1 = ser.readline().decode().strip()
        while not line2:
            line2 = ser.readline().decode().strip()

        if line1 and line2:
            try:

                # SQL-Abfrage mit korrekten Platzhaltern und Escape-Sequenz
                sql = f"""INSERT INTO rfidcards(Card_detected, rfid_uid, Zeitstempel) VALUES (%s, %s, %s)"""

                cursor.execute(sql, (line1, line2, Zeitstempel))
                db_rfid_cards.commit()  # Änderungen committen

                print(
                    f"RFID-Karte mit Card detected:{line1} und UID: {line2} und Zeitstempel: {Zeitstempel} erfolgreich gespeichert.")

            except (pymysql.Error, ValueError) as e:
                print(f"Fehler beim Speichern der RFID-Karte: {e}")
except KeyboardInterrupt:
    print("Programm beendet.")
finally:
    # Verbindung schließen, falls vorhanden
    if db_rfid_cards:
        db_rfid_cards.close()
