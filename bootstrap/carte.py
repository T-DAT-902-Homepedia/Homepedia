import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

# --- Configuration ---
st.set_page_config(
    page_title="Carte des pathologies",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Carte des pathologies en France")

# --- Chargement des données ---
@st.cache_data
def load_data():
    # Données pathologies
    df = pd.read_csv("data_pathologies.csv", sep=";")
    
    # Shapefile des départements
    geo = gpd.read_file("departements.geojson")
    
    return df, geo

df, geo = load_data()

st.success(f"✅ {len(df)} lignes chargées")

# --- Sidebar ---
st.sidebar.title("🎛️ Filtres")

# Liste des pathologies disponibles
pathologies = sorted(df["patho_niv1"].dropna().unique())
pathologie_choisie = st.sidebar.selectbox(
    "Choisir une pathologie",
    pathologies
)

# Liste des années
annees = sorted(df["annee"].unique())
annee_choisie = st.sidebar.selectbox(
    "Choisir une année",
    annees,
    index=len(annees)-1  # Dernière année par défaut
)

# --- Filtrage des données ---
df_filtered = df[
    (df["patho_niv1"] == pathologie_choisie) &
    (df["annee"] == annee_choisie)
]

# On agrège par département
df_dept = df_filtered.groupby("dept").agg(
    nb_patients=("Ntop", "sum"),
    prevalence=("prev", "mean")
).reset_index()

# --- Fusion avec le shapefile ---
# Le code département doit être au même format
df_dept["dept"] = df_dept["dept"].astype(str).str.zfill(2)
geo["code"] = geo["code"].astype(str).str.zfill(2)

# On fusionne les deux dataframes
merged = geo.merge(df_dept, left_on="code", right_on="dept", how="left")

# --- Affichage de la carte ---
st.subheader(f"📊 {pathologie_choisie} en {annee_choisie}")

fig = px.choropleth(
    merged,
    geojson=merged.geometry,
    locations=merged.index,
    color="prevalence",
    hover_name="nom",
    hover_data={"prevalence": ":.2f", "nb_patients": True},
    color_continuous_scale="Reds",
    title=f"Prévalence de {pathologie_choisie} par département ({annee_choisie})",
    labels={
        "prevalence": "Prévalence (%)",
        "nb_patients": "Nb patients"
    }
)

fig.update_geos(
    fitbounds="locations",
    visible=False
)

fig.update_layout(
    height=600,
    margin={"r":0,"t":50,"l":0,"b":0}
)

st.plotly_chart(fig, use_container_width=True)

# --- Stats en dessous ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total patients",
        f"{df_dept['nb_patients'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Prévalence moyenne",
        f"{df_dept['prevalence'].mean():.2f}%"
    )

with col3:
    dept_max = df_dept.loc[df_dept["prevalence"].idxmax(), "dept"]
    st.metric(
        "Département le plus touché",
        f"Dept {dept_max}"
    )