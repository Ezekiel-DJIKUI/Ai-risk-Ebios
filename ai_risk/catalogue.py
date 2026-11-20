"""Catalogue de scénarios de menace propres aux systèmes d'IA et des mesures associées.

Échelles (inspirées d'EBIOS RM) :
  gravité       1 Mineure, 2 Significative, 3 Grave, 4 Critique
  vraisemblance 1 Peu vraisemblable, 2 Vraisemblable, 3 Très vraisemblable, 4 Quasi certain

Chaque scénario s'applique si le système possède TOUTES les caractéristiques de `si`.
Chaque mesure réduit la vraisemblance d'un certain nombre de niveaux.
"""
from __future__ import annotations

from dataclasses import dataclass, field

CARACTERISTIQUES = {
    "llm": "utilise un modèle de langage",
    "rag": "interroge une base documentaire (RAG)",
    "agent_outils": "peut appeler des outils ou déclencher des actions",
    "donnees_personnelles": "traite des données personnelles",
    "modele_tiers": "repose sur un modèle ou une API d'un fournisseur tiers",
    "expose_public": "accessible par des utilisateurs externes",
    "entrainement_maison": "modèle entraîné ou affiné sur des données internes",
}

IMPACTS = ("confidentialite", "integrite", "disponibilite", "conformite")


@dataclass(frozen=True)
class Mesure:
    id: str
    nom: str
    reduction: int = 1


@dataclass(frozen=True)
class Scenario:
    id: str
    nom: str
    description: str
    source_risque: str
    si: tuple[str, ...]
    impact: str
    vraisemblance: int
    mesures: tuple[Mesure, ...] = field(default_factory=tuple)


M = Mesure
CATALOGUE: tuple[Scenario, ...] = (
    Scenario("IA-01", "Injection de prompt directe",
             "Un utilisateur détourne les consignes du modèle pour obtenir un comportement non prévu.",
             "Utilisateur malveillant", ("llm", "expose_public"), "integrite", 3,
             (M("M-01", "Filtrage et validation des entrées"), M("M-02", "Séparation stricte consignes système / contenu utilisateur"),
              M("M-03", "Tests d'attaque adverses (red teaming) avant mise en production"))),
    Scenario("IA-02", "Injection de prompt indirecte via les documents",
             "Un document piégé ajouté à la base documentaire contient des instructions exécutées par le modèle.",
             "Attaquant externe ou interne", ("llm", "rag"), "integrite", 2,
             (M("M-04", "Contrôle de l'origine et de l'intégrité des documents indexés"), M("M-01", "Filtrage et validation des entrées"))),
    Scenario("IA-03", "Fuite de données sensibles dans les réponses",
             "Le modèle restitue des données personnelles ou confidentielles à un utilisateur non habilité.",
             "Utilisateur curieux ou malveillant", ("llm", "donnees_personnelles"), "confidentialite", 3,
             (M("M-05", "Contrôle d'accès aux documents appliqué au moment de la recherche"), M("M-06", "Filtrage des sorties (données personnelles)"),
              M("M-07", "Minimisation des données indexées"))),
    Scenario("IA-04", "Actions non souhaitées par un agent (autonomie excessive)",
             "L'agent déclenche une action à impact (envoi, suppression, paiement) sur une instruction manipulée ou mal comprise.",
             "Utilisateur malveillant ou erreur du modèle", ("agent_outils",), "integrite", 2,
             (M("M-08", "Validation humaine des actions à impact", 2), M("M-09", "Droits minimaux pour les outils de l'agent"))),
    Scenario("IA-05", "Empoisonnement des données d'entraînement",
             "Des données manipulées introduites dans l'entraînement biaisent ou piègent le modèle.",
             "Attaquant interne ou fournisseur de données", ("entrainement_maison",), "integrite", 2,
             (M("M-10", "Traçabilité et validation des jeux de données"), M("M-11", "Évaluation du modèle sur un jeu de référence avant déploiement"))),
    Scenario("IA-06", "Hallucination prise pour une information fiable",
             "Le modèle invente une réponse plausible, utilisée sans vérification pour une décision.",
             "Défaillance du modèle", ("llm",), "integrite", 3,
             (M("M-12", "Citation systématique des sources dans les réponses"), M("M-13", "Avertissement et vérification humaine pour les usages sensibles"))),
    Scenario("IA-07", "Dépendance et fuite chez le fournisseur du modèle",
             "Les requêtes envoyées au fournisseur tiers sont conservées ou réutilisées, ou le service devient indisponible.",
             "Fournisseur tiers", ("modele_tiers",), "confidentialite", 2,
             (M("M-14", "Clauses contractuelles : non-réutilisation des données, localisation, réversibilité"), M("M-15", "Plan de continuité en cas d'indisponibilité du fournisseur"))),
    Scenario("IA-08", "Non-conformité réglementaire du traitement",
             "Traitement de données personnelles par l'IA sans base légale, information des personnes ni analyse d'impact.",
             "Organisation elle-même", ("donnees_personnelles",), "conformite", 2,
             (M("M-16", "Registre de traitement et analyse d'impact (AIPD) à jour"), M("M-17", "Information des utilisateurs sur l'usage de l'IA"))),
    Scenario("IA-09", "Déni de service par surconsommation",
             "Des requêtes massives ou très longues épuisent le quota ou le budget et rendent le service indisponible.",
             "Utilisateur malveillant", ("llm", "expose_public"), "disponibilite", 2,
             (M("M-18", "Limitation de débit et de taille des requêtes"), M("M-19", "Supervision des coûts et alertes"))),
)
