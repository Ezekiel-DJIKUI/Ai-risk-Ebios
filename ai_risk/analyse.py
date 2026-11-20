"""Analyse des risques d'un système d'IA décrit en JSON."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .catalogue import CARACTERISTIQUES, CATALOGUE, IMPACTS, Mesure, Scenario

NIVEAUX_GRAVITE = {1: "Mineure", 2: "Significative", 3: "Grave", 4: "Critique"}
NIVEAUX_VRAISEMBLANCE = {1: "Peu vraisemblable", 2: "Vraisemblable", 3: "Très vraisemblable", 4: "Quasi certain"}


@dataclass
class Risque:
    scenario: Scenario
    gravite: int
    vraisemblance_initiale: int
    vraisemblance_residuelle: int
    mesures_en_place: list[Mesure]
    mesures_manquantes: list[Mesure]

    @property
    def niveau_initial(self) -> int:
        return self.gravite * self.vraisemblance_initiale

    @property
    def niveau_residuel(self) -> int:
        return self.gravite * self.vraisemblance_residuelle

    @property
    def priorite(self) -> str:
        n = self.niveau_residuel
        return "P1 – inacceptable" if n >= 9 else "P2 – à traiter" if n >= 5 else "P3 – acceptable sous surveillance"


def charger_systeme(chemin: str | Path) -> dict:
    with open(chemin, encoding="utf-8") as f:
        systeme = json.load(f)
    valider_systeme(systeme)
    return systeme


def valider_systeme(systeme: dict) -> None:
    inconnues = set(systeme.get("caracteristiques", [])) - set(CARACTERISTIQUES)
    if inconnues:
        raise ValueError(f"caractéristiques inconnues : {sorted(inconnues)}")
    gravites = systeme.get("gravite_par_impact", {})
    for impact in IMPACTS:
        g = gravites.get(impact)
        if g not in NIVEAUX_GRAVITE:
            raise ValueError(f"gravité manquante ou invalide pour « {impact} » (1 à 4)")


def analyser(systeme: dict) -> list[Risque]:
    caract = set(systeme.get("caracteristiques", []))
    en_place = set(systeme.get("mesures_en_place", []))
    risques = []
    for sc in CATALOGUE:
        if not set(sc.si) <= caract:
            continue
        v0 = sc.vraisemblance
        # Exposition publique : la surface d'attaque augmente la vraisemblance (plafonnée à 4).
        if "expose_public" in caract and "expose_public" not in sc.si and sc.source_risque.startswith("Utilisateur"):
            v0 = min(4, v0 + 1)
        appliquees = [m for m in sc.mesures if m.id in en_place]
        manquantes = [m for m in sc.mesures if m.id not in en_place]
        v1 = max(1, v0 - sum(m.reduction for m in appliquees))
        risques.append(Risque(sc, systeme["gravite_par_impact"][sc.impact], v0, v1, appliquees, manquantes))
    return sorted(risques, key=lambda r: (-r.niveau_residuel, -r.gravite, r.scenario.id))
