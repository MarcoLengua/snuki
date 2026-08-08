# SNUKI — Software-Prototyp (Tastatur)

Läuft komplett auf dem PC, ohne Hardware — Tastatur simuliert die
Loch-Sensoren, damit du die Renn-Logik und die Grafik schon testen
kannst, bevor die Pappautomaten fertig sind.

## Setup

```
pip install -r requirements.txt
python main.py
```

Getestet mit Python 3.10+ und pygame 2.5+.

## Steuerung

| Spieler | 0 Schritte | 1 Schritt | 2 Schritte | 3 Schritte |
|---|---|---|---|---|
| Spieler 1 | Q | W | E | D |
| Spieler 2 | I | O | P | Ü |

- **R** — Rennen neu starten
- **ESC** — Beenden
- **Leertaste** — nach einem Sieg neu starten

Falls die **Ü**-Taste bei dir nicht auslöst (abhängig von Tastatur-Layout
und Betriebssystem), lauf `python key_probe.py`, drück die Taste, und
schau dir im Terminal an, welchen `pygame.K_...`-Namen sie tatsächlich
sendet. Trag den dann in `config.py` unter `KEY_MAPS` ein.

## Projektstruktur

```
config.py        Spieler, Farben, Tastenbelegung, Streckenlänge — hier
                  fügst du später den 3. Spieler hinzu
input_handler.py Tastatur-Input heute; Platzhalter für den Sensor-Input
                  später (gleiche Schnittstelle: (spieler, schritte))
game_state.py    Reine Spiellogik: Positionen, Zielbedingung
renderer.py      Zeichnet Strecke, Pferde, HUD, Siegerbildschirm
main.py          Game-Loop, verbindet alles
key_probe.py     Hilfsskript zum Herausfinden von Tastencodes
```

## Von Tastatur auf echte Sensoren umstellen (später)

Die Trennung ist bewusst so gebaut, dass beim Umstieg auf die Pi +
MCP23017-Hardware **nur `input_handler.py` und `main.py`** angefasst
werden müssen:

1. In `input_handler.py` die `SensorInputProvider`-Klasse fertig
   implementieren (Grundgerüst mit Adafruit-Bibliotheken ist schon als
   Kommentar hinterlegt).
2. In `main.py` `KeyboardInputProvider()` durch `SensorInputProvider()`
   ersetzen.

`game_state.py` und `renderer.py` bleiben komplett unverändert, weil
beide Input-Quellen dieselben `(spieler_index, schritte)`-Events liefern.

## 3. Spieler hinzufügen

In `config.py`:

1. `PLAYER_NAMES` um einen dritten Eintrag erweitern
2. In `KEY_MAPS` den auskommentierten dritten Block aktivieren und
   Tasten deiner Wahl eintragen

Alles andere (Strecke, Rendering, Sieglogik) läuft automatisch für
beliebig viele Spieler mit.
