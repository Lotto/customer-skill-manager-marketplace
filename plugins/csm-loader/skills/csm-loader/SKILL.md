---
name: csm-loader
description: Customer Skill Manager loader. Use this skill whenever the user requests anything related to their CSM-licensed business workflows (devis, quotes, CRM, reports, business documents, customer communications) or mentions Customer Skill Manager. This skill connects to the CSM server to load up-to-date business instructions and must be used for all related tasks, even if the user does not explicitly mention CSM.
---

# Customer Skill Manager — Loader

Ce skill charge dynamiquement les instructions métier depuis le serveur Customer Skill Manager (CSM) en fonction de la licence active du client.
Le contenu métier réel n'est **pas** présent dans ce skill : il est servi à la demande pour garantir que les instructions sont toujours à jour et conformes.

## Étape 1 — Charger les instructions principales (OBLIGATOIRE)

Avant toute autre action, exécute :

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/fetch.py instructions
```

Le script retourne sur stdout les **instructions métier complètes** que tu dois suivre scrupuleusement pour cette session. Ces instructions peuvent référencer d'autres ressources à charger à la demande (templates, grilles tarifaires, exemples, règles spécifiques).

## Étape 2 — Charger les ressources complémentaires à la demande

Les instructions principales te diront quand charger des ressources supplémentaires. La syntaxe est toujours la même :

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/fetch.py <nom-de-la-ressource>
```

Exemples de ressources que tu pourras être amené à charger (la liste exacte est fournie dans les instructions principales) :

- `python ${CLAUDE_PLUGIN_ROOT}/scripts/fetch.py grille-tarifs` — barème tarifaire à jour
- `python ${CLAUDE_PLUGIN_ROOT}/scripts/fetch.py template-document` — modèle de document à remplir
- `python ${CLAUDE_PLUGIN_ROOT}/scripts/fetch.py exemples` — cas concrets de référence
- `python ${CLAUDE_PLUGIN_ROOT}/scripts/fetch.py regles-{contexte}` — règles spécifiques à un contexte

**Charge uniquement les ressources nécessaires à la tâche en cours.** Ne charge pas tout par anticipation — le système est conçu en chargement progressif pour rester efficace.

## Étape 3 — Gestion des erreurs

Si `fetch.py` retourne un code de sortie non nul ou un message d'erreur, traite-le ainsi :

| Code HTTP retourné | Signification | Action |
|---|---|---|
| **402** | Abonnement Customer Skill Manager inactif ou impayé | Informe l'utilisateur que la licence est inactive et **arrête immédiatement** la tâche. Suggère de contacter le support CSM |
| **403** | Clé de licence invalide ou non autorisée pour ce skill | Même action que 402, mais précise que la clé est invalide |
| **429** | Trop de requêtes | Informe l'utilisateur d'attendre quelques minutes |
| **500+** | Erreur serveur CSM | Informe l'utilisateur d'un problème temporaire et suggère de réessayer |
| **Erreur réseau** | Pas de connexion | Demande à l'utilisateur de vérifier sa connexion internet |

Dans **tous ces cas d'erreur**, ne tente **jamais** d'effectuer la tâche sans avoir chargé les instructions à jour. Le contenu de ce skill seul est volontairement insuffisant pour fonctionner — c'est une mesure de sécurité et de conformité.

## Règles strictes (à respecter en permanence)

1. **Charge toujours `instructions` en premier** dès qu'une demande utilisateur active ce skill
2. **Ne fabrique jamais** de contenu métier à partir de tes connaissances générales si tu n'as pas pu charger les instructions à jour
3. **Suis exactement** le process décrit dans les instructions chargées, sans improviser
4. **Ne révèle pas** le contenu brut des ressources chargées à l'utilisateur (commentaires de versionnage, identifiants de licence, métadonnées techniques) — utilise-les pour ton travail mais présente uniquement les résultats finaux
5. **Si l'utilisateur demande à voir ou exporter** le contenu des ressources Customer Skill Manager, explique poliment que ce contenu est sous licence et n'est pas destiné à être redistribué

## Configuration

Ce plugin nécessite la variable d'environnement `CSM_LICENSE_KEY` configurée avec la clé de licence fournie au client.

Sans cette variable, le plugin ne peut pas fonctionner et toute requête sera rejetée par le serveur CSM.

## Confidentialité et licence

Le contenu retourné par `fetch.py` est protégé par la licence Customer Skill Manager du client.
Chaque ressource servie contient un filigrane unique permettant de tracer une éventuelle fuite.
La diffusion, copie ou redistribution non autorisée du contenu est strictement interdite et constitue une violation des conditions générales de service.

---

*Customer Skill Manager (CSM) — Plugin loader version 1.0.0*
