import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration de la page ---
st.set_page_config(
    page_title="Homepedia Dashboard",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Homepedia — Analyse des médias français")

# --- Chargement des données ---
@st.cache_data  # Met en cache pour ne pas recharger à chaque fois
def load_data():
    df = pd.read_csv("speech_time_mw.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    return df

df = load_data()

st.success(f"✅ {len(df)} lignes chargées")

# --- Sidebar (menu latéral) ---
st.sidebar.title("🎛️ Filtres")

# Filtre type de média
media_type = st.sidebar.selectbox(
    "Type de média",
    ["Tous", "radio", "tv"]
)

# Filtre chaîne publique/privée
channel_type = st.sidebar.selectbox(
    "Type de chaîne",
    ["Toutes", "Publique", "Privée"]
)

# --- Application des filtres ---
df_filtered = df.copy()

if media_type != "Tous":
    df_filtered = df_filtered[df_filtered["media_type"] == media_type]

if channel_type == "Publique":
    df_filtered = df_filtered[df_filtered["is_public_channel"] == True]
elif channel_type == "Privée":
    df_filtered = df_filtered[df_filtered["is_public_channel"] == False]

# --- Graphique 1 : Evolution du temps de parole par année ---
st.subheader("📊 Evolution du temps de parole H/F par année")

# On agrège par année
df_year = df_filtered.groupby("year").agg(
    male=("male_duration", "sum"),
    female=("female_duration", "sum")
).reset_index()

# On transforme en format long pour plotly
df_melted = df_year.melt(
    id_vars="year",
    value_vars=["male", "female"],
    var_name="genre",
    value_name="duree"
)
df_melted["genre"] = df_melted["genre"].map({
    "male": "Hommes",
    "female": "Femmes"
})

fig1 = px.line(
    df_melted,
    x="year",
    y="duree",
    color="genre",
    title="Temps de parole total par année",
    labels={"year": "Année", "duree": "Durée (secondes)", "genre": "Genre"},
    color_discrete_map={"Hommes": "#1f77b4", "Femmes": "#e377c2"}
)
st.plotly_chart(fig1, use_container_width=True)

# --- Graphique 2 : Répartition H/F par chaîne ---
st.subheader("📊 Répartition H/F par chaîne")

df_channel = df_filtered.groupby("channel_name").agg(
    male=("male_duration", "sum"),
    female=("female_duration", "sum")
).reset_index()

# On calcule le pourcentage femmes
df_channel["total"] = df_channel["male"] + df_channel["female"]
df_channel["pct_female"] = (df_channel["female"] / df_channel["total"] * 100).round(1)
df_channel = df_channel.sort_values("pct_female", ascending=False).head(20)

fig2 = px.bar(
    df_channel,
    x="channel_name",
    y="pct_female",
    title="% de temps de parole féminin par chaîne (Top 20)",
    labels={"channel_name": "Chaîne", "pct_female": "% Femmes"},
    color="pct_female",
    color_continuous_scale="RdYlGn"
)
fig2.add_hline(y=50, line_dash="dash", line_color="black", annotation_text="50%")
st.plotly_chart(fig2, use_container_width=True)

# --- Graphique 3 : Comparaison public vs privé ---
st.subheader("📊 Public vs Privé")

df_public = df_filtered.groupby("is_public_channel").agg(
    male=("male_duration", "sum"),
    female=("female_duration", "sum")
).reset_index()

df_public["is_public_channel"] = df_public["is_public_channel"].map({
    True: "Public",
    False: "Privé"
})

df_public_melted = df_public.melt(
    id_vars="is_public_channel",
    value_vars=["male", "female"],
    var_name="genre",
    value_name="duree"
)
df_public_melted["genre"] = df_public_melted["genre"].map({
    "male": "Hommes",
    "female": "Femmes"
})

fig3 = px.bar(
    df_public_melted,
    x="is_public_channel",
    y="duree",
    color="genre",
    barmode="group",
    title="Temps de parole H/F : chaînes publiques vs privées",
    labels={"is_public_channel": "Type de chaîne", "duree": "Durée (secondes)"},
    color_discrete_map={"Hommes": "#1f77b4", "Femmes": "#e377c2"}
)
st.plotly_chart(fig3, use_container_width=True)