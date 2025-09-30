import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIG ---
# Lien vers ton Google Sheet (⚠️ il doit être partagé en "Toute personne ayant le lien peut modifier")
SHEET_URL = "https://docs.google.com/spreadsheets/d/1uCtnN1FN4eOPJ5iNvJPnSXGysFMbBM2Q43gN-r74AUg/export?format=csv"

# Connexion à Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

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
        # Lire les données existantes
        try:
            df_exist = conn.read(spreadsheet=SHEET_URL)
            df_exist = df_exist.dropna(how="all")  # Nettoyer les lignes vides
        except Exception:
            df_exist = pd.DataFrame(columns=[
                "Collaborateur", "Date", "Mois", "Entreprise", "Équipe", "Métier", "Manager",
                "Commentaire", "Objectif Annuel", "Sous-objectif", "Avancement",
                "Formation", "Réalisée", "Compétence"
            ])

        # Nouvelle ligne
        new_row = pd.DataFrame([{
            "Collaborateur": collaborateur,
            "Date": datetime.date.today(),
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
        }])

        # Fusionner + écrire dans Google Sheet
        df_final = pd.concat([df_exist, new_row], ignore_index=True)
        conn.update(spreadsheet=SHEET_URL, data=df_final)

        st.success("✅ Données enregistrées dans Google Sheets !")

# --- Visualisation ---
if st.checkbox("📈 Voir le suivi global"):
    df = conn.read(spreadsheet=SHEET_URL)
    df = df.dropna(how="all")
    st.dataframe(df)

    if not df.empty:
        st.subheader("Évolution du bien-être (moyenne)")
        df_moy = df.groupby("Mois")[["Entreprise", "Équipe", "Métier", "Manager"]].mean()
        st.line_chart(df_moy)

        st.subheader("Avancement des objectifs (%)")
        st.bar_chart(df["Avancement"])
