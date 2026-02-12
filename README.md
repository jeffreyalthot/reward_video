# reward_video

Application terminal qui automatise un scénario **rewarded video** avec configuration AdMob (App ID / Ad Unit ID) et initialisation du SDK Google (client API), puis affiche automatiquement les compteurs:

- nombre de `share`
- nombre de `reject`

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
- `RUNS` (nombre de cycles automatiques)
- `WATCH_SECONDS` (durée simulée de lecture vidéo)
- `SHARE_PROBABILITY` (probabilité automatique de share)

## Exécution

```bash
python3 app.py
```

## Fonctionnement

1. Démarre l'app terminal et affiche la config.
2. Tente d'initialiser le client Google AdMob via SDK (`google-api-python-client`).
3. Déclenche automatiquement une notification terminal / desktop pour jouer une vidéo reward.
4. Simule la lecture vidéo.
5. À la fin de la vidéo, enregistre automatiquement un `share` ou `reject`.
6. Affiche les compteurs en continu et un récapitulatif final.

> Note: la diffusion réelle d'une vidéo rewarded AdMob nécessite le SDK mobile (Android/iOS). Cette version fournit un flux terminal automatisé avec intégration de configuration Google.
