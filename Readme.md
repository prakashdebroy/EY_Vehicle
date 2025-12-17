# Ey-Techathon 6.0 — Car Monitoring & AI Speaking 

This repository houses a competition project built for Ey-Techathon 6.0. The project addresses a selected challenge related to real-time monitoring and accessible interaction: a modular, demonstrable system that consolidates live sensor/vision inputs, applies configurable rules, and provides natural-language and voice-driven explanations and responses.

## Installation (Windows)

1. Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the project:

```powershell
python main.py
```

The web dashboard is available at http://localhost:5001 (default). Use the UI and voice control to interact with the system during the demo.

## Project Presentation (for Judges)

This is a complete, demonstrable project. Present it as a unified system that showcases the following features and capabilities:

- **Live Monitoring Dashboard:** a single interface displaying incoming sensor and vision data, recent events, and the current evaluated rule states.
- **Rule-Based Automation:** configurable rules that evaluate sensor inputs and trigger actions or alerts; rules are easy to demonstrate by simulating sensor changes.
- **Conversational Explanation:** an LLM-backed explanation layer that summarizes system state, explains why an alert fired, and recommends actions in clear natural language.
- **Voice Interaction:** speech-to-text input from a microphone, routed to the conversational layer, with spoken responses (text-to-speech) so judges can interact hands-free.
- **Demo Scenarios:** prepared scenarios to show end-to-end flows: detect anomaly → rule triggers → dashboard highlights → ask for explanation → receive spoken and on-screen guidance.

## How to Demo (short script for judges)

1. Open the dashboard and point out the live feed and rule panel.
2. Trigger a sensor/vision event (or simulate it) and show the alert.
3. Ask the system (voice or chat) "Why did this alert occur?" — demonstrate the LLM explanation.
4. Ask for recommended next steps and show the suggested actions.
5. Toggle a rule or adjust thresholds live to show configurability.

## What Makes This Project Competitive

- End-to-end integration: from inputs (sensors/vision) through rule evaluation to human-friendly explanations and voice interaction.
- Focus on accessibility and clarity: the conversational layer helps non-expert judges understand system reasoning instantly.
- Modular and demonstrable: each component (`main.py`, `dashboard.py`, `sensors.py`, `rules.py`, `llm_gemini.py`, `voice.py`) can be shown independently or together to illustrate design and implementation choices.

## Files to Point the Judges To

- `main.py` — launch point for the project.
- `dashboard.py` — the web UI controller and demo entry.
- `sensors.py` — adapters & sample inputs for demonstration.
- `rules.py` — rule definitions and evaluator used in the demo.
- `llm_gemini.py` — the conversational/explanation wrapper used to generate human-readable responses.

