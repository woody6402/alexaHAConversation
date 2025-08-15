# Alexa Custom Skill – Haushelfer

Dieser Alexa Custom Skill verbindet Alexa mit deinem Home Assistant und ermöglicht dir, Geräte zu steuern und Statusabfragen auf Deutsch zu machen.

## Voraussetzungen

- **Amazon Developer Account** für die Alexa Skills Kit (ASK) Entwicklung
- **AWS Lambda** Zugang
- **Home Assistant** mit aktivierter [Conversation API](https://www.home-assistant.io/integrations/conversation/)
- **Home Assistant Long-Lived Access Token** für die Authentifizierung

---

## Installation

### 1. Alexa Developer Console – Skill anlegen
1. Gehe zu [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask).
2. Klicke **"Create Skill"**.
3. Vergib einen Namen (z. B. `Haushelfer`).
4. Wähle **Custom** als Skill-Typ und **Alexa-Hosted (Node.js)** oder **AWS Lambda** (empfohlen: AWS Lambda).
5. Lade das **Interaction Model** hoch:
   - Wechsle zu **Build → Interaction Model → JSON Editor**.
   - Ersetze den Inhalt durch die Datei [`interaction_model.json`](interaction_model.json) aus diesem Repository.
   - Klicke **Save Model** und dann **Build Model**.

---

### 2. AWS Lambda Funktion einrichten
1. Öffne die [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Erstelle eine neue Funktion (Python 3.9 oder neuer).
3. Lade den Inhalt der Datei [`lambda_function.py`](lambda_function.py) hoch.
4. Setze im Lambda-Tab **Configuration → Environment Variables** die folgenden Variablen (siehe unten).
5. Kopiere die ARN der Lambda-Funktion.
6. In der Alexa Developer Console → **Endpoint**: Wähle **AWS Lambda ARN**, füge die ARN ein.

---

## Umgebungsvariablen

| Variable   | Beschreibung |
|------------|--------------|
| `HA_URL`   | Basis-URL deines Home Assistant (z. B. `https://meine-ha-domain.de`). |
| `HA_TOKEN` | Long-Lived Access Token aus Home Assistant (`Profil → Long-Lived Access Tokens`). |
| `HA_LANG`  | Sprache für die Home Assistant Conversation API (`de` für Deutsch, Standard: `de`). |
| `HA_AGENT` | *(Optional)* Agent-ID, falls mehrere Agents in HA existieren. |
| `HA_HOME`  | Begrüßungstext, wenn der Skill gestartet wird (Standard: `Hausassistent`). |
| `HA_PROMPT`| *(Optional)* Zusätzlicher Prompt-Text für genauere Antworten von HA. |

---

## Nutzung

Nachdem der Skill veröffentlicht oder im Developer-Modus aktiviert wurde, kannst du ihn mit Befehlen wie z. B. starten:

> **"Alexa, starte den Haushelfer"**  
> **"Alexa, frage den Haushelfer nach der Temperatur im Wohnzimmer"**  
> **"Alexa, sage dem Haushelfer, er soll das Licht im Flur einschalten"**

---

## Debugging

- Fehler und Debug-Ausgaben erscheinen in den **CloudWatch Logs** deiner Lambda-Funktion.
- Falls Alexa meldet, dass der Home Assistant nicht erreichbar ist:
  - Prüfe `HA_URL` und `HA_TOKEN`.
  - Stelle sicher, dass dein Home Assistant von AWS aus erreichbar ist.
