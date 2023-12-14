# Bedienungsanleitung zum gmu python script für das Projekt Gewächshaussteuerung in LF7

### starten mit Funktionen bis Abschnitt 3
- '/src/' auf raspi kopieren

```bash
python3 gmu.py --loop --segment --hum --temp
```

### generelle Bedienung

- es gibt drei möglichkeiten das Programm zu starten.
- erklärung aller commands mit `python3 gmu.py --help`
1. manuell auf den raspi kopieren und mit python3 gmu.py ausführen
2. über das deploy script auf den raspi kopieren und automatisch ausführen lassen
    ``` bash
    ./deploy.sh run "--loop --segment --lcd --matrix --hum --temp --light -u 4"
    ```
3. das deploy script benutzen um einen systemd service enzurichten
    ```
    ./deploy.sh enable
    ```
    - wenn der service manuell eigerichtet wird dran denken `--service-mode` mitzugeben