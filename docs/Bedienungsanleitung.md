# 9.3 Bedienungsanleitung GMU (v1.6)
> tracetronic GmbH - Marco Kolitsch & Jan Meineke

#### Position der Sensoren
Bitte darauf achten, dass die Sensoren für Luftfeuchtigkeit und Temperatur (DHT11 blauer kleiner Plastikkasten) nicht direkt an Türen und Fenster aufzustellen sind. Am besten ist auf höhe der Pflanzen, ziemlich mittig im Raum. Auch zu beachten ist, dass der Helligkeitssensor, beschriftet mit `light` bestmöglich draußen oder zumindest oberhalb der Lampen angebracht wird, sofern das Gewächshaus ein lichtdurchlässiges Dach hat. Wird dies nicht eingehalten, kann es dazu führen, dass das Licht wechselweise an und aus geschaltet wird.

#### Update Intervall
Wenn der Prozess wie in dieser Anleitung beschrieben gestartet wird, läuft dieser unbegrenzt. Mit einem update Intervall der Daten von 4 sekunden.

#### LCD Anzeige und Messwerte
Auf der LCD Anzeige sind Luftfeuchtigkeit und Temperatur gemessen vom Sensor zu finden. Diese werden im oben genannten Intervall aktualisiert. Wenn die angebenen Daten etwas komisch erscheinen, ist es ratsam mit einem zweiten, handelsüblichem Sensor die Werte aubzugleichen. Abweichungen von bis zu +- 2°C bzw. +- 5% Luftfeuchte und bis zu +-20% LUX sind zu erwarten. Desweiteren kann auch durch Provokation durch Draufhalten auf den Sensor die Glaubwürdigkeit der gemessen Werte eingeschätzt werden, wenn diese daraufhin realistisch an/absteigen.

#### 7-segment Anzeige
Auf der 7-Segment Anzeige sind die Werte für Temperatur und Luftfeuchtigkeit abwechselnd angezeigt.

#### Matrix Anzeige und Lichtlevel
Die Matrix zeigt in Form von Smileys die Bewertung der Helligkeit. Ein lachender Smiley stellt optimale Lichtbedingungen dar. Ein trauriger darauf, dass es entweder zu hell, oder zu dunkel ist. Um genauere Informationen darüber zu erlangen, ob es zu hell oder dunkel ist, kann aus der generierten `gmu.csv` abgelesen werden.

#### CSV
Das Programm generiert in dem Verzeichnis aus dem das Programm gestart wird eine CSV Datei (gmu.csv). Diese kann auf dem Raspi per RDP mit einem Tabellenkalkulationsprogramm geöffnet werden. Alternativ kann diese auch auf das lokale System kopiert werden: `scp pi@ipv4:~/gmu.csv .` . Nach einem Neustart des Programms wird die CSV Datei nicht überschrieben, sondern die neuen Werte werden an die bestehende Datei angehangen.
Je Zeile sind folgende Werte zu finden:

|time|temperature (°C)|humidity (%)|light (lux)|light rating|relay open|


#### Relay aka Lichtsteuerung
Meldet der Lichtsensor zu niedrige werte, die den Pflanzenwachstum beeinträchtigen könnten, wird das Licht angesteuert (Lampen an). Ausnahme ist, dass es Nachts zwischen 22:00 und 6:00 ist. Zwischen diesen Uhrzeiten wird das Licht nicht aktiviert, um die Ruhrphase der Pflanzen nicht zu beeinträchtigen.

## Generelle Bedienung

> Erklärung aller commands mit `python3 gmu.py --help`

### Nach einem Neustart
Zum raspi per SSH oder RDP verbinden und den Befehl:
```bash
python3 gmu.py --loop --segment --lcd --matrix \
    --hum --temp --light --csv --relay -u 4
```

Wenn der Prozess im Hintergrund laufen soll:
```bash
python3 gmu.py --loop --segment --lcd --matrix \
    --hum --temp --light --csv --relay -u 4 &> /dev/null &
```

Alternativ kann gmu auch als systemd service laufen. Wurde der service enabled, startet dieser nach dem Neustart automatisch weiter. Um den service zu `enablen`: `sudo systemctl enable gmu.service`, neustarten: `sudo systemctl restart gmu.service`.

### Starten
Es gibt drei möglichkeiten das Programm zu starten.

1. manuell auf den raspi kopieren und mit python3 gmu.py ausführen
2. über das deploy script auf den raspi kopieren und automatisch ausführen lassen
    ``` bash
    ./deploy.sh run "--loop --segment --lcd --matrix --hum --temp --light --csv --relay -u 4"
    ```
3. das deploy script benutzen um einen systemd service enzurichten
    ```
    ./deploy.sh enable
    ```
    - wenn der service manuell eigerichtet wird dran denken `--service-mode` mitzugeben
