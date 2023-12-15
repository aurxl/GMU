# LF7 Cyberphysiche Systeme ergänzen - Projekt Gewächshaussteuerung

**Bei Fragen zur Bedienung bitte unter docs/Bedienungsanleitung nachsehen**

## 1 Projektbeschreibung
```
Für Ihren Auftraggeber Floristik GmbH, Kaditzer Straße 4-10, 01139 Dresden sollen Sie eine vorhan-
dene Gewächshaussteuerung in Betrieb nehmen und erweitern.
Aktuell ist die Steuerung nur mit einem Sensor DHT11 zur Temperaturmessung und mit einer 7-Seg-
ment-LED-Anzeige zur Ausgabe der gemessenen Temperatur versehen.
Die Steuerung konnte noch nicht in Betrieb genommen werden.
Die Steuerung wird abschnittsweise erweitert (Hard- und Software). Erweiterungen sind in jedem Ab-
schnitt im PAP/Struktogramm, Python-Skript und sonstigen notwendigen Unterlagen zu dokumentie-
ren.
```

## 2 Projektablauf
### 1. Analyse und Steuerung
> 1.+ 2. Woche
- Blockschaltbild der geplanten Steuereung aller Projektabschnitte
- Übersicht über Messbereiche und Toleranzen aller im weiteren Verlauf genutzten Sensoren
    - Bonus Für Datenblätter

### 2. Inbetriebnahme der Steuerung
> 3. Woche
- Temperaturmessung erfolgt im "Dauerbetrieb"
    - Sensor: DHT11
    - Anzeige: 7-Segment-LED-Anzeige
        - Ausgabe Temperaturwerte in "ausreichender Genauigkeit"
- Protokollierung dieses Prozesses wird angelegt
- Dokumentation um ein PAP **oder** ein Struktogramm erweitern
    - inkl "ablauffähiges Python-Skript"

### 3. Hinzufügen des Luftfeuchtigkeitssensors
> 4. Woche
- Luftfeuchtigkeitssensor hinzufügen
    - Sensor: DHT11 (selber wie bei der Temperaturmessung)
    - Anzeige: 7-Segment-LED-Anzeige
        - Ausgabe Temperaturwerte in "sinvoller Genauigkeit"
- Erweiterung des PAP/ Struktogramms und des Python-Skripts
- ZIP Datei mit folgenden Inhalten anfertigen (due: Freitag 23:59Uhr der Projektwoche)
    - Dokumentation, mit folgenden Anlagen:
        - Python-Skript
        - Inbetriebnahme Protokoll

**Ab Woche 5: Gespräche zu Unterlagen/ Bewertungskriterien**

### 4. Erweiterung der Anzeige
> 5. Woche
- Anzeige Temp und Hum zusätzlich auf LCD(2X16)

### 5. Hinzufügen eines Helligkeitssensors mit Bewertung
> 6.- 8. Woche
- Integration eines Helligkeitssensors
- Recherche + Dokumentation zu: 
    - reale Werte zum Lichtbedarf der blühenden Pflanze
- Prüfen, ob der Sensor für die benötigte Lichtstärke (in Lux) geeignet ist
- Bewertung gemessener Lichtstärke und passendes Symbol auf auf der Anzeigematrix 
    - hierfür passende Symbole definieren und Dokumentieren (Bilder der Anzeige mit in die Doku einbinden)
- Umsetzung im Python-Skript

### 6. Helligkeitssteuerung des Gewächshauses
> 9.+ 11. Woche
- Lichtsteuerung mit Relais
    - unter Berücksichtigung aktueller (Tages-)Zeit
    - Zeit mit Zeitserver (10.254.5.115) syncen
        - Einstellungen auf Raspi überprüfen:
            ``` sh
            sudo apt install ntp
            sudo sh -c "echo 'server 10.254.5.115' >> /etc/ntp.conf && systemctl restart ntp.service"
            ```
- Speicherung der Werte (Zeit, Temp, Hum, Licht, Zustand des Relais) in einer CSV- Datei
    - Diese soll mit einem Tabellenkalkulationsprogramm ausgewertet werden können
- Erstellung einer Anleitung/ Kundendoku des Gesamtsystems - Keine Inbetriebnahme Doku
    - auch Erklärung der Symbole auf der Matrixanzeige
- Zusammenfassung der Benutzeranleitung, Python-Skript und Doku in ZIP zsm. fassen
    - bis Freitag 23:59Uhr der aktuellen Projektwoche ins Lernsax LF7/Projekt/Schülerarbeiten/Woche 11

**Ab Woche 12: Gespräche zu Unterlagen / Bewertungskriterien siehe Anlage 4**

### 7. Datenbank
> 12.+ 13. Woche
- gemessene Daten in einer Datenbank speichern
    - influxdb?
    - vllt die Datenbank gleich mit in 6. implementieren, und dann die Daten aus der Datenbank in die csv dumpen
