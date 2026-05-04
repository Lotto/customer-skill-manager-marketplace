# Customer Skill Manager — Marketplace

> Marketplace officiel des plugins Claude Code distribués via Customer Skill Manager (CSM).

## Plugins disponibles

| Plugin | Description | Version |
|---|---|---|
| [`csm-loader`](./plugins/csm-loader) | Stub léger qui charge dynamiquement les ressources métier (instructions, templates, grilles tarifaires) depuis le serveur CSM en fonction de la licence du client. | 1.0.0 |

## Installation

### 1. Ajouter ce marketplace à Claude Code

```bash
/plugin marketplace add https://github.com/Lotto/customer-skill-manager-marketplace
```

### 2. Installer le plugin

```bash
/plugin install csm-loader@customer-skill-manager
```

### 3. Configurer la clé de licence

Voir la [documentation du plugin](./plugins/csm-loader/README.md#3-configurer-la-clé-de-licence).

## Comment ça fonctionne

Customer Skill Manager (CSM) permet à des éditeurs de skills métier de **distribuer, mettre à jour et révoquer** dynamiquement leurs contenus auprès de leurs clients, sans toucher à l'infrastructure Claude du client.

- **Le client** installe ce plugin léger une seule fois et configure sa clé de licence.
- **L'éditeur** met à jour les ressources côté serveur CSM ; les changements sont disponibles instantanément chez tous les clients actifs.
- **La révocation** est immédiate en cas de non-paiement (le serveur retourne 402).
- **Le contenu** est filigrané par licence, ce qui permet de tracer toute fuite éventuelle.

## Architecture

```
csm-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # catalogue
├── plugins/
│   └── csm-loader/
│       ├── .claude-plugin/
│       │   └── plugin.json       # manifest du plugin
│       ├── skills/
│       │   └── csm-loader/
│       │       └── SKILL.md      # stub principal
│       ├── scripts/
│       │   └── fetch.py          # client HTTP du serveur CSM
│       └── README.md
└── README.md
```

## Pour les revendeurs

Si vous êtes éditeur de skills métier et souhaitez distribuer vos contenus via CSM, contactez l'équipe Customer Skill Manager.

## Licence

Plugin sous licence **propriétaire**. Utilisation conditionnée à une licence CSM active.
