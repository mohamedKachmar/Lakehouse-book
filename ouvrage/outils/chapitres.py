"""Textes propres à l'ouvrage pour les chapitres 2 à 6 (le contenu vient des supports de TP)."""

SYNTHESE_REMPLACEMENT = []

CHAPITRES = [
    # ------------------------------------------------------------------ chapitre 2
    {
        "numero": 2, "source": "support0_installation.tex", "fichier": "ch2_environnement.tex",
        "label": "ch:environnement", "prefixe": "c2",
        "court": "L'environnement de travail",
        "titre": "L'environnement de travail",
        "soustitre": "Un Lakehouse complet sur votre ordinateur, en une commande",
        "objectifs": [
            "installer Docker et l'environnement des travaux pratiques ;",
            "décrire le rôle de chaque service : stockage S3, catalogue, Spark, JupyterLab, PostgreSQL et outils optionnels ;",
            "vérifier que l'environnement fonctionne et diagnostiquer un problème courant ;",
            "démarrer et arrêter les groupes de services selon les besoins de chaque TP.",
        ],
        "fiche": [
            ("Durée indicative", "environ 1 h, dont le téléchargement des images (8 à 10~Go)"),
            ("Matériel", "8~Go de mémoire vive au minimum (16~Go conseillés) et 15~Go d'espace disque libre"),
        ],
        "remplacements": [
            ("\\textbf{Faites une capture d'écran de ce résultat}, elle figurera dans votre compte rendu.\n", ""),
            ("Airflow, préparation des données), réservées à l'enseignant.", "Airflow, préparation des données), utilisées pour construire l'environnement."),
            ("Scripts de préparation des données, réservés à l'enseignant.", "Scripts qui ont servi à préparer les données des TP."),
            ("\\section{Installer l'environnement du cours}", "\\section{Installer l'environnement des travaux pratiques}"),
            ("Étape 1 -- Récupérer le dossier du cours", "Étape 1 -- Récupérer le dépôt d'accompagnement"),
        ],
        "supprimer": [
            r"\n% =+\n\\section\{Avant la séance 1\}.*\Z",
            r"\\newcommand\{\\dossier\}[^\n]*\n",
            r"\\newcommand\{\\fic\}[^\n]*\n",
        ],
        "fin_liste": True,
        "aretenir": [
            "L'environnement complet tourne dans des conteneurs Docker, décrits par un seul fichier \\cmd{docker-compose.yml}.",
            "Le socle (stockage S3, catalogue Iceberg, PostgreSQL, JupyterLab avec Spark) démarre avec \\cmd{docker compose up -d} ; les autres outils démarrent à la demande, par profil.",
            "Les données sont conservées dans des volumes Docker : arrêter les conteneurs ne les efface pas.",
            "Le script \\cmd{check\\_env.py} vérifie en une commande que chaque service répond.",
            "On ne modifie que deux choses : le fichier \\cmd{.env} et le dossier \\cmd{notebooks/mon\\_travail/}.",
        ],
        "plusloin": "La documentation de Docker Compose (\\url{https://docs.docker.com/compose/}) détaille les "
                    "profils, les volumes et les réseaux utilisés ici. Le fichier \\cmd{docker-compose.yml} du "
                    "dépôt d'accompagnement est commenté : le lire est une bonne façon de comprendre comment les "
                    "services se connectent les uns aux autres.",
    },
    # ------------------------------------------------------------------ chapitre 3
    {
        "numero": 3, "source": "tp1_donnees_structurees.tex", "fichier": "ch3_tp1.tex",
        "label": "ch:tp1", "prefixe": "c3",
        "court": "TP 1 -- Données structurées",
        "titre": "TP 1 -- Données structurées",
        "soustitre": "De la base de données au tableau de bord, en passant par Bronze, Silver et Gold",
        "objectifs": [
            "ingérer dans le Lakehouse les tables d'une base PostgreSQL et des fichiers CSV ;",
            "nettoyer et contrôler les données en couche Silver, avec une quarantaine ;",
            "construire une couche Gold et répondre en SQL aux questions de la direction ;",
            "charger les nouvelles données de façon incrémentale, avec \\cmd{MERGE}, et relire une version passée d'une table ;",
            "entraîner un modèle qui prédit les retards de livraison, en évitant la fuite de données ;",
            "comparer Iceberg et Delta Lake, et présenter les résultats dans un tableau de bord.",
        ],
        "fiche": [
            ("Durée indicative", "2 séances de 3 h, et environ 2 h 30 de travail personnel"),
            ("Prérequis", "chapitre~\\ref{ch:environnement} : environnement installé, \\og ENVIRONNEMENT PRÊT \\fg{} affiché par \\cmd{check\\_env.py}"),
            ("Notebooks", "\\nb{notebooks/tp1/}, cinq notebooks numérotés de 01 à 05"),
        ],
        "remplacements": [
            ("mises à jour publiées par l'enseignant.", "mises à jour publiées dans le dépôt."),
            ("Ne faites ni \\cmd{git commit} ni \\cmd{git push}, car le dépôt du cours est en lecture seule.\n",
             "Ne faites ni \\cmd{git commit} ni \\cmd{git push} dans le dépôt d'accompagnement.\n"),
            ("Gardez sous la main l'\\textbf{aide-mémoire PySpark} de la dernière page, qui contient toutes les\nopérations dont vous aurez besoin.",
             "Gardez sous la main l'\\textbf{aide-mémoire PySpark} de l'annexe~\\ref{ann:aide}, qui contient toutes\nles opérations dont vous aurez besoin."),
            ("à faire en fin de séance 2 ou en travail personnel.", "à faire en travail personnel."),
        ],
        "aretenir": [
            "La couche Bronze garde les données telles qu'elles sont arrivées, lues en texte, avec leur origine.",
            "La couche Silver type, contrôle et dédoublonne ; les lignes rejetées vont en quarantaine avec leur raison, et une règle peut être bloquante ou une simple alerte.",
            "La couche Gold répond aux questions métier ; Spark SQL interroge les tables comme une base de données.",
            "L'ingestion incrémentale ne charge que les nouvelles lignes, grâce à un filigrane et à \\cmd{MERGE} ; chaque écriture crée un instantané que l'on peut relire.",
            "Un modèle ne doit utiliser que des informations connues au moment de la prédiction, sinon ses performances sont trompeuses (fuite de données).",
            "Iceberg et Delta Lake rendent le même service : des transactions et un historique sur des fichiers Parquet.",
        ],
        "plusloin": "Le fonctionnement de \\cmd{MERGE} et du voyage dans le temps est décrit dans la spécification "
                    "d'Iceberg \\citep{icebergspec} et dans l'article sur Delta Lake \\citep{armbrust2020}. La "
                    "modélisation des tables Gold sera approfondie au chapitre~\\ref{ch:tp2}, et "
                    "\\citet{kimball2013} en reste la référence.",
    },
    # ------------------------------------------------------------------ chapitre 4
    {
        "numero": 4, "source": "tp2_texte_json.tex", "fichier": "ch4_tp2.tex",
        "label": "ch:tp2", "prefixe": "c4",
        "remplacements": [("L'aide-mémoire de la dernière page rassemble", "L'aide-mémoire de l'annexe~\\ref{ann:aide} rassemble")],
        "court": "TP 2 -- Texte et JSON",
        "titre": "TP 2 -- Texte et JSON",
        "soustitre": "Avis clients, suivi des colis, modélisation dimensionnelle avec dbt et analyse du texte",
        "objectifs": [
            "distinguer données structurées, semi-structurées et non structurées ;",
            "ingérer du texte libre et des messages JSON sans perdre l'original ;",
            "lire un JSON imbriqué avec un schéma écrit, et déplier ses listes en tables ;",
            "construire une couche Gold en schéma en constellation avec dbt, testée et documentée ;",
            "transformer du texte en variables (TF-IDF) et repérer automatiquement les avis négatifs.",
        ],
        "fiche": [
            ("Durée indicative", "2 séances de 3 h, et environ 2 h de travail personnel"),
            ("Prérequis", "chapitre~\\ref{ch:tp1} : tables Silver \\cmd{orders}, \\cmd{order\\_items}, \\cmd{customers}, \\cmd{products} et \\cmd{sellers}"),
            ("Notebooks", "\\nb{notebooks/tp2/}, quatre notebooks et le projet dbt \\cmd{dbt\\_etoile}"),
        ],
        "aretenir": [
            "Un fichier CSV peut contenir des retours à la ligne dans un champ : il se lit avec l'option \\cmd{multiLine}.",
            "On garde le JSON brut en Bronze, puis on le lit en Silver avec un schéma écrit, qui couvre toutes les versions du format.",
            "\\cmd{explode} déplie une liste : un message devient autant de lignes que d'événements.",
            "dbt organise les transformations SQL en modèles versionnés, testés et documentés, et en déduit le lineage.",
            "Un schéma en constellation partage ses dimensions entre plusieurs tables de faits.",
            "TF-IDF transforme un texte en vecteur de nombres, utilisable par un modèle de classification.",
        ],
        "plusloin": "La documentation de dbt (\\url{https://docs.getdbt.com}) présente les tests, les sources et "
                    "la documentation générée. \\citet{kimball2013} détaille les dimensions conformes, qui "
                    "rendent possible un schéma en constellation.",
    },
    # ------------------------------------------------------------------ chapitre 5
    {
        "numero": 5, "source": "tp3_images_orchestration_bi.tex", "fichier": "ch5_tp3.tex",
        "label": "ch:tp3", "prefixe": "c5",
        "court": "TP 3 -- Images, orchestration et BI",
        "titre": "TP 3 -- Images, orchestration et BI",
        "soustitre": "Un pipeline de bout en bout : automatisé, contrôlé, optimisé et exposé",
        "objectifs": [
            "stocker des images dans le Lakehouse, contrôler leur qualité et repérer les doublons ;",
            "décrire une image par un vecteur, pour retrouver les images semblables et contrôler un catalogue ;",
            "transformer un notebook en pipeline automatisé et idempotent, orchestré par Airflow ;",
            "mesurer et corriger l'effet des petits fichiers, par le compactage et le partitionnement ;",
            "exposer les tables aux équipes métier avec Trino et Superset, et interroger plusieurs bases en une requête ;",
            "superviser la plateforme et observer le lineage des données.",
        ],
        "fiche": [
            ("Durée indicative", "3 séances de 3 h, et environ 3 h de travail personnel"),
            ("Prérequis", "chapitres~\\ref{ch:tp1} et~\\ref{ch:tp2} : tables Silver et projet dbt"),
            ("Notebooks", "\\nb{notebooks/tp3/}, cinq notebooks, les scripts du dossier \\nb{pipeline/} et trois DAG"),
        ],
        "remplacements": [
            ("\\textbf{Mettre à jour l'environnement, une fois, au début de la séance 1.}",
             "\\textbf{Mettre à jour l'environnement, une fois, avant de commencer.}"),
            ("rassemble tout ce que vous avez construit pendant le module.", "rassemble tout ce que vous avez construit dans les chapitres précédents."),
            ("Vous assemblez une architecture complète, de la donnée brute au tableau de bord, comme en\nentreprise. Le TP 4 y ajoutera le traitement des données en continu.",
             "Vous assemblez une architecture complète, de la donnée brute au tableau de bord, comme en\nentreprise. Le chapitre~\\ref{ch:tp4} y ajoutera le traitement des données en continu."),
        ],
        "aretenir": [
            "Une image entre dans le Lakehouse avec ses octets et une empreinte \\cmd{sha256}, qui reconnaît les copies exactes ; une photo recadrée demande une règle métier.",
            "Un réseau pré-entraîné transforme une image en vecteur ; des vecteurs proches désignent des images semblables.",
            "Un pipeline automatisé doit être idempotent : relancé, il ne change pas le résultat. Airflow l'enchaîne, le relance et l'arrête si un contrôle échoue.",
            "Chaque écriture ajoute des fichiers : on compacte, on expire les anciens instantanés et on partitionne selon les filtres fréquents.",
            "Trino lit les mêmes tables que Spark, sans copie, et joint plusieurs bases dans une même requête.",
            "La supervision surveille les services ; l'observabilité des données retrace leur origine.",
        ],
        "plusloin": "La documentation d'Airflow (\\url{https://airflow.apache.org/docs/}) décrit les capteurs, les "
                    "relances et le calendrier des DAG. La spécification d'OpenLineage "
                    "(\\url{https://openlineage.io}) précise le contenu des événements de lineage. Pour la "
                    "représentation des images par des réseaux pré-entraînés, voir \\citet{howard2019}.",
    },
    # ------------------------------------------------------------------ chapitre 6
    {
        "numero": 6, "source": "tp4_batch_streaming.tex", "fichier": "ch6_tp4.tex",
        "label": "ch:tp4", "prefixe": "c6",
        "court": "TP 4 -- Batch ou streaming",
        "titre": "TP 4 -- Batch ou streaming",
        "soustitre": "Des événements en continu : Kafka, Spark Structured Streaming et Iceberg",
        "objectifs": [
            "écrire une requête Spark Structured Streaming et choisir son mode de sortie ;",
            "créer un topic Kafka, produire et consommer des messages, et lire le retard d'un groupe ;",
            "écrire un flux dans Iceberg sans perte ni doublon, même après une panne ;",
            "distinguer l'heure de l'événement de l'heure de traitement, et choisir un watermark ;",
            "mettre à jour une table depuis un flux avec \\cmd{foreachBatch} et \\cmd{MERGE} ;",
            "choisir, mesures à l'appui, entre traitement par lots, flux continu et flux déclenché.",
        ],
        "fiche": [
            ("Durée indicative", "2 séances de 3 h, et environ 2 h de travail personnel"),
            ("Prérequis", "chapitres~\\ref{ch:tp1} à~\\ref{ch:tp3}, et le profil \\cmd{streaming}"),
            ("Notebooks", "\\nb{notebooks/tp4/}, cinq notebooks et le module \\cmd{flux.py}"),
        ],
        "remplacements": [
            ("\\textbf{Mettre à jour l'environnement, une fois, au début de la séance 1.}",
             "\\textbf{Mettre à jour l'environnement, une fois, avant de commencer.}"),
            ("Les données n'ont plus de fin : c'est un \\textbf{flux}. Ce TP termine le module. Il ajoute à\nl'architecture construite aux TP 1 à 3 la dimension temps réel,",
             "Les données n'ont plus de fin : c'est un \\textbf{flux}. Ce dernier TP ajoute à\nl'architecture construite aux TP 1 à 3 la dimension temps réel,"),
        ],
        "aretenir": [
            "Spark Structured Streaming traite un flux comme une table qui grandit, par micro-lots ; une agrégation garde un état entre les micro-lots.",
            "Kafka conserve les messages après lecture ; l'ordre n'est garanti que dans une partition, et la clé choisit la partition.",
            "Le checkpoint et le commit atomique d'Iceberg garantissent qu'un message est écrit une fois et une seule.",
            "Le watermark dit combien de temps attendre les retardataires ; il règle le compromis entre fraîcheur et exactitude.",
            "Le même code tourne en continu ou à heure fixe : seul le déclencheur change.",
            "On choisit le streaming d'après le délai dont le métier a besoin, pas d'après la technologie.",
        ],
        "plusloin": "\\citet{akidau2015} et \\citet{akidau2018} exposent le modèle Dataflow, les fenêtres et les "
                    "watermarks. \\citet{kreps2011} décrivent la conception de Kafka, et \\citet{armbrust2018} celle "
                    "de Spark Structured Streaming. \\citet{kleppmann2017} (chapitre sur les flux) relie ces notions "
                    "aux bases de données.",
    },
]
