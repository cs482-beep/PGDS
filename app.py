import os
import subprocess
import sys

# Étape 1 : Forcer l'installation automatique de Plotly si Streamlit l'oublie
try:
    import plotly.express as px
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
    import plotly.express as px

import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# CONFIGURATION DE LA PAGE & STYLE DESIGN
# ==========================================
st.set_page_config(
    page_title="Stockify - Gestion de Stock DH",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injection CSS pour un design professionnel haut de gamme (Bleu, Rose, Blanc)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f4f7f6 50%, #eef2f7 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    h1, h2, h3 {
        color: #1e3c72 !important;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    }
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #ff416c 0%, #ff4b2b 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.3);
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 65, 108, 0.5);
        color: white !important;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.04);
        border-left: 6px solid #ff416c;
        margin-bottom: 15px;
    }
    .metric-card.blue {
        border-left: 6px solid #2a5298;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# GESTION DES DONNÉES (CSV)
# ==========================================
CSV_FILE = "stock_data.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            return df
        except:
            return pd.DataFrame(columns=["Date", "Type", "Produit", "Quantite", "Prix_DH", "Categorie"])
    else:
        # Données initiales par défaut si le fichier n'existe pas
        data = {
            "Date": [datetime.now().date()],
            "Type": ["Entrée"],
            "Produit": ["Exemple Produit"],
            "Quantite": [10],
            "Prix_DH": [1500.0],
            "Categorie": ["Électronique"]
        }
        df = pd.DataFrame(data)
        df.to_csv(CSV_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

if 'df_stock' not in st.session_state:
    st.session_state.df_stock = load_data()

# ==========================================
# ÉCRAN DE CONNEXION (LOGIN)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.4, 1])
    
    with col2:
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center; background-color: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border-top: 8px solid #2a5298;'>
                <h1 style='margin-bottom: 5px; color: #1e3c72;'>📦 Stockify Pro</h1>
                <p style='color: #666; font-size: 14px;'>Gestion de Stock & Statistiques (DH)</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("<h3 style='margin-top:0;'>Connexion sécurisée</h3>", unsafe_allow_html=True)
            username = st.text_input("Identifiant utilisateur", placeholder="admin")
            password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
            submit_login = st.form_submit_button("Se connecter au Tableau de bord")
            
            if submit_login:
                if username == "admin" and password == "admin123":
                    st.session_state.logged_in = True
                    st.success("Connexion réussie !")
                    st.rerun()
                else:
                    st.error("Identifiant ou mot de passe incorrect.")
    st.stop()

# ==========================================
# APPLICATION PRINCIPALE
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:white; text-align:center;'>📦 Stockify</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 👤 Session Active")
    st.caption("Rôle : **Administrateur**")
    if st.button("🔴 Se déconnecter", key="logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("---")
    menu = st.radio("Navigation", ["📊 Tableau de bord", "📥 Entrées / Sorties", "📋 Historique & Fichiers"])

df = st.session_state.df_stock

# ------------------------------------------
# DASHBOARD
# ------------------------------------------
if menu == "📊 Tableau de bord":
    st.title("📊 Tableau de Bord Financier & Logistique")
    st.markdown("Suivi en temps réel des flux de marchandises valorisés en Dirhams (DH).")
    
    total_entrees_qty = df[df['Type'] == 'Entrée']['Quantite'].sum()
    total_sorties_qty = df[df['Type'] == 'Sortie']['Quantite'].sum()
    
    df['Valeur_Total'] = df['Quantite'] * df['Prix_DH']
    valeur_entrees = df[df['Type'] == 'Entrée']['Valeur_Total'].sum()
    valeur_sorties = df[df['Type'] == 'Sortie']['Valeur_Total'].sum()
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f"""
            <div class='metric-card blue'>
                <p style='color:#666; font-size:13px; margin:0; font-weight:600;'>FLUX DES ENTRÉES</p>
                <h2 style='margin:5px 0 0 0; color:#2a5298;'>📈 {total_entrees_qty} <span style='font-size:14px; color:#666;'>unités</span></h2>
            </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""
            <div class='metric-card blue'>
                <p style='color:#666; font-size:13px; margin:0; font-weight:600;'>VALEUR DES ENTRÉES</p>
                <h2 style='margin:5px 0 0 0; color:#1e3c72;'>{valeur_entrees:,.2f} <span style='font-size:14px;'>DH</span></h2>
            </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
            <div class='metric-card'>
                <p style='color:#666; font-size:13px; margin:0; font-weight:600;'>FLUX DES SORTIES</p>
                <h2 style='margin:5px 0 0 0; color:#ff416c;'>📉 {total_sorties_qty} <span style='font-size:14px; color:#666;'>unités</span></h2>
            </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""
            <div class='metric-card'>
                <p style='color:#666; font-size:13px; margin:0; font-weight:600;'>VALEUR DES SORTIES</p>
                <h2 style='margin:5px 0 0 0; color:#ff4b2b;'>{valeur_sorties:,.2f} <span style='font-size:14px;'>DH</span></h2>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("💰 Valeur Totale des Flux par Produit (DH)")
        if not df.empty:
            fig_bar = px.bar(
                df, x="Produit", y="Valeur_Total", color="Type",
                barmode="group",
                labels={"Valeur_Total": "Valeur Totale (DH)"},
                color_discrete_map={'Entrée': '#2a5298', 'Sortie': '#ff416c'},
                template="plotly_white"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
    with chart_col2:
        st.subheader("🏷️ Répartition Financière par Catégorie")
        if not df.empty:
            fig_pie = px.pie(
                df, names="Categorie", values="Valeur_Total",
                color_discrete_sequence=['#2a5298', '#ff416c', '#00c9ff', '#ffb347'],
                hole=0.4,
                template="plotly_white"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

# ------------------------------------------
# ENTRÉES / SORTIES
# ------------------------------------------
elif menu == "📥 Entrées / Sorties":
    st.title("📥 Enregistrer un nouveau mouvement de stock")
    
    with st.form("stock_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            type_mvt = st.selectbox("Nature de l'opération", ["Entrée", "Sortie"])
            produit = st.text_input("Nom ou Désignation du produit", placeholder="Ex: Machine à café")
            categorie = st.selectbox("Catégorie associée", ["Électronique", "Accessoires", "Mobilier", "Autre"])
        with col2:
            quantite = st.number_input("Quantité", min_value=1, step=1, value=1)
            prix_dh = st.number_input("Prix Unitaire (en DH)", min_value=0.0, step=10.0, value=0.0, format="%.2f")
            date_mvt = st.date_input("Date effective", datetime.now().date())
            
        submit_btn = st.form_submit_button("💾 Enregistrer la transaction")
        
        if submit_btn:
            if produit.strip() == "":
                st.error("Le nom du produit ne peut pas être vide.")
            elif prix_dh <= 0:
                st.error("Veuillez indiquer un prix valide en DH supérieur à 0.")
            else:
                new_row = pd.DataFrame([{
                    "Date": date_mvt,
                    "Type": type_mvt,
                    "Produit": produit,
                    "Quantite": quantite,
                    "Prix_DH": prix_dh,
                    "Categorie": categorie
                }])
                
                st.session_state.df_stock = pd.concat([df, new_row], ignore_index=True)
                save_data(st.session_state.df_stock)
                st.success(f"Opération ajoutée avec succès !")
                st.rerun()

# ------------------------------------------
# HISTORIQUE
# ------------------------------------------
elif menu == "📋 Historique & Fichiers":
    st.title("📋 Grand Livre des Stocks & Historique")
    
    if not df.empty:
        search = st.text_input("🔍 Filtrer instantanément par nom de produit...", "")
        if search:
            filtered_df = df[df['Produit'].str.contains(search, case=False, na=False)]
        else:
            filtered_df = df
            
        display_df = filtered_df.copy()
        if 'Valeur_Total' not in display_df.columns:
            display_df['Valeur_Total (DH)'] = display_df['Quantite'] * display_df['Prix_DH']
        else:
            display_df.rename(columns={'Valeur_Total': 'Valeur_Total (DH)'}, inplace=True)
            
        st.dataframe(display_df, use_container_width=True)
