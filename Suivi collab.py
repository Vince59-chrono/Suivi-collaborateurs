import streamlit as st
import pandas as pd
import datetime
import os

FICHIER = "suivi_collaborateurs.csv"

# Initialiser le fichier si inexistant
if not os.path.exists(FICHIER):
    df_init = pd.DataFrame(columns=[
        "Date", "Mois", "Entreprise", "Équipe", "Métier", "Manager",
        "Commentaire",
        "Objectif Annuel", "Sous-objectif", "Avancement",
        "Formation", "Réalisée", "Compétence"
    ])
    df_init.to_csv(FICHIER, index=False)

st.set_page_config(page_title="Suivi Collaborateurs", page_icon="📊", layout="centered")
st.title("📊 Suivi Collaborateur - Bien-être & Objectifs")

# Sélection du mois
mois = st.selectbox("Mois", ["Janv", "Fév", "Mars", "Avril", "Mai", "Juin", 
                             "Juil", "Août", "Sept", "Oct", "Nov", "Déc"])

st.subheader("😊 Bien-être (1=Pas bien → 5=Très bien)")
bien_etre = {
    "Entreprise": st.slider("Comment te sens-tu dans l'entreprise ?", 1, 5, 3),
    "Équipe": st.slider("Comment te sens-tu dans l'équipe ?", 1, 5, 3),
    "Métier": st.slider("Comment te sens-tu dans ton métier ?", 1, 5, 3),
    "Manager": st.slider("Comment te sens-tu avec ton manager ?", 1, 5, 3)
}
commentaire = st.text_area("Commentaires libres")

st.subheader("🎯 Objectifs")
objectif = st.text_input("Objectif annuel")
sous_obj = st.text_input("Sous-objectif du mois")
avancement = st.slider("Avancement (%)", 0, 100, 0)

st.subheader("🚀 Développement personnel")
formation = st.text_input("Formation prévue")
realisee = st.radio("Formation réalisée ?", ["Oui", "Non"])
competence = st.text_input("Compétence ciblée")

# Sauvegarde
if st.button("💾 Enregistrer"):
    data = {
        "Date": datetime.date.today(),
        "Mois": mois,
        **bien_etre,
        "Commentaire": commentaire,
        "Objectif Annuel": objectif,
        "Sous-objectif": sous_obj,
        "Avancement": avancement,
        "Formation": formation,
        "Réalisée": realisee,
        "Compétence": competence
    }
    df = pd.DataFrame([data])
    df.to_csv(FICHIER, mode="a", header=False, index=False)
    st.success("✅ Données enregistrées !")

# Visualisation des données
if st.checkbox("📈 Voir le suivi"):
    df = pd.read_csv(FICHIER)
    st.dataframe(df)

    if not df.empty:
        st.subheader("Évolution du bien-être")
        st.line_chart(df[["Entreprise", "Équipe", "Métier", "Manager"]])

        st.subheader("Avancement des objectifs (%)")
        st.bar_chart(df["Avancement"])
