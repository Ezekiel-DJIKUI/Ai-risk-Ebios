"""Génération du rapport d'analyse au format Markdown."""
from __future__ import annotations

from datetime import date

from .analyse import NIVEAUX_GRAVITE, NIVEAUX_VRAISEMBLANCE, Risque


def matrice(risques: list[Risque], residuelle: bool) -> str:
    cases: dict[tuple[int, int], list[str]] = {}
    for r in risques:
        v = r.vraisemblance_residuelle if residuelle else r.vraisemblance_initiale
        cases.setdefault((r.gravite, v), []).append(r.scenario.id)
    lignes = ["| Gravité \\ Vraisemblance | " + " | ".join(f"{v} {NIVEAUX_VRAISEMBLANCE[v]}" for v in range(1, 5)) + " |",
              "|---|" + "---|" * 4]
    for g in range(4, 0, -1):
        lignes.append(f"| **{g} {NIVEAUX_GRAVITE[g]}** | " + " | ".join(", ".join(cases.get((g, v), [])) or "·" for v in range(1, 5)) + " |")
    return "\n".join(lignes)


def generer(systeme: dict, risques: list[Risque]) -> str:
    p1 = [r for r in risques if r.priorite.startswith("P1")]
    out = [
        f"# Analyse des risques IA – {systeme.get('nom', 'Système')}",
        "",
        f"*Générée le {date.today().isoformat()} – méthode inspirée d'EBIOS RM. À valider en atelier avec les métiers, le RSSI et le DPO.*",
        "",
        "## Périmètre",
        "",
        systeme.get("description", ""),
        "",
        "Caractéristiques : " + ", ".join(systeme.get("caracteristiques", [])),
        "",
        "## Synthèse",
        "",
        f"- {len(risques)} scénarios de risque retenus",
        f"- {len(p1)} risque(s) résiduel(s) inacceptable(s) (P1)",
        "",
        "## Cartographie des risques initiaux",
        "",
        matrice(risques, residuelle=False),
        "",
        "## Cartographie des risques résiduels (mesures en place)",
        "",
        matrice(risques, residuelle=True),
        "",
        "## Détail et plan de traitement",
        "",
        "| Priorité | Scénario | Gravité | Vraisemblance init. → résid. | Mesures à mettre en place |",
        "|---|---|---|---|---|",
    ]
    for r in risques:
        manquantes = "<br>".join(f"{m.id} {m.nom}" for m in r.mesures_manquantes) or "—"
        out.append(f"| {r.priorite} | **{r.scenario.id}** {r.scenario.nom} | {r.gravite} | "
                   f"{r.vraisemblance_initiale} → {r.vraisemblance_residuelle} | {manquantes} |")
    return "\n".join(out) + "\n"
