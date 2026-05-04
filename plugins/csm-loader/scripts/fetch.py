#!/usr/bin/env python3
"""
Customer Skill Manager — Resource Fetcher
==========================================

Récupère les ressources métier depuis le serveur CSM en fonction
de la licence active du client.

Usage:
    python fetch.py <resource_name>

Variables d'environnement:
    CSM_LICENSE_KEY  (obligatoire)  Clé de licence du client
    CSM_ENDPOINT     (optionnel)    URL du serveur CSM (défaut: production)
    CSM_TIMEOUT      (optionnel)    Timeout en secondes (défaut: 15)

Codes de sortie:
    0   Succès
    1   Erreur HTTP (402, 403, 429, 5xx)
    2   Erreur réseau ou timeout
    3   Erreur de configuration (clé manquante, mauvais argument)
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import urllib.parse

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

DEFAULT_ENDPOINT = "https://api.customer-skill-manager.example.com/v1/skill-resource"
DEFAULT_TIMEOUT = 15
MAX_RETRIES = 2
RETRY_DELAY = 1.5  # secondes

ENDPOINT = os.getenv("CSM_ENDPOINT", DEFAULT_ENDPOINT)
LICENSE_KEY = os.getenv("CSM_LICENSE_KEY", "").strip()
TIMEOUT = int(os.getenv("CSM_TIMEOUT", DEFAULT_TIMEOUT))

USER_AGENT = "csm-loader/1.0.0 (python-urllib)"


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def fail(message: str, code: int = 1) -> None:
    """Affiche une erreur structurée sur stderr et quitte."""
    sys.stderr.write(f"[CSM ERROR] {message}\n")
    sys.exit(code)


def fetch_resource(resource_name: str) -> str:
    """Appelle le serveur CSM avec retry sur erreur 5xx."""
    params = urllib.parse.urlencode({"resource": resource_name})
    url = f"{ENDPOINT}?{params}"

    headers = {
        "X-License-Key": LICENSE_KEY,
        "User-Agent": USER_AGENT,
        "Accept": "text/markdown, text/plain, application/json",
    }

    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                return response.read().decode("utf-8")

        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8")
            except Exception:
                pass

            # Erreurs définitives — pas de retry
            if e.code in (402, 403, 404, 429):
                msg = f"HTTP {e.code}"
                if e.code == 402:
                    msg += " — Licence inactive ou abonnement impayé. Contactez le support CSM."
                elif e.code == 403:
                    msg += " — Licence invalide ou ressource non autorisée."
                elif e.code == 404:
                    msg += f" — Ressource '{resource_name}' introuvable."
                elif e.code == 429:
                    msg += " — Trop de requêtes. Réessayez dans quelques minutes."
                if body:
                    msg += f"\nDétail serveur: {body[:500]}"
                fail(msg, code=1)

            # Erreurs serveur — retry possible
            if 500 <= e.code < 600 and attempt < MAX_RETRIES:
                last_error = f"HTTP {e.code} (tentative {attempt + 1}/{MAX_RETRIES + 1})"
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue

            fail(f"HTTP {e.code} — Erreur serveur CSM. {body[:200]}", code=1)

        except urllib.error.URLError as e:
            if attempt < MAX_RETRIES:
                last_error = f"Erreur réseau (tentative {attempt + 1}/{MAX_RETRIES + 1}): {e.reason}"
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            fail(f"Erreur réseau: {e.reason}. Vérifiez votre connexion internet.", code=2)

        except TimeoutError:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            fail(f"Timeout après {TIMEOUT}s. Le serveur CSM ne répond pas.", code=2)

        except Exception as e:
            fail(f"Erreur inattendue: {type(e).__name__}: {e}", code=2)

    fail(f"Échec après {MAX_RETRIES + 1} tentatives. Dernière erreur: {last_error}", code=2)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> None:
    if sys.version_info < (3, 10):
        fail(
            f"Python 3.10+ requis (version détectée: "
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}). "
            "Mettez à jour Python pour utiliser le plugin CSM.",
            code=3,
        )

    if len(sys.argv) != 2:
        fail("Usage: python fetch.py <resource_name>", code=3)

    resource = sys.argv[1].strip()
    if not resource:
        fail("Le nom de la ressource ne peut pas être vide.", code=3)

    # Validation basique du nom de ressource (alphanumérique, tirets, underscores)
    if not all(c.isalnum() or c in "-_" for c in resource):
        fail(f"Nom de ressource invalide: '{resource}' (alphanumériques, tirets et underscores uniquement)", code=3)

    if not LICENSE_KEY:
        fail(
            "Variable d'environnement CSM_LICENSE_KEY manquante.\n"
            "Configurez-la avec la clé fournie par le support Customer Skill Manager.",
            code=3,
        )

    content = fetch_resource(resource)
    sys.stdout.write(content)
    if not content.endswith("\n"):
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
