#!/usr/bin/env python3
"""Terminal app that automates a rewarded-video flow for AdMob-like usage."""

from __future__ import annotations

import os
import random
import subprocess
import time
from dataclasses import dataclass


try:
    # Optional dependency: demonstrates Google SDK usage for API initialization.
    from googleapiclient.discovery import build  # type: ignore
except Exception:  # dependency may not be installed in minimal environments
    build = None


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
        share_probability: float = 0.75,
    ) -> None:
        self.app_id = app_id
        self.ad_unit_id = ad_unit_id
        self.api_key = api_key
        self.runs = runs
        self.watch_seconds = watch_seconds
        self.share_probability = share_probability
        self.stats = AppStats()

    def setup_google_sdk(self) -> None:
        """Initialize Google SDK client when available.

        Note: rewarded ad serving is handled by mobile SDKs. In terminal mode,
        we only validate SDK access and keep a simulated playback flow.
        """
        if build is None:
            print("[INFO] google-api-python-client non installé -> mode simulation.")
            return

        if not self.api_key:
            print("[INFO] GOOGLE_API_KEY absent -> mode simulation.")
            return

        try:
            _ = build("admob", "v1", developerKey=self.api_key, cache_discovery=False)
            print("[OK] SDK Google initialisé (API AdMob client prêt).")
        except Exception as err:
            print(f"[WARN] Initialisation SDK Google impossible: {err}")
            print("[INFO] Poursuite en mode simulation locale.")

    def notify(self, message: str) -> None:
        print(f"\n[NOTIFICATION] {message}")
        try:
            subprocess.run(["notify-send", "Reward Video", message], check=False)
        except FileNotFoundError:
            pass

    def play_reward_video(self) -> bool:
        """Simulate watching a rewarded video and auto decide share/reject."""
        self.notify("Lecture automatique d'une vidéo reward...")
        for second in range(1, self.watch_seconds + 1):
            print(f"  ▶ Vidéo en cours... {second}/{self.watch_seconds}s", end="\r", flush=True)
            time.sleep(1)
        print()
        return random.random() < self.share_probability

    def run(self) -> None:
        print("=== Reward Video Terminal App (AdMob) ===")
        print(f"App ID      : {self.app_id or 'NON CONFIGURÉ'}")
        print(f"Ad Unit ID  : {self.ad_unit_id or 'NON CONFIGURÉ'}")
        print("----------------------------------------")
        self.setup_google_sdk()

        for index in range(1, self.runs + 1):
            print(f"\nCycle {index}/{self.runs}")
            shared = self.play_reward_video()
            if shared:
                self.stats.shares += 1
                print("✅ SHARE envoyé automatiquement dans le terminal.")
            else:
                self.stats.rejects += 1
                print("❌ REJECT enregistré automatiquement dans le terminal.")

            print(
                f"Compteurs => share: {self.stats.shares} | reject: {self.stats.rejects}"
            )

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
        share_probability=float(os.getenv("SHARE_PROBABILITY", "0.7")),
    )
    app.run()
