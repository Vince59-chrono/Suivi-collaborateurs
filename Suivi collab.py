import streamlit as st
import pandas as pd
import datetime
from pyairtable import Table

# --- CONFIG ---
# ⚠️ Ta clé API doit être stockée dans les "Secrets" Streamlit Cloud sous le nom AIRTABLE_API_KEY
AIRTABLE_API_KEY = st.secrets["AIRTABLE_API_KEY"]

# ID de ta base Airtable (trouvé dans l’URL)
BASE_ID = "appum6305mahJtMzR"

# Nom exact de ta table Airtable
TABLE_NAME = "SuiviRH"

# Connexion à Airtable
table = Table(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)

# Configuration de la page Streamlit
st.set_page_config(page_title="Suivi Collaborateurs", page_icon="📊", layout="centered")
st.title("📊 Suivi Collaborateur - Bien-être & Objectifs")

# --- Formulaire ---
collaborateur = st.text_input("👤 Nom du collaborateur")
mois = st.selectbox("📅 Mois", 
                    ["Janv","Fév","Mars","Avril","Mai","Juin",
                     "Juil","Août","Sept","Oct","Nov","Déc"])

st.subheader("😊 Bien-être (1 = Pas bien → 5 = Très bien)")
bien_etre = {
    "Entreprise": st.slider("Entreprise ?", 1, 5, 3),
    "Équipe": st.slider("Équipe ?", 1, 5, 3),
    "Métier": st.slider("Métier ?", 1, 5, 3),
    "Manager": st.slider("Manager ?", 1, 5, 3)
}
commentaire = st.text_area("📝 Commentaires")

st.subheader("🎯 Objectifs")
objectif = st.text_input("Objectif annuel")
sous_obj = st.text_input("Sous-objectif du mois")
avancement = st.slider("Avancement (%)", 0, 100, 0)

st.subheader("🚀 Développement personnel")
formation = st.text_input("Formation prévue")
realisee = st.radio("Formation réalisée ?", ["Oui", "Non"])
competence = st.text_input("Compétence ciblée")

# --- Sauvegarde ---
if st.button("💾 Enregistrer"):
    if collaborateur.strip() == "":
        st.warning("⚠️ Merci de renseigner le nom du collaborateur")
    else:
        new_row = {
            "Collaborateur": collaborateur,
            "Date": str(datetime.date.today()),
            "Mois": mois,
            "Entreprise": bien_etre["Entreprise"],
            "Équipe": bien_etre["Équipe"],
            "Métier": bien_etre["Métier"],
            "Manager": bien_etre["Manager"],
            "Commentaire": commentaire,
            "Objectif Annuel": objectif,
            "Sous-objectif": sous_obj,
            "Avancement": avancement,
            "Formation": formation,
            "Réalisée": realisee,
            "Compétence": competence
        }
        table.create(new_row)
        st.success("✅ Données enregistrées dans Airtable !")

# --- Visualisation ---
if st.checkbox("📈 Voir le suivi global"):
    records = table.all()
    df = pd.DataFrame([r["fields"] for r in records])
    st.dataframe(df)

    if not df.empty:
        st.subheader("Évolution du bien-être (moyenne)")
        df_moy = df.groupby("Mois")[["Entreprise", "Équipe", "Métier", "Manager"]].mean()
        st.line_chart(df_moy)

        st.subheader("Avancement des objectifs (%)")
        if "Avancement" in df.columns:
            st.bar_chart(df["Avancement"])
