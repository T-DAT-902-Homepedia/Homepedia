# Dataset : Communes de France 2025

**Source :** [data.gouv.fr](https://www.data.gouv.fr/datasets/communes-et-villes-de-france-en-csv-excel-json-parquet-et-feather/)
**Resource ID :** `f5df602b-3800-44d7-b2df-fa40a0350325`
**Format :** CSV (16.3 MB, UTF-8, séparateur `,`)
**Millésime :** 2025, basé sur la géographie au 1er janvier 2024
**Licence :** Licence Ouverte v2 (LO v2)

---

## Colonnes retenues

Sur les 46 colonnes disponibles, 18 ont été sélectionnées pour leur pertinence dans le contexte d'une plateforme d'analyse du marché immobilier français.

### Identification géographique

| Colonne | Type | Description |
|---|---|---|
| `code_insee` | `string` | Code commune assigné par l'INSEE. Identifiant principal de la commune, utilisé comme clé de jointure avec les données DVF (Demandes de Valeurs Foncières) et la majorité des jeux de données open data. Format : 5 caractères (ex : `75056` pour Paris, `69123` pour Lyon). |
| `code_postal` | `string` | Code postal principal de la commune. Utilisé pour la recherche par les utilisateurs. Une commune peut avoir plusieurs codes postaux (voir `codes_postaux`). |
| `codes_postaux` | `string` | Liste de tous les codes postaux rattachés à la commune, séparés par des virgules. Utile pour la recherche et la correspondance avec des données issues d'autres sources. |

### Noms de la commune

| Colonne | Type | Description |
|---|---|---|
| `nom_standard` | `string` | Nom normalisé de la commune, avec article si applicable (ex : `Le Havre`, `Les Sables-d'Olonne`). Utilisé pour l'affichage dans l'interface. |
| `nom_sans_accent` | `string` | Nom de la commune sans accents, caractères spéciaux ni espaces. Utilisé pour la recherche et l'autocomplétion insensible aux accents (ex : `le-havre`, `les-sables-dolonne`). |

### Hiérarchie administrative

| Colonne | Type | Description |
|---|---|---|
| `dep_code` | `string` | Code du département de la commune, assigné par l'INSEE (ex : `75`, `69`, `2A`). Utilisé pour les filtres et regroupements par département. |
| `dep_nom` | `string` | Nom du département (ex : `Paris`, `Rhône`, `Corse-du-Sud`). Affiché dans les filtres et les résultats de recherche. |
| `reg_code` | `string` | Code de la région de la commune, assigné par l'INSEE (ex : `11` pour Île-de-France). Utilisé pour les filtres et les visualisations à l'échelle régionale. |
| `reg_nom` | `string` | Nom de la région (ex : `Île-de-France`, `Auvergne-Rhône-Alpes`). Affiché dans les filtres et les regroupements géographiques. |
| `typecom` | `string` | Type de la commune en version abrégée. Valeurs possibles : `COM` (commune standard), `COMA` (commune associée), `COMD` (commune déléguée), `ARM` (arrondissement municipal, ex : Paris, Lyon, Marseille). Permet de distinguer les entités géographiques dans les visualisations. |

### Coordonnées géographiques

| Colonne | Type | Description |
|---|---|---|
| `latitude_centre` | `float` | Latitude du centroïde géographique du territoire communal (WGS84). Utilisé pour le positionnement des marqueurs et la clustering sur la carte MapLibre. |
| `longitude_centre` | `float` | Longitude du centroïde géographique du territoire communal (WGS84). Utilisé conjointement avec `latitude_centre` pour le positionnement cartographique. |

### Données démographiques et territoriales

| Colonne | Type | Description |
|---|---|---|
| `population` | `float` | Population municipale de la commune (recensement INSEE). Fournit le contexte du marché local : distinguer les petites communes rurales des grandes agglomérations. |
| `superficie_km2` | `float` | Superficie de la commune en kilomètres carrés. Permet de calculer ou de vérifier la densité de population. |
| `densite` | `float` | Densité de population en habitants par km². Pré-calculé par la source. Utile pour les overlays de carte et les analyses de marché par type de territoire. |

### Classification du territoire

| Colonne | Type | Description |
|---|---|---|
| `grille_densite` | `string` | Grille communale de densité à 7 niveaux selon la classification INSEE (ex : `1`, `2`, ..., `7`). |
| `grille_densite_texte` | `string` | Libellé de la grille de densité (ex : `Commune densément peuplée`, `Commune rurale peu dense`, `Bourg rural`). Permet de catégoriser les communes pour filtres et analyses dans l'interface. |

### Contexte économique et urbain (optionnel)

| Colonne | Type | Description |
|---|---|---|
| `epci_code` | `string` | Code de l'EPCI (Établissement Public de Coopération Intercommunale) auquel appartient la commune. Permet les regroupements à l'échelle des communautés de communes ou d'agglomération. |
| `epci_nom` | `string` | Nom de l'EPCI (ex : `Métropole du Grand Paris`, `Communauté de communes du Pays de Gex`). Affiché comme niveau intermédiaire entre la commune et le département. |

---

## Colonnes exclues

Les 28 colonnes suivantes ont été écartées car non pertinentes pour un usage immobilier :

| Colonnes exclues | Raison |
|---|---|
| `nom_sans_pronom`, `nom_a`, `nom_de`, `nom_standard_majuscule` | Variantes de noms inutiles — `nom_standard` et `nom_sans_accent` suffisent |
| `typecom_texte` | Redondant avec `typecom` |
| `canton_code`, `canton_nom` | Découpage électoral, non pertinent pour l'immobilier |
| `academie_code`, `academie_nom` | Découpage scolaire hors scope |
| `zone_emploi`, `code_insee_centre_zone_emploi` | Trop spécifique pour le MVP |
| `code_unite_urbaine`, `nom_unite_urbaine`, `taille_unite_urbain`, `type_commune_unite_urbain`, `statut_commune_unite_urbain` | Redondant avec `grille_densite` |
| `altitude_moyenne`, `altitude_minimale`, `altitude_maximale` | Non pertinent pour l'immobilier |
| `latitude_mairie`, `longitude_mairie` | `latitude_centre` / `longitude_centre` sont plus représentatifs |
| `gentile` | Non pertinent |
| `url_wikipedia`, `url_villedereve` | Liens externes hors scope |
