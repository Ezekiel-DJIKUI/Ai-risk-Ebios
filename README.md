# AI-Risk — analyse des risques d'un système d'IA, inspirée d'EBIOS RM

Outil en Python qui produit une **première analyse des risques de sécurité d'un système d'IA** (assistant, RAG, agent) : scénarios de menace propres à l'IA, cartographie gravité × vraisemblance, effet des mesures déjà en place et **plan de traitement priorisé**.

> Projet personnel – 2026 (en cours). Le système analysé dans l'exemple est **fictif**.

## Pourquoi

Les analyses de risques classiques couvrent mal les menaces propres à l'IA : injection de prompt, fuite de données dans les réponses, autonomie excessive d'un agent, hallucinations, dépendance au fournisseur du modèle. L'objectif est de préparer un atelier de gestion des risques en partant d'un catalogue structuré, plutôt que d'une page blanche. L'outil ne remplace pas l'atelier : la gravité et les mesures sont à valider avec les métiers, le RSSI et le DPO.

## Démarche

1. **Description du système** (JSON) : ses caractéristiques (`llm`, `rag`, `agent_outils`, `donnees_personnelles`, `modele_tiers`, `expose_public`, `entrainement_maison`), la gravité d'une atteinte à chaque critère (confidentialité, intégrité, disponibilité, conformité, de 1 à 4), et les mesures déjà en place.
2. **Sélection des scénarios** applicables parmi un catalogue de 9 menaces propres à l'IA, chacune avec sa source de risque.
3. **Évaluation** : gravité × vraisemblance. La vraisemblance augmente si le système est exposé au public.
4. **Traitement** : chaque mesure en place réduit la vraisemblance ; le risque résiduel est classé P1 (inacceptable), P2 (à traiter) ou P3 (acceptable sous surveillance).
5. **Rapport Markdown** : deux cartographies (initiale et résiduelle) et le plan de traitement, avec les mesures manquantes.

## Utilisation

```bash
python -m pip install -r requirements.txt
python -m ai_risk data/assistant_rag_exemple.json -o exemple_rapport.md
python -m pytest -q
```

## Résultat sur l'exemple

Assistant client en ligne d'un assureur fictif (RAG sur les contrats, création de demandes de rappel, modèle fourni par un tiers) : 8 scénarios retenus. Le risque prioritaire (P1) est la **fuite de données personnelles dans les réponses**, de gravité critique, faute de contrôle d'accès appliqué au moment de la recherche documentaire. Voir [`exemple_rapport.md`](exemple_rapport.md).

## Limites

- Catalogue volontairement court, à enrichir avec des référentiels publics de menaces sur l'IA.
- Les niveaux de vraisemblance et l'effet des mesures sont des valeurs de départ, à calibrer en atelier.

## Pistes d'évolution

- Ajouter les parties prenantes et les chemins d'attaque, pour se rapprocher des ateliers 3 et 4 d'EBIOS RM.
- Exporter la cartographie en graphique et le plan de traitement en tableur.
- Relier chaque mesure aux exigences réglementaires applicables.
