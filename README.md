# Alexa Custom Skill – Haushelfer

This Alexa Custom Skill connects Alexa to your Home Assistant instance, allowing you to control devices and request status updates in German.

## Prerequisites

- **Amazon Developer Account** for Alexa Skills Kit (ASK) development
- **AWS Lambda** access
- **Home Assistant** with the [Conversation API](https://www.home-assistant.io/integrations/conversation/) enabled
- **Home Assistant Long-Lived Access Token** for authentication

---

## Installation

### 1. Create the Skill in the Alexa Developer Console
1. Go to the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask).
2. Click **"Create Skill"**.
3. Enter a name (e.g., `the homeassistant`).
4. Choose **Custom** as the skill type and **AWS Lambda** as the backend service (recommended).
5. Upload the **Interaction Model**:
   - Navigate to **Build → Interaction Model → JSON Editor**.
   - Replace the content with the [`interaction_model.json`](interaction_model.json) file from this repository.
   - Click **Save Model** and then **Build Model**.

---

### 2. Set up the AWS Lambda Function
1. Open the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Create a new function (Python 3.9 or newer).
3. Upload the contents of the [`lambda_function.py`](lambda_function.py) file.
4. In **Configuration → Environment Variables**, set the variables listed below.
5. Copy the ARN of your Lambda function.
6. In the Alexa Developer Console → **Endpoint**: choose **AWS Lambda ARN** and paste the ARN.

---

## Environment Variables

| Variable   | Description |
|------------|-------------|
| `HA_URL`   | Base URL of your Home Assistant (e.g., `https://my-ha-domain.com`). |
| `HA_TOKEN` | Long-Lived Access Token from Home Assistant (`Profile → Long-Lived Access Tokens`). |
| `HA_LANG`  | Language for the Home Assistant Conversation API (`de` for German, default: `de`). |
| `HA_AGENT` | *(Optional)* Agent ID if multiple agents are configured in HA. |
| `HA_HOME`  | Greeting text when the skill is launched (default: `Hausassistent`). |
| `HA_PROMPT`| *(Optional)* Additional prompt text for more precise responses from HA. |

---

## Usage

Once the skill is published or enabled in developer mode, you can interact with it using commands such as:

> **"Alexa, frage den Haushelfer"**  
> **"Status Klimaanlage"**  
> **"schalte die Kaffeemaschine aus"**

Currently the interaction is done in German, but can be easily translated to en ...

---

## Debugging

- Errors and debug output appear in the **CloudWatch Logs** of your Lambda function.
- If Alexa reports that Home Assistant is not reachable:
  - Check `HA_URL` and `HA_TOKEN`.
  - Make sure your Home Assistant instance is accessible from AWS.
