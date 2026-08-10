# Hardware-Setup: Pi 3B+ + 3× HW-839 (MCP23017) + Mikroschalter

Alles hier läuft **auf dem Raspberry Pi**, nicht auf deinem PC.

## 1. I2C aktivieren

```
sudo raspi-config
```
→ Interface Options → I2C → Enable → reboot.

Danach prüfen, ob die I2C-Tools installiert sind:
```
sudo apt install -y i2c-tools python3-pip
```

## 2. Verkabelung: I2C-Bus (gemeinsam für alle 3 Boards)

Alle drei HW-839-Boards teilen sich denselben I2C-Bus — nur 4 Leitungen,
parallel an alle drei Boards angeschlossen:

| Pi Pin | HW-839 Pin | alle 3 Boards |
|---|---|---|
| 3.3V (Pin 1) | VCC | ja, parallel |
| GND (Pin 6) | GND | ja, parallel |
| GPIO2 / SDA (Pin 3) | SDA | ja, parallel |
| GPIO3 / SCL (Pin 5) | SCL | ja, parallel |

**Wichtig:** Nicht 5V verwenden — der Pi-I2C-Bus verträgt nur 3.3V-Pegel,
und die HW-839-Boards laufen mit 3.3V problemlos.

## 3. Adressen einstellen (A0/A1/A2-Pins am Board)

Jedes Board braucht eine eigene I2C-Adresse, sonst kollidieren sie auf
dem Bus. Die HW-839-Boards haben 3 Adress-Jumper/Pins (A0, A1, A2) —
auf GND oder VCC brücken:

| Board | A2 | A1 | A0 | Adresse | Spieler |
|---|---|---|---|---|---|
| Board 1 | GND | GND | GND | 0x20 | Spieler 1 |
| Board 2 | GND | GND | VCC | 0x21 | Spieler 2 |
| Board 3 | GND | VCC | GND | 0x22 | Spieler 3 |

## 4. Boards erkennen

Nach dem Verkabeln (auch wenn nur 1 Board dran hängt):
```
i2cdetect -y 1
```
Du solltest die konfigurierten Adressen (20, 21, 22 in Hex) in der
Tabelle auftauchen sehen. Taucht nichts auf: Verkabelung prüfen (SDA/SCL
nicht vertauscht, GND wirklich verbunden, Adress-Pins wirklich auf GND/VCC
und nicht offen/floating).

## 5. Mikroschalter anschließen

Die A142-Mikroschalter haben 3 Pins: **COM**, **NO** (Normally Open),
**NC** (Normally Closed). Wir nutzen **COM + NO**:

- **COM** → GND (gemeinsame Masse, kannst du für alle Schalter eines
  Boards zusammenlegen)
- **NO** → ein GPA/GPB-Pin am MCP23017

Wir aktivieren den internen Pull-Up im MCP23017 per Software — dann liegt
der Pin im Ruhezustand auf HIGH (3.3V) und wird beim Tasterdruck auf LOW
(GND) gezogen. Keine externen Widerstände nötig.

## 6. Python-Bibliotheken installieren

```
pip install --break-system-packages adafruit-blinka adafruit-circuitpython-mcp230xx
```

(`--break-system-packages` ist auf aktuellem Raspberry Pi OS nötig, weil
Python-Pakete sonst über apt verwaltet werden.)

## 7. Testreihenfolge (empfohlen)

1. **Nur 1 Board, 0 Schalter**: `i2cdetect -y 1` → Adresse sichtbar?
2. **1 Board, 1 Schalter auf Breadboard**: `switch_test.py` (unten) →
   Tasterdruck wird im Terminal angezeigt?
3. **Alle 3 Boards, je 1 Testschalter**: gleiche Adress-Erkennung für
   alle drei
4. Erst danach alle 13 Schalter pro Spieler final verkabeln/verlöten
