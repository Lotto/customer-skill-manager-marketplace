# CSM Loader

> Plugin Customer Skill Manager pour Claude Code

Ce plugin charge dynamiquement les ressources métier (instructions, templates, grilles tarifaires, exemples) depuis le serveur **Customer Skill Manager (CSM)** en fonction de la licence active du client.

## Comment ça marche

Le plugin embarque un **stub léger** : aucun contenu métier n'est présent localement. À chaque demande utilisateur, le skill `csm-loader` invoque le script `fetch.py` qui récupère la ressource appropriée depuis le serveur CSM, en l'authentifiant avec la clé de licence du client.

```
┌─────────────────────────────┐         ┌──────────────────────┐
│  Claude Code (côté client)  │         │  Serveur CSM         │
│                             │  HTTPS  │                      │
│  csm-loader                 │  + key  │  Vérif licence       │
│  ├── SKILL.md (stub)        │────────▶│  Vérif abonnement    │
│  └── scripts/fetch.py       │◀────────│  Watermark + log     │
│                             │ content │  Retour ressource    │
└─────────────────────────────┘         └──────────────────────┘
```

## Prérequis

- **Claude Code** installé
- **Python 3.10+** disponible dans le PATH
- Une **clé de licence CSM active**, fournie par votre revendeur

## Installation

### 1. Ajouter le marketplace

```bash
/plugin marketplace add https://github.com/Lotto/customer-skill-manager-marketplace
```

### 2. Installer le plugin

```bash
/plugin install csm-loader@customer-skill-manager
```

### 3. Configurer la clé de licence

Ajoutez votre clé de licence dans votre environnement shell :

**macOS / Linux** (dans `~/.zshrc` ou `~/.bashrc`) :
```bash
export CSM_LICENSE_KEY="csm_live_votre_cle_ici"
```

**Windows** (PowerShell) :
```powershell
[System.Environment]::SetEnvironmentVariable('CSM_LICENSE_KEY','csm_live_votre_cle_ici','User')
```

Redémarrez votre terminal pour que la variable soit prise en compte.

## Vérification

Démarrez une session Claude Code et tapez :

```
Liste les ressources disponibles via mon plugin CSM.
```

Claude doit déclencher automatiquement le skill `csm-loader`, exécuter `fetch.py instructions`, et présenter les capacités configurées sur votre licence.

## Variables d'environnement

| Variable | Obligatoire | Défaut | Description |
|---|---|---|---|
| `CSM_LICENSE_KEY` | Oui | — | Clé de licence fournie par votre revendeur |
| `CSM_ENDPOINT` | Non | `https://api.customer-skill-manager.example.com/v1/skill-resource` | URL du serveur CSM (utile pour staging/dev) |
| `CSM_TIMEOUT` | Non | `15` | Timeout en secondes pour les appels HTTP |

## Codes d'erreur

| Code HTTP | Signification | Action recommandée |
|---|---|---|
| `402` | Abonnement inactif | Contactez le support pour régulariser |
| `403` | Clé de licence invalide | Vérifiez la valeur de `CSM_LICENSE_KEY` |
| `404` | Ressource inexistante | La ressource n'est pas configurée pour votre licence |
| `429` | Rate limit dépassé | Patientez quelques minutes |
| `5xx` | Erreur serveur | Réessayez plus tard, le plugin retente automatiquement |

## Confidentialité

Le contenu servi par le serveur CSM est **filigrané** par licence. La copie ou redistribution non autorisée est tracable et constitue une violation des conditions générales de service.

## Support

Contactez le support fourni avec votre licence Customer Skill Manager.

## Licence

Plugin distribué sous licence **propriétaire**. L'utilisation requiert une licence CSM active.
