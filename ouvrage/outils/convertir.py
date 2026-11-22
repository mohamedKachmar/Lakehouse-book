"""Transforme les supports de TP (docs/*.tex) en chapitres de l'ouvrage.

Usage : python3 outils/convertir.py   (depuis le dossier ouvrage/)
Les textes propres à l'ouvrage (titre, objectifs, à retenir, pour aller plus loin) sont dans
outils/chapitres.py ; les supports restent la source du contenu des TP.
"""
import re
import unicodedata
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chapitres import CHAPITRES

DOCS = Path("/home/claude/lakehouse-tp/docs")
OUV = Path(__file__).resolve().parent.parent


def corps(texte):
    """Le contenu après le tableau « En bref », jusqu'à \\end{document}."""
    debut = texte.index("En bref")
    debut = texte.index("\\end{tabularx}", debut) + len("\\end{tabularx}")
    fin = texte.index("\\end{document}")
    return texte[debut:fin].strip("\n")


def extraire_aide_memoire(texte):
    m = re.search(r"\\clearpage\s*\n% =+\n\\section\*\{Annexe -- (Aide-mémoire[^}]*)\}\\label\{sec:aidememoire\}\n% =+\n", texte)
    if not m:
        return texte, None
    return texte[:m.start()], texte[m.end():]


def synthese(texte):
    """« Livrables » devient une synthèse à rédiger, sans consigne de rendu."""
    texte = re.sub(r"\\section\{Livrables\}\\label\{sec:livrables\}", r"\\section{Synthèse}\\label{sec:livrables}", texte)
    texte = re.sub(r"\\subsection\*\{Le compte rendu\}\s*\n\s*Au format PDF, nommé \\cmd\{[^}]*\}, il ne recopie pas le code mais explique vos choix\s*\n\s*et vos résultats\. Il contient :",
                   "Pour faire le point, rédigez une synthèse de ce TP. Elle ne recopie pas le code mais explique\n"
                   "vos choix et vos résultats. Elle couvre :", texte)
    texte = re.sub(r"\n\\subsection\*\{Les notebooks\}.*?(?=\n\\clearpage|\Z)", "\n", texte, flags=re.S)
    return texte


def prefixer_labels(texte, prefixe):
    labels = set(re.findall(r"\\label\{([^}]+)\}", texte))
    # Les captures portent leur étiquette en troisième argument : \capture{fichier}{légende}{étiquette}
    captures = set(re.findall(r"^\\capture\{.*\}\{([a-z]+:[^{}]+)\}\s*$", texte, flags=re.M))
    for lab in sorted(labels | captures, key=len, reverse=True):
        texte = re.sub(r"\\(label|ref|pageref)\{" + re.escape(lab) + r"\}", r"\\\1{" + prefixe + ":" + lab + "}", texte)
        texte = re.sub(r"(^\\capture\{.*\})\{" + re.escape(lab) + r"\}(\s*)$", r"\1{" + prefixe + ":" + lab + r"}\2", texte, flags=re.M)
    return texte


# Entrées d'index pour chaque « Notion clé » (None : pas d'entrée)
INDEX_NOTIONS = {
    "Deux sortes de doublons": "doublon", "Déplier une liste": "explode",
    "Format de fichier, format de table": "format de table", "Fuite de données": "fuite de données",
    "Garder le JSON brut": "JSON", "Heure de l'événement et watermark": "watermark",
    "Idempotence": "idempotence", "Ingestion incrémentale": "ingestion incrémentale",
    "L'apprentissage par transfert": "apprentissage par transfert",
    "Le checkpoint et la garantie \\emph{exactly-once}": "checkpoint",
    "Le déclencheur, ou \\emph{trigger}": "déclencheur (trigger)", "Le journal de Kafka": "Kafka",
    "Le lineage": "lineage", "Le modèle de la couche Gold": "couche Gold",
    "Lire le JSON avec un schéma écrit": "schéma explicite",
    "Mettre à jour une table depuis un flux": "foreachBatch", "On lit les fichiers bruts en texte": "couche Bronze",
    "Orchestrer un pipeline": "orchestration", "Ranger les fichiers": "compactage",
    "Spark Structured Streaming": "Spark Structured Streaming",
    "Structuré, semi-structuré, non structuré": "données semi-structurées",
    "Séparer le stockage et le calcul": "séparation du stockage et du calcul", "TF-IDF": "TF-IDF",
    "Un CSV n'a pas toujours un enregistrement par ligne": "CSV multiligne",
    "Une image est une donnée non structurée": "image",
    "Une valeur nulle n'est pas forcément une erreur": "valeur nulle",
    "dbt (\\emph{data build tool})": "dbt", "Événement et état": "événement",
}


def indexer_notions(texte):
    def ajout(m):
        entree = INDEX_NOTIONS.get(m.group(1))
        if entree is None:
            print("  notion sans entrée d'index :", m.group(1))
            return m.group(0)
        cle = unicodedata.normalize("NFKD", entree).encode("ascii", "ignore").decode().lower()
        return m.group(0) + "\\index{" + (entree if cle == entree else cle + "@" + entree) + "}"
    return re.sub(r"\\begin\{notion\}\[([^\]]+)\]", ajout, texte)


def remplacer(texte, remplacements, nom):
    for avant, apres in remplacements:
        if avant not in texte:
            raise SystemExit(f"{nom} : texte introuvable : {avant[:70]!r}")
        texte = texte.replace(avant, apres)
    return texte


def entete(ch):
    lignes = [f"% {'=' * 69}", f"%  Chapitre {ch['numero']} -- généré par outils/convertir.py depuis docs/{ch['source']}",
              f"% {'=' * 69}",
              f"\\chapter[{ch['court']}]{{{ch['titre']}}}\\label{{{ch['label']}}}",
              f"\\soustitre{{{ch['soustitre']}}}", "", "\\begin{objectifs}"]
    lignes += [f"  \\item {o}" for o in ch["objectifs"]]
    lignes += ["\\end{objectifs}", "", "\\begin{center}\\small\\renewcommand{\\arraystretch}{1.2}",
               "\\begin{tabularx}{\\textwidth}{@{}>{\\bfseries}l X@{}}", "\\toprule"]
    lignes += [f"{k} & {v} \\\\" for k, v in ch["fiche"]]
    lignes += ["\\bottomrule", "\\end{tabularx}", "\\end{center}", ""]
    return "\n".join(lignes)


def fin(ch):
    lignes = ["", "\\begin{aretenir}"] + [f"  \\item {r}" for r in ch["aretenir"]] + ["\\end{aretenir}", ""]
    lignes += ["\\begin{plusloin}", ch["plusloin"], "\\end{plusloin}", ""]
    return "\n".join(lignes)


def main():
    aides = []
    for ch in CHAPITRES:
        texte = (DOCS / ch["source"]).read_text(encoding="utf-8")
        texte = corps(texte)
        texte, aide = extraire_aide_memoire(texte)
        texte = synthese(texte)
        texte = remplacer(texte, ch.get("remplacements", []), ch["source"])
        for motif in ch.get("supprimer", []):
            texte, n = re.subn(motif, "", texte, flags=re.S)
            if n == 0:
                raise SystemExit(f"{ch['source']} : motif à supprimer introuvable : {motif[:60]!r}")
        texte = indexer_notions(texte)
        texte = prefixer_labels(texte, ch["prefixe"])
        texte = re.sub(r"\n\\clearpage\s*$", "\n", texte.rstrip()) + "\n"
        (OUV / "chapitres" / ch["fichier"]).write_text(entete(ch) + texte + fin(ch), encoding="utf-8")
        print("écrit :", ch["fichier"])
        if aide:
            aide = aide.replace("\\end{document}", "").strip()
            aides.append(f"\\section{{{ch['court']}}}\\label{{ann:aide-{ch['prefixe']}}}\n\n{aide}\n")
    annexe = ["% Généré par outils/convertir.py : aide-mémoires des TP",
              "\\chapter{Aide-mémoires}\\label{ann:aide}",
              "Ces aide-mémoires regroupent, pour chaque travail pratique, les instructions les plus utiles.",
              "Ils complètent la documentation officielle des outils, sans la remplacer.", ""] + aides
    (OUV / "annexes" / "aide_memoires.tex").write_text("\n".join(annexe), encoding="utf-8")
    print("écrit : annexes/aide_memoires.tex")


if __name__ == "__main__":
    main()
