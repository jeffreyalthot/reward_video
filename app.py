#!/usr/bin/env python3
"""Terminal app for rewarded-video workflow with explicit user actions."""

from __future__ import annotations

import importlib
import json
import os
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class AppStats:
    shares: int = 0
    rejects: int = 0


class RewardVideoTerminalApp:
    def __init__(
        self,
        app_id: str,
        ad_unit_id: str,
        api_key: str,
        runs: int = 10,
        watch_seconds: int = 5,
        video_url: str = "",
        log_file: str = "events_log.jsonl",
    ) -> None:
        self.app_id = app_id
        self.ad_unit_id = ad_unit_id
        self.api_key = api_key
        self.runs = runs
        self.watch_seconds = watch_seconds
        self.video_url = video_url
        self.log_file = Path(log_file)
        self.stats = AppStats()

    def _load_google_build(self):
        module = importlib.import_module("googleapiclient.discovery")
        return getattr(module, "build", None)

    def setup_google_sdk(self) -> None:
        """Initialize Google API client when available."""
        try:
            build = self._load_google_build()
        except ModuleNotFoundError:
            print("[INFO] google-api-python-client non installé.")
            return

        if not self.api_key:
            print("[INFO] GOOGLE_API_KEY absent -> initialisation API ignorée.")
            return

        try:
            _ = build("admob", "v1", developerKey=self.api_key, cache_discovery=False)
            print("[OK] Client API Google AdMob initialisé.")
        except Exception as err:
            print(f"[WARN] Initialisation API Google impossible: {err}")

    def notify(self, message: str) -> None:
        print(f"\n[NOTIFICATION] {message}")
        try:
            subprocess.run(["notify-send", "Reward Video", message], check=False)
        except FileNotFoundError:
            pass

    def _prompt_choice(self, prompt: str, allowed: set[str]) -> str:
        while True:
            user_input = input(prompt).strip().lower()
            if user_input in allowed:
                return user_input
            print(f"Valeur invalide. Choix attendus: {', '.join(sorted(allowed))}")

    def _open_video_if_configured(self) -> None:
        if not self.video_url:
            return
        try:
            subprocess.run(["xdg-open", self.video_url], check=False)
            print(f"[INFO] Vidéo ouverte: {self.video_url}")
        except FileNotFoundError:
            print("[INFO] xdg-open indisponible, ouvrez la vidéo manuellement.")

    def _log_event(self, cycle: int, action: str) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cycle": cycle,
            "action": action,
            "app_id": self.app_id,
            "ad_unit_id": self.ad_unit_id,
        }
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with self.log_file.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(event, ensure_ascii=False) + "\n")

    def play_reward_video(self, cycle: int) -> str:
        self.notify("Lecture d'une vidéo reward.")
        self._open_video_if_configured()

        print(
            f"Patientez {self.watch_seconds}s pendant le visionnage "
            "(ou regardez la vidéo depuis l'URL configurée)."
        )
        for second in range(1, self.watch_seconds + 1):
            print(f"  ▶ Vidéo en cours... {second}/{self.watch_seconds}s", end="\r", flush=True)
            time.sleep(1)
        print()

        watched = self._prompt_choice("La vidéo a été regardée entièrement ? (y/n): ", {"y", "n"})
        if watched == "n":
            return "reject"

        return self._prompt_choice("Action utilisateur finale (share/reject): ", {"share", "reject"})

    def run(self) -> None:
        print("=== Reward Video Terminal App (AdMob) ===")
        print(f"App ID      : {self.app_id or 'NON CONFIGURÉ'}")
        print(f"Ad Unit ID  : {self.ad_unit_id or 'NON CONFIGURÉ'}")
        print(f"Event log   : {self.log_file}")
        print("----------------------------------------")
        self.setup_google_sdk()

        for index in range(1, self.runs + 1):
            print(f"\nCycle {index}/{self.runs}")
            action = self.play_reward_video(index)
            self._log_event(index, action)

            if action == "share":
                self.stats.shares += 1
                print("✅ SHARE enregistré.")
            else:
                self.stats.rejects += 1
                print("❌ REJECT enregistré.")

            print(f"Compteurs => share: {self.stats.shares} | reject: {self.stats.rejects}")

        print("\n=== Résultat final ===")
        print(f"Nombre de share : {self.stats.shares}")
        print(f"Nombre de reject: {self.stats.rejects}")


if __name__ == "__main__":
    app = RewardVideoTerminalApp(
        app_id=os.getenv("ADMOB_APP_ID", ""),
        ad_unit_id=os.getenv("ADMOB_REWARDED_AD_UNIT_ID", ""),
        api_key=os.getenv("GOOGLE_API_KEY", ""),
        runs=int(os.getenv("RUNS", "5")),
        watch_seconds=int(os.getenv("WATCH_SECONDS", "3")),
        video_url=os.getenv("REWARDED_VIDEO_URL", ""),
        log_file=os.getenv("EVENTS_LOG_FILE", "events_log.jsonl"),
    )
    app.run()
