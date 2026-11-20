from pathlib import Path

import pytest

from ai_risk.analyse import analyser, charger_systeme, valider_systeme
from ai_risk.rapport import generer

DATA = Path(__file__).resolve().parent.parent / "data"
GRAV = {"confidentialite": 4, "integrite": 3, "disponibilite": 2, "conformite": 3}


def test_exemple_scenarios_et_priorites():
    risques = analyser(charger_systeme(DATA / "assistant_rag_exemple.json"))
    ids = {r.scenario.id for r in risques}
    assert {"IA-01", "IA-02", "IA-03", "IA-04", "IA-06", "IA-07", "IA-08", "IA-09"} <= ids
    assert "IA-05" not in ids  # pas d'entraînement maison
    fuite = next(r for r in risques if r.scenario.id == "IA-03")
    assert fuite.gravite == 4 and fuite.priorite.startswith("P1")
    assert risques[0].niveau_residuel == max(r.niveau_residuel for r in risques)  # tri


def test_mesures_reduisent_le_risque():
    base = {"caracteristiques": ["agent_outils"], "gravite_par_impact": GRAV, "mesures_en_place": []}
    sans = analyser(base)[0]
    avec = analyser({**base, "mesures_en_place": ["M-08"]})[0]
    assert avec.vraisemblance_residuelle == max(1, sans.vraisemblance_residuelle - 2)
    assert [m.id for m in avec.mesures_manquantes] == ["M-09"]


def test_exposition_publique_augmente_la_vraisemblance():
    interne = analyser({"caracteristiques": ["llm", "donnees_personnelles"], "gravite_par_impact": GRAV})
    public = analyser({"caracteristiques": ["llm", "donnees_personnelles", "expose_public"], "gravite_par_impact": GRAV})
    v = lambda rs: next(r for r in rs if r.scenario.id == "IA-03").vraisemblance_initiale
    assert v(public) == v(interne) + 1


def test_validation_des_entrees():
    with pytest.raises(ValueError):
        valider_systeme({"caracteristiques": ["inconnue"], "gravite_par_impact": GRAV})
    with pytest.raises(ValueError):
        valider_systeme({"caracteristiques": ["llm"], "gravite_par_impact": {"confidentialite": 9}})


def test_rapport_markdown():
    s = charger_systeme(DATA / "assistant_rag_exemple.json")
    md = generer(s, analyser(s))
    assert "Cartographie des risques résiduels" in md and "IA-03" in md
