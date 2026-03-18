from pathlib import Path
import pandas as pd


def main():
    base_dir = Path(__file__).parent
    dtype = {'code_insee': str, 'nom_standard': str, 'nom_sans_pronom': str, 'nom_a': str, 'nom_de': str,
             'nom_sans_accent': str, 'nom_standard_majuscule': str, 'typecom': str, 'typecom_texte': str,
             'reg_code': str, 'reg_nom': str, 'dep_code': str, 'dep_nom': str, 'canton_code': str, 'canton_nom': str,
             'epci_code': str, 'epci_nom': str, 'code_postal': str, 'codes_postaux': str, 'academie_code': str,
             'academie_nom': str, 'zone_emploi': str, 'code_insee_centre_zone_emploi': str, 'population': float,
             'superficie_hectare': float, 'superficie_km2': float, 'densite': float, 'altitude_moyenne': float,
             'altitude_minimale': float, 'altitude_maximale': float, 'latitude_mairie': float,
             'longitude_mairie': float, 'latitude_centre': float, 'latitude_centre': float, 'grille_densite': str,
             'gentile': str, 'url_wikipedia': str, 'url_villedereve': str}

    df = pd.read_csv(base_dir / 'data/communes-france-2025.csv', index_col=0, dtype=dtype, sep=',')
    print(df.loc[0:10, ['code_insee', 'nom_sans_accent']])

if __name__ == "__main__":
    main()
