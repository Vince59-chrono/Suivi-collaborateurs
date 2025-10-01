import streamlit as st
import pandas as pd
import datetime
from supabase import create_client


# --- CONFIG ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Suivi Collaborateurs", page_icon="📊", layout="centered")
st.title("📊 Suivi Collaborateur - Bien-être & Objectifs")

# --- Formulaire ---
collaborateur = st.text_input("👤 Nom du collaborateur")
mois = st.selectbox("📅 Mois",
                    ["Janv","Fév","Mars","Avril","Mai","Juin",
                     "Juil","Août","Sept","Oct","Nov","Déc"])

st.subheader("😊 Bien-être (1 = Pas bien → 5 = Très bien)")
bien_etre = {
    "entreprise": st.slider("Entreprise ?", 1, 5, 3),
    "equipe": st.slider("Équipe ?", 1, 5, 3),
    "metier": st.slider("Métier ?", 1, 5, 3),
    "manager": st.slider("Manager ?", 1, 5, 3)
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
        data = {
            "collaborateur": collaborateur,
            "date": str(datetime.date.today()),
            "mois": mois,
            "entreprise": bien_etre["entreprise"],
            "equipe": bien_etre["equipe"],
            "metier": bien_etre["metier"],
            "manager": bien_etre["manager"],
            "commentaire": commentaire,
            "objectif": objectif,
            "sous_obj": sous_obj,
            "avancement": avancement,
            "formation": formation,
            "realisee": realisee,
            "competence": competence
        }
        supabase.table("suivi").insert(data).execute()
        st.success("✅ Données enregistrées dans Supabase !")

# --- Visualisation ---
if st.checkbox("📈 Voir le suivi global"):
    response = supabase.table("suivi").select("*").execute()
    df = pd.DataFrame(response.data)
    
    if df.empty:
        st.info("ℹ️ Aucune donnée enregistrée pour le moment.")
    else:
        st.dataframe(df)

        st.subheader("Évolution du bien-être (moyenne)")
        df_moy = df.groupby("mois")[["entreprise", "equipe", "metier", "manager"]].mean()
        st.line_chart(df_moy)

        st.subheader("Avancement des objectifs (%)")
        if "avancement" in df.columns:
            st.bar_chart(df["avancement"])

        # Export Excel
        st.subheader("📂 Exporter les données")
        fichier_export = "export_suivi.xlsx"
        df.to_excel(fichier_export, index=False)
        with open(fichier_export, "rb") as f:
            st.download_button("⬇️ Télécharger en Excel", f, file_name=fichier_export)

