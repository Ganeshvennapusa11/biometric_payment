# # import streamlit as st
# # import os
# # import geocoder
# # import plotly.graph_objects as go
# # import pickle
# # import threading

# # from streamlit import components
# # from face_register import register_user, scan_biopay_qr
# # from model_utils import train_model
# # from face_auth import authenticate
# # from blink_auth import challenge_response_auth
# # from otp_utils import send_transaction_mail
# # from risk_engine import calculate_risk_score
# # from user_utils import (
# #     get_all_users, get_user_data, update_profile_photo,
# #     update_failed_attempts, delete_user, rename_user, update_transaction, update_user_balance
# # )

# # # ---------------- PAGE CONFIG & STYLING ----------------
# # st.set_page_config(page_title="BioPay | Secure Face Payments", layout="wide", page_icon="🛡️")

# # st.markdown("""
# # <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

# # <style>
# # /* ─── RESET & ROOT ──────────────────────────────── */
# # *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

# # :root {
# #     --bg:          #07080d;
# #     --surface:     #0e1018;
# #     --card:        #13151f;
# #     --border:      rgba(255,255,255,0.07);
# #     --border-glow: rgba(99,179,237,0.35);
# #     --accent:      #63b3ed;
# #     --accent2:     #4fd1c5;
# #     --accent3:     #f6ad55;
# #     --success:     #48bb78;
# #     --danger:      #fc8181;
# #     --warn:        #f6ad55;
# #     --text:        #e8ecf4;
# #     --text-muted:  #7b8494;
# #     --font-head:   'Syne', sans-serif;
# #     --font-body:   'DM Sans', sans-serif;
# #     --r:           14px;
# #     --r-lg:        20px;
# # }

# # /* ─── APP SHELL ─────────────────────────────────── */
# # .stApp {
# #     background: var(--bg) !important;
# #     font-family: var(--font-body) !important;
# #     color: var(--text) !important;
# # }

# # /* Subtle grid lines background */
# # .stApp::before {
# #     content: '';
# #     position: fixed;
# #     inset: 0;
# #     background-image:
# #         linear-gradient(rgba(99,179,237,0.03) 1px, transparent 1px),
# #         linear-gradient(90deg, rgba(99,179,237,0.03) 1px, transparent 1px);
# #     background-size: 48px 48px;
# #     pointer-events: none;
# #     z-index: 0;
# # }

# # .block-container {
# #     padding: 2rem 2.5rem 3rem !important;
# #     max-width: 1280px !important;
# # }

# # /* ─── TITLE ─────────────────────────────────────── */
# # .bp-title-wrap {
# #     display: flex;
# #     align-items: center;
# #     justify-content: center;
# #     gap: 16px;
# #     padding: 2.4rem 0 1.6rem;
# # }

# # .bp-logo {
# #     width: 48px; height: 48px;
# #     background: linear-gradient(135deg, var(--accent), var(--accent2));
# #     border-radius: 14px;
# #     display: flex; align-items: center; justify-content: center;
# #     font-size: 1.5rem;
# #     box-shadow: 0 0 28px rgba(99,179,237,0.4);
# # }

# # .bp-title {
# #     font-family: var(--font-head);
# #     font-size: 2rem;
# #     font-weight: 800;
# #     letter-spacing: -0.03em;
# #     color: #fff;
# # }

# # .bp-title span {
# #     background: linear-gradient(90deg, var(--accent), var(--accent2));
# #     -webkit-background-clip: text;
# #     -webkit-text-fill-color: transparent;
# # }

# # .bp-tagline {
# #     text-align: center;
# #     font-size: 0.8rem;
# #     font-weight: 500;
# #     letter-spacing: 0.18em;
# #     text-transform: uppercase;
# #     color: var(--text-muted);
# #     margin-bottom: 2.2rem;
# # }

# # /* ─── TABS ───────────────────────────────────────── */
# # .stTabs [role="tablist"] {
# #     background: var(--card) !important;
# #     border: 1px solid var(--border) !important;
# #     border-radius: 12px !important;
# #     padding: 5px !important;
# #     gap: 4px !important;
# # }

# # .stTabs [role="tab"] {
# #     font-family: var(--font-head) !important;
# #     font-size: 0.78rem !important;
# #     font-weight: 700 !important;
# #     letter-spacing: 0.08em !important;
# #     text-transform: uppercase !important;
# #     color: var(--text-muted) !important;
# #     border-radius: 9px !important;
# #     padding: 9px 20px !important;
# #     border: none !important;
# #     background: transparent !important;
# #     transition: all 0.2s ease !important;
# # }

# # .stTabs [role="tab"][aria-selected="true"] {
# #     background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
# #     color: #07080d !important;
# #     box-shadow: 0 4px 18px rgba(99,179,237,0.35) !important;
# # }

# # .stTabs [data-testid="stTabsContent"] {
# #     background: var(--card) !important;
# #     border: 1px solid var(--border) !important;
# #     border-radius: var(--r-lg) !important;
# #     padding: 2.5rem 2rem !important;
# #     margin-top: 12px !important;
# # }

# # /* ─── SECTION HEADERS ────────────────────────────── */
# # h3 {
# #     font-family: var(--font-head) !important;
# #     font-size: 1.25rem !important;
# #     font-weight: 700 !important;
# #     color: var(--text) !important;
# #     letter-spacing: -0.02em !important;
# #     margin-bottom: 1.2rem !important;
# # }

# # h4 {
# #     font-family: var(--font-head) !important;
# #     font-size: 0.95rem !important;
# #     font-weight: 700 !important;
# #     letter-spacing: 0.05em !important;
# #     text-transform: uppercase !important;
# #     color: var(--text-muted) !important;
# #     margin-bottom: 0.8rem !important;
# # }

# # /* ─── BUTTONS ────────────────────────────────────── */
# # .stButton > button {
# #     font-family: var(--font-head) !important;
# #     font-size: 0.82rem !important;
# #     font-weight: 700 !important;
# #     letter-spacing: 0.06em !important;
# #     text-transform: uppercase !important;
# #     border-radius: var(--r) !important;
# #     padding: 0.7rem 1.5rem !important;
# #     border: none !important;
# #     cursor: pointer !important;
# #     transition: all 0.2s ease !important;
# #     width: 100% !important;
# #     background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
# #     color: #07080d !important;
# #     box-shadow: 0 4px 18px rgba(99,179,237,0.25) !important;
# # }

# # .stButton > button:hover {
# #     transform: translateY(-2px) !important;
# #     box-shadow: 0 8px 28px rgba(99,179,237,0.4) !important;
# # }

# # .stButton > button:active { transform: translateY(0) !important; }

# # .stButton > button:disabled {
# #     background: var(--surface) !important;
# #     color: var(--text-muted) !important;
# #     box-shadow: none !important;
# #     transform: none !important;
# #     cursor: not-allowed !important;
# # }

# # /* ─── INPUTS ─────────────────────────────────────── */
# # .stTextInput > label,
# # .stSelectbox > label,
# # .stNumberInput > label {
# #     font-family: var(--font-head) !important;
# #     font-size: 0.72rem !important;
# #     font-weight: 600 !important;
# #     letter-spacing: 0.1em !important;
# #     text-transform: uppercase !important;
# #     color: var(--text-muted) !important;
# #     margin-bottom: 6px !important;
# # }

# # .stTextInput input,
# # .stNumberInput input {
# #     background: var(--surface) !important;
# #     border: 1px solid var(--border) !important;
# #     border-radius: var(--r) !important;
# #     color: var(--text) !important;
# #     font-family: var(--font-body) !important;
# #     font-size: 0.95rem !important;
# #     padding: 0.65rem 1rem !important;
# #     transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
# # }

# # .stTextInput input:focus,
# # .stNumberInput input:focus {
# #     border-color: var(--accent) !important;
# #     box-shadow: 0 0 0 3px rgba(99,179,237,0.15) !important;
# # }

# # /* Selectbox */
# # .stSelectbox [data-baseweb="select"] > div {
# #     background: var(--surface) !important;
# #     border: 1px solid var(--border) !important;
# #     border-radius: var(--r) !important;
# #     color: var(--text) !important;
# #     font-family: var(--font-body) !important;
# # }

# # /* ─── CHECKBOX ───────────────────────────────────── */
# # .stCheckbox label {
# #     font-family: var(--font-body) !important;
# #     font-size: 0.88rem !important;
# #     color: var(--text-muted) !important;
# # }

# # /* ─── METRICS ────────────────────────────────────── */
# # [data-testid="stMetric"] {
# #     background: var(--surface) !important;
# #     border: 1px solid var(--border) !important;
# #     border-radius: var(--r) !important;
# #     padding: 1rem 1.2rem !important;
# # }

# # [data-testid="stMetricLabel"] {
# #     font-family: var(--font-head) !important;
# #     font-size: 0.72rem !important;
# #     font-weight: 600 !important;
# #     letter-spacing: 0.1em !important;
# #     text-transform: uppercase !important;
# #     color: var(--text-muted) !important;
# # }

# # [data-testid="stMetricValue"] {
# #     font-family: var(--font-head) !important;
# #     font-size: 1.8rem !important;
# #     font-weight: 800 !important;
# #     color: var(--accent) !important;
# # }

# # /* ─── ALERTS ─────────────────────────────────────── */
# # .stAlert {
# #     border-radius: var(--r) !important;
# #     font-family: var(--font-body) !important;
# #     font-size: 0.88rem !important;
# #     border: none !important;
# # }

# # .stAlert[data-baseweb="notification"] {
# #     background: rgba(99,179,237,0.08) !important;
# #     border-left: 3px solid var(--accent) !important;
# # }

# # /* Success */
# # div[data-testid="stAlert"] > div[class*="success"] {
# #     background: rgba(72,187,120,0.1) !important;
# #     border-left: 3px solid var(--success) !important;
# #     color: #9ae6b4 !important;
# # }

# # /* Error */
# # div[data-testid="stAlert"] > div[class*="error"] {
# #     background: rgba(252,129,129,0.1) !important;
# #     border-left: 3px solid var(--danger) !important;
# #     color: #feb2b2 !important;
# # }

# # /* Warning */
# # div[data-testid="stAlert"] > div[class*="warning"] {
# #     background: rgba(246,173,85,0.1) !important;
# #     border-left: 3px solid var(--warn) !important;
# #     color: #fbd38d !important;
# # }

# # /* ─── EXPANDER ───────────────────────────────────── */
# # .streamlit-expanderHeader {
# #     font-family: var(--font-head) !important;
# #     font-size: 0.88rem !important;
# #     font-weight: 600 !important;
# #     background: var(--surface) !important;
# #     border: 1px solid var(--border) !important;
# #     border-radius: var(--r) !important;
# #     color: var(--text) !important;
# #     padding: 0.8rem 1rem !important;
# # }

# # .streamlit-expanderContent {
# #     background: var(--surface) !important;
# #     border: 1px solid var(--border) !important;
# #     border-top: none !important;
# #     border-radius: 0 0 var(--r) var(--r) !important;
# #     padding: 1rem !important;
# # }

# # /* ─── CONTAINER / CARD ───────────────────────────── */
# # [data-testid="stVerticalBlockBorderWrapper"] {
# #     background: var(--surface) !important;
# #     border: 1px solid var(--border) !important;
# #     border-radius: var(--r-lg) !important;
# #     padding: 1.5rem !important;
# # }

# # /* ─── SPINNER ────────────────────────────────────── */
# # .stSpinner > div {
# #     border-color: var(--accent) transparent transparent !important;
# # }

# # /* ─── STATUS ─────────────────────────────────────── */
# # [data-testid="stStatusWidget"] {
# #     background: var(--surface) !important;
# #     border: 1px solid var(--border) !important;
# #     border-radius: var(--r) !important;
# #     font-family: var(--font-body) !important;
# # }

# # /* ─── DIVIDER ────────────────────────────────────── */
# # hr {
# #     border: none !important;
# #     border-top: 1px solid var(--border) !important;
# #     margin: 1.5rem 0 !important;
# # }

# # /* ─── IMAGES ─────────────────────────────────────── */
# # img {
# #     border-radius: var(--r) !important;
# #     border: 1px solid var(--border) !important;
# # }

# # /* ─── QR + BIO-ID BADGE ──────────────────────────── */
# # .bio-id-badge {
# #     display: inline-flex;
# #     align-items: center;
# #     gap: 8px;
# #     background: var(--surface);
# #     border: 1px solid var(--border-glow);
# #     border-radius: 8px;
# #     padding: 6px 14px;
# #     font-family: 'Courier New', monospace;
# #     font-size: 0.85rem;
# #     color: var(--accent);
# #     letter-spacing: 0.04em;
# # }

# # /* ─── SUCCESS ANIMATION ──────────────────────────── */
# # .checkmark-circle {
# #     width: 120px; height: 120px;
# #     position: relative; display: inline-block;
# #     margin: 0 auto; text-align: center;
# # }
# # .checkmark-circle .background {
# #     width: 120px; height: 120px;
# #     border-radius: 50%;
# #     background: linear-gradient(135deg, var(--success), #38a169);
# #     position: absolute;
# #     box-shadow: 0 0 40px rgba(72,187,120,0.5);
# # }
# # .checkmark-circle .checkmark.draw:after {
# #     animation-delay: 100ms;
# #     animation-duration: 0.8s;
# #     animation-timing-function: ease;
# #     animation-name: checkmark;
# #     transform: scaleX(-1) rotate(135deg);
# # }
# # .checkmark-circle .checkmark:after {
# #     opacity: 1; height: 60px; width: 30px;
# #     transform-origin: left top;
# #     border-right: 12px solid white;
# #     border-top: 12px solid white; content: '';
# #     left: 30px; top: 60px; position: absolute;
# # }
# # @keyframes checkmark {
# #     0%   { height: 0; width: 0; opacity: 1; }
# #     20%  { height: 0; width: 30px; opacity: 1; }
# #     40%  { height: 60px; width: 30px; opacity: 1; }
# #     100% { height: 60px; width: 30px; opacity: 1; }
# # }

# # /* ─── SUCCESS PAGE CARD ──────────────────────────── */
# # .success-card {
# #     background: linear-gradient(145deg, rgba(72,187,120,0.06), rgba(79,209,197,0.06));
# #     border: 1px solid rgba(72,187,120,0.2);
# #     border-radius: var(--r-lg);
# #     padding: 2rem;
# #     margin-top: 1.5rem;
# # }

# # .tx-label {
# #     font-family: var(--font-head);
# #     font-size: 0.7rem;
# #     font-weight: 700;
# #     letter-spacing: 0.14em;
# #     text-transform: uppercase;
# #     color: var(--text-muted);
# #     margin-bottom: 4px;
# # }

# # .tx-value {
# #     font-family: 'Courier New', monospace;
# #     font-size: 0.92rem;
# #     color: var(--accent);
# #     margin-bottom: 16px;
# # }

# # .tx-amount {
# #     font-family: var(--font-head);
# #     font-size: 2.8rem;
# #     font-weight: 800;
# #     color: var(--success);
# #     letter-spacing: -0.04em;
# #     margin: 8px 0 16px;
# # }

# # /* ─── HOME QUICK ACTION CARDS ────────────────────── */
# # .action-card {
# #     background: var(--surface);
# #     border: 1px solid var(--border);
# #     border-radius: var(--r-lg);
# #     padding: 1.5rem;
# #     height: 100%;
# #     transition: border-color 0.2s ease;
# # }
# # .action-card:hover { border-color: var(--border-glow); }

# # .action-card-title {
# #     font-family: var(--font-head);
# #     font-size: 0.72rem;
# #     font-weight: 700;
# #     letter-spacing: 0.12em;
# #     text-transform: uppercase;
# #     color: var(--text-muted);
# #     margin-bottom: 12px;
# # }

# # /* ─── STEP INDICATORS (payment flow) ─────────────── */
# # .step-row {
# #     display: flex;
# #     align-items: center;
# #     gap: 12px;
# #     background: var(--surface);
# #     border: 1px solid var(--border);
# #     border-radius: var(--r);
# #     padding: 0.9rem 1.2rem;
# #     margin-bottom: 8px;
# #     font-family: var(--font-body);
# #     font-size: 0.88rem;
# #     color: var(--text-muted);
# # }

# # .step-num {
# #     width: 26px; height: 26px;
# #     background: linear-gradient(135deg, var(--accent), var(--accent2));
# #     border-radius: 50%;
# #     display: flex; align-items: center; justify-content: center;
# #     font-family: var(--font-head);
# #     font-size: 0.72rem;
# #     font-weight: 800;
# #     color: #07080d;
# #     flex-shrink: 0;
# # }

# # /* ─── SCROLLBAR ──────────────────────────────────── */
# # ::-webkit-scrollbar { width: 6px; }
# # ::-webkit-scrollbar-track { background: var(--bg); }
# # ::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 3px; }
# # ::-webkit-scrollbar-thumb:hover { background: #4a5568; }

# # /* ─── HIDE STREAMLIT CHROME ──────────────────────── */
# # #MainMenu, footer, header { visibility: hidden; }

# # /* ─── MARKDOWN ───────────────────────────────────── */
# # .stMarkdown p, .stMarkdown li {
# #     font-family: var(--font-body) !important;
# #     color: var(--text-muted) !important;
# #     font-size: 0.9rem !important;
# #     line-height: 1.6 !important;
# # }
# # .stMarkdown strong { color: var(--text) !important; }
# # .stMarkdown code {
# #     background: rgba(99,179,237,0.1) !important;
# #     color: var(--accent) !important;
# #     border-radius: 6px !important;
# #     padding: 2px 8px !important;
# #     font-size: 0.85rem !important;
# # }
# # </style>
# # """, unsafe_allow_html=True)

# # # ─── TITLE ───────────────────────────────────────────────────────────────────
# # st.markdown("""
# # <div class="bp-title-wrap">
# #     <div class="bp-logo">🛡️</div>
# #     <div class="bp-title">Bio<span>Pay</span></div>
# # </div>
# # <p class="bp-tagline">Biometric-Secured Payment Infrastructure · Zero-Trust Identity Layer</p>
# # """, unsafe_allow_html=True)

# # # ---------------- SESSION STATE ----------------
# # if "page" not in st.session_state: st.session_state.page = "landing"
# # if "logged_in" not in st.session_state: st.session_state.logged_in = False
# # if "user_folder" not in st.session_state: st.session_state.user_folder = ""
# # if "qr_scanned_id" not in st.session_state: st.session_state.qr_scanned_id = ""
# # if "payment_step" not in st.session_state: st.session_state.payment_step = "input"
# # if "last_tx_details" not in st.session_state: st.session_state.last_tx_details = {}

# # try:
# #     import winsound
# #     HAS_WINSOUND = True
# # except ImportError:
# #     HAS_WINSOUND = False

# # def play_beep():
# #     if HAS_WINSOUND:
# #         try:
# #             winsound.Beep(1000, 300)
# #         except:
# #             pass # Fallback for non-windows environments
# #     else:
# #         components.html("""
# #             <script>
# #             var context = new (window.AudioContext || window.webkitAudioContext)();
# #             var osc = context.createOscillator();
# #             osc.connect(context.destination);
# #             osc.start();
# #             setTimeout(function () { osc.stop(); }, 200);
# #             </script>
# #         """, height=0)

# # # ─── TOP NAVBAR LOGIC ─────────────────────────────
# # nav_l, nav_r = st.columns([3, 1.2])
# # with nav_l:
# #     # Clicking the logo resets the view to the Landing Page
# #     if st.button("🛡️ BioPay", key="logo_home", use_container_width=False):
# #         st.session_state.page = "landing"
# #         st.rerun()

# # with nav_r:
# #     if not st.session_state.logged_in:
# #         # Top-right corner buttons for Guest
# #         btn_col1, btn_col2 = st.columns(2)
# #         with btn_col1:
# #             if st.button("LOGIN", key="nav_login_btn"):
# #                 st.session_state.page = "login"
# #                 st.rerun()
# #         with btn_col2:
# #             if st.button("REGISTER", key="nav_reg_btn"):
# #                 st.session_state.page = "register"
# #                 st.rerun()
# #     else:
# #         # Logout button for Logged-in users
# #         if st.button("🚪 LOGOUT", use_container_width=True):
# #             st.session_state.logged_in = False
# #             st.session_state.user_folder = ""
# #             st.session_state.page = "landing"
# #             st.rerun()

# # st.divider()

# # # ─── NAVIGATION GATEKEEPER (GUEST VIEW) ────────────────────────
# # if not st.session_state.logged_in:
    
# #     # 1. LANDING / ABOUT PAGE
# #     if st.session_state.page == "landing":
# #         st.markdown("""
# #             <div style="text-align:center; padding: 4rem 1rem;">
# #                 <h1 style="font-family:'Syne'; font-size:3.5rem; font-weight:800; line-height:1.1; margin-bottom:1.5rem;">
# #                     Secure Payments, <span style="color:#63b3ed;">Biometric</span> Trust.
# #                 </h1>
# #                 <p style="color:#7b8494; font-size:1.1rem; max-width:800px; margin: 0 auto 3rem;">
# #                     BioPay is a next-generation infrastructure for zero-trust identity verification. 
# #                     We combine military-grade encryption with facial liveness challenges to eliminate fraud 
# #                     and ensure your transactions are 100% spoof-proof.
# #                 </p>
# #             </div>
# #         """, unsafe_allow_html=True)
        
# #         # Feature Highlights
# #         col_f1, col_f2, col_f3 = st.columns(3)
# #         with col_f1:
# #             st.markdown('<div class="action-card"><h4>🧬 Neural Mapping</h4><p>Proprietary face-matching AI with high-precision biometric accuracy.</p></div>', unsafe_allow_html=True)
# #         with col_f2:
# #             st.markdown('<div class="action-card"><h4>👁️ Gaze Defense</h4><p>Anti-spoofing challenges that block photos, videos, and deepfake attacks.</p></div>', unsafe_allow_html=True)
# #         with col_f3:
# #             st.markdown('<div class="action-card"><h4>🛡️ Zero-Trust</h4><p>Decentralized ledger architecture ensures your data remains immutable and private.</p></div>', unsafe_allow_html=True)

# # # 2. LOGIN PAGE
# #     # 2. LOGIN PAGE
# #     elif st.session_state.page == "login":
# #         st.markdown("""
# #         <style>
# #         .stApp { background: #07080d !important; }
# #         h3 { text-align: center; margin-bottom: 30px; }
        
# #         /* Input Styling to match reference image */
# #         .stTextInput input {
# #             background: transparent !important;
# #             border: none !important;
# #             border-bottom: 1px solid #333 !important;
# #             border-radius: 0px !important;
# #             color: white !important;
# #         }
# #         .stTextInput input:focus {
# #             border-bottom: 2px solid #63b3ed !important;
# #             box-shadow: none !important;
# #         }
# #         </style>
# #         """, unsafe_allow_html=True)
# #         st.markdown("### Secure User Access")
# #         with st.container(border=True):
# #             l_em = st.text_input("Email Address", placeholder="Registered Email", key="login_em")
# #             l_ps = st.text_input("Password", type="password", placeholder="Enter Password", key="login_ps")
            
# #             if st.button("Verify Identity & Face", key="login_btn"):
# #                 if l_em and l_ps:
# #                     # 1. ADMIN OVERRIDE
# #                     if l_em == "vedavyaskodandapani@gmail.com" and l_ps == "Vedavyasvishal@45":
# #                         st.session_state.logged_in = True
# #                         st.session_state.user_folder = "ADMIN"
# #                         st.success("Admin Access Verified")
# #                         st.rerun()
                    
# #                     # 2. STANDARD USER AUTHENTICATION
# #                     safe_folder = l_em.replace("@", "_").replace(".", "_")
# #                     u_data = get_user_data(safe_folder)
                    
# #                     if u_data and u_data.get('password') == l_ps:
# #                         # --- AUTOMATIC SCREEN FLASH OVERLAY ---
# #                         flash_zone = st.empty()
# #                         flash_zone.markdown("""
# #                             <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
# #                                         background-color: white; z-index: 9999; display: flex; 
# #                                         justify-content: center; align-items: center;">
# #                                 <h2 style="color: black; font-family: sans-serif;">🔆 ILLUMINATING FOR SCAN...</h2>
# #                             </div>
# #                             <style>.stApp { background-color: white !important; }</style>
# #                         """, unsafe_allow_html=True)

# #                         # Trigger Biometric Scan
# #                         auth_status, confidence_score = authenticate(safe_folder)
                        
# #                         # Remove Flash Overlay once scan is done
# #                         flash_zone.empty()

# #                         if auth_status:
# #                             st.session_state.logged_in = True
# #                             st.session_state.user_folder = safe_folder
# #                             st.success("Access Granted!")
# #                             st.rerun()
                        
# #                         # --- SECONDARY VERIFICATION (MFA) ---
# #                         elif 50 <= confidence_score <= 85:
# #                             st.warning(f"⚠️ Lighting/Match weak ({int(confidence_score)}%). Answer security challenge.")
                            
# #                             sq_dict = u_data.get('security_questions', {})
# #                             if sq_dict:
# #                                 question = list(sq_dict.keys())[0]
# #                                 correct_ans = sq_dict[question]
                                
# #                                 ans_input = st.text_input(f"Question: {question}", type="password", key="mfa_input")
# #                                 if st.button("Submit Answer"):
# #                                     if ans_input.strip().lower() == correct_ans.strip().lower():
# #                                         st.session_state.logged_in = True
# #                                         st.session_state.user_folder = safe_folder
# #                                         st.success("Knowledge Verified. Access Granted!")
# #                                         st.rerun()
# #                                     else:
# #                                         st.error("Incorrect Answer.")
# #                         else:
# #                             st.error("Biometric Mismatch")
# #                     else:
# #                         st.error("Invalid Email or Password")
# #                 else:
# #                     st.warning("Enter both credentials.")
        
# #         if st.button("← Back", key="back_to_landing"):
# #             st.session_state.page = "landing"
# #             st.rerun()
            
# #     # 3. REGISTER PAGE
# #     elif st.session_state.page == "register":
# #     # Applying the same clean, centered styling used in Login
# #         st.markdown("""
# #         <style>
# #         .stApp { background: #07080d !important; }
# #         h3 { text-align: center; margin-bottom: 30px; }
        
# #         /* Input Styling to match reference image */
# #         .stTextInput input {
# #             background: transparent !important;
# #             border: none !important;
# #             border-bottom: 1px solid #333 !important;
# #             border-radius: 0px !important;
# #             color: white !important;
# #         }
# #         .stTextInput input:focus {
# #             border-bottom: 2px solid #63b3ed !important;
# #             box-shadow: none !important;
# #         }
# #         </style>
# #         """, unsafe_allow_html=True)

# #         st.markdown("### Identity Enrollment")
# #         validation_box = st.empty()
        
# #         # ─── SECTION 1: PERSONAL DETAILS ───
# #         col1, col2 = st.columns(2)
# #         with col1:
# #             fn = st.text_input("Full Name", placeholder="e.g. Arjun Sharma", key="reg_fn")
# #             em = st.text_input("Email Address", placeholder="you@example.com", key="reg_em")
# #             bn = st.selectbox("Bank Name", options=["SBI", "HDFC", "ICICI", "Axis", "PNB", "Kotak"], index=0, key="reg_bn")

# #         with col2:
# #             mb = st.text_input("Mobile Number", placeholder="10-digit number", key="reg_mb")
# #             nc = st.text_input("Native City", placeholder="Your home city", key="reg_nc")
            
# #         # ─── SECTION 2: PASSWORD PAIR (Side by Side) ───
# #         st.write("<br>", unsafe_allow_html=True)
# #         p_col1, p_col2 = st.columns(2)
# #         with p_col1:
# #             reg_ps = st.text_input("Create Secure Password", type="password", placeholder="••••••••", key="reg_pass_main")
# #         with p_col2:
# #             conf_ps = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="reg_pass_conf")

# #         # ─── SECTION 3: CONSENT (Placed Down Here) ───
# #         st.write("<div style='height: 10px;'></div>", unsafe_allow_html=True)
# #         agree = st.checkbox("I consent to biometric data capture & storage", key="reg_agree")

# #         st.markdown("<hr>", unsafe_allow_html=True)
        
# #         # ─── SECTION 4: RECOVERY ───
# #         st.markdown("#### 🛡️ Security Recovery")
# #         sq_col, sa_col = st.columns([2, 1])
# #         with sq_col:
# #             sq = st.selectbox("Security Question", [
# #                 "What was the name of your first school?", 
# #                 "What is your mother's maiden name?", 
# #                 "What was your first pet's name?"
# #             ], key="reg_sq")
# #         with sa_col:
# #             sa = st.text_input("Secret Answer", type="password", placeholder="Your answer", key="reg_sa")

# #         # ─── LOGIC ───
# #         can_reg = False
# #         if fn and em and mb and sa and agree and reg_ps and conf_ps:
# #             from user_utils import check_user_exists
# #             exists, msg = check_user_exists(em, fn, mb)
# #             if exists: 
# #                 validation_box.error(f"⛔ {msg}")
# #             elif reg_ps != conf_ps: 
# #                 validation_box.error("⛔ Passwords do not match.")
# #             else:
# #                 validation_box.success("✓ Identity & Credentials validated.")
# #                 can_reg = True

# #         # ─── BUTTONS ───
# #         if st.button("🚀 Initialize Biometric Scanner", disabled=not can_reg, key="reg_init_btn", use_container_width=True):
# #             with st.status("Registering...") as status:
# #                 register_user(fn, em, mb, nc, bn, {sq: sa}, reg_ps)
# #                 train_model()
# #                 status.update(label="Enrollment Successful!", state="complete")
# #             st.success("Registration Complete! Please Login to continue.")
            
# #         if st.button("← Back to About", key="back_reg", use_container_width=True):
# #             st.session_state.page = "landing"
# #             st.rerun()

# # # ─── LOGGED IN CONTENT ───────────────────────────
# # else:
# #     # Check if the logged-in session belongs to the Admin
# #     if st.session_state.user_folder == "ADMIN":
# #         # --- 1. DATA AGGREGATION ---
# #         users = get_all_users()
# #         total_balance = 0
# #         compliant_count = 0
# #         total_users = len(users)
# #         all_user_data = []

# #         for u in users:
# #             data = get_user_data(u)
# #             if data:
# #                 bal = data.get('balance', 0)
# #                 total_balance += bal
# #                 if bal >= 5000:
# #                     compliant_count += 1
# #                 all_user_data.append(data)

# #         compliance_rate = (compliant_count / total_users * 100) if total_users > 0 else 0

# #         # --- 2. HEADER & GOD-VIEW METRICS ---
# #         st.markdown("## 🛠️ Admin Command Center")
# #         st.info("System Management Mode | Global Infrastructure Oversight")

# #         m1, m2, m3, m4 = st.columns(4)
# #         m1.metric("Total Liquidity", f"₹{total_balance:,}")
# #         m2.metric("Compliance Rate", f"{compliance_rate:.1f}%")
# #         m3.metric("Registered Nodes", total_users)
# #         m4.metric("System Status", "Stable")

# #         st.divider()

# #         # --- 3. BULK ACTION & SEARCH ---
# #         col_header, col_bulk = st.columns([2, 1])
# #         with col_header:
# #             st.markdown("### 👤 User Directory")
# #         with col_bulk:
# #             if st.button("📢 Bulk Warning (Non-Compliant)", type="primary", use_container_width=True):
# #                 warn_count = 0
# #                 for u_data in all_user_data:
# #                     if u_data.get('balance', 0) < 5000:
# #                         # Professional HTML warning template logic
# #                         u_email = u_data.get('email')
# #                         u_name = u_data.get('full_name')
# #                         subj = "URGENT: BioPay Minimum Balance Requirement"
# #                         html_warning = f"""
# #                         <div style="font-family: sans-serif; padding: 20px; border: 1px solid #e2e8f0; border-radius: 10px; max-width: 600px;">
# #                             <h2 style="color: #2d3748;">Greetings from BioPay</h2>
# #                             <p>Dear <strong>{u_name}</strong>,</p>
# #                             <p>Your account is below the required <strong>minimum balance of ₹5,000.00</strong>.</p>
# #                             <div style="background-color: #fffaf0; border-left: 4px solid #f6ad55; padding: 15px; margin: 20px 0;">
# #                                 <p style="margin: 0; color: #975a16;"><strong>Notice:</strong> Please restore your balance within <strong>3 business days</strong>.</p>
# #                             </div>
# #                             <p style="font-size: 0.8rem; color: #718096;">Greetings,<br><strong>BioPay System Administration</strong></p>
# #                         </div>
# #                         """
# #                         if send_transaction_mail(u_email, subj, html_warning):
# #                             warn_count += 1
# #                 st.toast(f"Broadcasted warnings to {warn_count} users.")

# #         search_query = st.text_input("🔍 Search users by name or email...", placeholder="e.g. Vedavyas")

# #         # --- 4. USER MANAGEMENT LIST ---
# #         for u_data in all_user_data:
# #             u_email = u_data.get('email')
# #             u_name = u_data.get('full_name')
# #             u_id = u_data.get('unique_id')
# #             u_bal = u_data.get('balance', 0)

# #             # Filter logic
# #             if search_query.lower() not in u_name.lower() and search_query.lower() not in u_email.lower():
# #                 continue

# #             with st.container(border=True):
# #                 c1, c2, c3 = st.columns([2.5, 1, 1])
                
# #                 with c1:
# #                     st.markdown(f"**{u_name}**")
# #                     st.caption(f"ID: `{u_id}` | Email: {u_email}")
                
# #                 with c2:
# #                     color = "#48bb78" if u_bal >= 5000 else "#fc8181"
# #                     st.markdown(f"<p style='color:#7b8494; font-size:0.75rem; margin-bottom:0;'>BALANCE</p><h4 style='color:{color}; margin-top:0;'>₹{u_bal:,}</h4>", unsafe_allow_html=True)
                
# #                 with c3:
# #                     st.write("<div style='height:15px'></div>", unsafe_allow_html=True)
# #                     if st.button("⚠️ Send Warning", key=f"warn_btn_{u_id}", use_container_width=True):
# #                         subj = "URGENT: BioPay Minimum Balance Requirement"
# #                         html_warning = f"""
# #                         <div style="font-family: sans-serif; padding: 20px; border: 1px solid #e2e8f0; border-radius: 10px; max-width: 600px;">
# #                             <h2 style="color: #2d3748;">Greetings from BioPay</h2>
# #                             <p>Dear <strong>{u_name}</strong>,</p>
# #                             <p>We noticed your account is below the required <strong>minimum balance of ₹5,000.00</strong>.</p>
# #                             <div style="background-color: #fffaf0; border-left: 4px solid #f6ad55; padding: 15px; margin: 20px 0;">
# #                                 <p style="margin: 0; color: #975a16;"><strong>Notice:</strong> Please restore your balance within <strong>3 business days</strong>.</p>
# #                             </div>
# #                             <p style="font-size: 0.8rem; color: #718096;">Greetings,<br><strong>BioPay System Administration</strong></p>
# #                         </div>
# #                         """
# #                         if send_transaction_mail(u_email, subj, html_warning):
# #                             st.success(f"Warning dispatched to {u_name}")
# #                         else:
# #                             st.error("Mail server error.")
# #     else:
# #         # STANDARD MEMBER VIEW
# #         tab_home, tab_pay, tab_list = st.tabs(["🏠 Home", "💸 Payment", "📂 People"])
# #         st.divider()
        
# #         # ... (Include your Home, Payment, and List tab logic below as normal)
# #         with tab_home:
# #             # Fetch the data for the SPECIFIC user who logged in
# #             user_folder = st.session_state.user_folder
# #             u_data = get_user_data(user_folder)
            
# #             if u_data:
# #                 st.markdown(f"### Welcome back, {u_data.get('full_name', 'User')}!")
                
# #                 # ─── TOP METRICS ROW ───
# #                 h_col1, h_col2, h_col3 = st.columns(3)

# #                 with h_col1:
# #                     st.markdown('<div class="action-card"><div class="action-card-title">👛 My Wallet</div>', unsafe_allow_html=True)
# #                     st.metric("Available Balance", f"₹ {u_data.get('balance', 0)}")
# #                     st.caption("Last updated: Real-time")
# #                     st.markdown('</div>', unsafe_allow_html=True)

# #                 with h_col2:
# #                     st.markdown('<div class="action-card"><div class="action-card-title">🆔 My Bio-ID</div>', unsafe_allow_html=True)
# #                     st.code(u_data.get('unique_id', 'Not Assigned'), language=None)
# #                     st.caption("Use this ID for manual transfers")
# #                     st.markdown('</div>', unsafe_allow_html=True)

# #                 with h_col3:
# #                     st.markdown('<div class="action-card"><div class="action-card-title">📱 Receive Money</div>', unsafe_allow_html=True)
# #                     qr_path = f"dataset/{user_folder}/qr_code.png"
# #                     if os.path.exists(qr_path):
# #                         st.image(qr_path, width=120)
# #                     else:
# #                         st.warning("QR Code not found.")
# #                     st.markdown('</div>', unsafe_allow_html=True)

# #                 st.divider()

# #                 # ─── QUICK ACTIONS ROW ───
# #                 st.markdown("#### Quick Payment Tools")
# #                 q_col1, q_col2 = st.columns(2)

# #                 with q_col1:
# #                     st.markdown('<div class="action-card"><div class="action-card-title">📷 QR Scanner</div>', unsafe_allow_html=True)
# #                     if st.button("🚀 Open Camera Scanner", key="home_qr_scan"):
# #                         scanned = scan_biopay_qr()
# #                         if scanned:
# #                             st.session_state.qr_scanned_id = scanned
# #                             st.session_state.payment_step = "confirm"
# #                             st.rerun() 
# #                     st.markdown('</div>', unsafe_allow_html=True)

# #                 with q_col2:
# #                     st.markdown('<div class="action-card"><div class="action-card-title">⌨️ Manual Entry</div>', unsafe_allow_html=True)
# #                     m_id = st.text_input("Enter Receiver Bio-ID", key="home_manual_id", 
# #                                         label_visibility="collapsed", placeholder="Enter Receiver's Bio-ID")
# #                     if st.button("Set Receiver", key="home_save_id"):
# #                         if m_id:
# #                             st.session_state.qr_scanned_id = m_id
# #                             st.success(f"Receiver set to: {m_id}")
# #                     st.markdown('</div>', unsafe_allow_html=True)
# #             else:
# #                 st.error("Error loading user profile. Please try logging in again.")

# #         with tab_pay:
# #         # ─── AUTH GATE ───
# #             if not st.session_state.logged_in:
# #                 st.markdown("""
# #                 <div style="text-align:center; padding: 3rem 1rem;">
# #                     <div style="font-size:3rem; margin-bottom:1rem;">🔒</div>
# #                     <h3 style="color:#e8ecf4; font-family:'Syne',sans-serif; margin-bottom:0.5rem;">Access Restricted</h3>
# #                     <p style="color:#7b8494; font-size:0.9rem;">Please <strong>Login</strong> with your credentials and face identity to enable payments.</p>
# #                 </div>
# #                 """, unsafe_allow_html=True)
# #                 st.stop()

# #             # Set the sender folder to the logged-in user automatically
# #             sender_folder = st.session_state.user_folder
# #             u_info = get_user_data(sender_folder)
# #             sender_bio_id = u_info.get("unique_id", "Not Assigned")

# #             # ─── STAGE 1: INPUT ──────────────────────────────
# #             if st.session_state.payment_step == "input":
# #                 st.markdown("### Secure Payment Terminal")

# #                 st.markdown(f"**Authenticated Sender**")
# #                 st.markdown(f'<div class="bio-id-badge">🆔 {sender_bio_id}</div>', unsafe_allow_html=True)
# #                 st.write("")

# #                 col_scan, col_manual = st.columns(2)
# #                 with col_scan:
# #                     st.markdown('<div class="action-card"><div class="action-card-title">📷 Scan Receiver QR</div>', unsafe_allow_html=True)
# #                     if st.button("Open QR Camera", key="qr_pay"):
# #                         rid = scan_biopay_qr()
# #                         if rid:
# #                             st.session_state.qr_scanned_id = rid
# #                             st.session_state.payment_step = "confirm"
# #                             st.rerun()
# #                     st.markdown('</div>', unsafe_allow_html=True)

# #                 with col_manual:
# #                     st.markdown('<div class="action-card"><div class="action-card-title">⌨️ Enter Receiver Bio-ID</div>', unsafe_allow_html=True)
# #                     rid_input = st.text_input("Receiver Bio-ID", value=st.session_state.qr_scanned_id,
# #                                             label_visibility="collapsed", placeholder="Receiver's Bio-ID")
# #                     if st.button("Proceed to Confirm", key="proceed_pay"):
# #                         if rid_input:
# #                             st.session_state.qr_scanned_id = rid_input
# #                             st.session_state.payment_step = "confirm"
# #                             st.rerun()
# #                     st.markdown('</div>', unsafe_allow_html=True)

# #             # ─── STAGE 2: CONFIRM & AUTH ──────────────────────
# #             elif st.session_state.payment_step == "confirm":
# #                 st.markdown("### Transaction Authorization")
# #                 current_bal = u_info.get("balance", 0)

# #                 col_info, col_bal = st.columns([3, 1])
# #                 with col_info:
# #                     st.markdown(f"""
# #                     <div style="background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:1rem;">
# #                         <div class="tx-label">From</div>
# #                         <div class="tx-value">{sender_bio_id}</div>
# #                         <div class="tx-label">To</div>
# #                         <div class="tx-value">{st.session_state.qr_scanned_id}</div>
# #                     </div>
# #                     """, unsafe_allow_html=True)
# #                 with col_bal:
# #                     st.metric("Available", f"₹{current_bal}")

# #                 with st.container(border=True):
# #                     amount = st.number_input("Transfer Amount (₹)", min_value=1, value=100)

# #                 st.markdown("<hr>", unsafe_allow_html=True)
# #                 st.markdown("#### 🔐 Security Checks")
# #                 st.markdown("""
# #                 <div class="step-row"><div class="step-num">1</div>Biometric face authentication</div>
# #                 <div class="step-row"><div class="step-num">2</div>Randomized gaze liveness challenge</div>
# #                 <div class="step-row"><div class="step-num">3</div>ML anomaly & risk scoring</div>
# #                 """, unsafe_allow_html=True)
# #                 st.write("")

# #                 if st.button("⚡ Verify Identity & Authorize", disabled=(amount > current_bal)):
# #                     # --- 1. AUTOMATIC FLASH FOR PAYMENT ---
# #                     pay_flash = st.empty()
# #                     pay_flash.markdown("""
# #                         <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
# #                                     background-color: white; z-index: 9999; display: flex; 
# #                                     justify-content: center; align-items: center;">
# #                             <h2 style="color: black; font-family: sans-serif;">🔒 SECURE SCANNING...</h2>
# #                         </div>
# #                         <style>.stApp { background-color: white !important; }</style>
# #                     """, unsafe_allow_html=True)

# #                     # --- 2. RUN AUTHENTICATION WITH SCORE ---
# #                     # Returns (True/False, confidence_score)
# #                     auth_status, confidence_score = authenticate(sender_folder)
                    
# #                     # Remove Flash
# #                     pay_flash.empty()

# #                     proceed_tx = False

# #                     if auth_status:
# #                         st.success("✅ Identity Confirmed")
# #                         # Proceed to Liveness if primary face matches
# #                         if challenge_response_auth():
# #                             st.success("✅ Liveness Verified")
# #                             proceed_tx = True
# #                         else:
# #                             st.error("❌ Liveness Check Failed")
                    
# #                     # --- 3. LOW LIGHT / WEAK MATCH FALLBACK ---
# #                     elif 50 <= confidence_score <= 85:
# #                         st.warning(f"⚠️ Poor lighting detected ({int(confidence_score)}%). Verification required.")
# #                         sq_dict = u_info.get("security_questions", {})
# #                         if sq_dict:
# #                             question = list(sq_dict.keys())[0]
# #                             correct_ans = sq_dict[question]
# #                             ans_input = st.text_input(f"Question: {question}", type="password", key="pay_mfa")
# #                             if st.button("Authorize with Secret Answer"):
# #                                 if ans_input.strip().lower() == correct_ans.strip().lower():
# #                                     st.success("✅ Knowledge Verified")
# #                                     proceed_tx = True
# #                                 else:
# #                                     st.error("❌ Incorrect Answer")
# #                     else:
# #                         st.error("❌ Biometric Mismatch")

# #                     # --- 4. PROCESS TRANSACTION & SEND PROFESSIONAL EMAIL ---
# #                     if proceed_tx:
# #                         with st.spinner("Processing Secure Ledger Update..."):
# #                             # This one call now does EVERYTHING (History, Balance, Hash, and both Mails)
# #                             if update_transaction(sender_folder, amount, st.session_state.qr_scanned_id):
                                
# #                                 # Get updated data for the success screen UI
# #                                 updated_info = get_user_data(sender_folder)
# #                                 real_hash = updated_info['transactions'][-1]['hash']

# #                                 st.session_state.last_tx_details = {
# #                                     "sender": sender_bio_id,
# #                                     "receiver": st.session_state.qr_scanned_id,
# #                                     "amount": amount,
# #                                     "hash": real_hash
# #                                 }
# #                                 st.session_state.payment_step = "success"
# #                                 st.rerun()
# #             # ─── STAGE 3: SUCCESS ────────────────────────────
# #             elif st.session_state.payment_step == "success":
# #                 tx = st.session_state.last_tx_details

# #                 st.markdown("""
# #                 <div style="text-align:center; padding: 2.5rem 1rem 1.5rem;">
# #                     <div class="checkmark-circle" style="margin: 0 auto 1.5rem;">
# #                         <div class="background"></div>
# #                         <div class="checkmark draw"></div>
# #                     </div>
# #                     <h2 style="font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800;
# #                                 color:#48bb78; letter-spacing:-0.03em; margin-bottom:0.4rem;">
# #                         Transaction Successful
# #                     </h2>
# #                     <p style="color:#7b8494; font-size:0.88rem; font-family:'DM Sans',sans-serif;">
# #                         Funds transferred securely via BioPay
# #                     </p>
# #                 </div>
# #                 """, unsafe_allow_html=True)

# #                 st.markdown(f"""
# #                 <div class="success-card">
# #                     <div class="tx-label">From Sender ID</div>
# #                     <div class="tx-value">{tx['sender']}</div>
# #                     <div class="tx-label">To Receiver ID</div>
# #                     <div class="tx-value">{tx['receiver']}</div>
# #                     <div class="tx-label">Amount Transferred</div>
# #                     <div class="tx-amount">₹ {tx['amount']}</div>
# #                 </div>
# #                 """, unsafe_allow_html=True)

# #                 st.info("📧 Debit/Credit notifications dispatched to registered email addresses.")
# #                 st.write("")

# #                 if st.button("← Return to Dashboard"):
# #                     st.session_state.payment_step = "input"
# #                     st.session_state.qr_scanned_id = ""
# #                     st.rerun()
# #             pass

# #         with tab_list:
# #             # ─── PEOPLE / CONTACTS TAB ───────────────────────────
# #             with tab_list:
# #                 st.markdown("### 📱 Quick Pay")
# #                 st.caption("Select a verified contact to initiate a secure biometric transfer.")
                
# #                 users = get_all_users()
                
# #                 if not users:
# #                     st.info("No active biometric profiles found.")
# #                 else:
# #                     for u in users:
# #                         u_info = get_user_data(u)
# #                         if not u_info or u == st.session_state.user_folder:
# #                             continue

# #                         # Clean Professional Card
# #                         with st.container():
# #                             col_img, col_info, col_btn = st.columns([1, 4, 2])
                            
# #                             with col_img:
# #                                 # User Initial Circle
# #                                 initial = u_info.get('full_name', 'U')[0]
# #                                 st.markdown(f"""
# #                                     <div style="background: linear-gradient(135deg, #63b3ed, #4fd1c5); 
# #                                                 width:50px; height:50px; border-radius:50%; 
# #                                                 display:flex; align-items:center; justify-content:center; 
# #                                                 color:#07080d; font-weight:bold; font-size:1.2rem; box-shadow: 0 4px 15px rgba(99,179,237,0.3);">
# #                                         {initial}
# #                                     </div>
# #                                 """, unsafe_allow_html=True)
                            
# #                             with col_info:
# #                                 st.markdown(f"**{u_info.get('full_name')}**")
# #                                 st.markdown(f"<code style='color:#63b3ed; font-size:0.8rem;'>{u_info.get('unique_id')}</code>", unsafe_allow_html=True)
                            
# #                             with col_btn:
# #                                 if st.button(f"💸 PAY", key=f"pay_btn_{u}"):
# #                                     # 1. Store the ID
# #                                     st.session_state.qr_scanned_id = u_info.get('unique_id')
# #                                     # 2. FORCE NAVIGATION TO PAYMENT TAB
# #                                     # Note: This depends on how you named your tabs. 
# #                                     # If you are using a radio or selectbox for navigation:
# #                                     st.session_state.active_tab = "PAYMENT" 
# #                                     st.rerun()
                            
# #                             st.markdown("<hr style='margin:12px 0; border-top: 1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

# #             pass


# import streamlit as st
# import os
# import plotly.graph_objects as go
# import threading

# from streamlit import components
# from face_register import register_user, scan_biopay_qr
# from model_utils import train_model
# from face_auth import authenticate
# from blink_auth import challenge_response_auth
# from otp_utils import send_transaction_mail
# from risk_engine import calculate_risk_score, get_risk_thresholds
# from user_utils import (
#     get_all_users, get_user_data, update_profile_photo,
#     update_failed_attempts, delete_user, rename_user,
#     update_transaction, update_user_balance,
#     verify_user_pin, has_pin_registered,
# )

# # ---------------- PAGE CONFIG & STYLING ----------------
# st.set_page_config(page_title="BioPay | Secure Face Payments", layout="wide", page_icon="🛡️")

# st.markdown("""
# <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

# <style>
# *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

# :root {
#     --bg:          #07080d;
#     --surface:     #0e1018;
#     --card:        #13151f;
#     --border:      rgba(255,255,255,0.07);
#     --border-glow: rgba(99,179,237,0.35);
#     --accent:      #63b3ed;
#     --accent2:     #4fd1c5;
#     --accent3:     #f6ad55;
#     --success:     #48bb78;
#     --danger:      #fc8181;
#     --warn:        #f6ad55;
#     --text:        #e8ecf4;
#     --text-muted:  #7b8494;
#     --font-head:   'Syne', sans-serif;
#     --font-body:   'DM Sans', sans-serif;
#     --r:           14px;
#     --r-lg:        20px;
# }

# .stApp {
#     background: var(--bg) !important;
#     font-family: var(--font-body) !important;
#     color: var(--text) !important;
# }

# .stApp::before {
#     content: '';
#     position: fixed;
#     inset: 0;
#     background-image:
#         linear-gradient(rgba(99,179,237,0.03) 1px, transparent 1px),
#         linear-gradient(90deg, rgba(99,179,237,0.03) 1px, transparent 1px);
#     background-size: 48px 48px;
#     pointer-events: none;
#     z-index: 0;
# }

# .block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1280px !important; }

# .bp-title-wrap { display: flex; align-items: center; justify-content: center; gap: 16px; padding: 2.4rem 0 1.6rem; }
# .bp-logo { width: 48px; height: 48px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 0 28px rgba(99,179,237,0.4); }
# .bp-title { font-family: var(--font-head); font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; color: #fff; }
# .bp-title span { background: linear-gradient(90deg, var(--accent), var(--accent2)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
# .bp-tagline { text-align: center; font-size: 0.8rem; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 2.2rem; }

# .stTabs [role="tablist"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 5px !important; gap: 4px !important; }
# .stTabs [role="tab"] { font-family: var(--font-head) !important; font-size: 0.78rem !important; font-weight: 700 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; color: var(--text-muted) !important; border-radius: 9px !important; padding: 9px 20px !important; border: none !important; background: transparent !important; transition: all 0.2s ease !important; }
# .stTabs [role="tab"][aria-selected="true"] { background: linear-gradient(135deg, var(--accent), var(--accent2)) !important; color: #07080d !important; box-shadow: 0 4px 18px rgba(99,179,237,0.35) !important; }
# .stTabs [data-testid="stTabsContent"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: var(--r-lg) !important; padding: 2.5rem 2rem !important; margin-top: 12px !important; }

# h3 { font-family: var(--font-head) !important; font-size: 1.25rem !important; font-weight: 700 !important; color: var(--text) !important; letter-spacing: -0.02em !important; margin-bottom: 1.2rem !important; }
# h4 { font-family: var(--font-head) !important; font-size: 0.95rem !important; font-weight: 700 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; color: var(--text-muted) !important; margin-bottom: 0.8rem !important; }

# .stButton > button { font-family: var(--font-head) !important; font-size: 0.82rem !important; font-weight: 700 !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; border-radius: var(--r) !important; padding: 0.7rem 1.5rem !important; border: none !important; cursor: pointer !important; transition: all 0.2s ease !important; width: 100% !important; background: linear-gradient(135deg, var(--accent), var(--accent2)) !important; color: #07080d !important; box-shadow: 0 4px 18px rgba(99,179,237,0.25) !important; }
# .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(99,179,237,0.4) !important; }
# .stButton > button:disabled { background: var(--surface) !important; color: var(--text-muted) !important; box-shadow: none !important; transform: none !important; cursor: not-allowed !important; }

# .stTextInput > label, .stSelectbox > label, .stNumberInput > label { font-family: var(--font-head) !important; font-size: 0.72rem !important; font-weight: 600 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; color: var(--text-muted) !important; margin-bottom: 6px !important; }
# .stTextInput input, .stNumberInput input { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--r) !important; color: var(--text) !important; font-family: var(--font-body) !important; font-size: 0.95rem !important; padding: 0.65rem 1rem !important; transition: border-color 0.2s ease, box-shadow 0.2s ease !important; }
# .stTextInput input:focus, .stNumberInput input:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(99,179,237,0.15) !important; }
# .stSelectbox [data-baseweb="select"] > div { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--r) !important; color: var(--text) !important; font-family: var(--font-body) !important; }
# .stCheckbox label { font-family: var(--font-body) !important; font-size: 0.88rem !important; color: var(--text-muted) !important; }

# [data-testid="stMetric"] { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--r) !important; padding: 1rem 1.2rem !important; }
# [data-testid="stMetricLabel"] { font-family: var(--font-head) !important; font-size: 0.72rem !important; font-weight: 600 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; color: var(--text-muted) !important; }
# [data-testid="stMetricValue"] { font-family: var(--font-head) !important; font-size: 1.8rem !important; font-weight: 800 !important; color: var(--accent) !important; }

# .stAlert { border-radius: var(--r) !important; font-family: var(--font-body) !important; font-size: 0.88rem !important; border: none !important; }

# [data-testid="stVerticalBlockBorderWrapper"] { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--r-lg) !important; padding: 1.5rem !important; }

# hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.5rem 0 !important; }
# img { border-radius: var(--r) !important; border: 1px solid var(--border) !important; }

# /* ─── RISK METER ────────────────────────────────── */
# .risk-meter-wrap {
#     background: var(--surface);
#     border: 1px solid var(--border);
#     border-radius: var(--r-lg);
#     padding: 1.4rem 1.6rem;
#     margin-bottom: 1.2rem;
# }
# .risk-header {
#     font-family: var(--font-head);
#     font-size: 0.72rem;
#     font-weight: 700;
#     letter-spacing: 0.14em;
#     text-transform: uppercase;
#     color: var(--text-muted);
#     margin-bottom: 10px;
# }
# .risk-score-num {
#     font-family: var(--font-head);
#     font-size: 3rem;
#     font-weight: 800;
#     letter-spacing: -0.04em;
#     line-height: 1;
# }
# .risk-bar-bg {
#     height: 8px;
#     background: rgba(255,255,255,0.07);
#     border-radius: 4px;
#     margin: 12px 0 8px;
#     overflow: hidden;
# }
# .risk-bar-fill {
#     height: 100%;
#     border-radius: 4px;
#     transition: width 0.6s ease;
# }
# .risk-factor-row {
#     display: flex;
#     align-items: center;
#     justify-content: space-between;
#     padding: 7px 0;
#     border-bottom: 1px solid rgba(255,255,255,0.04);
#     font-size: 0.83rem;
#     color: var(--text-muted);
# }
# .risk-factor-row:last-child { border-bottom: none; }
# .risk-factor-name { flex: 1; }
# .risk-factor-bar {
#     flex: 2;
#     height: 4px;
#     background: rgba(255,255,255,0.07);
#     border-radius: 2px;
#     margin: 0 10px;
#     overflow: hidden;
# }
# .risk-factor-bar-fill { height: 100%; border-radius: 2px; }
# .risk-factor-score { width: 36px; text-align: right; font-family: 'Courier New'; color: var(--text); font-size: 0.78rem; }

# /* ─── PIN CHALLENGE CARD ─────────────────────────── */
# .pin-gate-card {
#     background: linear-gradient(145deg, rgba(246,173,85,0.06), rgba(252,129,129,0.06));
#     border: 1px solid rgba(246,173,85,0.3);
#     border-radius: var(--r-lg);
#     padding: 2rem;
#     text-align: center;
#     margin: 1rem 0;
# }
# .pin-gate-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
# .pin-gate-title {
#     font-family: var(--font-head);
#     font-size: 1.1rem;
#     font-weight: 700;
#     color: var(--warn);
#     margin-bottom: 0.4rem;
# }
# .pin-gate-sub { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1.2rem; }

# /* ─── BIO-ID BADGE ───────────────────────────────── */
# .bio-id-badge { display: inline-flex; align-items: center; gap: 8px; background: var(--surface); border: 1px solid var(--border-glow); border-radius: 8px; padding: 6px 14px; font-family: 'Courier New', monospace; font-size: 0.85rem; color: var(--accent); letter-spacing: 0.04em; }

# /* ─── SUCCESS ANIMATION ──────────────────────────── */
# .checkmark-circle { width: 120px; height: 120px; position: relative; display: inline-block; margin: 0 auto; text-align: center; }
# .checkmark-circle .background { width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, var(--success), #38a169); position: absolute; box-shadow: 0 0 40px rgba(72,187,120,0.5); }
# .checkmark-circle .checkmark.draw:after { animation-delay: 100ms; animation-duration: 0.8s; animation-timing-function: ease; animation-name: checkmark; transform: scaleX(-1) rotate(135deg); }
# .checkmark-circle .checkmark:after { opacity: 1; height: 60px; width: 30px; transform-origin: left top; border-right: 12px solid white; border-top: 12px solid white; content: ''; left: 30px; top: 60px; position: absolute; }
# @keyframes checkmark { 0% { height: 0; width: 0; opacity: 1; } 20% { height: 0; width: 30px; opacity: 1; } 40% { height: 60px; width: 30px; opacity: 1; } 100% { height: 60px; width: 30px; opacity: 1; } }

# .success-card { background: linear-gradient(145deg, rgba(72,187,120,0.06), rgba(79,209,197,0.06)); border: 1px solid rgba(72,187,120,0.2); border-radius: var(--r-lg); padding: 2rem; margin-top: 1.5rem; }
# .tx-label { font-family: var(--font-head); font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 4px; }
# .tx-value { font-family: 'Courier New', monospace; font-size: 0.92rem; color: var(--accent); margin-bottom: 16px; }
# .tx-amount { font-family: var(--font-head); font-size: 2.8rem; font-weight: 800; color: var(--success); letter-spacing: -0.04em; margin: 8px 0 16px; }

# .action-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-lg); padding: 1.5rem; height: 100%; transition: border-color 0.2s ease; }
# .action-card:hover { border-color: var(--border-glow); }
# .action-card-title { font-family: var(--font-head); font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 12px; }

# .step-row { display: flex; align-items: center; gap: 12px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--r); padding: 0.9rem 1.2rem; margin-bottom: 8px; font-family: var(--font-body); font-size: 0.88rem; color: var(--text-muted); }
# .step-num { width: 26px; height: 26px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: var(--font-head); font-size: 0.72rem; font-weight: 800; color: #07080d; flex-shrink: 0; }

# ::-webkit-scrollbar { width: 6px; }
# ::-webkit-scrollbar-track { background: var(--bg); }
# ::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 3px; }
# #MainMenu, footer, header { visibility: hidden; }

# .stMarkdown p, .stMarkdown li { font-family: var(--font-body) !important; color: var(--text-muted) !important; font-size: 0.9rem !important; line-height: 1.6 !important; }
# .stMarkdown strong { color: var(--text) !important; }
# .stMarkdown code { background: rgba(99,179,237,0.1) !important; color: var(--accent) !important; border-radius: 6px !important; padding: 2px 8px !important; font-size: 0.85rem !important; }
# </style>
# """, unsafe_allow_html=True)

# # ─── TITLE ────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="bp-title-wrap">
#     <div class="bp-logo">🛡️</div>
#     <div class="bp-title">Bio<span>Pay</span></div>
# </div>
# <p class="bp-tagline">Biometric-Secured Payment Infrastructure · Zero-Trust Identity Layer</p>
# """, unsafe_allow_html=True)

# # ─── SESSION STATE ────────────────────────────────────────────────────────────
# defaults = {
#     "page":           "landing",
#     "logged_in":      False,
#     "user_folder":    "",
#     "qr_scanned_id":  "",
#     "payment_step":   "input",
#     "last_tx_details": {},
#     "pin_verified":   False,    # NEW: tracks PIN gate for current transaction
#     "risk_result":    None,     # NEW: cached risk result for current tx attempt
# }
# for k, v in defaults.items():
#     if k not in st.session_state:
#         st.session_state[k] = v

# try:
#     import winsound
#     HAS_WINSOUND = True
# except ImportError:
#     HAS_WINSOUND = False


# # ─── HELPERS ──────────────────────────────────────────────────────────────────

# def play_beep():
#     if HAS_WINSOUND:
#         try:
#             winsound.Beep(1000, 300)
#         except Exception:
#             pass
#     else:
#         components.html("""
#             <script>
#             var ctx = new (window.AudioContext || window.webkitAudioContext)();
#             var osc = ctx.createOscillator();
#             osc.connect(ctx.destination);
#             osc.start();
#             setTimeout(function(){ osc.stop(); }, 200);
#             </script>
#         """, height=0)


# def _risk_color(level: str) -> str:
#     return {"Low": "#48bb78", "Medium": "#f6ad55", "High": "#fc8181", "Critical": "#e53e3e"}.get(level, "#63b3ed")


# def render_risk_panel(risk: dict):
#     """Render the animated risk score meter + factor breakdown."""
#     score  = risk["score"]
#     level  = risk["level"]
#     color  = _risk_color(level)
#     pct    = score  # 0-100

#     # Score bar colour gradient based on level
#     bar_color = color

#     st.markdown(f"""
#     <div class="risk-meter-wrap">
#         <div class="risk-header">🔬 Live Risk Analysis</div>
#         <div style="display:flex; align-items:flex-end; gap:12px; margin-bottom:4px;">
#             <div class="risk-score-num" style="color:{color};">{score}</div>
#             <div style="font-family:var(--font-head); font-weight:700; font-size:1rem;
#                         color:{color}; padding-bottom:8px;">{level} Risk</div>
#         </div>
#         <div class="risk-bar-bg">
#             <div class="risk-bar-fill" style="width:{pct}%; background:{bar_color};"></div>
#         </div>
#         <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:1rem;">
#             {risk['recommendation']}
#         </div>
#     """, unsafe_allow_html=True)

#     # Factor breakdown rows
#     for f in risk.get("breakdown", []):
#         frac   = (f["score"] / f["max"] * 100) if f["max"] > 0 else 0
#         f_col  = _risk_color("High") if frac > 60 else (_risk_color("Medium") if frac > 30 else _risk_color("Low"))
#         st.markdown(f"""
#         <div class="risk-factor-row">
#             <span class="risk-factor-name">{f['factor']}</span>
#             <div class="risk-factor-bar">
#                 <div class="risk-factor-bar-fill" style="width:{frac:.0f}%; background:{f_col};"></div>
#             </div>
#             <span class="risk-factor-score">{f['score']:.0f}/{f['max']}</span>
#         </div>
#         """, unsafe_allow_html=True)

#     st.markdown("</div>", unsafe_allow_html=True)

#     # Hover tooltip for factor reasons in an expander
#     with st.expander("📋 Factor details"):
#         for f in risk.get("breakdown", []):
#             st.markdown(f"- **{f['factor']}**: {f['reason']}")


# # ─── NAVBAR ───────────────────────────────────────────────────────────────────
# nav_l, nav_r = st.columns([3, 1.2])
# with nav_l:
#     if st.button("🛡️ BioPay", key="logo_home", use_container_width=False):
#         st.session_state.page = "landing"
#         st.rerun()

# with nav_r:
#     if not st.session_state.logged_in:
#         btn_col1, btn_col2 = st.columns(2)
#         with btn_col1:
#             if st.button("LOGIN", key="nav_login_btn"):
#                 st.session_state.page = "login"
#                 st.rerun()
#         with btn_col2:
#             if st.button("REGISTER", key="nav_reg_btn"):
#                 st.session_state.page = "register"
#                 st.rerun()
#     else:
#         if st.button("🚪 LOGOUT", use_container_width=True):
#             st.session_state.logged_in  = False
#             st.session_state.user_folder = ""
#             st.session_state.page       = "landing"
#             st.rerun()

# st.divider()

# # ══════════════════════════════════════════════════════════════════════════════
# # GUEST PAGES
# # ══════════════════════════════════════════════════════════════════════════════
# if not st.session_state.logged_in:

#     # ─── LANDING ──────────────────────────────────────────────────────────
#     if st.session_state.page == "landing":
#         st.markdown("""
#             <div style="text-align:center; padding: 4rem 1rem;">
#                 <h1 style="font-family:'Syne'; font-size:3.5rem; font-weight:800; line-height:1.1; margin-bottom:1.5rem;">
#                     Secure Payments, <span style="color:#63b3ed;">Biometric</span> Trust.
#                 </h1>
#                 <p style="color:#7b8494; font-size:1.1rem; max-width:800px; margin: 0 auto 3rem;">
#                     BioPay is a next-generation infrastructure for zero-trust identity verification.
#                     We combine military-grade encryption with facial liveness challenges to eliminate fraud
#                     and ensure your transactions are 100% spoof-proof.
#                 </p>
#             </div>
#         """, unsafe_allow_html=True)

#         col_f1, col_f2, col_f3 = st.columns(3)
#         with col_f1:
#             st.markdown('<div class="action-card"><h4>🧬 Neural Mapping</h4><p>Proprietary face-matching AI with high-precision biometric accuracy.</p></div>', unsafe_allow_html=True)
#         with col_f2:
#             st.markdown('<div class="action-card"><h4>👁️ Gaze Defense</h4><p>Anti-spoofing challenges that block photos, videos, and deepfake attacks.</p></div>', unsafe_allow_html=True)
#         with col_f3:
#             st.markdown('<div class="action-card"><h4>🛡️ Zero-Trust</h4><p>Decentralized ledger architecture ensures your data remains immutable and private.</p></div>', unsafe_allow_html=True)

#     # ─── LOGIN ────────────────────────────────────────────────────────────
#     elif st.session_state.page == "login":
#         st.markdown("### Secure User Access")
#         with st.container(border=True):
#             l_em = st.text_input("Email Address", placeholder="Registered Email", key="login_em")
#             l_ps = st.text_input("Password", type="password", placeholder="Enter Password", key="login_ps")

#             if st.button("Verify Identity & Face", key="login_btn"):
#                 if l_em and l_ps:
#                     if l_em == "vedavyaskodandapani@gmail.com" and l_ps == "Vedavyasvishal@45":
#                         st.session_state.logged_in   = True
#                         st.session_state.user_folder = "ADMIN"
#                         st.success("Admin Access Verified")
#                         st.rerun()

#                     safe_folder = l_em.replace("@", "_").replace(".", "_")
#                     u_data = get_user_data(safe_folder)

#                     if u_data and u_data.get("password") == l_ps:
#                         flash_zone = st.empty()
#                         flash_zone.markdown("""
#                             <div style="position:fixed;top:0;left:0;width:100vw;height:100vh;
#                                         background:#fff;z-index:9999;display:flex;
#                                         justify-content:center;align-items:center;">
#                                 <h2 style="color:black;font-family:sans-serif;">🔆 ILLUMINATING FOR SCAN...</h2>
#                             </div>""", unsafe_allow_html=True)

#                         auth_status, confidence_score = authenticate(safe_folder)
#                         flash_zone.empty()

#                         if auth_status:
#                             st.session_state.logged_in   = True
#                             st.session_state.user_folder = safe_folder
#                             st.success("Access Granted!")
#                             st.rerun()
#                         elif 50 <= confidence_score <= 85:
#                             st.warning(f"⚠️ Lighting/Match weak ({int(confidence_score)}%). Answer security challenge.")
#                             sq_dict = u_data.get("security_questions", {})
#                             if sq_dict:
#                                 question   = list(sq_dict.keys())[0]
#                                 correct_ans = sq_dict[question]
#                                 ans_input  = st.text_input(f"Question: {question}", type="password", key="mfa_input")
#                                 if st.button("Submit Answer"):
#                                     if ans_input.strip().lower() == correct_ans.strip().lower():
#                                         st.session_state.logged_in   = True
#                                         st.session_state.user_folder = safe_folder
#                                         st.success("Knowledge Verified. Access Granted!")
#                                         st.rerun()
#                                     else:
#                                         st.error("Incorrect Answer.")
#                         else:
#                             st.error("Biometric Mismatch")
#                     else:
#                         st.error("Invalid Email or Password")
#                 else:
#                     st.warning("Enter both credentials.")

#         if st.button("← Back", key="back_to_landing"):
#             st.session_state.page = "landing"
#             st.rerun()

#     # ─── REGISTER ─────────────────────────────────────────────────────────
#     elif st.session_state.page == "register":
#         st.markdown("### Identity Enrollment")
#         validation_box = st.empty()

#         col1, col2 = st.columns(2)
#         with col1:
#             fn = st.text_input("Full Name",     placeholder="e.g. Arjun Sharma", key="reg_fn")
#             em = st.text_input("Email Address", placeholder="you@example.com",   key="reg_em")
#             bn = st.selectbox("Bank Name", ["SBI","HDFC","ICICI","Axis","PNB","Kotak"], key="reg_bn")
#         with col2:
#             mb = st.text_input("Mobile Number", placeholder="10-digit number",   key="reg_mb")
#             nc = st.text_input("Native City",   placeholder="Your home city",    key="reg_nc")

#         st.write("<br>", unsafe_allow_html=True)
#         p_col1, p_col2 = st.columns(2)
#         with p_col1:
#             reg_ps  = st.text_input("Create Secure Password", type="password", placeholder="••••••••", key="reg_pass_main")
#         with p_col2:
#             conf_ps = st.text_input("Confirm Password",       type="password", placeholder="••••••••", key="reg_pass_conf")

#         # ── NEW: PIN REGISTRATION ──────────────────────────────────────────
#         st.markdown("<hr>", unsafe_allow_html=True)
#         st.markdown("""
#         <div style="background:rgba(246,173,85,0.07);border:1px solid rgba(246,173,85,0.25);
#                     border-radius:12px;padding:1rem 1.2rem;margin-bottom:1rem;">
#             <div style="font-family:'Syne',sans-serif;font-size:0.72rem;font-weight:700;
#                         letter-spacing:0.14em;text-transform:uppercase;color:#f6ad55;margin-bottom:6px;">
#                 🔐 Transaction Security PIN
#             </div>
#             <div style="font-size:0.83rem;color:#7b8494;">
#                 Your 4-digit PIN is requested when a transaction carries elevated risk.
#                 Keep it private — it is stored encrypted and never shown again.
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         pin_col1, pin_col2 = st.columns(2)
#         with pin_col1:
#             reg_pin  = st.text_input("Create 4-Digit PIN", type="password",
#                                      placeholder="e.g. 9341", max_chars=4, key="reg_pin_main")
#         with pin_col2:
#             conf_pin = st.text_input("Confirm PIN",        type="password",
#                                      placeholder="Repeat PIN",  max_chars=4, key="reg_pin_conf")
#         # ──────────────────────────────────────────────────────────────────

#         st.write("<div style='height:10px;'></div>", unsafe_allow_html=True)
#         agree = st.checkbox("I consent to biometric data capture & storage", key="reg_agree")

#         st.markdown("<hr>", unsafe_allow_html=True)
#         st.markdown("#### 🛡️ Security Recovery")
#         sq_col, sa_col = st.columns([2, 1])
#         with sq_col:
#             sq = st.selectbox("Security Question", [
#                 "What was the name of your first school?",
#                 "What is your mother's maiden name?",
#                 "What was your first pet's name?"
#             ], key="reg_sq")
#         with sa_col:
#             sa = st.text_input("Secret Answer", type="password", placeholder="Your answer", key="reg_sa")

#         # ── VALIDATION ────────────────────────────────────────────────────
#         can_reg = False
#         if fn and em and mb and sa and agree and reg_ps and conf_ps and reg_pin and conf_pin:
#             from user_utils import check_user_exists
#             exists, msg = check_user_exists(em, fn, mb)
#             if exists:
#                 validation_box.error(f"⛔ {msg}")
#             elif reg_ps != conf_ps:
#                 validation_box.error("⛔ Passwords do not match.")
#             elif not reg_pin.isdigit() or len(reg_pin) != 4:
#                 validation_box.error("⛔ PIN must be exactly 4 numeric digits.")
#             elif reg_pin != conf_pin:
#                 validation_box.error("⛔ PINs do not match.")
#             else:
#                 validation_box.success("✓ Identity, credentials & PIN validated.")
#                 can_reg = True

#         if st.button("🚀 Initialize Biometric Scanner", disabled=not can_reg,
#                      key="reg_init_btn", use_container_width=True):
#             with st.status("Registering...") as status:
#                 # Pass PIN to register_user
#                 register_user(fn, em, mb, nc, bn, {sq: sa}, reg_ps, reg_pin)
#                 train_model()
#                 status.update(label="Enrollment Successful!", state="complete")
#             st.success("Registration Complete! Please Login to continue.")

#         if st.button("← Back to About", key="back_reg", use_container_width=True):
#             st.session_state.page = "landing"
#             st.rerun()

# # ══════════════════════════════════════════════════════════════════════════════
# # LOGGED-IN CONTENT
# # ══════════════════════════════════════════════════════════════════════════════
# else:
#     # ─── ADMIN VIEW ───────────────────────────────────────────────────────
#     if st.session_state.user_folder == "ADMIN":
#         users        = get_all_users()
#         total_balance = 0
#         compliant_count = 0
#         total_users   = len(users)
#         all_user_data = []

#         for u in users:
#             data = get_user_data(u)
#             if data:
#                 bal = data.get("balance", 0)
#                 total_balance   += bal
#                 if bal >= 5000:
#                     compliant_count += 1
#                 all_user_data.append(data)

#         compliance_rate = (compliant_count / total_users * 100) if total_users > 0 else 0

#         st.markdown("## 🛠️ Admin Command Center")
#         st.info("System Management Mode | Global Infrastructure Oversight")

#         m1, m2, m3, m4 = st.columns(4)
#         m1.metric("Total Liquidity",    f"₹{total_balance:,}")
#         m2.metric("Compliance Rate",    f"{compliance_rate:.1f}%")
#         m3.metric("Registered Nodes",   total_users)
#         m4.metric("System Status",      "Stable")

#         st.divider()

#         col_header, col_bulk = st.columns([2, 1])
#         with col_header:
#             st.markdown("### 👤 User Directory")
#         with col_bulk:
#             if st.button("📢 Bulk Warning (Non-Compliant)", type="primary", use_container_width=True):
#                 warn_count = 0
#                 for u_data in all_user_data:
#                     if u_data.get("balance", 0) < 5000:
#                         u_email = u_data.get("email")
#                         u_name  = u_data.get("full_name")
#                         subj    = "URGENT: BioPay Minimum Balance Requirement"
#                         html_warning = f"""
#                         <div style="font-family:sans-serif;padding:20px;">
#                             <h2>Greetings from BioPay</h2>
#                             <p>Dear <strong>{u_name}</strong>, your account is below ₹5,000.00 minimum.</p>
#                         </div>"""
#                         if send_transaction_mail(u_email, subj, html_warning):
#                             warn_count += 1
#                 st.toast(f"Broadcasted warnings to {warn_count} users.")

#         search_query = st.text_input("🔍 Search users...", placeholder="Name or email")

#         for u_data in all_user_data:
#             u_email = u_data.get("email")
#             u_name  = u_data.get("full_name")
#             u_id    = u_data.get("unique_id")
#             u_bal   = u_data.get("balance", 0)
#             u_fail  = u_data.get("failed_attempts", 0)

#             if search_query.lower() not in u_name.lower() and search_query.lower() not in u_email.lower():
#                 continue

#             with st.container(border=True):
#                 c1, c2, c3, c4 = st.columns([2.5, 1, 1, 1])
#                 with c1:
#                     st.markdown(f"**{u_name}**")
#                     st.caption(f"ID: `{u_id}` | {u_email}")
#                 with c2:
#                     color = "#48bb78" if u_bal >= 5000 else "#fc8181"
#                     st.markdown(f"<p style='color:#7b8494;font-size:0.75rem;margin-bottom:0;'>BALANCE</p><h4 style='color:{color};margin-top:0;'>₹{u_bal:,}</h4>", unsafe_allow_html=True)
#                 with c3:
#                     fa_color = "#fc8181" if u_fail >= 3 else ("#f6ad55" if u_fail >= 1 else "#48bb78")
#                     st.markdown(f"<p style='color:#7b8494;font-size:0.75rem;margin-bottom:0;'>FAILED ATTEMPTS</p><h4 style='color:{fa_color};margin-top:0;'>{u_fail}</h4>", unsafe_allow_html=True)
#                 with c4:
#                     st.write("<div style='height:15px'></div>", unsafe_allow_html=True)
#                     if st.button("⚠️ Warn", key=f"warn_btn_{u_id}", use_container_width=True):
#                         subj = "URGENT: BioPay Minimum Balance Requirement"
#                         html_warning = f"<p>Dear {u_name}, please restore your balance.</p>"
#                         if send_transaction_mail(u_email, subj, html_warning):
#                             st.success(f"Warning sent to {u_name}")

#     # ─── MEMBER VIEW ──────────────────────────────────────────────────────
#     else:
#         tab_home, tab_pay, tab_list = st.tabs(["🏠 Home", "💸 Payment", "📂 People"])
#         st.divider()

#         # ═══ HOME TAB ════════════════════════════════════════════════════
#         with tab_home:
#             user_folder = st.session_state.user_folder
#             u_data      = get_user_data(user_folder)

#             if u_data:
#                 st.markdown(f"### Welcome back, {u_data.get('full_name', 'User')}!")

#                 h_col1, h_col2, h_col3 = st.columns(3)

#                 with h_col1:
#                     st.markdown('<div class="action-card"><div class="action-card-title">👛 My Wallet</div>', unsafe_allow_html=True)
#                     st.metric("Available Balance", f"₹ {u_data.get('balance', 0)}")
#                     st.caption("Last updated: Real-time")
#                     st.markdown('</div>', unsafe_allow_html=True)

#                 with h_col2:
#                     st.markdown('<div class="action-card"><div class="action-card-title">🆔 My Bio-ID</div>', unsafe_allow_html=True)
#                     st.code(u_data.get("unique_id", "Not Assigned"), language=None)
#                     st.caption("Use this ID for manual transfers")
#                     st.markdown('</div>', unsafe_allow_html=True)

#                 with h_col3:
#                     st.markdown('<div class="action-card"><div class="action-card-title">📱 Receive Money</div>', unsafe_allow_html=True)
#                     qr_path = f"dataset/{user_folder}/qr_code.png"
#                     if os.path.exists(qr_path):
#                         st.image(qr_path, width=120)
#                     else:
#                         st.warning("QR Code not found.")
#                     st.markdown('</div>', unsafe_allow_html=True)

#                 st.divider()

#                 # PIN status badge
#                 if has_pin_registered(user_folder):
#                     st.markdown("""
#                     <div style="display:inline-flex;align-items:center;gap:8px;
#                                 background:rgba(72,187,120,0.08);border:1px solid rgba(72,187,120,0.25);
#                                 border-radius:8px;padding:6px 14px;font-size:0.82rem;color:#48bb78;margin-bottom:1rem;">
#                         🔐 Transaction PIN registered — high-risk protection active
#                     </div>""", unsafe_allow_html=True)
#                 else:
#                     st.warning("⚠️ No transaction PIN found. Re-register to enable high-risk PIN protection.")

#                 st.markdown("#### Quick Payment Tools")
#                 q_col1, q_col2 = st.columns(2)

#                 with q_col1:
#                     st.markdown('<div class="action-card"><div class="action-card-title">📷 QR Scanner</div>', unsafe_allow_html=True)
#                     if st.button("🚀 Open Camera Scanner", key="home_qr_scan"):
#                         scanned = scan_biopay_qr()
#                         if scanned:
#                             st.session_state.qr_scanned_id = scanned
#                             st.session_state.payment_step  = "confirm"
#                             st.rerun()
#                     st.markdown('</div>', unsafe_allow_html=True)

#                 with q_col2:
#                     st.markdown('<div class="action-card"><div class="action-card-title">⌨️ Manual Entry</div>', unsafe_allow_html=True)
#                     m_id = st.text_input("Enter Receiver Bio-ID", key="home_manual_id",
#                                          label_visibility="collapsed", placeholder="Enter Receiver's Bio-ID")
#                     if st.button("Set Receiver", key="home_save_id"):
#                         if m_id:
#                             st.session_state.qr_scanned_id = m_id
#                             st.success(f"Receiver set to: {m_id}")
#                     st.markdown('</div>', unsafe_allow_html=True)
#             else:
#                 st.error("Error loading user profile. Please log in again.")

#         # ═══ PAYMENT TAB ═════════════════════════════════════════════════
#         with tab_pay:
#             sender_folder = st.session_state.user_folder
#             u_info        = get_user_data(sender_folder)
#             sender_bio_id = u_info.get("unique_id", "Not Assigned")

#             # ── STAGE 1: INPUT ────────────────────────────────────────────
#             if st.session_state.payment_step == "input":
#                 st.markdown("### Secure Payment Terminal")
#                 st.markdown(f"**Authenticated Sender**")
#                 st.markdown(f'<div class="bio-id-badge">🆔 {sender_bio_id}</div>', unsafe_allow_html=True)
#                 st.write("")

#                 col_scan, col_manual = st.columns(2)
#                 with col_scan:
#                     st.markdown('<div class="action-card"><div class="action-card-title">📷 Scan Receiver QR</div>', unsafe_allow_html=True)
#                     if st.button("Open QR Camera", key="qr_pay"):
#                         rid = scan_biopay_qr()
#                         if rid:
#                             st.session_state.qr_scanned_id = rid
#                             st.session_state.payment_step  = "confirm"
#                             st.rerun()
#                     st.markdown('</div>', unsafe_allow_html=True)

#                 with col_manual:
#                     st.markdown('<div class="action-card"><div class="action-card-title">⌨️ Enter Receiver Bio-ID</div>', unsafe_allow_html=True)
#                     rid_input = st.text_input("Receiver Bio-ID", value=st.session_state.qr_scanned_id,
#                                               label_visibility="collapsed", placeholder="Receiver's Bio-ID")
#                     if st.button("Proceed to Confirm", key="proceed_pay"):
#                         if rid_input:
#                             st.session_state.qr_scanned_id = rid_input
#                             st.session_state.payment_step  = "confirm"
#                             st.rerun()
#                     st.markdown('</div>', unsafe_allow_html=True)

#             # ── STAGE 2: CONFIRM, RISK SCORE & AUTH ──────────────────────
#             elif st.session_state.payment_step == "confirm":
#                 st.markdown("### Transaction Authorization")
#                 current_bal = u_info.get("balance", 0)

#                 col_info, col_bal = st.columns([3, 1])
#                 with col_info:
#                     st.markdown(f"""
#                     <div style="background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:1rem;">
#                         <div class="tx-label">From</div>
#                         <div class="tx-value">{sender_bio_id}</div>
#                         <div class="tx-label">To</div>
#                         <div class="tx-value">{st.session_state.qr_scanned_id}</div>
#                     </div>""", unsafe_allow_html=True)
#                 with col_bal:
#                     st.metric("Available", f"₹{current_bal}")

#                 with st.container(border=True):
#                     amount = st.number_input("Transfer Amount (₹)", min_value=1, value=100)

#                 # ── LIVE RISK PREVIEW ─────────────────────────────────────
#                 if amount > 0:
#                     risk = calculate_risk_score(sender_folder, amount)
#                     st.session_state.risk_result = risk
#                     render_risk_panel(risk)

#                     if risk["blocked"]:
#                         st.error("🚫 Transaction blocked by risk engine. Contact support if you believe this is a mistake.")
#                         if st.button("← Go Back"):
#                             st.session_state.payment_step = "input"
#                             st.rerun()
#                         st.stop()

#                 st.markdown("<hr>", unsafe_allow_html=True)
#                 st.markdown("#### 🔐 Security Checks")

#                 risk = st.session_state.risk_result or {}
#                 pin_label = " + PIN Verification" if risk.get("requires_pin") else ""
#                 st.markdown(f"""
#                 <div class="step-row"><div class="step-num">1</div>Biometric face authentication</div>
#                 <div class="step-row"><div class="step-num">2</div>Randomized gaze liveness challenge</div>
#                 <div class="step-row"><div class="step-num">3</div>ML anomaly & risk scoring{pin_label}</div>
#                 """, unsafe_allow_html=True)
#                 st.write("")

#                 # ── PIN GATE (shown only when risk requires it) ───────────
#                 if risk.get("requires_pin") and not st.session_state.pin_verified:
#                     st.markdown("""
#                     <div class="pin-gate-card">
#                         <div class="pin-gate-icon">🔐</div>
#                         <div class="pin-gate-title">PIN Verification Required</div>
#                         <div class="pin-gate-sub">
#                             This transaction was flagged as high-risk.<br>
#                             Enter your 4-digit security PIN to proceed.
#                         </div>
#                     </div>""", unsafe_allow_html=True)

#                     pin_input = st.text_input("Enter your 4-digit PIN",
#                                               type="password", max_chars=4,
#                                               placeholder="••••", key="pay_pin_input")
#                     if st.button("✅ Verify PIN", key="verify_pin_btn"):
#                         if verify_user_pin(sender_folder, pin_input):
#                             st.session_state.pin_verified = True
#                             st.success("✅ PIN Verified — proceed to biometric check")
#                             st.rerun()
#                         else:
#                             update_failed_attempts(sender_folder)
#                             st.error("❌ Incorrect PIN. Attempt logged.")
#                     st.stop()   # Don't render the auth button until PIN clears

#                 # ── MAIN AUTH BUTTON ──────────────────────────────────────
#                 if st.button("⚡ Verify Identity & Authorize",
#                              disabled=(amount > current_bal)):
#                     pay_flash = st.empty()
#                     pay_flash.markdown("""
#                         <div style="position:fixed;top:0;left:0;width:100vw;height:100vh;
#                                     background:#fff;z-index:9999;display:flex;
#                                     justify-content:center;align-items:center;">
#                             <h2 style="color:black;font-family:sans-serif;">🔒 SECURE SCANNING...</h2>
#                         </div>""", unsafe_allow_html=True)

#                     auth_status, confidence_score = authenticate(sender_folder)
#                     pay_flash.empty()

#                     proceed_tx = False

#                     if auth_status:
#                         st.success("✅ Identity Confirmed")
#                         if challenge_response_auth():
#                             st.success("✅ Liveness Verified")
#                             proceed_tx = True
#                         else:
#                             st.error("❌ Liveness Check Failed")
#                             update_failed_attempts(sender_folder)

#                     elif 50 <= confidence_score <= 85:
#                         st.warning(f"⚠️ Poor lighting ({int(confidence_score)}%). Knowledge verification required.")
#                         sq_dict = u_info.get("security_questions", {})
#                         if sq_dict:
#                             question    = list(sq_dict.keys())[0]
#                             correct_ans = sq_dict[question]
#                             ans_input   = st.text_input(f"Question: {question}", type="password", key="pay_mfa")
#                             if st.button("Authorize with Secret Answer"):
#                                 if ans_input.strip().lower() == correct_ans.strip().lower():
#                                     st.success("✅ Knowledge Verified")
#                                     proceed_tx = True
#                                 else:
#                                     st.error("❌ Incorrect Answer")
#                                     update_failed_attempts(sender_folder)
#                     else:
#                         st.error("❌ Biometric Mismatch")
#                         update_failed_attempts(sender_folder)

#                     if proceed_tx:
#                         with st.spinner("Processing Secure Ledger Update..."):
#                             if update_transaction(sender_folder, amount, st.session_state.qr_scanned_id):
#                                 updated_info = get_user_data(sender_folder)
#                                 real_hash    = updated_info["transactions"][-1]["hash"]

#                                 st.session_state.last_tx_details = {
#                                     "sender":    sender_bio_id,
#                                     "receiver":  st.session_state.qr_scanned_id,
#                                     "amount":    amount,
#                                     "hash":      real_hash,
#                                     "risk_score": risk.get("score", 0),
#                                     "risk_level": risk.get("level", "—"),
#                                 }
#                                 st.session_state.payment_step = "success"
#                                 st.session_state.pin_verified = False   # reset for next tx
#                                 st.rerun()

#             # ── STAGE 3: SUCCESS ──────────────────────────────────────────
#             elif st.session_state.payment_step == "success":
#                 tx = st.session_state.last_tx_details

#                 st.markdown("""
#                 <div style="text-align:center;padding:2.5rem 1rem 1.5rem;">
#                     <div class="checkmark-circle" style="margin:0 auto 1.5rem;">
#                         <div class="background"></div>
#                         <div class="checkmark draw"></div>
#                     </div>
#                     <h2 style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
#                                color:#48bb78;letter-spacing:-0.03em;margin-bottom:0.4rem;">
#                         Transaction Successful
#                     </h2>
#                     <p style="color:#7b8494;font-size:0.88rem;">Funds transferred securely via BioPay</p>
#                 </div>""", unsafe_allow_html=True)

#                 risk_color = _risk_color(tx.get("risk_level", "Low"))
#                 st.markdown(f"""
#                 <div class="success-card">
#                     <div class="tx-label">From Sender ID</div>
#                     <div class="tx-value">{tx['sender']}</div>
#                     <div class="tx-label">To Receiver ID</div>
#                     <div class="tx-value">{tx['receiver']}</div>
#                     <div class="tx-label">Amount Transferred</div>
#                     <div class="tx-amount">₹ {tx['amount']}</div>
#                     <div class="tx-label">Risk Score at Authorization</div>
#                     <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
#                                 color:{risk_color};margin-bottom:12px;">
#                         {tx.get('risk_score', '—')} / 100 &nbsp;·&nbsp; {tx.get('risk_level', '—')} Risk
#                     </div>
#                 </div>""", unsafe_allow_html=True)

#                 st.info("📧 Debit/Credit notifications dispatched to registered email addresses.")
#                 st.write("")

#                 if st.button("← Return to Dashboard"):
#                     st.session_state.payment_step  = "input"
#                     st.session_state.qr_scanned_id = ""
#                     st.session_state.risk_result   = None
#                     st.rerun()

#         # ═══ PEOPLE TAB ══════════════════════════════════════════════════
#         with tab_list:
#             st.markdown("### 📱 Quick Pay")
#             st.caption("Select a verified contact to initiate a secure biometric transfer.")

#             users = get_all_users()
#             if not users:
#                 st.info("No active biometric profiles found.")
#             else:
#                 for u in users:
#                     u_info_c = get_user_data(u)
#                     if not u_info_c or u == st.session_state.user_folder:
#                         continue

#                     with st.container():
#                         col_img, col_info, col_btn = st.columns([1, 4, 2])
#                         with col_img:
#                             initial = u_info_c.get("full_name", "U")[0]
#                             st.markdown(f"""
#                                 <div style="background:linear-gradient(135deg,#63b3ed,#4fd1c5);
#                                             width:50px;height:50px;border-radius:50%;
#                                             display:flex;align-items:center;justify-content:center;
#                                             color:#07080d;font-weight:bold;font-size:1.2rem;">
#                                     {initial}
#                                 </div>""", unsafe_allow_html=True)
#                         with col_info:
#                             st.markdown(f"**{u_info_c.get('full_name')}**")
#                             st.markdown(f"<code style='color:#63b3ed;font-size:0.8rem;'>{u_info_c.get('unique_id')}</code>", unsafe_allow_html=True)
#                         with col_btn:
#                             if st.button("💸 PAY", key=f"pay_btn_{u}"):
#                                 st.session_state.qr_scanned_id = u_info_c.get("unique_id")
#                                 st.session_state.payment_step  = "confirm"
#                                 st.session_state.pin_verified  = False
#                                 st.rerun()

#                         st.markdown("<hr style='margin:12px 0;border-top:1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

import streamlit as st
import os
import plotly.graph_objects as go
import threading

from streamlit import components
from face_register import register_user, scan_biopay_qr
from model_utils import train_model
from face_auth import authenticate
from blink_auth import challenge_response_auth
from otp_utils import send_transaction_mail
from risk_engine import calculate_risk_score, get_risk_thresholds
from user_utils import (
    get_all_users, get_user_data, update_profile_photo,
    update_failed_attempts, delete_user, rename_user,
    update_transaction, update_user_balance,
    verify_user_pin, has_pin_registered,
)

# ---------------- PAGE CONFIG & STYLING ----------------
st.set_page_config(page_title="BioPay | Secure Face Payments", layout="wide", page_icon="🛡️")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:          #07080d;
    --surface:     #0e1018;
    --card:        #13151f;
    --border:      rgba(255,255,255,0.07);
    --border-glow: rgba(99,179,237,0.35);
    --accent:      #63b3ed;
    --accent2:     #4fd1c5;
    --accent3:     #f6ad55;
    --success:     #48bb78;
    --danger:      #fc8181;
    --warn:        #f6ad55;
    --text:        #e8ecf4;
    --text-muted:  #7b8494;
    --font-head:   'Syne', sans-serif;
    --font-body:   'DM Sans', sans-serif;
    --r:           14px;
    --r-lg:        20px;
}

.stApp {
    background: var(--bg) !important;
    font-family: var(--font-body) !important;
    color: var(--text) !important;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(99,179,237,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,179,237,0.03) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
}

.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1280px !important; }

.bp-title-wrap { display: flex; align-items: center; justify-content: center; gap: 16px; padding: 2.4rem 0 1.6rem; }
.bp-logo { width: 48px; height: 48px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 0 28px rgba(99,179,237,0.4); }
.bp-title { font-family: var(--font-head); font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; color: #fff; }
.bp-title span { background: linear-gradient(90deg, var(--accent), var(--accent2)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.bp-tagline { text-align: center; font-size: 0.8rem; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 2.2rem; }

.stTabs [role="tablist"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 5px !important; gap: 4px !important; }
.stTabs [role="tab"] { font-family: var(--font-head) !important; font-size: 0.78rem !important; font-weight: 700 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; color: var(--text-muted) !important; border-radius: 9px !important; padding: 9px 20px !important; border: none !important; background: transparent !important; transition: all 0.2s ease !important; }
.stTabs [role="tab"][aria-selected="true"] { background: linear-gradient(135deg, var(--accent), var(--accent2)) !important; color: #07080d !important; box-shadow: 0 4px 18px rgba(99,179,237,0.35) !important; }
.stTabs [data-testid="stTabsContent"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: var(--r-lg) !important; padding: 2.5rem 2rem !important; margin-top: 12px !important; }

h3 { font-family: var(--font-head) !important; font-size: 1.25rem !important; font-weight: 700 !important; color: var(--text) !important; letter-spacing: -0.02em !important; margin-bottom: 1.2rem !important; }
h4 { font-family: var(--font-head) !important; font-size: 0.95rem !important; font-weight: 700 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; color: var(--text-muted) !important; margin-bottom: 0.8rem !important; }

.stButton > button { font-family: var(--font-head) !important; font-size: 0.82rem !important; font-weight: 700 !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; border-radius: var(--r) !important; padding: 0.7rem 1.5rem !important; border: none !important; cursor: pointer !important; transition: all 0.2s ease !important; width: 100% !important; background: linear-gradient(135deg, var(--accent), var(--accent2)) !important; color: #07080d !important; box-shadow: 0 4px 18px rgba(99,179,237,0.25) !important; }
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(99,179,237,0.4) !important; }
.stButton > button:disabled { background: var(--surface) !important; color: var(--text-muted) !important; box-shadow: none !important; transform: none !important; cursor: not-allowed !important; }

.stTextInput > label, .stSelectbox > label, .stNumberInput > label { font-family: var(--font-head) !important; font-size: 0.72rem !important; font-weight: 600 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; color: var(--text-muted) !important; margin-bottom: 6px !important; }
.stTextInput input, .stNumberInput input { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--r) !important; color: var(--text) !important; font-family: var(--font-body) !important; font-size: 0.95rem !important; padding: 0.65rem 1rem !important; transition: border-color 0.2s ease, box-shadow 0.2s ease !important; }
.stTextInput input:focus, .stNumberInput input:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(99,179,237,0.15) !important; }
.stSelectbox [data-baseweb="select"] > div { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--r) !important; color: var(--text) !important; font-family: var(--font-body) !important; }
.stCheckbox label { font-family: var(--font-body) !important; font-size: 0.88rem !important; color: var(--text-muted) !important; }

[data-testid="stMetric"] { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--r) !important; padding: 1rem 1.2rem !important; }
[data-testid="stMetricLabel"] { font-family: var(--font-head) !important; font-size: 0.72rem !important; font-weight: 600 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; color: var(--text-muted) !important; }
[data-testid="stMetricValue"] { font-family: var(--font-head) !important; font-size: 1.8rem !important; font-weight: 800 !important; color: var(--accent) !important; }

.stAlert { border-radius: var(--r) !important; font-family: var(--font-body) !important; font-size: 0.88rem !important; border: none !important; }

[data-testid="stVerticalBlockBorderWrapper"] { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--r-lg) !important; padding: 1.5rem !important; }

hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.5rem 0 !important; }
img { border-radius: var(--r) !important; border: 1px solid var(--border) !important; }

/* ─── RISK METER ────────────────────────────────── */
.risk-meter-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}
.risk-header {
    font-family: var(--font-head);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 10px;
}
.risk-score-num {
    font-family: var(--font-head);
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
}
.risk-bar-bg {
    height: 8px;
    background: rgba(255,255,255,0.07);
    border-radius: 4px;
    margin: 12px 0 8px;
    overflow: hidden;
}
.risk-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s ease;
}
.risk-factor-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 7px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.83rem;
    color: var(--text-muted);
}
.risk-factor-row:last-child { border-bottom: none; }
.risk-factor-name { flex: 1; }
.risk-factor-bar {
    flex: 2;
    height: 4px;
    background: rgba(255,255,255,0.07);
    border-radius: 2px;
    margin: 0 10px;
    overflow: hidden;
}
.risk-factor-bar-fill { height: 100%; border-radius: 2px; }
.risk-factor-score { width: 36px; text-align: right; font-family: 'Courier New'; color: var(--text); font-size: 0.78rem; }

/* ─── PIN CHALLENGE CARD ─────────────────────────── */
.pin-gate-card {
    background: linear-gradient(145deg, rgba(246,173,85,0.06), rgba(252,129,129,0.06));
    border: 1px solid rgba(246,173,85,0.3);
    border-radius: var(--r-lg);
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
}
.pin-gate-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
.pin-gate-title {
    font-family: var(--font-head);
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--warn);
    margin-bottom: 0.4rem;
}
.pin-gate-sub { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1.2rem; }

/* ─── BIO-ID BADGE ───────────────────────────────── */
.bio-id-badge { display: inline-flex; align-items: center; gap: 8px; background: var(--surface); border: 1px solid var(--border-glow); border-radius: 8px; padding: 6px 14px; font-family: 'Courier New', monospace; font-size: 0.85rem; color: var(--accent); letter-spacing: 0.04em; }

/* ─── SUCCESS ANIMATION ──────────────────────────── */
.checkmark-circle { width: 120px; height: 120px; position: relative; display: inline-block; margin: 0 auto; text-align: center; }
.checkmark-circle .background { width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, var(--success), #38a169); position: absolute; box-shadow: 0 0 40px rgba(72,187,120,0.5); }
.checkmark-circle .checkmark.draw:after { animation-delay: 100ms; animation-duration: 0.8s; animation-timing-function: ease; animation-name: checkmark; transform: scaleX(-1) rotate(135deg); }
.checkmark-circle .checkmark:after { opacity: 1; height: 60px; width: 30px; transform-origin: left top; border-right: 12px solid white; border-top: 12px solid white; content: ''; left: 30px; top: 60px; position: absolute; }
@keyframes checkmark { 0% { height: 0; width: 0; opacity: 1; } 20% { height: 0; width: 30px; opacity: 1; } 40% { height: 60px; width: 30px; opacity: 1; } 100% { height: 60px; width: 30px; opacity: 1; } }

.success-card { background: linear-gradient(145deg, rgba(72,187,120,0.06), rgba(79,209,197,0.06)); border: 1px solid rgba(72,187,120,0.2); border-radius: var(--r-lg); padding: 2rem; margin-top: 1.5rem; }
.tx-label { font-family: var(--font-head); font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 4px; }
.tx-value { font-family: 'Courier New', monospace; font-size: 0.92rem; color: var(--accent); margin-bottom: 16px; }
.tx-amount { font-family: var(--font-head); font-size: 2.8rem; font-weight: 800; color: var(--success); letter-spacing: -0.04em; margin: 8px 0 16px; }

.action-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-lg); padding: 1.5rem; height: 100%; transition: border-color 0.2s ease; }
.action-card:hover { border-color: var(--border-glow); }
.action-card-title { font-family: var(--font-head); font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 12px; }

.step-row { display: flex; align-items: center; gap: 12px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--r); padding: 0.9rem 1.2rem; margin-bottom: 8px; font-family: var(--font-body); font-size: 0.88rem; color: var(--text-muted); }
.step-num { width: 26px; height: 26px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: var(--font-head); font-size: 0.72rem; font-weight: 800; color: #07080d; flex-shrink: 0; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 3px; }
#MainMenu, footer, header { visibility: hidden; }

.stMarkdown p, .stMarkdown li { font-family: var(--font-body) !important; color: var(--text-muted) !important; font-size: 0.9rem !important; line-height: 1.6 !important; }
.stMarkdown strong { color: var(--text) !important; }
.stMarkdown code { background: rgba(99,179,237,0.1) !important; color: var(--accent) !important; border-radius: 6px !important; padding: 2px 8px !important; font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)

# ─── TITLE ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bp-title-wrap">
    <div class="bp-logo">🛡️</div>
    <div class="bp-title">Bio<span>Pay</span></div>
</div>
<p class="bp-tagline">Biometric-Secured Payment Infrastructure · Zero-Trust Identity Layer</p>
""", unsafe_allow_html=True)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
defaults = {
    "page":           "landing",
    "logged_in":      False,
    "user_folder":    "",
    "qr_scanned_id":  "",
    "payment_step":   "input",
    "last_tx_details": {},
    "pin_verified":   False,    # NEW: tracks PIN gate for current transaction
    "risk_result":    None,     # NEW: cached risk result for current tx attempt
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def play_beep():
    if HAS_WINSOUND:
        try:
            winsound.Beep(1000, 300)
        except Exception:
            pass
    else:
        components.html("""
            <script>
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            var osc = ctx.createOscillator();
            osc.connect(ctx.destination);
            osc.start();
            setTimeout(function(){ osc.stop(); }, 200);
            </script>
        """, height=0)


def _risk_color(level: str) -> str:
    return {"Low": "#48bb78", "Medium": "#f6ad55", "High": "#fc8181", "Critical": "#e53e3e"}.get(level, "#63b3ed")


def render_risk_panel(risk: dict):
    """Render the animated risk score meter + factor breakdown."""
    score  = risk["score"]
    level  = risk["level"]
    color  = _risk_color(level)
    pct    = score  # 0-100

    # Score bar colour gradient based on level
    bar_color = color

    st.markdown(f"""
    <div class="risk-meter-wrap">
        <div class="risk-header">🔬 Live Risk Analysis</div>
        <div style="display:flex; align-items:flex-end; gap:12px; margin-bottom:4px;">
            <div class="risk-score-num" style="color:{color};">{score}</div>
            <div style="font-family:var(--font-head); font-weight:700; font-size:1rem;
                        color:{color}; padding-bottom:8px;">{level} Risk</div>
        </div>
        <div class="risk-bar-bg">
            <div class="risk-bar-fill" style="width:{pct}%; background:{bar_color};"></div>
        </div>
        <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:1rem;">
            {risk['recommendation']}
        </div>
    """, unsafe_allow_html=True)

    # Factor breakdown rows
    for f in risk.get("breakdown", []):
        frac   = (f["score"] / f["max"] * 100) if f["max"] > 0 else 0
        f_col  = _risk_color("High") if frac > 60 else (_risk_color("Medium") if frac > 30 else _risk_color("Low"))
        st.markdown(f"""
        <div class="risk-factor-row">
            <span class="risk-factor-name">{f['factor']}</span>
            <div class="risk-factor-bar">
                <div class="risk-factor-bar-fill" style="width:{frac:.0f}%; background:{f_col};"></div>
            </div>
            <span class="risk-factor-score">{f['score']:.0f}/{f['max']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Hover tooltip for factor reasons in an expander
    with st.expander("📋 Factor details"):
        for f in risk.get("breakdown", []):
            st.markdown(f"- **{f['factor']}**: {f['reason']}")


# ─── NAVBAR ───────────────────────────────────────────────────────────────────
nav_l, nav_r = st.columns([3, 1.2])
with nav_l:
    if st.button("🛡️ BioPay", key="logo_home", use_container_width=False):
        st.session_state.page = "landing"
        st.rerun()

with nav_r:
    if not st.session_state.logged_in:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("LOGIN", key="nav_login_btn"):
                st.session_state.page = "login"
                st.rerun()
        with btn_col2:
            if st.button("REGISTER", key="nav_reg_btn"):
                st.session_state.page = "register"
                st.rerun()
    else:
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.logged_in  = False
            st.session_state.user_folder = ""
            st.session_state.page       = "landing"
            st.rerun()

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# GUEST PAGES
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:

    # ─── LANDING ──────────────────────────────────────────────────────────
    if st.session_state.page == "landing":
        st.markdown("""
            <div style="text-align:center; padding: 4rem 1rem;">
                <h1 style="font-family:'Syne'; font-size:3.5rem; font-weight:800; line-height:1.1; margin-bottom:1.5rem;">
                    Secure Payments, <span style="color:#63b3ed;">Biometric</span> Trust.
                </h1>
                <p style="color:#7b8494; font-size:1.1rem; max-width:800px; margin: 0 auto 3rem;">
                    BioPay is a next-generation infrastructure for zero-trust identity verification.
                    We combine military-grade encryption with facial liveness challenges to eliminate fraud
                    and ensure your transactions are 100% spoof-proof.
                </p>
            </div>
        """, unsafe_allow_html=True)

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.markdown('<div class="action-card"><h4>🧬 Neural Mapping</h4><p>Proprietary face-matching AI with high-precision biometric accuracy.</p></div>', unsafe_allow_html=True)
        with col_f2:
            st.markdown('<div class="action-card"><h4>✨ Blink Defense</h4><p>Dynamic liveness detection that blocks static photos, video replays, and spoofing attacks.</p></div>', unsafe_allow_html=True)
        with col_f3:
            st.markdown('<div class="action-card"><h4>🛡️ Zero-Trust</h4><p>Decentralized ledger architecture ensures your data remains immutable and private.</p></div>', unsafe_allow_html=True)

    # ─── LOGIN ────────────────────────────────────────────────────────────
    elif st.session_state.page == "login":
        st.markdown("""
        <style>
        .stApp { background: #07080d !important; }
        h3 { text-align: center; margin-bottom: 30px; }
        
        /* Input Styling to match reference image */
        .stTextInput input {
            background: transparent !important;
            border: none !important;
            border-bottom: 1px solid #333 !important;
            border-radius: 0px !important;
            color: white !important;
        }
        .stTextInput input:focus {
            border-bottom: 2px solid #63b3ed !important;
            box-shadow: none !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("### Secure User Access")
        with st.container(border=True):
            l_em = st.text_input("Email Address", placeholder="Registered Email", key="login_em")
            l_ps = st.text_input("Password", type="password", placeholder="Enter Password", key="login_ps")

            if st.button("Verify Identity & Face", key="login_btn"):
                if l_em and l_ps:
                    if l_em == "vedavyaskodandapani@gmail.com" and l_ps == "Vedavyasvishal@45":
                        st.session_state.logged_in   = True
                        st.session_state.user_folder = "ADMIN"
                        st.success("Admin Access Verified")
                        st.rerun()

                    safe_folder = l_em.replace("@", "_").replace(".", "_")
                    u_data = get_user_data(safe_folder)

                    if u_data and u_data.get("password") == l_ps:
                        flash_zone = st.empty()
                        flash_zone.markdown("""
                            <div style="position:fixed;top:0;left:0;width:100vw;height:100vh;
                                        background:#fff;z-index:9999;display:flex;
                                        justify-content:center;align-items:center;">
                                <h2 style="color:black;font-family:sans-serif;">🔆 ILLUMINATING FOR SCAN...</h2>
                            </div>""", unsafe_allow_html=True)

                        auth_status, confidence_score = authenticate(safe_folder)
                        flash_zone.empty()

                        if auth_status:
                            st.session_state.logged_in   = True
                            st.session_state.user_folder = safe_folder
                            st.success("Access Granted!")
                            st.rerun()
                        elif 50 <= confidence_score <= 85:
                            st.warning(f"⚠️ Lighting/Match weak ({int(confidence_score)}%). Answer security challenge.")
                            sq_dict = u_data.get("security_questions", {})
                            if sq_dict:
                                question   = list(sq_dict.keys())[0]
                                correct_ans = sq_dict[question]
                                ans_input  = st.text_input(f"Question: {question}", type="password", key="mfa_input")
                                if st.button("Submit Answer"):
                                    if ans_input.strip().lower() == correct_ans.strip().lower():
                                        st.session_state.logged_in   = True
                                        st.session_state.user_folder = safe_folder
                                        st.success("Knowledge Verified. Access Granted!")
                                        st.rerun()
                                    else:
                                        st.error("Incorrect Answer.")
                        else:
                            st.error("Biometric Mismatch")
                    else:
                        st.error("Invalid Email or Password")
                else:
                    st.warning("Enter both credentials.")

        if st.button("← Back", key="back_to_landing"):
            st.session_state.page = "landing"
            st.rerun()

    # ─── REGISTER ─────────────────────────────────────────────────────────
    elif st.session_state.page == "register":
        st.markdown("""
        <style>
        .stApp { background: #07080d !important; }
        h3 { text-align: center; margin-bottom: 30px; }
        
        /* Input Styling to match reference image */
        .stTextInput input {
            background: transparent !important;
            border: none !important;
            border-bottom: 1px solid #333 !important;
            border-radius: 0px !important;
            color: white !important;
        }
        .stTextInput input:focus {
            border-bottom: 2px solid #63b3ed !important;
            box-shadow: none !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("### Identity Enrollment")
        validation_box = st.empty()

        col1, col2 = st.columns(2)
        with col1:
            fn = st.text_input("Full Name",placeholder="Your name", key="reg_fn")
            em = st.text_input("Email Address",placeholder="Your Email address", key="reg_em")
            bn = st.selectbox("Bank Name", ["SBI","HDFC","ICICI","Axis","PNB","Kotak"], key="reg_bn")
        with col2:
            mb = st.text_input("Mobile Number", placeholder="10-digit number",   key="reg_mb")
            nc = st.text_input("Native City",   placeholder="Your home city",    key="reg_nc")

        st.write("<br>", unsafe_allow_html=True)
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            reg_ps  = st.text_input("Create Secure Password", type="password", placeholder="••••••••", key="reg_pass_main")
        with p_col2:
            conf_ps = st.text_input("Confirm Password",       type="password", placeholder="••••••••", key="reg_pass_conf")

        # ── NEW: PIN REGISTRATION ──────────────────────────────────────────
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(246,173,85,0.07);border:1px solid rgba(246,173,85,0.25);
                    border-radius:12px;padding:1rem 1.2rem;margin-bottom:1rem;">
            <div style="font-family:'Syne',sans-serif;font-size:0.72rem;font-weight:700;
                        letter-spacing:0.14em;text-transform:uppercase;color:#f6ad55;margin-bottom:6px;">
                🔐 Transaction Security PIN
            </div>
            <div style="font-size:0.83rem;color:#7b8494;">
                Your 4-digit PIN is requested when a transaction carries elevated risk.
                Keep it private — it is stored encrypted and never shown again.
            </div>
        </div>
        """, unsafe_allow_html=True)

        pin_col1, pin_col2 = st.columns(2)
        with pin_col1:
            reg_pin  = st.text_input("Create 4-Digit PIN", type="password",
                                     placeholder="Your Pin",max_chars=4, key="reg_pin_main")
        with pin_col2:
            conf_pin = st.text_input("Confirm PIN",        type="password",
                                     placeholder="Repeat PIN",  max_chars=4, key="reg_pin_conf")
        # ──────────────────────────────────────────────────────────────────

        st.write("<div style='height:10px;'></div>", unsafe_allow_html=True)
        agree = st.checkbox("I consent to biometric data capture & storage", key="reg_agree")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### 🛡️ Security Recovery")
        sq_col, sa_col = st.columns([2, 1])
        with sq_col:
            sq = st.selectbox("Security Question", [
                "What was the name of your first school?",
                "What is your mother's maiden name?",
                "What was your first pet's name?"
            ], key="reg_sq")
        with sa_col:
            sa = st.text_input("Secret Answer", type="password", placeholder="Your answer", key="reg_sa")

        # ── VALIDATION ────────────────────────────────────────────────────
        can_reg = False
        if fn and em and mb and sa and agree and reg_ps and conf_ps and reg_pin and conf_pin:
            from user_utils import check_user_exists
            exists, msg = check_user_exists(em, fn, mb)
            if exists:
                validation_box.error(f"⛔ {msg}")
            elif reg_ps != conf_ps:
                validation_box.error("⛔ Passwords do not match.")
            elif not reg_pin.isdigit() or len(reg_pin) != 4:
                validation_box.error("⛔ PIN must be exactly 4 numeric digits.")
            elif reg_pin != conf_pin:
                validation_box.error("⛔ PINs do not match.")
            else:
                validation_box.success("✓ Identity, credentials & PIN validated.")
                can_reg = True

        if st.button("🚀 Initialize Biometric Scanner", disabled=not can_reg,
                     key="reg_init_btn", use_container_width=True):
            with st.status("Registering...") as status:
                # Pass PIN to register_user
                register_user(fn, em, mb, nc, bn, {sq: sa}, reg_ps, reg_pin)
                train_model()
                status.update(label="Enrollment Successful!", state="complete")
            st.success("Registration Complete! Please Login to continue.")

        if st.button("← Back to About", key="back_reg", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# LOGGED-IN CONTENT
# ══════════════════════════════════════════════════════════════════════════════
else:
    # ─── ADMIN VIEW ───────────────────────────────────────────────────────
    if st.session_state.user_folder == "ADMIN":
        users        = get_all_users()
        total_balance = 0
        compliant_count = 0
        total_users   = len(users)
        all_user_data = []

        for u in users:
            data = get_user_data(u)
            if data:
                bal = data.get("balance", 0)
                total_balance   += bal
                if bal >= 5000:
                    compliant_count += 1
                all_user_data.append(data)

        compliance_rate = (compliant_count / total_users * 100) if total_users > 0 else 0

        st.markdown("## 🛠️ Admin Command Center")
        st.info("System Management Mode | Global Infrastructure Oversight")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Liquidity",    f"₹{total_balance:,}")
        m2.metric("Compliance Rate",    f"{compliance_rate:.1f}%")
        m3.metric("Registered Nodes",   total_users)
        m4.metric("System Status",      "Stable")

        st.divider()

        col_header, col_bulk = st.columns([2, 1])
        with col_header:
            st.markdown("### 👤 User Directory")
        with col_bulk:
            # ─── UPDATED ADMIN WARNING UI ──────────────────────────────────────────
            if st.button("📢 Bulk Warning (Non-Compliant)", type="primary", use_container_width=True):
                warn_count = 0
                for u_data in all_user_data:
                    if u_data.get("balance", 0) < 5000:
                        u_email = u_data.get("email")
                        u_name  = u_data.get("full_name")
                        subj    = "🚨 ACTION REQUIRED: BioPay Account Compliance"
                        
                        # Professional HTML Email Template
                        html_warning = f"""
                        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 30px; background-color: #f8fafc; border-radius: 12px; max-width: 550px; margin: auto; border: 1px solid #e2e8f0;">
                            <div style="text-align: center; margin-bottom: 20px;">
                                <h1 style="color: #1e293b; font-size: 24px; margin: 0;">BioPay Security</h1>
                                <p style="color: #64748b; font-size: 14px;">Official System Notice</p>
                            </div>
                            <div style="background-color: #ffffff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                                <p style="color: #475569;">Hi <strong>{u_name}</strong>,</p>
                                <p style="color: #475569; line-height: 1.6;">Our automated compliance system has flagged your account for being below the <strong>₹5,000 minimum liquidity threshold</strong>.</p>
                                
                                <div style="background-color: #fff1f2; border: 1px solid #fecdd3; border-left: 5px solid #e11d48; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #9f1239; font-weight: 600;">⚠️ Urgent Action Needed</p>
                                    <p style="margin: 5px 0 0 0; color: #be123c; font-size: 14px;">Please credit your account to avoid temporary service suspension.</p>
                                </div>
                                
                                <p style="color: #475569; font-size: 14px; line-height: 1.6;">To maintain the integrity of our biometric financial network, all nodes must meet minimum requirements.</p>
                            </div>
                            <p style="text-align: center; color: #94a3b8; font-size: 12px; margin-top: 25px;">
                                © 2026 BioPay Infrastructure Group <br>
                                This is an automated security message.
                            </p>
                        </div>
                        """
                        if send_transaction_mail(u_email, subj, html_warning):
                            warn_count += 1
                st.toast(f"Broadcasted to {warn_count} users.", icon="🚀")

        search_query = st.text_input("🔍 Search users...", placeholder="Name or email")

        for u_data in all_user_data:
            u_email = u_data.get("email")
            u_name  = u_data.get("full_name")
            u_id    = u_data.get("unique_id")
            u_bal   = u_data.get("balance", 0)
            u_fail  = u_data.get("failed_attempts", 0)

            if search_query.lower() not in u_name.lower() and search_query.lower() not in u_email.lower():
                continue

            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([2.5, 1, 1, 1])
                with c1:
                    st.markdown(f"**{u_name}**")
                    st.caption(f"ID: `{u_id}` | {u_email}")
                with c2:
                    color = "#48bb78" if u_bal >= 5000 else "#fc8181"
                    st.markdown(f"<p style='color:#7b8494;font-size:0.75rem;margin-bottom:0;'>BALANCE</p><h4 style='color:{color};margin-top:0;'>₹{u_bal:,}</h4>", unsafe_allow_html=True)
                with c3:
                    fa_color = "#fc8181" if u_fail >= 3 else ("#f6ad55" if u_fail >= 1 else "#48bb78")
                    st.markdown(f"<p style='color:#7b8494;font-size:0.75rem;margin-bottom:0;'>FAILED ATTEMPTS</p><h4 style='color:{fa_color};margin-top:0;'>{u_fail}</h4>", unsafe_allow_html=True)
                with c4:
                    with c4:
                        st.write("<div style='height:15px'></div>", unsafe_allow_html=True)
                        if st.button("⚠️ Warn", key=f"warn_btn_{u_id}", use_container_width=True):
                            subj = "🚨 ACTION REQUIRED: BioPay Account Compliance"
                            
                            # Matching the high-end Professional UI
                            html_warning = f"""
                            <div style="font-family: 'Segoe UI', sans-serif; padding: 25px; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; max-width: 500px;">
                                <div style="border-bottom: 2px solid #e11d48; padding-bottom: 10px; margin-bottom: 15px;">
                                    <h2 style="color: #1e293b; margin: 0; font-size: 20px;">BioPay Compliance Alert</h2>
                                </div>
                                <p style="color: #475569;">Dear <strong>{u_name}</strong>,</p>
                                <p style="color: #475569; line-height: 1.5;">This is a formal notice regarding your account <code>{u_id}</code>.</p>
                                
                                <div style="background-color: #fff1f2; padding: 15px; border-radius: 8px; margin: 15px 0; border: 1px solid #fecdd3;">
                                    <p style="margin: 0; color: #9f1239; font-size: 14px;">
                                        <strong>Status:</strong> Non-Compliant<br>
                                        <strong>Requirement:</strong> Minimum Balance of ₹5,000.00
                                    </p>
                                </div>
                                
                                <p style="color: #64748b; font-size: 13px;">Please update your liquidity to maintain active status on the network.</p>
                                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin-top: 20px;">
                                <p style="text-align: center; color: #94a3b8; font-size: 11px;">BioPay Infrastructure • Automated Security Dispatch</p>
                            </div>
                            """
                            
                            if send_transaction_mail(u_email, subj, html_warning):
                                st.success(f"Professional warning sent to {u_name}")

    # ─── MEMBER VIEW ──────────────────────────────────────────────────────
    else:
        tab_home, tab_pay, tab_list = st.tabs(["🏠 Home", "💸 Payment", "📂 People"])
        st.divider()

        # ═══ HOME TAB ════════════════════════════════════════════════════
        with tab_home:
            user_folder = st.session_state.user_folder
            u_data      = get_user_data(user_folder)

            if u_data:
                st.markdown(f"### Welcome back, {u_data.get('full_name', 'User')}!")

                h_col1, h_col2, h_col3 = st.columns(3)

                with h_col1:
                    st.markdown('<div class="action-card"><div class="action-card-title">👛 My Wallet</div>', unsafe_allow_html=True)
                    st.metric("Available Balance", f"₹ {u_data.get('balance', 0)}")
                    st.caption("Last updated: Real-time")
                    st.markdown('</div>', unsafe_allow_html=True)

                with h_col2:
                    st.markdown('<div class="action-card"><div class="action-card-title">🆔 My Bio-ID</div>', unsafe_allow_html=True)
                    st.code(u_data.get("unique_id", "Not Assigned"), language=None)
                    st.caption("Use this ID for manual transfers")
                    st.markdown('</div>', unsafe_allow_html=True)

                with h_col3:
                    st.markdown('<div class="action-card"><div class="action-card-title">📱 Receive Money</div>', unsafe_allow_html=True)
                    qr_path = f"dataset/{user_folder}/qr_code.png"
                    if os.path.exists(qr_path):
                        st.image(qr_path, width=120)
                    else:
                        st.warning("QR Code not found.")
                    st.markdown('</div>', unsafe_allow_html=True)

                st.divider()

                # PIN status badge
                if has_pin_registered(user_folder):
                    st.markdown("""
                    <div style="display:inline-flex;align-items:center;gap:8px;
                                background:rgba(72,187,120,0.08);border:1px solid rgba(72,187,120,0.25);
                                border-radius:8px;padding:6px 14px;font-size:0.82rem;color:#48bb78;margin-bottom:1rem;">
                        🔐 Transaction PIN registered — high-risk protection active
                    </div>""", unsafe_allow_html=True)
                else:
                    st.warning("⚠️ No transaction PIN found. Re-register to enable high-risk PIN protection.")

                st.markdown("#### Quick Payment Tools")
                q_col1, q_col2 = st.columns(2)

                with q_col1:
                    st.markdown('<div class="action-card"><div class="action-card-title">📷 QR Scanner</div>', unsafe_allow_html=True)
                    if st.button("🚀 Open Camera Scanner", key="home_qr_scan"):
                        scanned = scan_biopay_qr()
                        if scanned:
                            st.session_state.qr_scanned_id = scanned
                            st.session_state.payment_step  = "confirm"
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                with q_col2:
                    st.markdown('<div class="action-card"><div class="action-card-title">⌨️ Manual Entry</div>', unsafe_allow_html=True)
                    m_id = st.text_input("Enter Receiver Bio-ID", key="home_manual_id",
                                         label_visibility="collapsed", placeholder="Enter Receiver's Bio-ID")
                    if st.button("Set Receiver", key="home_save_id"):
                        if m_id:
                            st.session_state.qr_scanned_id = m_id
                            st.success(f"Receiver set to: {m_id}")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Error loading user profile. Please log in again.")

        # ═══ PAYMENT TAB ═════════════════════════════════════════════════
        with tab_pay:
            sender_folder = st.session_state.user_folder
            u_info        = get_user_data(sender_folder)
            sender_bio_id = u_info.get("unique_id", "Not Assigned")

            # ── STAGE 1: INPUT ────────────────────────────────────────────
            if st.session_state.payment_step == "input":
                st.markdown("### Secure Payment Terminal")
                st.markdown(f"**Authenticated Sender**")
                st.markdown(f'<div class="bio-id-badge">🆔 {sender_bio_id}</div>', unsafe_allow_html=True)
                st.write("")

                col_scan, col_manual = st.columns(2)
                with col_scan:
                    st.markdown('<div class="action-card"><div class="action-card-title">📷 Scan Receiver QR</div>', unsafe_allow_html=True)
                    if st.button("Open QR Camera", key="qr_pay"):
                        rid = scan_biopay_qr()
                        if rid:
                            st.session_state.qr_scanned_id = rid
                            st.session_state.payment_step  = "confirm"
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_manual:
                    st.markdown('<div class="action-card"><div class="action-card-title">⌨️ Enter Receiver Bio-ID</div>', unsafe_allow_html=True)
                    rid_input = st.text_input("Receiver Bio-ID", value=st.session_state.qr_scanned_id,
                                              label_visibility="collapsed", placeholder="Receiver's Bio-ID")
                    if st.button("Proceed to Confirm", key="proceed_pay"):
                        if rid_input:
                            st.session_state.qr_scanned_id = rid_input
                            st.session_state.payment_step  = "confirm"
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

            # ── STAGE 2: CONFIRM, RISK SCORE & AUTH ──────────────────────
            elif st.session_state.payment_step == "confirm":
                st.markdown("### Transaction Authorization")
                current_bal = u_info.get("balance", 0)

                col_info, col_bal = st.columns([3, 1])
                with col_info:
                    st.markdown(f"""
                    <div style="background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:1rem;">
                        <div class="tx-label">From</div>
                        <div class="tx-value">{sender_bio_id}</div>
                        <div class="tx-label">To</div>
                        <div class="tx-value">{st.session_state.qr_scanned_id}</div>
                    </div>""", unsafe_allow_html=True)
                with col_bal:
                    st.metric("Available", f"₹{current_bal}")

                with st.container(border=True):
                    amount = st.number_input("Transfer Amount (₹)", min_value=1, value=100)

                # ── LIVE RISK PREVIEW ─────────────────────────────────────
                if amount > 0:
                    risk = calculate_risk_score(sender_folder, amount)
                    st.session_state.risk_result = risk
                    render_risk_panel(risk)

                    if risk["blocked"]:
                        st.error("🚫 Transaction blocked by risk engine. Contact support if you believe this is a mistake.")
                        if st.button("← Go Back"):
                            st.session_state.payment_step = "input"
                            st.rerun()
                        st.stop()

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("#### 🔐 Security Checks")

                risk = st.session_state.risk_result or {}
                pin_label = " + PIN Verification" if risk.get("requires_pin") else ""
                st.markdown(f"""
                <div class="step-row"><div class="step-num">1</div>Biometric face authentication</div>
                <div class="step-row"><div class="step-num">2</div>Randomized gaze liveness challenge</div>
                <div class="step-row"><div class="step-num">3</div>ML anomaly & risk scoring{pin_label}</div>
                """, unsafe_allow_html=True)
                st.write("")

                # ── PIN GATE (shown only when risk requires it) ───────────
                if risk.get("requires_pin") and not st.session_state.pin_verified:
                    st.markdown("""
                    <div class="pin-gate-card">
                        <div class="pin-gate-icon">🔐</div>
                        <div class="pin-gate-title">PIN Verification Required</div>
                        <div class="pin-gate-sub">
                            This transaction was flagged as high-risk.<br>
                            Enter your 4-digit security PIN to proceed.
                        </div>
                    </div>""", unsafe_allow_html=True)

                    pin_input = st.text_input("Enter your 4-digit PIN",
                                              type="password", max_chars=4,
                                              placeholder="••••", key="pay_pin_input")
                    if st.button("✅ Verify PIN", key="verify_pin_btn"):
                        if verify_user_pin(sender_folder, pin_input):
                            st.session_state.pin_verified = True
                            st.success("✅ PIN Verified — proceed to biometric check")
                            st.rerun()
                        else:
                            update_failed_attempts(sender_folder, False)
                            st.error("❌ Incorrect PIN. Attempt logged.")
                    st.stop()   # Don't render the auth button until PIN clears

                # ── MAIN AUTH BUTTON ──────────────────────────────────────
                if st.button("⚡ Verify Identity & Authorize",
                             disabled=(amount > current_bal)):
                    pay_flash = st.empty()
                    pay_flash.markdown("""
                        <div style="position:fixed;top:0;left:0;width:100vw;height:100vh;
                                    background:#fff;z-index:9999;display:flex;
                                    justify-content:center;align-items:center;">
                            <h2 style="color:black;font-family:sans-serif;">🔒 SECURE SCANNING...</h2>
                        </div>""", unsafe_allow_html=True)

                    auth_status, confidence_score = authenticate(sender_folder)
                    pay_flash.empty()

                    proceed_tx = False

                    if auth_status:
                        st.success("✅ Identity Confirmed")
                        if challenge_response_auth():
                            st.success("✅ Liveness Verified")
                            proceed_tx = True
                        else:
                            st.error("❌ Liveness Check Failed")
                            update_failed_attempts(sender_folder, False)

                    elif 50 <= confidence_score <= 85:
                        st.warning(f"⚠️ Poor lighting ({int(confidence_score)}%). Knowledge verification required.")
                        sq_dict = u_info.get("security_questions", {})
                        if sq_dict:
                            question    = list(sq_dict.keys())[0]
                            correct_ans = sq_dict[question]
                            ans_input   = st.text_input(f"Question: {question}", type="password", key="pay_mfa")
                            if st.button("Authorize with Secret Answer"):
                                if ans_input.strip().lower() == correct_ans.strip().lower():
                                    st.success("✅ Knowledge Verified")
                                    proceed_tx = True
                                else:
                                    st.error("❌ Incorrect Answer")
                                    update_failed_attempts(sender_folder, False)
                    else:
                        st.error("❌ Biometric Mismatch")
                        update_failed_attempts(sender_folder, False)

                    if proceed_tx:
                        with st.spinner("Processing Secure Ledger Update..."):
                            if update_transaction(sender_folder, amount, st.session_state.qr_scanned_id):
                                updated_info = get_user_data(sender_folder)
                                real_hash    = updated_info["transactions"][-1]["hash"]

                                st.session_state.last_tx_details = {
                                    "sender":    sender_bio_id,
                                    "receiver":  st.session_state.qr_scanned_id,
                                    "amount":    amount,
                                    "hash":      real_hash,
                                    "risk_score": risk.get("score", 0),
                                    "risk_level": risk.get("level", "—"),
                                }
                                st.session_state.payment_step = "success"
                                st.session_state.pin_verified = False   # reset for next tx
                                st.rerun()

            # ── STAGE 3: SUCCESS ──────────────────────────────────────────
            elif st.session_state.payment_step == "success":
                tx = st.session_state.last_tx_details

                st.markdown("""
                <div style="text-align:center;padding:2.5rem 1rem 1.5rem;">
                    <div class="checkmark-circle" style="margin:0 auto 1.5rem;">
                        <div class="background"></div>
                        <div class="checkmark draw"></div>
                    </div>
                    <h2 style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
                               color:#48bb78;letter-spacing:-0.03em;margin-bottom:0.4rem;">
                        Transaction Successful
                    </h2>
                    <p style="color:#7b8494;font-size:0.88rem;">Funds transferred securely via BioPay</p>
                </div>""", unsafe_allow_html=True)

                risk_color = _risk_color(tx.get("risk_level", "Low"))
                st.markdown(f"""
                <div class="success-card">
                    <div class="tx-label">From Sender ID</div>
                    <div class="tx-value">{tx['sender']}</div>
                    <div class="tx-label">To Receiver ID</div>
                    <div class="tx-value">{tx['receiver']}</div>
                    <div class="tx-label">Amount Transferred</div>
                    <div class="tx-amount">₹ {tx['amount']}</div>
                    <div class="tx-label">Risk Score at Authorization</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                                color:{risk_color};margin-bottom:12px;">
                        {tx.get('risk_score', '—')} / 100 &nbsp;·&nbsp; {tx.get('risk_level', '—')} Risk
                    </div>
                </div>""", unsafe_allow_html=True)

                st.info("📧 Debit/Credit notifications dispatched to registered email addresses.")
                st.write("")

                if st.button("← Return to Dashboard"):
                    st.session_state.payment_step  = "input"
                    st.session_state.qr_scanned_id = ""
                    st.session_state.risk_result   = None
                    st.rerun()

        # ═══ PEOPLE TAB ══════════════════════════════════════════════════
        with tab_list:
            st.markdown("### 📱 Quick Pay")
            st.caption("Select a verified contact to initiate a secure biometric transfer.")

            users = get_all_users()
            if not users:
                st.info("No active biometric profiles found.")
            else:
                for u in users:
                    u_info_c = get_user_data(u)
                    if not u_info_c or u == st.session_state.user_folder:
                        continue

                    with st.container():
                        col_img, col_info, col_btn = st.columns([1, 4, 2])
                        with col_img:
                            initial = u_info_c.get("full_name", "U")[0]
                            st.markdown(f"""
                                <div style="background:linear-gradient(135deg,#63b3ed,#4fd1c5);
                                            width:50px;height:50px;border-radius:50%;
                                            display:flex;align-items:center;justify-content:center;
                                            color:#07080d;font-weight:bold;font-size:1.2rem;">
                                    {initial}
                                </div>""", unsafe_allow_html=True)
                        with col_info:
                            st.markdown(f"**{u_info_c.get('full_name')}**")
                            st.markdown(f"<code style='color:#63b3ed;font-size:0.8rem;'>{u_info_c.get('unique_id')}</code>", unsafe_allow_html=True)
                        with col_btn:
                            if st.button("💸 PAY", key=f"pay_btn_{u}"):
                                st.session_state.qr_scanned_id = u_info_c.get("unique_id")
                                st.session_state.payment_step  = "confirm"
                                st.session_state.pin_verified  = False
                                st.rerun()

                        st.markdown("<hr style='margin:12px 0;border-top:1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)