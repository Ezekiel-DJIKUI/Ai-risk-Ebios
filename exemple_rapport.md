# Analyse des risques IA – Assistant client « Aide Contrats » (fictif)

*Générée le 2026-11-20 – méthode inspirée d'EBIOS RM. À valider en atelier avec les métiers, le RSSI et le DPO.*

## Périmètre

Assistant conversationnel en ligne d'un assureur fictif. Il répond aux questions des clients sur leurs contrats en s'appuyant sur une base documentaire (conditions générales, FAQ, courriers) et peut créer une demande de rappel dans le CRM. Le modèle est fourni par un éditeur tiers via API.

Caractéristiques : llm, rag, agent_outils, donnees_personnelles, modele_tiers, expose_public

## Synthèse

- 8 scénarios de risque retenus
- 1 risque(s) résiduel(s) inacceptable(s) (P1)

## Cartographie des risques initiaux

| Gravité \ Vraisemblance | 1 Peu vraisemblable | 2 Vraisemblable | 3 Très vraisemblable | 4 Quasi certain |
|---|---|---|---|---|
| **4 Critique** | · | IA-07 | · | IA-03 |
| **3 Grave** | · | IA-02, IA-08 | IA-01, IA-04, IA-06 | · |
| **2 Significative** | · | IA-09 | · | · |
| **1 Mineure** | · | · | · | · |

## Cartographie des risques résiduels (mesures en place)

| Gravité \ Vraisemblance | 1 Peu vraisemblable | 2 Vraisemblable | 3 Très vraisemblable | 4 Quasi certain |
|---|---|---|---|---|
| **4 Critique** | · | IA-07 | · | IA-03 |
| **3 Grave** | · | IA-01, IA-02, IA-04, IA-06, IA-08 | · | · |
| **2 Significative** | IA-09 | · | · | · |
| **1 Mineure** | · | · | · | · |

## Détail et plan de traitement

| Priorité | Scénario | Gravité | Vraisemblance init. → résid. | Mesures à mettre en place |
|---|---|---|---|---|
| P1 – inacceptable | **IA-03** Fuite de données sensibles dans les réponses | 4 | 4 → 4 | M-05 Contrôle d'accès aux documents appliqué au moment de la recherche<br>M-06 Filtrage des sorties (données personnelles)<br>M-07 Minimisation des données indexées |
| P2 – à traiter | **IA-07** Dépendance et fuite chez le fournisseur du modèle | 4 | 2 → 2 | M-14 Clauses contractuelles : non-réutilisation des données, localisation, réversibilité<br>M-15 Plan de continuité en cas d'indisponibilité du fournisseur |
| P2 – à traiter | **IA-01** Injection de prompt directe | 3 | 3 → 2 | M-01 Filtrage et validation des entrées<br>M-03 Tests d'attaque adverses (red teaming) avant mise en production |
| P2 – à traiter | **IA-02** Injection de prompt indirecte via les documents | 3 | 2 → 2 | M-04 Contrôle de l'origine et de l'intégrité des documents indexés<br>M-01 Filtrage et validation des entrées |
| P2 – à traiter | **IA-04** Actions non souhaitées par un agent (autonomie excessive) | 3 | 3 → 2 | M-08 Validation humaine des actions à impact |
| P2 – à traiter | **IA-06** Hallucination prise pour une information fiable | 3 | 3 → 2 | M-13 Avertissement et vérification humaine pour les usages sensibles |
| P2 – à traiter | **IA-08** Non-conformité réglementaire du traitement | 3 | 2 → 2 | M-16 Registre de traitement et analyse d'impact (AIPD) à jour<br>M-17 Information des utilisateurs sur l'usage de l'IA |
| P3 – acceptable sous surveillance | **IA-09** Déni de service par surconsommation | 2 | 2 → 1 | M-19 Supervision des coûts et alertes |
