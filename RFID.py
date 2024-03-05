import serial
import pymysql
import datetime


# Serielle Verbindung zum Arduino herstellen
ser = serial.Serial('COM5', 9600)  # 'COM4' an Ihre Umgebung anpassen

# Verbesserte Fehlerbehandlung bei der MySQL-Verbindung
try:
    db = pymysql.connect(host='localhost', user='root', password='', database='rfid_cards')
    cursor = db.cursor()
except pymysql.Error as e:
    print(f"Fehler bei der MySQL-Verbindung: {e}")
    exit(1)

try:
    while True:
        # Daten vom Arduino lesen und leere Zeilen ignorieren
        line = ser.readline().decode().strip()
        while not line:
            line = ser.readline().decode().strip()

        if line:
            try:

                # Behandeln Sie potenziell unvollständige Zeilen mithilfe einer bedingten Anweisung
                if len(line.split(',')) != 3:
                    print(f"Ungültiges Datenformat: {line}")
                    continue  # Fahren Sie mit der nächsten Iteration fort, wenn das Format ungültig ist

                    # Daten in geeignete Datentypen konvertieren
                    rfid_uid, Zeitstempel = line.split(',')
                    aktuellerZeitstempel = int(datetime.datetime.now().timestamp())  # Zeitstempel als String im aktuellen Format
                    rfid_uid = int(rfid_uid)
                    Card_detected = vars(Card_detected)



                # SQL-Abfrage mit korrekten Platzhaltern und Escape-Sequenz
                sql = f"INSERT INTO rfidcards (Card_detected, rfid_uid, Zeitstempel) VALUES (%s, %s, %S)"
                db.cursor.execute(sql, (Card_detected, rfid_uid, Zeitstempel))
                db.commit()  # Änderungen committen
                print(f"RFID-Karte mit Card detected:{Card_detected} und UID: {rfid_uid} und Zeitstempel: {Zeitstempel} erfolgreich gespeichert.")

            except (pymysql.Error, ValueError) as e:
                print(f"Fehler beim Speichern der RFID-Karte: {e}")
except KeyboardInterrupt:
    print("Programm beendet.")
finally:
    # Verbindung schließen, falls vorhanden
    if db:
        db.close()


