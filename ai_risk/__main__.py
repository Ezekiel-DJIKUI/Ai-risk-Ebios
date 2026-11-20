"""python -m ai_risk data/assistant_rag_exemple.json [-o rapport.md]"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analyse import analyser, charger_systeme
from .rapport import generer


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="ai_risk", description="Analyse des risques d'un système d'IA (inspirée d'EBIOS RM)")
    p.add_argument("systeme", help="description du système en JSON")
    p.add_argument("-o", "--sortie", help="fichier Markdown de sortie (sinon affichage)")
    args = p.parse_args(argv)
    systeme = charger_systeme(args.systeme)
    rapport = generer(systeme, analyser(systeme))
    if args.sortie:
        Path(args.sortie).write_text(rapport, encoding="utf-8")
        print(f"Rapport écrit dans {args.sortie}")
    else:
        print(rapport)
    return 0


if __name__ == "__main__":
    sys.exit(main())
