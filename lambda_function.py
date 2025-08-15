import os, json, urllib.request, urllib.error, traceback

HA_URL   = os.environ.get("HA_URL", "").rstrip("/")
HA_TOKEN = os.environ.get("HA_TOKEN", "")
HA_LANG  = os.environ.get("HA_LANG", "de")
HA_AGENT = os.environ.get("HA_AGENT")
HA_HOME = os.environ.get("HA_HOME", "Hausassistent")

HA_PROMPT = """. Bereite die Ausgabe so vor, dass sie von Alexa in Deutsch einfach gesprochen werden kann. 
Bei Fragen nach Sensoren verarbeite auch immer den Status.
Halte die Ausgabe zu Ergebnissen der Haussensoren kurz.
"""

HA_PROMPT = os.environ.get("HA_PROMPT", HA_PROMPT)

def sayX(text, end=True):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {"type": "PlainText", "text": (text or "OK.")[:8000]},
            "shouldEndSession": end
        }
    }

def _slot_q(event):
    try:
        return event["request"]["intent"]["slots"]["q"]["value"]
    except Exception:
        return ""

def say(text, end=False, reprompt="Noch etwas?", session_attrs=None):
    resp = {
        "version": "1.0",
        "response": {
            "outputSpeech": {"type": "PlainText", "text": (text or "OK.")[:8000]},
            "shouldEndSession": end
        }
    }
    if not end and reprompt:
        resp["response"]["reprompt"] = {"outputSpeech": {"type": "PlainText", "text": reprompt}}
    if session_attrs:
        resp["sessionAttributes"] = session_attrs
    return resp

def _ha_conversation(text, conv_id):
    url = f"{HA_URL.rstrip('/')}/api/conversation/process"
    payload = {"text": text, "language": HA_LANG, "conversation_id": conv_id}
    if HA_AGENT:
        payload["agent_id"] = HA_AGENT
    print(payload)
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)

def _pick(resp):
    # robust über verschiedene HA-Versionen
    try:
        s = resp.get("response", {}).get("speech", {}).get("plain", {}).get("speech")
        if s:
            return str(s)
    except Exception:
        pass
    # Fallbacks
    for k in ("response", "speech", "text", "message"):
        v = resp.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return "Okay."

def handler(event, context):
    try:
        # --- Logging fürs Debuggen ---
        print("Incoming:", json.dumps(event, ensure_ascii=False))
        req_type = event.get("request", {}).get("type")
        user_id = (event.get("session") or {}).get("user", {}).get("userId", "alexa")
        conv_id = f"alexa-{user_id[-12:]}"

        session_attrs = (event.get("session") or {}).get("attributes") or {}
        user_id = (event.get("session") or {}).get("user", {}).get("userId", "alexa")
        conv_id = session_attrs.get("conv_id") or f"alexa-{user_id[-12:]}"
        session_attrs["conv_id"] = conv_id

        if req_type == "LaunchRequest":
            return say(f"{HA_HOME}", end=False)

        if req_type == "IntentRequest": 
            name = event["request"]["intent"]["name"] 
            is_one_shot = bool(event.get("session", {}).get("new", False))
            if name == "FreeTextIntent": 
                q = _slot_q(event) 
                print(f"Extracted slot q: {q}") 
                end_flag = True if is_one_shot else False
                reprompt_text = None if is_one_shot else "Noch etwas?"
                if not q: 
                    return say("Kannst du das bitte wiederholen?", end=False, session_attrs=session_attrs) 
                try: 
                    if not HA_TOKEN: 
                        return say("Kein Home Assistant Token gesetzt. Bitte HA Token hinterlegen.") 
                    r = _ha_conversation(q + HA_PROMPT, conv_id) 
                    print("HA response:", json.dumps(r, ensure_ascii=False)) 
                    answer = _pick(r) # Falls HA leer antwortet, wenigstens den Slot zurückgeben 
                    if not answer or answer.strip().lower() in ("ok.", "okay.") and q: 
                        return say(f"Du hast gesagt: {q}") 
                    return say(answer, end=end_flag, reprompt=reprompt_text, session_attrs=session_attrs)

                except urllib.error.HTTPError as e:
                    body = e.read().decode("utf-8", "ignore")
                    print("HTTPError:", e.code, body)
                    return say(f"Home Assistant Fehler {e.code}.")
                except urllib.error.URLError as e:
                    print("URLError:", e)
                    return say("Ich konnte Home Assistant nicht erreichen.")
                except Exception as e:
                    print("Exception:", traceback.format_exc())
                    return say("Es gab einen Fehler bei der Verarbeitung:")
            elif name == "AMAZON.HelpIntent":
                return say("Du kannst mich alles fragen oder Geräte steuern.", end=False, session_attrs=session_attrs)
            elif name in ("AMAZON.StopIntent", "AMAZON.CancelIntent"):
                return say("Okay, bis zum nächsten Mal!", end=True)
            elif name == "AMAZON.FallbackIntent":
                return say("Das habe ich leider nicht verstanden.", end=False, reprompt="Bitte wiederholen.", session_attrs=session_attrs)
            else:
                return say("Okay.")

        if req_type == "SessionEndedRequest":
            return say("Tschüss!")
        return say("Okay.")
    except Exception:
        print("Top-level Exception:", traceback.format_exc())
        return say("Da ist etwas schiefgegangen.")

