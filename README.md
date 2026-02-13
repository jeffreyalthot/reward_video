# reward_video

Application terminal pour piloter un flux **rewarded video** avec actions utilisateur réelles (pas de tirage aléatoire) et journalisation des événements.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copier les variables puis les adapter:

```bash
cp .env.example .env
export $(grep -v '^#' .env | xargs)
```

Variables principales:

- `ADMOB_APP_ID`
- `ADMOB_REWARDED_AD_UNIT_ID`
- `GOOGLE_API_KEY`
- `RUNS` (nombre de cycles)
- `WATCH_SECONDS` (durée d'attente pendant le visionnage)
- `REWARDED_VIDEO_URL` (optionnel: URL à ouvrir automatiquement)
- `EVENTS_LOG_FILE` (optionnel: fichier JSONL des événements, par défaut `events_log.jsonl`)

## Exécution

```bash
python3 app.py
```

## Fonctionnement

1. Démarre l'app terminal et affiche la configuration.
2. Tente d'initialiser le client API AdMob (`google-api-python-client`).
3. Lance une notification locale et ouvre la vidéo si `REWARDED_VIDEO_URL` est définie.
4. Attend la durée de visionnage.
5. Demande une validation utilisateur explicite (`share` / `reject`).
6. Écrit chaque événement dans un journal JSONL horodaté.
7. Affiche les compteurs et le récapitulatif final.

## Limite AdMob importante

Les impressions rewarded officiellement comptées par AdMob nécessitent le SDK Mobile Ads Android/iOS. Ce script terminal enregistre des actions utilisateur locales mais ne remplace pas les callbacks SDK mobile (`onUserEarnedReward`, etc.).
