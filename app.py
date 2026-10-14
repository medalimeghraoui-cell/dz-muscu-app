import streamlit as st
import pandas as pd
import datetime
import math

# Configuration de la page adaptée aux mobiles
st.set_page_config(page_title="DZ Muscu App v2.0", page_icon="🏋️‍♂️", layout="centered")

# Style CSS pour le thème sombre Premium et moderne
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stApp { background-color: #0d1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; background-color: transparent; padding: 10px 16px; border-radius: 8px; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #58a6ff !important; background-color: #21262d !important; border-bottom: 2px solid #58a6ff; }
    div[data-testid="stBlock"] { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 16px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
    h1, h2, h3 { color: #58a6ff !important; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background-color: #238636 !important; color: white !important; border-radius: 8px !important; width: 100% !important; border: none !important; padding: 10px !important; font-weight: bold !important; }
    .stButton>button:hover { background-color: #2ea043 !important; }
    .nutrition-card { background-color: #21262d; border-left: 4px solid #58a6ff; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏋️‍♂️ DZ Muscu App v2.0")
st.write("Programme de 3 jours Full-Body & Nutrition Économique (20,000 DA/mois)")

# Initialisation de la base de données locale temporaire
if "workout_logs" not in st.session_state:
    st.session_state.workout_logs = pd.DataFrame(columns=["Date", "Séance", "Exercice", "Poids (kg)", "Répétitions"])

tab1, tab2, tab3, tab4 = st.tabs(["💪 Entraînement", "🥗 Nutrition", "📏 Suivi & Masse Grasse", "📈 Historique"])

# === ONGLET 1 : ENTRAÎNEMENT & LOGBOOK ===
with tab1:
    st.header("🏋️‍♂️ Suivi de votre Séance")
    seance = st.selectbox("Choisir la séance du jour :", ["Jour 1: Focus Poussée / Pectoraux", "Jour 2: Focus Tirage / Dos", "Jour 3: Séance Complète")])
    
    # Liste complète des 15 exercices structurés avec des images fiables
    exercices = {
        "Jour 1: Focus Poussée / Pectoraux": [
            {"name": "Squat à la barre (Barbell Squat)", "desc": "3 séries x 8-10 reps (Cuisses)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/barbell-squat-exercise-guide.png"},
            {"name": "Développé couché (Bench Press)", "desc": "4 séries x 8-12 reps (Pectoraux)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/barbell-bench-press-exercise-guide.png"},
            {"name": "Développé épaules aux haltères", "desc": "3 séries x 10 reps (Épaules antérieures)", "img": "https://workoutlabs.com/wp-content/uploads/2014/10/seated-dumbbell-shoulder-press-exercise-guide.png"},
            {"name": "Tirage vertical poulie haute", "desc": "3 séries x 10-12 reps (Grand dorsal)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/lat-pulldown-exercise-guide.png"},
            {"name": "Extensions Triceps à la poulie", "desc": "3 séries x 12 reps (Bras arrière)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/triceps-pushdown-exercise-guide.png"}
        ],
        "Jour 2: Focus Tirage / Dos": [
            {"name": "Soulevé de terre (Deadlift)", "desc": "3 séries x 8 reps (Ischios & Lombaires)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/barbell-deadlift-exercise-guide.png"},
            {"name": "Rowing barre (Barbell Row)", "desc": "4 séries x 8-10 reps (Épaisseur du dos)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/barbell-row-exercise-guide.png"},
            {"name": "Écartés inclinés haltères", "desc": "3 séries x 10-12 reps (Haut des pectoraux)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/incline-dumbbell-fly-exercise-guide.png"},
            {"name": "Élévations latérales aux haltères", "desc": "4 séries x 12-15 reps (Largeur d'épaules)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/dumbbell-lateral-raise-exercise-guide.png"},
            {"name": "Curl Biceps alterné avec haltères", "desc": "3 séries x 12 reps (Bras avant)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/alternating-dumbbell-biceps-curl-exercise-guide.png"}
        ],
        "Jour 3: Séance Complète": [
            {"name": "Presse à cuisses (Leg Press)", "desc": "4 séries x 10-12 reps (Cuisses)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/sled-leg-press-exercise-guide.png"},
            {"name": "Répulsions aux barres parallèles (Dips)", "desc": "3 séries x 10 reps (Bas des pectoraux & Triceps)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/chest-dips-exercise-guide.png"},
            {"name": "Rowing assis à la poulie basse", "desc": "3 séries x 10 reps (Milieu du dos)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/seated-cable-row-exercise-guide.png"},
            {"name": "Développé militaire à la barre", "desc": "3 séries x 8 reps (Épaules & Gainage)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/barbell-military-press-exercise-guide.png"},
            {"name": "Crunches abdominaux & Gainage", "desc": "3 séries x max reps (Abdos)", "img": "https://workoutlabs.com/wp-content/uploads/2013/05/crunches-exercise-guide.png"}
        ]
    }
    
    st.info("💡 Règle de Surcharge Progressive : si vous validez toutes vos reps, ajoutez +2.5 kg à la prochaine séance !")
    
    logs_du_jour = []
    for ex in exercices[seance]:
        st.subheader(ex["name"])
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(ex["img"], caption=ex["desc"], use_container_width=True)
        with col2:
            poids = st.number_input(f"Poids (kg) - {ex['name']}", min_value=0.0, step=2.5, key=f"w_{ex['name']}")
            reps = st.number_input(f"Répétitions - {ex['name']}", min_value=0, max_value=100, step=1, key=f"r_{ex['name']}")
            logs_du_jour.append({"Exercice": ex["name"], "Poids (kg)": poids, "Répétitions": reps})
        st.markdown("<hr style='border-color: #30363d;' />", unsafe_allow_html=True)
        
    if st.button("💾 Enregistrer la séance du jour"):
        nouveaux_logs = []
        date_today = datetime.date.today().strftime("%Y-%m-%d")
        for l in logs_du_jour:
            if l["Répétitions"] > 0:
                nouveaux_logs.append({"Date": date_today, "Séance": seance, "Exercice": l["Exercice"], "Poids (kg)": l["Poids (kg)"], "Répétitions": l["Répétitions"]})
        if nouveaux_logs:
            st.session_state.workout_logs = pd.concat([st.session_state.workout_logs, pd.DataFrame(nouveaux_logs)], ignore_index=True)
            st.success("✅ Données enregistrées ! Retrouvez-les dans l'onglet Historique.")
        else:
            st.warning("⚠️ Veuillez entrer des répétitions pour sauvegarder l'exercice.")

# === ONGLET 2 : NUTRITION COMPLÈTE ===
with tab2:
    st.header("🥗 Programme Nutritionnel Économique Complet")
    st.write("Répartition stratégique pour maximiser la synthèse protéique et stimuler les hormones naturellement.")
    
    st.markdown("""
    <div class='nutrition-card'>
        <h4>🥚 Repas 1 : Petit-Déjeuner (Production de Testostérone)</h4>
        <p>• <b>3 œufs entiers</b> (riches en bon cholestérol pour synthétiser le tissu musculaire).</p>
        <p>• <b>60g de flocons d'avoine</b> cuits dans l'eau avec une demi-banane (glucides complexes).</p>
    </div>
    <div class='nutrition-card'>
        <h4>🥩 Repas 2 : Déjeuner (Énergie & Anti-Cortisol)</h4>
        <p>• <b>150g de foie de poulet</b> (Kibda) sautés avec de l'ail et de l'oignon (abaisse le cortisol, riche en fer et zinc).</p>
        <p>• <b>150g de riz blanc</b> ou pâtes bouillies.</p>
        <p>• Une assiette de salade verte légère.</p>
    </div>
    <div class='nutrition-card'>
        <h4>🌌 Repas 3 : Unique Repas Post-Entraînement / Pré-Sommeil</h4>
        <p>• <b>1 boîte de thon à l'eau</b> égouttée ou 3 blancs d'œufs bouillis (acides aminés rapides).</p>
        <p>• <b>2 pots de fromage blanc nature</b> (caséine pour nourrir les muscles pendant 8h de sommeil).</p>
        <p>• <b>150g à 200g de pomme de terre bouillie</b> (glucides sains facilitant l'endormissement sans pic d'insuline trop violent).</p>
        <p>• <b>Une poignée de cacahuètes grillées sans sel</b> (magnésium et lipides pour maximiser l'hormone de croissance GH).</p>
    </div>
    """, unsafe_allow_html=True)
    st.warning("🚫 Règle d'or : Aucun sucre rapide (biscuits, boissons sucrées) avant le coucher pour éviter de bloquer l'hormone de croissance pendant la nuit.")

# === ONGLET 3 : SUIVI & MASSE GRASSE ===
with tab3:
    st.header("📏 Calculateur de Masse Grasse & Métrique")
    st.write("Formule officielle de l'US Navy (sans pinces ni balances coûteuses).")
    
    taille = st.number_input("Votre taille (cm) :", min_value=120.0, max_value=230.0, value=175.0)
    poids_actuel = st.number_input("Votre poids actuel (kg) :", min_value=30.0, max_value=200.0, value=75.0)
    cou = st.number_input("Tour de cou au milieu (cm) :", min_value=20.0, max_value=60.0, value=38.0)
    taille_ventre = st.number_input("Tour de taille au nombril (cm) :", min_value=40.0, max_value=150.0, value=85.0)
    
    if st.button("📊 Analyser la composition corporelle"):
        bmi = poids_actuel / ((taille / 100) ** 2)
        try:
            bf = 86.010 * math.log10(taille_ventre - cou) - 70.041 * math.log10(taille) + 36.76
            masse_grasse = poids_actuel * (bf / 100)
            masse_seche = poids_actuel - masse_grasse
            
            st.metric("📉 Taux de Masse Grasse estimé :", f"{bf:.1f} %")
            st.metric("💪 Masse Musculaire Sèche (LBM) :", f"{masse_seche:.1f} kg")
            st.metric("⚖️ Indice de Masse Corporelle (BMI) :", f"{bmi:.1f}")
        except:
            st.error("Veuillez vérifier les mesures (le tour de taille doit être supérieur au tour de cou).")

# === ONGLET 4 : HISTORIQUE ===
with tab4:
    st.header("📈 Suivi Historique des Performances")
    if not st.session_state.workout_logs.empty:
        st.dataframe(st.session_state.workout_logs, use_container_width=True)
        if st.button("🗑️ Réinitialiser tout l'historique"):
            st.session_state.workout_logs = pd.DataFrame(columns=["Date", "Séance", "Exercice", "Poids (kg)", "Répétitions"])
            st.rerun()
    else:
        st.info("📭 Aucun entraînement enregistré pour le moment. Allez au premier onglet pour enregistrer votre séance !")
