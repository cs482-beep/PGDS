import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# ==========================================
# CONFIGURATION DE LA PAGE & STYLE DE SIGN
# ==========================================
st.set_page_config(
    page_title="Stockify - Gestion de Stock",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injection CSS pour un design professionnel (Bleu, Rose, Blanc)
st.markdown("""
    <style>
    /* Fond de l'application avec un léger dégradé */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* Personnalisation de la barre latérale */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p {
        color: #ffffff;
    }
    
    /* Titres professionnels */
    h1, h2, h3 {
        color: #1e3c72 !important;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    }
    
    /* Boutons personnalisés avec dégradé Rose/Bleu */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.2);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 65, 108, 0.4);
        color: white;
    }
    
    /* Cartes blanches pour le Dashboard (KPIs) */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #ff416c; /* Touche de rose */
        margin-bottom: 15px;
    }
    .metric-card.blue {
        border-left: 5px solid #2a5298; /* Touche de bleu */
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# GESTION DES DONNÉES (CSV)
# ==========================================
CSV_FILE = "stock_data.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    else:
        return pd.DataFrame(columns=["Date", "Type", "Produit", "Quantite", "Categorie"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Initialisation des données dans la session
if 'df_stock' not in st.session_state:
    st.session_state.df_stock = load_data()

# ==========================================
# ÉCRAN DE CONNEXION (LOGIN)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center; background-color: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-top: 8px solid #2a5298;'>
                <h1 style='margin-bottom: 5px;'>📦 Stockify</h1>
                <p style='color: #666;'>Gestion de Stock & Statistiques</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.subheader("Connexion")
            username = st.text_input("Identifiant", placeholder="admin")
            password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
            submit_login = st.form_submit_button("Se connecter")
            
            if submit_login:
                # Identifiants de test (Modifiables ici)
                if username == "admin" and password == "admin123":
                    st.session_state.logged_in = True
                    st.success("Connexion réussie !")
                    st.rerun()
                else:
                    st.error("Identifiant ou mot de passe incorrect.")
    st.stop()

# ==========================================
# APPLICATION PRINCIPALE (APPRÈS CONNEXION)
# ==========================================

# Déconnexion dans la barre latérale
with st.sidebar:
    st.markdown("### 👤 Session Active")
    st.caption("Connecté en tant que: **Admin**")
    if st.button("Se déconnecter", key="logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("---")
    menu = st.radio("Navigation", ["📊 Tableaux de bord", "📥 Entrées / Sorties", "📋 Base de données"])

df = st.session_state.df_stock

# ------------------------------------------
# ONGLET 1 : TABLEAUX DE BORD (DASHBOARD)
# ------------------------------------------
if menu == "📊 Tableaux de bord":
    st.title("📊 Tableau de Bord des Stocks")
    st.markdown("Visualisez en temps réel l'état et les mouvements de votre stock.")
    
    # Calcul des indicateurs clés (KPIs)
    total_mouvements = len(df)
    total_entrees = df[df['Type'] == 'Entrée']['Quantite'].sum()
    total_sorties = df[df['Type'] == 'Sortie']['Quantite'].sum()
    
    # Affichage des KPIs stylisés
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f"""
            <div class='metric-card blue'>
                <p style='color:#555; font-size:14px; margin:0;'>TOTAL ENTRÉES</p>
                <h2 style='margin:5px 0 0 0; color:#2a5298;'>📈 {total_entrees} unités</h2>
            </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""
            <div class='metric-card'>
                <p style='color:#555; font-size:14px; margin:0;'>TOTAL SORTIES</p>
                <h2 style='margin:5px 0 0 0; color:#ff416c;'>📉 {total_sorties} unités</h2>
            </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
            <div class='metric-card blue'>
                <p style='color:#555; font-size:14px; margin:0;'>TOTAL TRANSACTIONS</p>
                <h2 style='margin:5px 0 0 0; color:#1e3c72;'>🔄 {total_mouvements} opérations</h2>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphiques avec Plotly (Couleurs adaptées)
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("📦 Volume des Flux par Produit")
        if not df.empty:
            fig_bar = px.bar(
                df, x="Produit", y="Quantite", color="Type",
                barmode="group",
                color_discrete_map={'Entrée': '#2a5298', 'Sortie': '#ff416c'},
                template="plotly_white"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Aucune donnée disponible.")
            
    with chart_col2:
        st.subheader("🏷️ Répartition par Catégorie")
        if not df.empty:
            fig_pie = px.pie(
                df, names="Categorie", values="Quantite",
                color_discrete_sequence=['#2a5298', '#ff416c', '#00c9ff', '#92fe9d'],
                hole=0.4,
                template="plotly_white"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Aucune donnée disponible.")

# ------------------------------------------
# ONGLET 2 : ENTRÉES / SORTIES (FORMULAIRE)
# ------------------------------------------
elif menu == "📥 Entrées / Sorties":
    st.title("📥 Enregistrer un Flux de Stock")
    st.markdown("Utilisez ce formulaire pour ajouter une entrée ou une sortie de marchandise.")
    
    with st.form("stock_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            type_mvt = st.selectbox("Type de mouvement", ["Entrée", "Sortie"])
            produit = st.text_input("Nom du produit", placeholder="Ex: Écran Asus 27\"")
            categorie = st.selectbox("Catégorie", ["Électronique", "Accessoires", "Mobilier", "Autre"])
        with col2:
            quantite = st.number_input("Quantité", min_value=1, step=1, value=1)
            date_mvt = st.date_input("Date de l'opération", datetime.now().date())
            
        submit_btn = st.form_submit_button("Valider l'opération")
        
        if submit_btn:
            if produit.strip() == "":
                st.error("Veuillez entrer le nom du produit.")
            else:
                # Ajout de la nouvelle ligne
                new_row = pd.DataFrame([{
                    "Date": date_mvt,
                    "Type": type_mvt,
                    "Produit": produit,
                    "Quantite": quantite,
                    "Categorie": categorie
                }])
                
                st.session_state.df_stock = pd.concat([df, new_row], ignore_index=True)
                save_data(st.session_state.df_stock)
                st.success(f"Opération enregistrée avec succès : {type_mvt} de {quantite} {produit}")
                st.rerun()

# ------------------------------------------
# ONGLET 3 : BASE DE DONNÉES (HISTORIQUE)
# ------------------------------------------
elif menu == "📋 Base de données":
    st.title("📋 Historique des Mouvements")
    st.markdown("Consultez et gérez l'ensemble des données enregistrées dans le fichier CSV.")
    
    if not df.empty:
        # Filtre rapide
        search = st.text_input("🔍 Rechercher un produit...", "")
        if search:
            filtered_df = df[df['Produit'].str.contains(search, case=False, na=False)]
        else:
            filtered_df = df
            
        # Affichage du tableau interactif
        st.dataframe(filtered_df, use_container_width=True)
        
        # Option de réinitialisation complète
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("⚠️ Réinitialiser toutes les données"):
            empty_df = pd.DataFrame(columns=["Date", "Type", "Produit", "Quantite", "Categorie"])
            st.session_state.df_stock = empty_df
            save_data(empty_df)
            st.warning("Toutes les données ont été effacées.")
            st.rerun()
    else:
        st.info("La base de données est actuellement vide.")