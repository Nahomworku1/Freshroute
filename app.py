import streamlit as st
import requests
import time
from datetime import datetime
import folium
from streamlit_folium import st_folium

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="FreshRoute — AI Post-Harvest Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "language" not in st.session_state:
    st.session_state.language = "English"

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

dark = st.session_state.dark_mode

# ═══════════════════════════════════════════════════════════════
# THEME TOKENS
# ═══════════════════════════════════════════════════════════════

if dark:
    BG = "#0F0F0A"; SURFACE = "#1A1A0F"; SURFACE2 = "#0F0F0A"
    TEXT = "#F5F0E8"; MUTED = "#8A8A6A"; LINE = "rgba(255,255,255,0.07)"
    LINE2 = "rgba(255,255,255,0.04)"; INPUT_BG = "#1A1A0F"
    METRIC_BG = "#1A1A0F"; CARD_BORDER = "rgba(255,255,255,0.07)"
    CHART_GRID = "rgba(255,255,255,0.05)"
else:
    BG = "#F8F6EE"; SURFACE = "#FFFFFF"; SURFACE2 = "#F0EDE0"
    TEXT = "#0F0F0A"; MUTED = "#7A7A5A"; LINE = "rgba(0,0,0,0.08)"
    LINE2 = "rgba(0,0,0,0.04)"; INPUT_BG = "#FFFFFF"
    METRIC_BG = "#FFFFFF"; CARD_BORDER = "rgba(0,0,0,0.08)"
    CHART_GRID = "rgba(0,0,0,0.05)"

FRESH = "#4BBF7A"; DANGER = "#D64936"; WARN = "#E07B2A"
BLUE = "#6BACDE"; GOLD = "#E8A84C"; PURPLE = "#9B7EE8"

# ═══════════════════════════════════════════════════════════════
# TRANSLATIONS
# ═══════════════════════════════════════════════════════════════

TRANSLATIONS = {
    "English": {
        "tagline": "AI Post-Harvest Intelligence · Global South",
        "live_weather": "Live weather data",
        "demo_mode": "Demo mode — add API key for live data",
        "live_rates": "Live FX rates",
        "estimated_rates": "Estimated FX rates",
        "updated": "Updated",
        "tab_dashboard": "📊 Intelligence Dashboard",
        "tab_business": "💰 Business Model",
        "tab_map": "🗺️ Route Map",
        "situation": "Real-time situation",
        "farmer": "Farmer",
        "hours_spoilage": "Hours until spoilage",
        "hrs_remaining": "hrs remaining",
        "temperature": "Temperature (live)",
        "humidity": "Humidity (live)",
        "accel_rot": "⚠ Accelerates rot",
        "acceptable": "Acceptable",
        "predicted_waste": "Predicted waste",
        "without_action": "without action",
        "value_at_risk": "Value at risk",
        "lost_no_action": "lost if no action taken",
        "spoilage_analysis": "Spoilage risk analysis",
        "ai_buyer": "AI buyer matching",
        "best_match": "Best match",
        "cold_storage": "Cold storage",
        "revenue_today": "Revenue if sold today",
        "vs_nothing": "vs. doing nothing",
        "fr_fee": "FreshRoute fee (1.5%)",
        "simulator_title": "Intervention simulator — change one variable, see the outcome",
        "waste": "Predicted waste",
        "harvest_lost": "of harvest lost",
        "farmer_earnings": "Farmer earnings",
        "vs_baseline": "vs. baseline",
        "heat_stress": "Heat stress",
        "moisture": "Moisture damage",
        "confidence": "Model confidence",
        "storage_status": "Storage status",
        "active": "Active ❄️",
        "none_storage": "None ⚠️",
        "shelf_ext": "Shelf life ×2.2",
        "open_air": "Open air — risk elevated",
        "low": "Low", "moderate": "Moderate", "high": "High", "critical": "Critical",
        "scenario_base": "No action (baseline)",
        "scenario_cold": "Add cold storage",
        "scenario_route": "Fix road route",
        "scenario_buyer": "Direct buyer link",
        "route_title": "Live route intelligence — buyer locations & road conditions",
        "nearest_buyers": "Nearest buyers",
        "route_intel": "Route intelligence",
        "biz_title": "Business model — FreshRoute revenue",
        "live_currency": "Live currency rates",
        "unit_econ": "Unit economics — per transaction",
        "avg_trans": "Avg transaction value",
        "fr_fee_label": "FreshRoute fee (1.5%)",
        "ai_cost": "Cost per AI response",
        "gross_margin": "Gross margin per match",
        "revenue_proj": "Revenue projections — 3 scenarios",
        "conservative": "Conservative",
        "moderate_biz": "Moderate",
        "scale": "Scale",
        "matches_month": "matches/month",
        "revenue_streams": "3 revenue streams over time",
        "market_opp": "Market opportunity",
        "run_analysis": "▶  Run Analysis",
        "auto_refresh": "⟳ Auto-refresh every 5 min",
        "location": "📍 Location",
        "crop": "🌱 Crop",
        "quantity": "⚖️ Quantity (kg)",
        "days_harvest": "📅 Days since harvest",
        "has_storage": "❄️ Has cold storage",
        "api_config": "API Configuration",
        "country": "🌍 Country",
        "language": "🌐 Language",
        "light_mode": "☀️ Light",
        "dark_mode": "🌙 Dark",
        "built_for": "Built for",
        "fao_stat": "post-harvest loss (FAO)",
        "farmers_global": "smallholder farmers globally",
        "fee_note": "fee on successful matches only",
        "narrative_base": "This is the baseline reality — <strong>{waste}% of the harvest lost</strong> before reaching a buyer. Not from drought. Not from conflict. From a lack of real-time market intelligence.",
        "narrative_cold": "Cold storage extends shelf life and eliminates pressure to sell cheap. Farmer can now negotiate with premium buyers. <strong>Waste drops by up to 36 percentage points.</strong>",
        "narrative_route": "Faster transit means less bruising and spoilage on arrival. Buyers pay full price for quality produce. <strong>Simple routing intelligence — real income difference.</strong>",
        "narrative_buyer": "Direct connection to highest-paying buyer eliminates the middleman discount. <strong>Maximum achievable outcome with current infrastructure.</strong>",
        "severe": "Severe", "high_label": "High", "moderate_label": "Moderate",
        "stream1_title": "Now — Transaction fees",
        "stream1_desc": "1.5% per successful match. Only charged when farmer sells. Zero risk to farmer.",
        "stream1_status": "Available today",
        "stream2_title": "Month 6 — Buyer subscriptions",
        "stream2_desc": "Cooperatives pay monthly for reliable supplier access and crop forecasts.",
        "stream2_status": "Pipeline",
        "stream3_title": "Year 2 — Data insights",
        "stream3_desc": "Governments and NGOs pay for anonymised crop flow intelligence — harvest volumes, price trends, loss rates.",
        "stream3_status": "Roadmap",
        "farmers_global_stat": "Smallholder farmers globally",
        "primary_target": "primary target",
        "ph_loss": "Post-harvest loss (FAO)",
        "ssa_food": "of food in Sub-Saharan Africa",
        "annual_loss": "Annual loss value",
        "world_bank": "to African farmers (World Bank)",
        "market_pen": "0.1% market penetration",
        "rev_opp": "annual revenue opportunity",
    },
    "Amharic (አማርኛ)": {
        "tagline": "AI የምርት ብልሹነት ስርዓት · Global South",
        "live_weather": "ቀጥታ የአየር ሁኔታ",
        "demo_mode": "ዴሞ ሁኔታ — API ቁልፍ ያስፈልጋል",
        "live_rates": "ቀጥታ የምንዛሬ ተመን",
        "estimated_rates": "የተቀመጠ ምንዛሬ",
        "updated": "ተዘምኗል",
        "tab_dashboard": "📊 የስለላ ሰሌዳ",
        "tab_business": "💰 የንግድ ሞዴል",
        "tab_map": "🗺️ የመንገድ ካርታ",
        "situation": "ቀጥታ ሁኔታ",
        "farmer": "አርሶ አደር",
        "hours_spoilage": "እስከ ብልሹነት ሰዓታት",
        "hrs_remaining": "ሰዓት ቀርቷል",
        "temperature": "ሙቀት (ቀጥታ)",
        "humidity": "እርጥበት (ቀጥታ)",
        "accel_rot": "⚠ ብልሹነትን ያፋጥናል",
        "acceptable": "ተቀባይነት ያለው",
        "predicted_waste": "የሚበሰብሰው ምርት",
        "without_action": "እርምጃ ካልተወሰደ",
        "value_at_risk": "አደጋ ላይ ያለ ገቢ",
        "lost_no_action": "እርምጃ ካልተወሰደ ይጠፋል",
        "spoilage_analysis": "የብልሹነት ስጋት ትንተና",
        "ai_buyer": "AI ገዥ ማዛመጃ",
        "best_match": "ምርጥ ገዥ",
        "cold_storage": "ቀዝቃዛ ቤት",
        "revenue_today": "ዛሬ ቢሸጥ ገቢ",
        "vs_nothing": "ምንም ካለማድረግ",
        "fr_fee": "FreshRoute ክፍያ (1.5%)",
        "simulator_title": "የእርምጃ ስሌት — አንድ ነገር ቀይሩ፣ ውጤቱን ይመልከቱ",
        "waste": "የሚበሰብሰው ምርት",
        "harvest_lost": "ከምርቱ ይጠፋል",
        "farmer_earnings": "የአርሶ አደሩ ገቢ",
        "vs_baseline": "ከመሠረቱ",
        "heat_stress": "ሙቀት ጉዳት",
        "moisture": "እርጥበት ጉዳት",
        "confidence": "የሞዴል እምነት",
        "storage_status": "ማከማቻ ሁኔታ",
        "active": "ቀዝቃዛ ቤት ❄️",
        "none_storage": "ምንም ⚠️",
        "shelf_ext": "ዕድሜ ×2.2 ይጨምራል",
        "open_air": "ክፍት አየር — ስጋት ከፍተኛ",
        "low": "ዝቅተኛ", "moderate": "መካከለኛ", "high": "ከፍተኛ", "critical": "አደጋ",
        "scenario_base": "ምንም እርምጃ (መሠረት)",
        "scenario_cold": "ቀዝቃዛ ቤት ይጨምሩ",
        "scenario_route": "መንገድ ቀይሩ",
        "scenario_buyer": "ቀጥታ ወደ ገዥ",
        "route_title": "ቀጥታ ካርታ — የገዥ ቦታዎች እና የመንገድ ሁኔታ",
        "nearest_buyers": "ቅርብ ገዥዎች",
        "route_intel": "የካርታ ትንተና",
        "biz_title": "የንግድ ሞዴል — FreshRoute ገቢ",
        "live_currency": "ቀጥታ የምንዛሬ ተመን",
        "unit_econ": "የአንድ ግብይት ኢኮኖሚክስ",
        "avg_trans": "አማካይ የግብይት ዋጋ",
        "fr_fee_label": "FreshRoute ክፍያ (1.5%)",
        "ai_cost": "የAI ምላሽ ዋጋ",
        "gross_margin": "ከፍተኛ ትርፍ",
        "revenue_proj": "የገቢ ትንበያ — 3 ሁኔታዎች",
        "conservative": "ዝቅተኛ",
        "moderate_biz": "መካከለኛ",
        "scale": "ትልቅ",
        "matches_month": "ግብይቶች/ወር",
        "revenue_streams": "3 የገቢ ምንጮች",
        "market_opp": "የገበያ እድል",
        "run_analysis": "▶  ትንተና ጀምር",
        "auto_refresh": "⟳ ራስ-ሰር ማደስ",
        "location": "📍 ቦታ",
        "crop": "🌱 ሰብል",
        "quantity": "⚖️ መጠን (ኪሎ)",
        "days_harvest": "📅 ከተሰበሰበ ቀናት",
        "has_storage": "❄️ ቀዝቃዛ ቤት አለ",
        "api_config": "API ውቅር",
        "country": "🌍 አገር",
        "language": "🌐 ቋንቋ",
        "light_mode": "☀️ ቀለል",
        "dark_mode": "🌙 ጨለማ",
        "built_for": "ለ",
        "fao_stat": "ከምርት ብልሹነት (FAO)",
        "farmers_global": "ዓለም አቀፍ አርሶ አደሮች",
        "fee_note": "ክፍያ ሲሳካ ብቻ",
        "narrative_base": "ይህ ያለ እርምጃ ያለው ሁኔታ ነው — <strong>{waste}% ከምርቱ ይጠፋል</strong>። ከሰለፍ አይደለም። ከጦርነት አይደለም። ከወቅታዊ መረጃ እጥረት ነው።",
        "narrative_cold": "ቀዝቃዛ ቤት ዕድሜ ያራዝማል። አርሶ አደሩ አሁን ለደንበኛ ዋጋ ለመደራደር ጊዜ አለው። <strong>ብልሹነት እስከ 36% ሊቀንስ ይችላል።</strong>",
        "narrative_route": "ፈጣን መንገድ ምርቱን ጠብቋል። <strong>ቀላል የመንገድ ምርጫ — ትልቅ የገቢ ልዩነት።</strong>",
        "narrative_buyer": "ቀጥታ ከፍተኛ ዋጋ ሻጭ ጋር። <strong>ከፍተኛ ሊሆን የሚችለው ውጤት።</strong>",
        "severe": "ከፍተኛ ሙቀት", "high_label": "ሙቀት", "moderate_label": "መካከለኛ",
        "stream1_title": "አሁን — የግብይት ክፍያ",
        "stream1_desc": "1.5% ሲሳካ ብቻ። አርሶ አደሩ ሲሸጥ ብቻ ይከፈላል።",
        "stream1_status": "ዛሬ ይሰራል",
        "stream2_title": "ወር 6 — የገዥ ደንበኝነት",
        "stream2_desc": "ህብረት ሥራዎች ወርሃዊ ይከፍላሉ።",
        "stream2_status": "ቀጣይ",
        "stream3_title": "ዓመት 2 — የመረጃ ግብይቶች",
        "stream3_desc": "መንግስታት የሰብል ፍሰት ዳታ ይከፍላሉ።",
        "stream3_status": "ዕቅድ",
        "farmers_global_stat": "ዓለም አቀፍ አርሶ አደሮች",
        "primary_target": "ዋና ኢላማ",
        "ph_loss": "ከምርት ብልሹነት (FAO)",
        "ssa_food": "ከምግብ ምርት",
        "annual_loss": "ዓመታዊ ኪሳራ",
        "world_bank": "ለአፍሪካ አርሶ አደሮች",
        "market_pen": "0.1% የገበያ ድርሻ",
        "rev_opp": "ዓመታዊ የገቢ እድል",
    },
    "Français": {
        "tagline": "Intelligence AI Post-Récolte · Sud Global",
        "live_weather": "Météo en direct",
        "demo_mode": "Mode démo — ajoutez une clé API",
        "live_rates": "Taux de change en direct",
        "estimated_rates": "Taux estimés",
        "updated": "Mis à jour",
        "tab_dashboard": "📊 Tableau de bord",
        "tab_business": "💰 Modèle économique",
        "tab_map": "🗺️ Carte des routes",
        "situation": "Situation en temps réel",
        "farmer": "Agriculteur",
        "hours_spoilage": "Heures avant gaspillage",
        "hrs_remaining": "h restantes",
        "temperature": "Température (direct)",
        "humidity": "Humidité (direct)",
        "accel_rot": "⚠ Accélère la détérioration",
        "acceptable": "Acceptable",
        "predicted_waste": "Gaspillage prévu",
        "without_action": "sans action",
        "value_at_risk": "Valeur à risque",
        "lost_no_action": "perdue sans action",
        "spoilage_analysis": "Analyse du risque de détérioration",
        "ai_buyer": "Mise en relation IA acheteur",
        "best_match": "Meilleur match",
        "cold_storage": "Chambre froide",
        "revenue_today": "Revenu si vendu aujourd'hui",
        "vs_nothing": "vs. ne rien faire",
        "fr_fee": "Frais FreshRoute (1.5%)",
        "simulator_title": "Simulateur d'intervention — changez une variable, voyez le résultat",
        "waste": "Gaspillage prévu",
        "harvest_lost": "de la récolte perdue",
        "farmer_earnings": "Revenus de l'agriculteur",
        "vs_baseline": "vs. référence",
        "heat_stress": "Stress thermique",
        "moisture": "Dommages humidité",
        "confidence": "Confiance du modèle",
        "storage_status": "État du stockage",
        "active": "Actif ❄️",
        "none_storage": "Aucun ⚠️",
        "shelf_ext": "Durée de vie ×2.2",
        "open_air": "Air libre — risque élevé",
        "low": "Faible", "moderate": "Modéré", "high": "Élevé", "critical": "Critique",
        "scenario_base": "Aucune action (référence)",
        "scenario_cold": "Ajouter chambre froide",
        "scenario_route": "Changer de route",
        "scenario_buyer": "Lien direct acheteur",
        "route_title": "Renseignements routes en direct",
        "nearest_buyers": "Acheteurs les plus proches",
        "route_intel": "Intelligence routière",
        "biz_title": "Modèle économique — revenus FreshRoute",
        "live_currency": "Taux de change en direct",
        "unit_econ": "Économie unitaire — par transaction",
        "avg_trans": "Valeur transaction moyenne",
        "fr_fee_label": "Frais FreshRoute (1.5%)",
        "ai_cost": "Coût par réponse IA",
        "gross_margin": "Marge brute par match",
        "revenue_proj": "Projections de revenus — 3 scénarios",
        "conservative": "Conservateur",
        "moderate_biz": "Modéré",
        "scale": "Grande échelle",
        "matches_month": "matches/mois",
        "revenue_streams": "3 sources de revenus",
        "market_opp": "Opportunité de marché",
        "run_analysis": "▶  Lancer l'analyse",
        "auto_refresh": "⟳ Actualisation auto 5 min",
        "location": "📍 Lieu",
        "crop": "🌱 Culture",
        "quantity": "⚖️ Quantité (kg)",
        "days_harvest": "📅 Jours depuis la récolte",
        "has_storage": "❄️ Stockage froid disponible",
        "api_config": "Configuration API",
        "country": "🌍 Pays",
        "language": "🌐 Langue",
        "light_mode": "☀️ Clair",
        "dark_mode": "🌙 Sombre",
        "built_for": "Construit pour",
        "fao_stat": "de pertes post-récolte (FAO)",
        "farmers_global": "agriculteurs dans le monde",
        "fee_note": "frais sur matches réussis uniquement",
        "narrative_base": "C'est la réalité de base — <strong>{waste}% de la récolte perdue</strong> avant d'atteindre un acheteur. Pas à cause de la sécheresse. Pas à cause d'un conflit. Par manque d'intelligence en temps réel.",
        "narrative_cold": "La chambre froide prolonge la durée de vie et élimine la pression de vendre à bas prix. <strong>Le gaspillage peut diminuer de 36 points de pourcentage.</strong>",
        "narrative_route": "Un transit plus rapide signifie moins de dommages et moins de gaspillage. <strong>Intelligence routière simple — vraie différence de revenus.</strong>",
        "narrative_buyer": "Connexion directe avec l'acheteur au meilleur prix. <strong>Résultat maximum réalisable avec l'infrastructure actuelle.</strong>",
        "severe": "Sévère", "high_label": "Élevé", "moderate_label": "Modéré",
        "stream1_title": "Maintenant — Frais de transaction",
        "stream1_desc": "1.5% par match réussi. Facturé uniquement quand l'agriculteur vend.",
        "stream1_status": "Disponible",
        "stream2_title": "Mois 6 — Abonnements acheteurs",
        "stream2_desc": "Les coopératives paient mensuellement pour l'accès aux fournisseurs.",
        "stream2_status": "Pipeline",
        "stream3_title": "An 2 — Données analytiques",
        "stream3_desc": "Gouvernements et ONG paient pour l'intelligence des flux agricoles.",
        "stream3_status": "Feuille de route",
        "farmers_global_stat": "Agriculteurs dans le monde",
        "primary_target": "cible principale",
        "ph_loss": "Pertes post-récolte (FAO)",
        "ssa_food": "de nourriture en Afrique subsaharienne",
        "annual_loss": "Valeur des pertes annuelles",
        "world_bank": "aux agriculteurs africains (Banque Mondiale)",
        "market_pen": "0.1% part de marché",
        "rev_opp": "opportunité de revenus annuels",
    },
    "Swahili": {
        "tagline": "Akili Bandia ya Baada ya Mavuno · Kusini Duniani",
        "live_weather": "Hali ya hewa ya moja kwa moja",
        "demo_mode": "Hali ya demo — ongeza ufunguo wa API",
        "live_rates": "Viwango vya fedha vya sasa",
        "estimated_rates": "Viwango vilivyokadiriwa",
        "updated": "Imesasishwa",
        "tab_dashboard": "📊 Dashibodi ya Ujuzi",
        "tab_business": "💰 Mfano wa Biashara",
        "tab_map": "🗺️ Ramani ya Barabara",
        "situation": "Hali ya wakati halisi",
        "farmer": "Mkulima",
        "hours_spoilage": "Masaa hadi kuharibika",
        "hrs_remaining": "masaa yaliyobaki",
        "temperature": "Joto (moja kwa moja)",
        "humidity": "Unyevu (moja kwa moja)",
        "accel_rot": "⚠ Inaharakisha kuoza",
        "acceptable": "Inakubalika",
        "predicted_waste": "Upotevu uliotabiriwa",
        "without_action": "bila hatua",
        "value_at_risk": "Thamani katika hatari",
        "lost_no_action": "itapotea bila hatua",
        "spoilage_analysis": "Uchambuzi wa hatari ya kuharibika",
        "ai_buyer": "Uoanishaji wa mnunuzi wa AI",
        "best_match": "Mechi bora",
        "cold_storage": "Ghala baridi",
        "revenue_today": "Mapato ikiuza leo",
        "vs_nothing": "dhidi ya kutotenda",
        "fr_fee": "Ada ya FreshRoute (1.5%)",
        "simulator_title": "Kisimulisha cha uingiliaji — badilisha kigezo kimoja, ona matokeo",
        "waste": "Upotevu uliotabiriwa",
        "harvest_lost": "ya mavuno imepotea",
        "farmer_earnings": "Mapato ya mkulima",
        "vs_baseline": "dhidi ya msingi",
        "heat_stress": "Mfadhaiko wa joto",
        "moisture": "Uharibifu wa unyevu",
        "confidence": "Imani ya mfano",
        "storage_status": "Hali ya uhifadhi",
        "active": "Inafanya kazi ❄️",
        "none_storage": "Hakuna ⚠️",
        "shelf_ext": "Maisha ya rafu ×2.2",
        "open_air": "Hewa wazi — hatari kubwa",
        "low": "Chini", "moderate": "Wastani", "high": "Juu", "critical": "Muhimu",
        "scenario_base": "Bila hatua (msingi)",
        "scenario_cold": "Ongeza ghala baridi",
        "scenario_route": "Rekebisha njia ya barabara",
        "scenario_buyer": "Unganisha moja kwa moja na mnunuzi",
        "route_title": "Ujuzi wa njia wa moja kwa moja",
        "nearest_buyers": "Wanunuzi wa karibu",
        "route_intel": "Ujuzi wa njia",
        "biz_title": "Mfano wa biashara — mapato ya FreshRoute",
        "live_currency": "Viwango vya fedha vya sasa",
        "unit_econ": "Uchumi wa kila muamala",
        "avg_trans": "Thamani ya wastani ya muamala",
        "fr_fee_label": "Ada ya FreshRoute (1.5%)",
        "ai_cost": "Gharama kwa kila jibu la AI",
        "gross_margin": "Faida kubwa kwa kila mechi",
        "revenue_proj": "Makadirio ya mapato — hali 3",
        "conservative": "Kihafidhina",
        "moderate_biz": "Wastani",
        "scale": "Kwa kiwango kikubwa",
        "matches_month": "mechi/mwezi",
        "revenue_streams": "Vyanzo 3 vya mapato",
        "market_opp": "Fursa ya soko",
        "run_analysis": "▶  Endesha Uchambuzi",
        "auto_refresh": "⟳ Sasisha kiotomatiki dakika 5",
        "location": "📍 Mahali",
        "crop": "🌱 Zao",
        "quantity": "⚖️ Kiasi (kg)",
        "days_harvest": "📅 Siku tangu kuvunwa",
        "has_storage": "❄️ Ana ghala baridi",
        "api_config": "Usanidi wa API",
        "country": "🌍 Nchi",
        "language": "🌐 Lugha",
        "light_mode": "☀️ Mwanga",
        "dark_mode": "🌙 Giza",
        "built_for": "Imejengwa kwa",
        "fao_stat": "ya upotevu baada ya mavuno (FAO)",
        "farmers_global": "wakulima duniani",
        "fee_note": "ada kwa mechi zilizofanikiwa tu",
        "narrative_base": "Hii ndiyo hali ya kawaida — <strong>{waste}% ya mavuno imepotea</strong> kabla ya kufikia mnunuzi. Si kwa ukame. Si kwa vita. Kwa ukosefu wa akili ya wakati halisi.",
        "narrative_cold": "Ghala baridi hurefusha maisha ya rafu. <strong>Upotevu unaweza kupungua kwa hadi asilimia 36.</strong>",
        "narrative_route": "Usafiri wa haraka hupunguza uharibifu. <strong>Ujuzi rahisi wa njia — tofauti ya kweli ya mapato.</strong>",
        "narrative_buyer": "Muunganiko wa moja kwa moja na mnunuzi anayetoa bei bora. <strong>Matokeo bora yanayoweza kufikiwa.</strong>",
        "severe": "Kali", "high_label": "Juu", "moderate_label": "Wastani",
        "stream1_title": "Sasa — Ada za muamala",
        "stream1_desc": "1.5% kwa kila mechi iliyofanikiwa. Inalipwa tu mkulima anapouza.",
        "stream1_status": "Inapatikana",
        "stream2_title": "Mwezi 6 — Usajili wa wanunuzi",
        "stream2_desc": "Vyama vya ushirika hulipa kila mwezi kwa ufikiaji wa wauzaji.",
        "stream2_status": "Mstari wa mbele",
        "stream3_title": "Mwaka 2 — Maarifa ya data",
        "stream3_desc": "Serikali na NGO hulipa kwa akili ya mtiririko wa mazao.",
        "stream3_status": "Ramani ya barabara",
        "farmers_global_stat": "Wakulima wadogo duniani",
        "primary_target": "lengo kuu",
        "ph_loss": "Upotevu baada ya mavuno (FAO)",
        "ssa_food": "ya chakula Afrika Kusini ya Sahara",
        "annual_loss": "Thamani ya hasara ya kila mwaka",
        "world_bank": "kwa wakulima wa Afrika (Benki ya Dunia)",
        "market_pen": "0.1% sehemu ya soko",
        "rev_opp": "fursa ya mapato ya kila mwaka",
    },
}

def T(key):
    lang = st.session_state.language
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, TRANSLATIONS["English"].get(key, key))

# ═══════════════════════════════════════════════════════════════
# COUNTRY DATABASE
# ═══════════════════════════════════════════════════════════════

COUNTRIES = {
    "🇪🇹 Ethiopia": {
        "flag":"🇪🇹","flag_colors":["#078930","#FCDD09","#DA121A"],
        "currency":"ETB","usd_rate":57.5,
        "cities":["Addis Ababa","Dire Dawa","Bahir Dar","Jimma","Mekelle","Hawassa"],
        "crops":["Tomatoes","Mangoes","Coffee cherries","Maize","Bananas","Leafy greens","Papaya","Sweet potato"],
        "farmer_name":"Abebe Girma",
        "weather_map":{"Addis Ababa":{"temp":22.0,"humidity":68,"description":"Partly cloudy"},"Dire Dawa":{"temp":36.0,"humidity":45,"description":"Hot and dry"},"Bahir Dar":{"temp":28.0,"humidity":74,"description":"Warm and humid"},"Jimma":{"temp":25.0,"humidity":80,"description":"Overcast"},"Mekelle":{"temp":24.0,"humidity":55,"description":"Clear skies"},"Hawassa":{"temp":26.0,"humidity":72,"description":"Light breeze"}},
        "city_coords":{"Addis Ababa":(9.032,38.747),"Dire Dawa":(9.601,41.866),"Bahir Dar":(11.593,37.389),"Jimma":(7.667,36.833),"Mekelle":(13.497,39.477),"Hawassa":(7.062,38.477)},
        "buyers":{"Tomatoes":[{"name":"Addis Ababa Produce Market","distance_km":28,"price_per_kg":18,"capacity_kg":500,"tag":"best","minutes":40},{"name":"Bishoftu Cold Hub","distance_km":45,"price_per_kg":14,"capacity_kg":1000,"tag":"cold","minutes":65},{"name":"Dire Dawa Wholesale","distance_km":445,"price_per_kg":22,"capacity_kg":2000,"tag":None,"minutes":360}],"Coffee cherries":[{"name":"Jimma Coffee Cooperative","distance_km":8,"price_per_kg":35,"capacity_kg":5000,"tag":"best","minutes":15},{"name":"Ethiopian Coffee Development","distance_km":15,"price_per_kg":30,"capacity_kg":3000,"tag":None,"minutes":25},{"name":"Addis Coffee Exporters","distance_km":340,"price_per_kg":42,"capacity_kg":10000,"tag":"cold","minutes":280}],"Mangoes":[{"name":"Ethiopia Fruit Exporters","distance_km":35,"price_per_kg":12,"capacity_kg":1000,"tag":"best","minutes":50},{"name":"Awash Juice Processors","distance_km":20,"price_per_kg":9,"capacity_kg":800,"tag":None,"minutes":30},{"name":"Addis Supermarkets","distance_km":60,"price_per_kg":15,"capacity_kg":3000,"tag":"cold","minutes":90}],"Maize":[{"name":"EGTE Grain Storage","distance_km":10,"price_per_kg":8,"capacity_kg":10000,"tag":"best","minutes":18},{"name":"Addis Flour Mills","distance_km":45,"price_per_kg":9,"capacity_kg":5000,"tag":None,"minutes":65},{"name":"Animal Feed Supplier","distance_km":18,"price_per_kg":7,"capacity_kg":8000,"tag":None,"minutes":28}]},
        "map_buyers":{"Addis Ababa":[{"name":"Addis Produce Market","lat":9.020,"lon":38.780,"price":18,"km":28,"tag":"best"},{"name":"Bishoftu Cold Hub","lat":8.740,"lon":38.980,"price":14,"km":45,"tag":"cold"},{"name":"Dire Dawa Wholesale","lat":9.600,"lon":41.866,"price":22,"km":445,"tag":None}],"Jimma":[{"name":"Jimma Coffee Coop","lat":7.680,"lon":36.820,"price":35,"km":8,"tag":"best"},{"name":"Jimma Cold Hub","lat":7.640,"lon":36.860,"price":28,"km":12,"tag":"cold"},{"name":"Addis Produce Market","lat":9.032,"lon":38.747,"price":42,"km":340,"tag":None}],"Dire Dawa":[{"name":"Dire Dawa Market","lat":9.610,"lon":41.870,"price":20,"km":5,"tag":"best"},{"name":"Harar Cold Storage","lat":9.310,"lon":42.120,"price":16,"km":52,"tag":"cold"},{"name":"Addis Produce Market","lat":9.032,"lon":38.747,"price":26,"km":445,"tag":None}],"Hawassa":[{"name":"Hawassa Market","lat":7.070,"lon":38.480,"price":17,"km":6,"tag":"best"},{"name":"Hawassa Cold Hub","lat":7.080,"lon":38.500,"price":13,"km":4,"tag":"cold"},{"name":"Addis Produce Market","lat":9.032,"lon":38.747,"price":22,"km":275,"tag":None}],"Bahir Dar":[{"name":"Bahir Dar Market","lat":11.600,"lon":37.390,"price":16,"km":7,"tag":"best"},{"name":"Gondar Cold Hub","lat":12.603,"lon":37.467,"price":13,"km":180,"tag":"cold"},{"name":"Addis Produce Market","lat":9.032,"lon":38.747,"price":22,"km":560,"tag":None}],"Mekelle":[{"name":"Mekelle Market","lat":13.505,"lon":39.480,"price":15,"km":5,"tag":"best"},{"name":"Mekelle Cold Hub","lat":13.510,"lon":39.500,"price":12,"km":4,"tag":"cold"},{"name":"Addis Produce Market","lat":9.032,"lon":38.747,"price":22,"km":780,"tag":None}]},
        "road_alerts":{"Addis Ababa":[{"lat":8.900,"lon":38.820,"type":"flood","msg":"⚠️ Addis-Nazret Road — Flooded","detail":"Adds +2.5 hours. Use western ring road."},{"lat":9.100,"lon":38.620,"type":"safe","msg":"✅ Western Ring Road — Clear","detail":"Safe route to western markets"}],"Jimma":[{"lat":7.600,"lon":36.750,"type":"flood","msg":"⚠️ Jimma-Addis Road — Flooded","detail":"Adds +1.5 hours"},{"lat":7.720,"lon":36.900,"type":"safe","msg":"✅ Southern Route — Clear","detail":"Safe alternative"}]},
        "city_en_map":{"Addis Ababa":"Addis Ababa","Dire Dawa":"Dire Dawa","Bahir Dar":"Bahir Dar","Jimma":"Jimma","Mekelle":"Mekele","Hawassa":"Awassa"},
    },
    "🇰🇪 Kenya": {
        "flag":"🇰🇪","flag_colors":["#006600","#000000","#CC0000"],
        "currency":"KES","usd_rate":129.0,
        "cities":["Nakuru","Nairobi","Kisumu","Eldoret","Mombasa","Thika"],
        "crops":["Tomatoes","Mangoes","Maize","Bananas","Leafy greens","Beans","Avocados","Potatoes"],
        "farmer_name":"James Kamau",
        "weather_map":{"Nakuru":{"temp":34.0,"humidity":78,"description":"Partly cloudy"},"Nairobi":{"temp":25.0,"humidity":65,"description":"Overcast"},"Kisumu":{"temp":32.0,"humidity":82,"description":"Humid"},"Eldoret":{"temp":22.0,"humidity":70,"description":"Cool"},"Mombasa":{"temp":31.0,"humidity":85,"description":"Hot and humid"},"Thika":{"temp":27.0,"humidity":72,"description":"Warm"}},
        "city_coords":{"Nakuru":(-0.303,36.080),"Nairobi":(-1.292,36.822),"Kisumu":(-0.102,34.762),"Eldoret":(0.520,35.270),"Mombasa":(-4.043,39.668),"Thika":(-1.033,37.069)},
        "buyers":{"Tomatoes":[{"name":"Nakuru Growers Co-op","distance_km":34,"price_per_kg":45,"capacity_kg":500,"tag":"best","minutes":48},{"name":"Eldama Cold Hub","distance_km":12,"price_per_kg":38,"capacity_kg":1000,"tag":"cold","minutes":18},{"name":"Nairobi Fresh Market","distance_km":156,"price_per_kg":52,"capacity_kg":2000,"tag":None,"minutes":192}],"Maize":[{"name":"NCPB Grain Store","distance_km":8,"price_per_kg":28,"capacity_kg":10000,"tag":"best","minutes":15},{"name":"Flour Mills Kenya","distance_km":55,"price_per_kg":32,"capacity_kg":5000,"tag":None,"minutes":70},{"name":"Animal Feed Co.","distance_km":18,"price_per_kg":22,"capacity_kg":8000,"tag":None,"minutes":25}],"Mangoes":[{"name":"Fruit Exporters Kenya","distance_km":45,"price_per_kg":62,"capacity_kg":1000,"tag":"best","minutes":55},{"name":"City Juice Processors","distance_km":22,"price_per_kg":48,"capacity_kg":800,"tag":None,"minutes":30},{"name":"Nairobi Wholesale","distance_km":80,"price_per_kg":70,"capacity_kg":3000,"tag":"cold","minutes":100}]},
        "map_buyers":{"Nakuru":[{"name":"Nakuru Growers Co-op","lat":-0.052,"lon":36.440,"price":45,"km":34,"tag":"best"},{"name":"Eldama Cold Hub","lat":-0.270,"lon":36.130,"price":38,"km":12,"tag":"cold"},{"name":"Nairobi Fresh Market","lat":-1.292,"lon":36.822,"price":52,"km":156,"tag":None}],"Nairobi":[{"name":"Wakulima Market","lat":-1.279,"lon":36.833,"price":50,"km":8,"tag":"best"},{"name":"Thika Cold Storage","lat":-1.033,"lon":37.069,"price":42,"km":45,"tag":"cold"},{"name":"Mombasa Wholesale","lat":-4.043,"lon":39.668,"price":60,"km":480,"tag":None}],"Kisumu":[{"name":"Kisumu Market","lat":-0.110,"lon":34.750,"price":40,"km":5,"tag":"best"},{"name":"Kisumu Cold Hub","lat":-0.090,"lon":34.780,"price":32,"km":8,"tag":"cold"},{"name":"Nairobi Market","lat":-1.292,"lon":36.822,"price":52,"km":350,"tag":None}]},
        "road_alerts":{"Nakuru":[{"lat":-0.580,"lon":36.200,"type":"flood","msg":"⚠️ B4 Highway — Flooded","detail":"Adds +2.1 hours. Use B7 via Njoro."},{"lat":-0.370,"lon":35.920,"type":"safe","msg":"✅ B7 Route — Clear","detail":"Via Njoro → Mau Summit. +22 min only"}]},
        "city_en_map":{"Nakuru":"Nakuru","Nairobi":"Nairobi","Kisumu":"Kisumu","Eldoret":"Eldoret","Mombasa":"Mombasa","Thika":"Thika"},
    },
    "🇬🇭 Ghana": {
        "flag":"🇬🇭","flag_colors":["#006B3F","#FCD116","#CE1126"],
        "currency":"GHS","usd_rate":12.5,
        "cities":["Accra","Kumasi","Tamale","Takoradi","Sunyani","Cape Coast"],
        "crops":["Tomatoes","Cassava","Plantain","Maize","Yams","Cocoa","Mangoes","Peppers"],
        "farmer_name":"Kwame Asante",
        "weather_map":{"Accra":{"temp":31.0,"humidity":75,"description":"Scattered clouds"},"Kumasi":{"temp":29.0,"humidity":82,"description":"Warm and humid"},"Tamale":{"temp":38.0,"humidity":35,"description":"Hot and dry"},"Takoradi":{"temp":30.0,"humidity":80,"description":"Coastal humid"},"Sunyani":{"temp":28.0,"humidity":78,"description":"Warm"},"Cape Coast":{"temp":29.0,"humidity":82,"description":"Coastal breeze"}},
        "city_coords":{"Accra":(5.603,-0.187),"Kumasi":(6.688,-1.624),"Tamale":(9.401,-0.839),"Takoradi":(4.898,-1.775),"Sunyani":(7.340,-2.329),"Cape Coast":(5.105,-1.246)},
        "buyers":{"Tomatoes":[{"name":"Makola Market Accra","distance_km":10,"price_per_kg":4,"capacity_kg":500,"tag":"best","minutes":20},{"name":"Tema Cold Storage","distance_km":28,"price_per_kg":3,"capacity_kg":1000,"tag":"cold","minutes":45},{"name":"Kumasi Wholesale","distance_km":250,"price_per_kg":5,"capacity_kg":2000,"tag":None,"minutes":200}],"Cassava":[{"name":"Accra Processing Hub","distance_km":15,"price_per_kg":1,"capacity_kg":5000,"tag":"best","minutes":30},{"name":"Tema Starch Factory","distance_km":30,"price_per_kg":1.2,"capacity_kg":8000,"tag":None,"minutes":50},{"name":"Kumasi Market","distance_km":250,"price_per_kg":1.5,"capacity_kg":3000,"tag":None,"minutes":200}],"Plantain":[{"name":"Accra Wholesale Market","distance_km":8,"price_per_kg":2,"capacity_kg":2000,"tag":"best","minutes":18},{"name":"Tema Export Hub","distance_km":32,"price_per_kg":2.5,"capacity_kg":5000,"tag":"cold","minutes":55},{"name":"Kumasi Market","distance_km":250,"price_per_kg":3,"capacity_kg":3000,"tag":None,"minutes":200}]},
        "map_buyers":{"Accra":[{"name":"Makola Market","lat":5.548,"lon":-0.213,"price":4,"km":10,"tag":"best"},{"name":"Tema Cold Storage","lat":5.666,"lon":-0.017,"price":3,"km":28,"tag":"cold"},{"name":"Kumasi Market","lat":6.688,"lon":-1.624,"price":5,"km":250,"tag":None}],"Kumasi":[{"name":"Kumasi Central Market","lat":6.700,"lon":-1.610,"price":4.5,"km":5,"tag":"best"},{"name":"Kumasi Cold Hub","lat":6.680,"lon":-1.640,"price":3.5,"km":8,"tag":"cold"},{"name":"Accra Market","lat":5.603,"lon":-0.187,"price":5,"km":250,"tag":None}]},
        "road_alerts":{"Accra":[{"lat":5.700,"lon":-0.100,"type":"flood","msg":"⚠️ Accra-Kumasi Highway — Flooded","detail":"Adds +1.5 hours. Use coastal road."},{"lat":5.550,"lon":-0.250,"type":"safe","msg":"✅ Coastal Road N1 — Clear","detail":"Safe alternative route"}]},
        "city_en_map":{"Accra":"Accra","Kumasi":"Kumasi","Tamale":"Tamale","Takoradi":"Takoradi","Sunyani":"Sunyani","Cape Coast":"Cape Coast"},
    },
    "🇺🇬 Uganda": {
        "flag":"🇺🇬","flag_colors":["#000000","#FCDC04","#DE3108"],
        "currency":"UGX","usd_rate":3750.0,
        "cities":["Kampala","Jinja","Gulu","Mbarara","Entebbe","Mbale"],
        "crops":["Maize","Bananas","Coffee","Tomatoes","Beans","Sweet potato","Cassava","Sorghum"],
        "farmer_name":"David Ochieng",
        "weather_map":{"Kampala":{"temp":29.0,"humidity":82,"description":"Partly cloudy"},"Jinja":{"temp":28.0,"humidity":80,"description":"Warm"},"Gulu":{"temp":33.0,"humidity":55,"description":"Hot"},"Mbarara":{"temp":26.0,"humidity":72,"description":"Mild"},"Entebbe":{"temp":27.0,"humidity":85,"description":"Humid"},"Mbale":{"temp":25.0,"humidity":78,"description":"Cool"}},
        "city_coords":{"Kampala":(0.348,32.583),"Jinja":(0.425,33.205),"Gulu":(2.775,32.300),"Mbarara":(-0.607,30.655),"Entebbe":(0.055,32.460),"Mbale":(1.083,34.183)},
        "buyers":{"Maize":[{"name":"Kampala Grain Market","distance_km":12,"price_per_kg":800,"capacity_kg":10000,"tag":"best","minutes":20},{"name":"Entebbe Cold Hub","distance_km":40,"price_per_kg":750,"capacity_kg":5000,"tag":"cold","minutes":55},{"name":"Jinja Wholesale","distance_km":80,"price_per_kg":900,"capacity_kg":8000,"tag":None,"minutes":90}],"Bananas":[{"name":"Kampala City Market","distance_km":12,"price_per_kg":400,"capacity_kg":2000,"tag":"best","minutes":20},{"name":"Entebbe Export Hub","distance_km":40,"price_per_kg":350,"capacity_kg":3000,"tag":"cold","minutes":55},{"name":"Jinja Market","distance_km":80,"price_per_kg":500,"capacity_kg":1500,"tag":None,"minutes":90}],"Tomatoes":[{"name":"Owino Market Kampala","distance_km":10,"price_per_kg":1200,"capacity_kg":500,"tag":"best","minutes":18},{"name":"Entebbe Cold Hub","distance_km":40,"price_per_kg":1000,"capacity_kg":800,"tag":"cold","minutes":55},{"name":"Jinja Market","distance_km":80,"price_per_kg":1400,"capacity_kg":1000,"tag":None,"minutes":90}]},
        "map_buyers":{"Kampala":[{"name":"Kampala City Market","lat":0.318,"lon":32.581,"price":1200,"km":10,"tag":"best"},{"name":"Entebbe Cold Hub","lat":0.055,"lon":32.460,"price":1000,"km":40,"tag":"cold"},{"name":"Jinja Market","lat":0.425,"lon":33.205,"price":1400,"km":80,"tag":None}],"Jinja":[{"name":"Jinja Market","lat":0.430,"lon":33.200,"price":900,"km":5,"tag":"best"},{"name":"Jinja Cold Hub","lat":0.415,"lon":33.215,"price":750,"km":8,"tag":"cold"},{"name":"Kampala Market","lat":0.348,"lon":32.583,"price":1200,"km":80,"tag":None}]},
        "road_alerts":{"Kampala":[{"lat":0.200,"lon":32.700,"type":"flood","msg":"⚠️ Kampala-Jinja Road — Heavy Traffic","detail":"Adds +1.5 hours. Use northern bypass."},{"lat":0.400,"lon":32.500,"type":"safe","msg":"✅ Northern Bypass — Clear","detail":"Faster route recommended"}]},
        "city_en_map":{"Kampala":"Kampala","Jinja":"Jinja","Gulu":"Gulu","Mbarara":"Mbarara","Entebbe":"Entebbe","Mbale":"Mbale"},
    },
    "🇳🇬 Nigeria": {
        "flag":"🇳🇬","flag_colors":["#008751","#FFFFFF","#008751"],
        "currency":"NGN","usd_rate":1580.0,
        "cities":["Lagos","Kano","Ibadan","Abuja","Kaduna","Enugu"],
        "crops":["Tomatoes","Yams","Cassava","Maize","Peppers","Plantain","Beans","Sorghum"],
        "farmer_name":"Emeka Okonkwo",
        "weather_map":{"Lagos":{"temp":31.0,"humidity":80,"description":"Humid coastal"},"Kano":{"temp":38.0,"humidity":25,"description":"Hot and dry"},"Ibadan":{"temp":30.0,"humidity":75,"description":"Warm"},"Abuja":{"temp":28.0,"humidity":65,"description":"Partly cloudy"},"Kaduna":{"temp":32.0,"humidity":55,"description":"Warm and dry"},"Enugu":{"temp":29.0,"humidity":78,"description":"Warm"}},
        "city_coords":{"Lagos":(6.524,3.379),"Kano":(12.000,8.517),"Ibadan":(7.378,3.947),"Abuja":(9.072,7.491),"Kaduna":(10.524,7.440),"Enugu":(6.441,7.499)},
        "buyers":{"Tomatoes":[{"name":"Mile 12 Market Lagos","distance_km":15,"price_per_kg":350,"capacity_kg":2000,"tag":"best","minutes":35},{"name":"Ketu Cold Storage","distance_km":20,"price_per_kg":300,"capacity_kg":3000,"tag":"cold","minutes":45},{"name":"Ibadan Wholesale","distance_km":130,"price_per_kg":400,"capacity_kg":5000,"tag":None,"minutes":150}],"Yams":[{"name":"Lagos Yam Market","distance_km":10,"price_per_kg":200,"capacity_kg":5000,"tag":"best","minutes":25},{"name":"Apapa Cold Hub","distance_km":25,"price_per_kg":180,"capacity_kg":8000,"tag":"cold","minutes":50},{"name":"Ibadan Market","distance_km":130,"price_per_kg":250,"capacity_kg":10000,"tag":None,"minutes":150}],"Cassava":[{"name":"Lagos Processing Hub","distance_km":18,"price_per_kg":80,"capacity_kg":10000,"tag":"best","minutes":38},{"name":"Ketu Cassava Factory","distance_km":22,"price_per_kg":70,"capacity_kg":15000,"tag":None,"minutes":48},{"name":"Ibadan Starch Mill","distance_km":130,"price_per_kg":90,"capacity_kg":20000,"tag":None,"minutes":150}]},
        "map_buyers":{"Lagos":[{"name":"Mile 12 Market","lat":6.600,"lon":3.380,"price":350,"km":15,"tag":"best"},{"name":"Ketu Cold Storage","lat":6.560,"lon":3.360,"price":300,"km":20,"tag":"cold"},{"name":"Ibadan Wholesale","lat":7.378,"lon":3.947,"price":400,"km":130,"tag":None}],"Kano":[{"name":"Kano Central Market","lat":12.010,"lon":8.520,"price":320,"km":5,"tag":"best"},{"name":"Kano Cold Hub","lat":11.990,"lon":8.510,"price":280,"km":8,"tag":"cold"},{"name":"Abuja Market","lat":9.072,"lon":7.491,"price":380,"km":350,"tag":None}]},
        "road_alerts":{"Lagos":[{"lat":6.500,"lon":3.300,"type":"flood","msg":"⚠️ Lagos-Ibadan Expressway — Flooding","detail":"Adds +2 hours. Use alternative."},{"lat":6.550,"lon":3.450,"type":"safe","msg":"✅ Lekki-Epe Expressway — Clear","detail":"Southern route available"}]},
        "city_en_map":{"Lagos":"Lagos","Kano":"Kano","Ibadan":"Ibadan","Abuja":"Abuja","Kaduna":"Kaduna","Enugu":"Enugu"},
    },
}

# ═══════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&family=JetBrains+Mono:wght@400;500&display=swap');

html,body,[class*="css"],.stApp{{
    font-family:'DM Sans',sans-serif!important;
    background-color:{BG}!important;
    color:{TEXT}!important;
}}
.block-container{{padding:1rem 2rem 2rem;max-width:100%;}}
section[data-testid="stSidebar"]{{background:{SURFACE}!important;}}
#MainMenu{{visibility:hidden;}}footer{{visibility:hidden;}}header{{visibility:hidden;}}

/* Streamlit overrides */
.stSelectbox label,.stSlider label,.stCheckbox label,.stTextInput label{{
    color:{MUTED}!important;font-size:11px!important;font-weight:500!important;
    text-transform:uppercase;letter-spacing:0.06em;
}}
.stSelectbox>div>div{{background:{INPUT_BG}!important;color:{TEXT}!important;border-color:{LINE}!important;border-radius:10px!important;}}
.stMetric{{background:{METRIC_BG};border:1px solid {CARD_BORDER};border-radius:14px;padding:14px 18px;}}
.stMetric label{{color:{MUTED}!important;font-size:10px!important;text-transform:uppercase;letter-spacing:0.08em;}}
.stMetric [data-testid="stMetricValue"]{{color:{TEXT}!important;font-family:'DM Serif Display',serif!important;font-size:22px!important;}}
.stMetric [data-testid="stMetricDelta"]{{font-size:11px!important;}}
div[data-testid="stHorizontalBlock"]>div{{gap:10px;}}
.stRadio label{{color:{TEXT}!important;font-size:12px!important;}}
.stRadio>div{{gap:6px!important;flex-wrap:wrap;}}
.stButton>button{{
    background:{FRESH}!important;color:#0A1A0A!important;
    border:none!important;border-radius:10px!important;
    font-weight:600!important;font-size:13px!important;
    padding:10px 20px!important;transition:all 0.2s!important;
}}
.stButton>button:hover{{opacity:0.85!important;transform:translateY(-1px)!important;}}
hr{{border-color:{LINE}!important;}}
[data-testid="stMarkdownContainer"] p{{color:{TEXT};}}
[data-testid="stTabs"] [data-baseweb="tab-list"]{{background:{SURFACE};border-radius:12px;padding:4px;gap:4px;}}
[data-testid="stTabs"] [data-baseweb="tab"]{{border-radius:9px!important;font-size:13px!important;font-weight:500!important;padding:8px 16px!important;}}
[data-testid="stTabs"] [aria-selected="true"]{{background:{BG}!important;color:{TEXT}!important;}}

/* Flag stripe */
.flag-stripe{{display:flex;height:4px;width:100%;margin-bottom:0;border-radius:2px;overflow:hidden;}}

/* Logo */
.logo{{font-family:'DM Serif Display',serif;font-size:26px;color:{GOLD};letter-spacing:-0.5px;}}
.logo em{{color:{FRESH};font-style:normal;}}
.tagline{{font-size:11px;color:{MUTED};letter-spacing:0.08em;text-transform:uppercase;margin-top:2px;}}

/* Cards */
.fr-card{{background:{SURFACE};border:1px solid {CARD_BORDER};border-radius:16px;padding:20px 22px;margin-bottom:14px;}}
.fr-card-green{{background:{SURFACE};border:1px solid rgba(75,191,122,0.25);border-radius:16px;padding:20px 22px;margin-bottom:14px;}}
.fr-card-red{{background:{'rgba(214,73,54,0.08)' if dark else 'rgba(214,73,54,0.04)'};border:1px solid rgba(214,73,54,0.2);border-radius:16px;padding:18px 20px;margin-bottom:14px;}}
.fr-card-gold{{background:{SURFACE};border:1px solid rgba(232,168,76,0.25);border-radius:16px;padding:20px 22px;margin-bottom:14px;}}
.fr-card-blue{{background:{SURFACE};border:1px solid rgba(107,172,222,0.25);border-radius:16px;padding:20px 22px;margin-bottom:14px;}}
.biz-card{{background:{SURFACE};border:1px solid {CARD_BORDER};border-radius:14px;padding:18px 20px;margin-bottom:12px;height:100%;}}

/* Labels */
.sec-label{{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:{MUTED};margin-bottom:8px;margin-top:4px;font-weight:500;}}

/* Numbers */
.big-num{{font-family:'JetBrains Mono',monospace;font-size:38px;font-weight:500;line-height:1;}}
.big-num-sm{{font-family:'JetBrains Mono',monospace;font-size:28px;font-weight:500;line-height:1;}}
.num-danger{{color:{DANGER};}}.num-warn{{color:{WARN};}}.num-good{{color:{FRESH};}}.num-blue{{color:{BLUE};}}.num-gold{{color:{GOLD};}}
.met-label{{font-size:11px;color:{MUTED};margin-top:4px;line-height:1.4;}}
.met-sub{{font-size:10px;color:{MUTED};}}

/* Risk bar */
.risk-bar-bg{{background:{LINE2};border-radius:5px;height:10px;margin:10px 0 6px;overflow:hidden;position:relative;}}

/* Inner cards */
.fcard-inner{{background:{SURFACE2};border:1px solid {CARD_BORDER};border-radius:10px;padding:12px 14px;}}

/* Buyer rows */
.buyer-row{{display:flex;align-items:center;justify-content:space-between;padding:11px 0;border-bottom:1px solid {LINE};font-size:13px;}}
.buyer-row:last-child{{border-bottom:none;}}

/* Tags */
.tag{{font-size:10px;padding:2px 9px;border-radius:6px;font-weight:600;display:inline-block;letter-spacing:0.02em;}}
.tag-green{{background:rgba(75,191,122,0.15);color:{FRESH};border:1px solid rgba(75,191,122,0.3);}}
.tag-blue{{background:rgba(107,172,222,0.15);color:{BLUE};border:1px solid rgba(107,172,222,0.3);}}
.tag-red{{background:rgba(214,73,54,0.15);color:#FF7B6B;border:1px solid rgba(214,73,54,0.3);}}
.tag-gold{{background:rgba(232,168,76,0.15);color:{GOLD};border:1px solid rgba(232,168,76,0.3);}}
.tag-gray{{background:rgba(255,255,255,0.06);color:{MUTED};border:1px solid {CARD_BORDER};}}

/* Dividers */
.fr-divider{{border:none;border-top:1px solid {LINE};margin:12px 0;}}

/* Narrative boxes */
.impact-box{{background:{'rgba(75,191,122,0.07)' if dark else 'rgba(75,191,122,0.05)'};border:1px solid rgba(75,191,122,0.2);border-left:3px solid {FRESH};border-radius:0 10px 10px 0;padding:14px 16px;font-size:13px;color:{TEXT};line-height:1.65;margin-top:10px;}}
.impact-box strong{{color:{FRESH};}}
.warn-box{{background:{'rgba(214,73,54,0.07)' if dark else 'rgba(214,73,54,0.04)'};border:1px solid rgba(214,73,54,0.2);border-left:3px solid {DANGER};border-radius:0 10px 10px 0;padding:14px 16px;font-size:13px;color:{TEXT};line-height:1.65;margin-top:10px;}}
.warn-box strong{{color:#FF7B6B;}}

/* Currency badge */
.curr-row{{display:flex;align-items:baseline;gap:8px;margin-top:4px;}}
.curr-local{{font-family:'JetBrains Mono',monospace;font-size:15px;font-weight:500;color:{FRESH};}}
.curr-usd{{font-size:11px;color:{MUTED};}}

/* Status indicators */
.status-live{{display:inline-flex;align-items:center;gap:5px;font-size:11px;color:{FRESH};}}
.status-demo{{display:inline-flex;align-items:center;gap:5px;font-size:11px;color:{GOLD};}}
.dot-live{{width:6px;height:6px;border-radius:50%;background:{FRESH};animation:pulse 2s infinite;flex-shrink:0;}}
.dot-demo{{width:6px;height:6px;border-radius:50%;background:{GOLD};flex-shrink:0;}}
@keyframes pulse{{0%,100%{{opacity:1;}}50%{{opacity:.3;}}}}

/* Progress ring-style metric */
.stat-pill{{display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:500;}}
.pill-green{{background:rgba(75,191,122,0.12);color:{FRESH};border:1px solid rgba(75,191,122,0.25);}}
.pill-red{{background:rgba(214,73,54,0.12);color:#FF7B6B;border:1px solid rgba(214,73,54,0.25);}}
.pill-gold{{background:rgba(232,168,76,0.12);color:{GOLD};border:1px solid rgba(232,168,76,0.25);}}
.pill-blue{{background:rgba(107,172,222,0.12);color:{BLUE};border:1px solid rgba(107,172,222,0.25);}}

/* Business stream cards */
.stream-card{{background:{SURFACE};border:1px solid {CARD_BORDER};border-radius:14px;padding:18px 20px;position:relative;overflow:hidden;}}
.stream-accent{{position:absolute;top:0;left:0;width:3px;height:100%;border-radius:3px 0 0 3px;}}
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# API FUNCTIONS
# ═══════════════════════════════════════════════════════════════

OPENWEATHER_KEY = st.secrets.get("OPENWEATHER_KEY", "")

@st.cache_data(ttl=300)
def get_weather_live(city_en, api_key):
    if not api_key or api_key == "2af51a55936420948648eafb14577646":
        return None
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_en}&appid={api_key}&units=metric",
            timeout=5
        )
        if r.status_code == 200:
            d = r.json()
            return {
                "temp": round(d["main"]["temp"], 1),
                "humidity": d["main"]["humidity"],
                "description": d["weather"][0]["description"].capitalize(),
                "real": True
            }
    except Exception:
        pass
    return None

@st.cache_data(ttl=3600)
def get_fx_rates():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        if r.status_code == 200:
            rates = r.json().get("rates", {})
            return {
                "ETB": rates.get("ETB", 57.5),
                "KES": rates.get("KES", 129.0),
                "GHS": rates.get("GHS", 12.5),
                "UGX": rates.get("UGX", 3750.0),
                "NGN": rates.get("NGN", 1580.0),
                "EUR": rates.get("EUR", 0.92),
                "GBP": rates.get("GBP", 0.79),
                "real": True
            }
    except Exception:
        pass
    return {"ETB":57.5,"KES":129.0,"GHS":12.5,"UGX":3750.0,"NGN":1580.0,"EUR":0.92,"GBP":0.79,"real":False}

# ═══════════════════════════════════════════════════════════════
# SPOILAGE INTELLIGENCE
# ═══════════════════════════════════════════════════════════════

def calculate_spoilage(crop, days, temp, humidity, storage):
    """
    Food science-based spoilage model.
    Temperature effect: each degree above 25C reduces shelf life by 6%.
    Humidity effect: above 80% accelerates fungal growth significantly.
    Cold storage: extends shelf life by 2.2x.
    """
    shelf = {
        "Tomatoes":7,"Mangoes":10,"Bananas":6,"Maize":60,"Leafy greens":3,
        "Coffee cherries":2,"Sweet potato":14,"Papaya":5,"Cassava":5,
        "Yams":21,"Plantain":8,"Beans":5,"Avocados":10,"Potatoes":21,
        "Cocoa":3,"Peppers":7,"Sorghum":60,"Coffee":30,
    }
    s = shelf.get(crop, 7)
    temp_factor    = max(0.4, 1.0 - max(0, temp - 25) * 0.06)
    humidity_factor = 0.75 if humidity > 80 else (0.88 if humidity > 70 else 1.0)
    storage_factor  = 2.2 if storage else 1.0
    adjusted_shelf  = s * temp_factor * humidity_factor * storage_factor
    remaining_days  = max(0, adjusted_shelf - days)
    remaining_hours = int(remaining_days * 24)
    waste_pct = 95 if remaining_hours <= 0 else max(5, int(100 - (remaining_days / adjusted_shelf) * 100))
    risk = "critical" if remaining_hours < 24 else ("high" if remaining_hours < 72 else ("moderate" if remaining_hours < 120 else "low"))
    return {
        "remaining_hours": remaining_hours,
        "waste_pct": waste_pct,
        "risk": risk,
        "adjusted_shelf": round(adjusted_shelf, 1),
        "confidence": 91
    }

def intervention_outcome(scenario_key, base_waste, base_earn):
    lang = st.session_state.language
    narr_map = {
        "scenario_base": T("narrative_base").replace("{waste}", str(base_waste)),
        "scenario_cold": T("narrative_cold"),
        "scenario_route": T("narrative_route"),
        "scenario_buyer": T("narrative_buyer"),
    }
    outcomes = {
        "scenario_base":  {"waste": base_waste,             "earnings": base_earn,        "narrative": narr_map["scenario_base"],  "box": "warn"},
        "scenario_cold":  {"waste": max(4, base_waste-36),  "earnings": base_earn * 1.9,  "narrative": narr_map["scenario_cold"],  "box": "impact"},
        "scenario_route": {"waste": max(12, base_waste-14), "earnings": base_earn * 1.35, "narrative": narr_map["scenario_route"], "box": "impact"},
        "scenario_buyer": {"waste": max(4, base_waste-38),  "earnings": base_earn * 2.1,  "narrative": narr_map["scenario_buyer"], "box": "impact"},
    }
    return outcomes.get(scenario_key, outcomes["scenario_base"])

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown('<div class="logo">Fresh<em>Route</em></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tagline">Global South Intelligence</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Language selector
    lang_options = list(TRANSLATIONS.keys())
    selected_lang = st.selectbox(
        T("language"),
        lang_options,
        index=lang_options.index(st.session_state.language)
    )
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

    # Country selector
    country_key = st.selectbox(T("country"), list(COUNTRIES.keys()))
    C = COUNTRIES[country_key]
    currency = C["currency"]

    # Flag stripe in sidebar
    fc = C["flag_colors"]
    st.markdown(f'<div class="flag-stripe"><div style="flex:1;background:{fc[0]}"></div><div style="flex:1;background:{fc[1]}"></div><div style="flex:1;background:{fc[2]}"></div></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    city           = st.selectbox(T("location"), C["cities"])
    crop           = st.selectbox(T("crop"), C["crops"])
    quantity       = st.slider(T("quantity"), 50, 2000, 200, step=50)
    days_harvested = st.slider(T("days_harvest"), 1, 14, 3)
    has_storage    = st.checkbox(T("has_storage"), value=False)

    st.markdown("---")
    st.markdown(f'<div class="sec-label">{T("api_config")}</div>', unsafe_allow_html=True)
    api_key_input = st.text_input("OpenWeatherMap API Key", value="", type="password", placeholder="Paste your key here")

    st.markdown("---")
    auto_refresh = st.checkbox(T("auto_refresh"), value=False)
    if st.button(T("run_analysis"), use_container_width=True):
        st.cache_data.clear()

# ═══════════════════════════════════════════════════════════════
# DATA COMPUTATION
# ═══════════════════════════════════════════════════════════════

api_key  = api_key_input or OPENWEATHER_KEY
city_en  = C["city_en_map"].get(city, city)

if api_key and api_key not in ("", "PASTE_YOUR_KEY_HERE"):
    live = get_weather_live(city_en, api_key)
    weather = {**(live or C["weather_map"].get(city, {"temp":28.0,"humidity":70,"description":"Warm"})),
               "city": city, "country": C["flag"],
               "real": bool(live)}
else:
    wdata   = C["weather_map"].get(city, {"temp":28.0,"humidity":70,"description":"Warm"})
    weather = {**wdata, "city": city, "country": C["flag"], "real": False}

fx_rates     = get_fx_rates()
usd_rate     = fx_rates.get(currency, C["usd_rate"])
eur_rate_mul = fx_rates.get("EUR", 0.92)

spoilage     = calculate_spoilage(crop, days_harvested, weather["temp"], weather["humidity"], has_storage)
buyer_db     = C["buyers"]
buyers_list  = buyer_db.get(crop, list(buyer_db.values())[0])
buyers_list  = [b for b in buyers_list if b["capacity_kg"] >= quantity * 0.5]
best_buyer   = buyers_list[0] if buyers_list else None
best_revenue = best_buyer["price_per_kg"] * quantity if best_buyer else 0
rev_no_action = best_revenue * (1 - spoilage["waste_pct"] / 100)
fr_fee       = round(best_revenue * 0.015, 0)

country_name = country_key.split(" ", 1)[1]

# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════

# Flag stripe
fc = C["flag_colors"]
st.markdown(f'<div class="flag-stripe"><div style="flex:1;background:{fc[0]}"></div><div style="flex:1;background:{fc[1]}"></div><div style="flex:1;background:{fc[2]}"></div></div>', unsafe_allow_html=True)

hc1, hc2, hc3 = st.columns([3, 2, 1])
with hc1:
    st.markdown(f'<div class="logo">Fresh<em>Route</em> {C["flag"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tagline">{T("tagline")} · {city}, {country_name}</div>', unsafe_allow_html=True)
with hc2:
    w_dot  = "dot-live" if weather.get("real") else "dot-demo"
    w_cls  = "status-live" if weather.get("real") else "status-demo"
    w_txt  = T("live_weather") if weather.get("real") else T("demo_mode")
    fx_txt = T("live_rates") if fx_rates.get("real") else T("estimated_rates")
    fx_cls = "status-live" if fx_rates.get("real") else "status-demo"
    fx_dot = "dot-live" if fx_rates.get("real") else "dot-demo"
    st.markdown(f"""
    <br>
    <div class="{w_cls}"><div class="{w_dot}"></div>{w_txt}</div>
    <div class="{fx_cls}" style="margin-top:3px"><div class="{fx_dot}"></div>{fx_txt} · {T("updated")}: {datetime.now().strftime('%H:%M:%S')}</div>
    """, unsafe_allow_html=True)
with hc3:
    st.markdown("<br>", unsafe_allow_html=True)
    btn_lbl = T("light_mode") if dark else T("dark_mode")
    st.button(btn_lbl, on_click=toggle_theme, use_container_width=True)

st.markdown(f"<hr style='border:none;border-top:1px solid {LINE};margin:10px 0 12px'>", unsafe_allow_html=True)

# ── VISIBLE CONTROL BAR ──────────────────────────────────────
ctrl1, ctrl2, ctrl3, ctrl4, ctrl5, ctrl6 = st.columns([1.4, 1.4, 1.2, 1.2, 1, 1])

with ctrl1:
    new_lang = st.selectbox("🌐 Language", list(TRANSLATIONS.keys()),
        index=list(TRANSLATIONS.keys()).index(st.session_state.language), key="lang_main")
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.rerun()

with ctrl2:
    new_country = st.selectbox("🌍 Country", list(COUNTRIES.keys()),
        index=list(COUNTRIES.keys()).index(country_key), key="country_main")

with ctrl3:
    new_city = st.selectbox("📍 City", C["cities"],
        index=C["cities"].index(city) if city in C["cities"] else 0, key="city_main")

with ctrl4:
    new_crop = st.selectbox("🌱 Crop", C["crops"],
        index=C["crops"].index(crop) if crop in C["crops"] else 0, key="crop_main")

with ctrl5:
    new_qty = st.slider("⚖️ Qty (kg)", 50, 2000, quantity, step=50, key="qty_main")

with ctrl6:
    new_days = st.slider("📅 Days", 1, 14, days_harvested, key="days_main")

# Update from controls
country_key   = new_country
C             = COUNTRIES[country_key]
currency      = C["currency"]
city          = new_city if new_city in C["cities"] else C["cities"][0]
crop          = new_crop if new_crop in C["crops"] else C["crops"][0]
quantity      = new_qty
days_harvested= new_days
country_name  = country_key.split(" ", 1)[1]
city_en       = C["city_en_map"].get(city, city)

if api_key and api_key not in ("","PASTE_YOUR_KEY_HERE"):
    live = get_weather_live(city_en, api_key)
    weather = {**(live or C["weather_map"].get(city, {"temp":28.0,"humidity":70,"description":"Warm"})),
               "city":city,"country":C["flag"],"real":bool(live)}
else:
    wdata   = C["weather_map"].get(city, {"temp":28.0,"humidity":70,"description":"Warm"})
    weather = {**wdata,"city":city,"country":C["flag"],"real":False}

usd_rate      = fx_rates.get(currency, C["usd_rate"])
spoilage      = calculate_spoilage(crop, days_harvested, weather["temp"], weather["humidity"], has_storage)
buyer_db      = C["buyers"]
buyers_list   = buyer_db.get(crop, list(buyer_db.values())[0])
buyers_list   = [b for b in buyers_list if b["capacity_kg"] >= quantity * 0.5]
best_buyer    = buyers_list[0] if buyers_list else None
best_revenue  = best_buyer["price_per_kg"] * quantity if best_buyer else 0
rev_no_action = best_revenue * (1 - spoilage["waste_pct"] / 100)
fr_fee        = round(best_revenue * 0.015, 0)

fc = C["flag_colors"]
st.markdown(f'<div class="flag-stripe" style="margin:8px 0 14px"><div style="flex:1;background:{fc[0]}"></div><div style="flex:1;background:{fc[1]}"></div><div style="flex:1;background:{fc[2]}"></div></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs([T("tab_dashboard"), T("tab_business"), T("tab_map")])

# ────────────────────────────────────────────────────────────────
# TAB 1: INTELLIGENCE DASHBOARD
# ────────────────────────────────────────────────────────────────
with tab1:

    # Situation header
    at_risk     = int(best_revenue * spoilage["waste_pct"] / 100)
    at_risk_usd = at_risk / usd_rate
    hours       = spoilage["remaining_hours"]

    st.markdown(f'<div class="sec-label">{T("situation")} — {city}, {country_name} {C["flag"]} · {T("farmer")}: {C["farmer_name"]}</div>', unsafe_allow_html=True)

    m1, m2, m3, m4, m5 = st.columns(5)

    hc  = "num-danger" if hours < 48           else ("num-warn" if hours < 96              else "num-good")
    tc  = "num-danger" if weather["temp"] > 32 else ("num-warn" if weather["temp"] > 28    else "num-good")
    huc = "num-blue"   if weather["humidity"] > 75 else "num-good"
    wc  = "num-danger" if spoilage["waste_pct"] > 30 else ("num-warn" if spoilage["waste_pct"] > 15 else "num-good")

    with m1:
        st.markdown(f"""<div class="fr-card">
            <div class="sec-label">{T("hours_spoilage")}</div>
            <div class="big-num {hc}">{hours}</div>
            <div class="met-label">{T("hrs_remaining")}</div>
        </div>""", unsafe_allow_html=True)

    with m2:
        st.markdown(f"""<div class="fr-card">
            <div class="sec-label">{T("temperature")}</div>
            <div class="big-num {tc}">{weather['temp']}°</div>
            <div class="met-label">{weather['description']}</div>
        </div>""", unsafe_allow_html=True)

    with m3:
        hw = T("accel_rot") if weather["humidity"] > 75 else T("acceptable")
        st.markdown(f"""<div class="fr-card">
            <div class="sec-label">{T("humidity")}</div>
            <div class="big-num {huc}">{weather['humidity']}%</div>
            <div class="met-label">{hw}</div>
        </div>""", unsafe_allow_html=True)

    with m4:
        st.markdown(f"""<div class="fr-card">
            <div class="sec-label">{T("predicted_waste")}</div>
            <div class="big-num {wc}">{spoilage['waste_pct']}%</div>
            <div class="met-label">{T("without_action")}</div>
        </div>""", unsafe_allow_html=True)

    with m5:
        st.markdown(f"""<div class="fr-card-red">
            <div class="sec-label">{T("value_at_risk")}</div>
            <div class="big-num num-danger">{currency} {at_risk:,}</div>
            <div class="met-label">${at_risk_usd:,.1f} USD · {T("lost_no_action")}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # Spoilage analysis + Buyer matching
    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown(f'<div class="sec-label">{T("spoilage_analysis")}</div>', unsafe_allow_html=True)

        risk_label = {"critical": T("critical"), "high": T("high"),
                      "moderate": T("moderate"), "low": T("low")}[spoilage["risk"]]
        risk_tag   = {"critical":"tag-red","high":"tag-red","moderate":"tag-gold","low":"tag-green"}[spoilage["risk"]]
        risk_fill  = {"critical":92,"high":65,"moderate":38,"low":18}[spoilage["risk"]]

        heat_l = T("severe") if weather["temp"] > 32 else (T("high_label") if weather["temp"] > 28 else T("moderate_label"))
        heat_c = DANGER if weather["temp"] > 32 else WARN
        hum_l  = T("high_label") if weather["humidity"] > 75 else T("moderate_label")
        hum_c  = WARN if weather["humidity"] > 75 else FRESH
        stor_l = T("active") if has_storage else T("none_storage")
        stor_c = FRESH if has_storage else WARN
        stor_s = T("shelf_ext") if has_storage else T("open_air")

        st.markdown(f"""<div class="fr-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
                <span style="font-size:14px;font-weight:600;color:{TEXT}">{crop} — {quantity} kg</span>
                <span class="tag {risk_tag}">{risk_label.upper()}</span>
            </div>
            <div class="risk-bar-bg">
                <div style="height:10px;border-radius:5px;background:linear-gradient(90deg,{FRESH} 0%,{WARN} 55%,{DANGER} 100%);width:{risk_fill}%"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:10px;color:{MUTED};margin-bottom:16px">
                <span>{T("low")}</span><span>{T("moderate")}</span><span>{T("high")}</span><span>{T("critical")}</span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
                <div class="fcard-inner">
                    <div class="met-sub">{T("heat_stress")}</div>
                    <div style="font-size:13px;font-weight:600;color:{heat_c};margin-top:4px">{heat_l}</div>
                    <div class="met-sub">{weather['temp']}°C ambient</div>
                </div>
                <div class="fcard-inner">
                    <div class="met-sub">{T("moisture")}</div>
                    <div style="font-size:13px;font-weight:600;color:{hum_c};margin-top:4px">{hum_l}</div>
                    <div class="met-sub">{weather['humidity']}% humidity</div>
                </div>
                <div class="fcard-inner">
                    <div class="met-sub">{T("confidence")}</div>
                    <div style="font-size:13px;font-weight:600;color:{FRESH};margin-top:4px">{spoilage['confidence']}%</div>
                    <div class="met-sub">Weather + crop science</div>
                </div>
                <div class="fcard-inner">
                    <div class="met-sub">{T("storage_status")}</div>
                    <div style="font-size:13px;font-weight:600;color:{stor_c};margin-top:4px">{stor_l}</div>
                    <div class="met-sub">{stor_s}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    with col_r:
        st.markdown(f'<div class="sec-label">{T("ai_buyer")}</div>', unsafe_allow_html=True)
        rev_today = best_buyer["price_per_kg"] * quantity if best_buyer else 0
        rev_usd   = rev_today / usd_rate

        buyer_rows_html = ""
        for i, b in enumerate(buyers_list[:3]):
            if b["tag"] == "best":
                tag_html = f' <span class="tag tag-green">{T("best_match")}</span>'
            elif b["tag"] == "cold":
                tag_html = f' <span class="tag tag-blue">{T("cold_storage")}</span>'
            else:
                tag_html = ""
            price_usd = b["price_per_kg"] / usd_rate
            buyer_rows_html += f"""
            <div class="buyer-row">
                <div>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:{MUTED};margin-right:6px">#{i+1}</span>
                    <span style="font-weight:600;color:{TEXT}">{b['name']}</span>{tag_html}
                    <div style="font-size:11px;color:{MUTED};margin-top:2px;padding-left:20px">
                        {b['distance_km']} km &nbsp;·&nbsp; {b['minutes']} min &nbsp;·&nbsp; cap. {b['capacity_kg']:,} kg
                    </div>
                </div>
                <div style="text-align:right">
                    <div class="curr-local">{currency} {b['price_per_kg']}</div>
                    <div class="curr-usd">${price_usd:.2f} USD</div>
                </div>
            </div>"""

        gain_pct = int((rev_today / max(1, rev_no_action) - 1) * 100)

        st.markdown(f'<div class="fr-card-green">{buyer_rows_html}<hr class="fr-divider"></div>', unsafe_allow_html=True)

        r1, r2, r3 = st.columns(3)
        with r1:
            st.metric(T("revenue_today"), f"{currency} {rev_today:,}", f"${rev_usd:,.1f} USD")
        with r2:
            st.metric(T("vs_nothing"), f"+{gain_pct}%")
        with r3:
            st.metric(T("fr_fee"), f"{currency} {int(fr_fee):,}", f"${fr_fee/usd_rate:.1f} USD")

    # Intervention simulator
    st.markdown(f"<hr style='border:none;border-top:1px solid {LINE};margin:8px 0 16px'>", unsafe_allow_html=True)
    st.markdown(f'<div class="sec-label">{T("simulator_title")}</div>', unsafe_allow_html=True)

    sim_labels = {
        "scenario_base":  T("scenario_base"),
        "scenario_cold":  T("scenario_cold"),
        "scenario_route": T("scenario_route"),
        "scenario_buyer": T("scenario_buyer"),
    }
    chosen_label = st.radio("", list(sim_labels.values()), horizontal=True, label_visibility="collapsed")
    chosen_key   = [k for k, v in sim_labels.items() if v == chosen_label][0]
    outcome      = intervention_outcome(chosen_key, spoilage["waste_pct"], rev_no_action)

    earn_change = ((outcome["earnings"] - rev_no_action) / max(1, rev_no_action)) * 100
    w_col = "num-danger" if outcome["waste"]>30 else ("num-warn" if outcome["waste"]>15 else "num-good")
    e_col = "num-good" if outcome["earnings"]>rev_no_action*1.1 else ("num-warn" if outcome["earnings"]>=rev_no_action else "num-danger")
    earn_usd = outcome["earnings"] / usd_rate
    sign = "+" if earn_change >= 0 else ""

    s1, s2, s3 = st.columns([1, 1, 2])
    with s1:
        st.markdown(f"""<div class="fr-card">
            <div class="sec-label">{T("waste")}</div>
            <div class="big-num {w_col}">{outcome['waste']}%</div>
            <div class="met-label">{T("harvest_lost")}</div>
        </div>""", unsafe_allow_html=True)
    with s2:
        st.markdown(f"""<div class="fr-card">
            <div class="sec-label">{T("farmer_earnings")}</div>
            <div class="big-num {e_col}">{currency} {int(outcome['earnings']):,}</div>
            <div class="met-label">${earn_usd:,.1f} USD &nbsp;·&nbsp; {sign}{earn_change:.0f}% {T("vs_baseline")}</div>
        </div>""", unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="{outcome["box"]}-box">{outcome["narrative"]}</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────
# TAB 2: BUSINESS MODEL
# ────────────────────────────────────────────────────────────────
with tab2:
    st.markdown(f'<div class="sec-label">{T("biz_title")} · {country_name} {C["flag"]}</div>', unsafe_allow_html=True)

    # Live currency converter
    st.markdown(f'<div class="sec-label">{T("live_currency")}</div>', unsafe_allow_html=True)
    rate_badge = f'<span class="stat-pill pill-green">🟢 {T("live_rates")}</span>' if fx_rates.get("real") else f'<span class="stat-pill pill-gold">🟡 {T("estimated_rates")}</span>'
    st.markdown(rate_badge, unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    cur1, cur2, cur3, cur4, cur5 = st.columns(5)
    eur_local = usd_rate / fx_rates.get("EUR", 0.92)
    gbp_local = usd_rate / fx_rates.get("GBP", 0.79)

    with cur1: st.metric(f"1 USD →", f"{currency} {usd_rate:,.1f}")
    with cur2: st.metric(f"1 EUR →", f"{currency} {eur_local:,.1f}")
    with cur3: st.metric(f"1 GBP →", f"{currency} {gbp_local:,.1f}")
    with cur4: st.metric(f"1 {currency} →", f"${1/usd_rate:.4f} USD")
    with cur5: st.metric(f"1 {currency} →", f"€{1/eur_local:.4f} EUR")

    st.markdown(f"<hr style='border:none;border-top:1px solid {LINE};margin:14px 0 16px'>", unsafe_allow_html=True)

    # Unit economics
    st.markdown(f'<div class="sec-label">{T("unit_econ")}</div>', unsafe_allow_html=True)
    ue1, ue2, ue3, ue4 = st.columns(4)
    fee_local = round(best_revenue * 0.015, 0)
    fee_usd   = fee_local / usd_rate
    cost_ai   = 0.008
    margin_pct = int(((fee_usd - cost_ai) / max(fee_usd, 0.01)) * 100)

    with ue1: st.metric(T("avg_trans"), f"{currency} {best_revenue:,}", f"${best_revenue/usd_rate:,.1f} USD")
    with ue2: st.metric(T("fr_fee_label"), f"{currency} {fee_local:,}", f"${fee_usd:,.2f} USD")
    with ue3: st.metric(T("ai_cost"), "< $0.01 USD", "GPT-4o-mini")
    with ue4: st.metric(T("gross_margin"), f"~{margin_pct}%", "after AI cost")

    st.markdown(f"<hr style='border:none;border-top:1px solid {LINE};margin:14px 0 16px'>", unsafe_allow_html=True)

    # Revenue projections
    st.markdown(f'<div class="sec-label">{T("revenue_proj")}</div>', unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    projections = [
        (T("conservative"), "100", 100, BLUE),
        (T("moderate_biz"), "1,000", 1000, FRESH),
        (T("scale"), "10,000", 10000, GOLD),
    ]
    for col, (label, count_str, matches, color) in zip([p1, p2, p3], projections):
        monthly_local = fee_local * matches
        monthly_usd   = monthly_local / usd_rate
        annual_usd    = monthly_usd * 12
        with col:
            st.markdown(f"""<div class="biz-card" style="border-top:3px solid {color}">
                <div class="sec-label">{label}</div>
                <div style="font-size:12px;color:{MUTED};margin-bottom:12px">{count_str} {T("matches_month")}</div>
                <div style="font-family:'DM Serif Display',serif;font-size:24px;color:{color}">{currency} {monthly_local:,.0f}</div>
                <div style="font-size:12px;color:{MUTED};margin-top:4px">${monthly_usd:,.0f} USD / month</div>
                <div style="font-size:12px;color:{MUTED}">${annual_usd:,.0f} USD / year</div>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"<hr style='border:none;border-top:1px solid {LINE};margin:14px 0 16px'>", unsafe_allow_html=True)

    # Revenue streams
    st.markdown(f'<div class="sec-label">{T("revenue_streams")}</div>', unsafe_allow_html=True)

    rs1, rs2, rs3 = st.columns(3)
    streams = [
        (T("stream1_title"), T("stream1_desc"), T("stream1_status"), FRESH, "pill-green"),
        (T("stream2_title"), T("stream2_desc"), T("stream2_status"), GOLD,  "pill-gold"),
        (T("stream3_title"), T("stream3_desc"), T("stream3_status"), BLUE,  "pill-blue"),
    ]
    for col, (title, desc, status, color, pill_cls) in zip([rs1, rs2, rs3], streams):
        with col:
            st.markdown(f"""<div class="stream-card">
                <div class="stream-accent" style="background:{color}"></div>
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
                    <div style="font-size:13px;font-weight:600;color:{color};padding-right:8px">{title}</div>
                    <span class="stat-pill {pill_cls}" style="white-space:nowrap;flex-shrink:0">{status}</span>
                </div>
                <div style="font-size:12px;color:{MUTED};line-height:1.65">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"<hr style='border:none;border-top:1px solid {LINE};margin:14px 0 16px'>", unsafe_allow_html=True)

    # Market opportunity
    st.markdown(f'<div class="sec-label">{T("market_opp")}</div>', unsafe_allow_html=True)

    ms1, ms2, ms3, ms4 = st.columns(4)
    with ms1: st.metric(T("farmers_global_stat"), "500M+", T("primary_target"))
    with ms2: st.metric(T("ph_loss"), "40%", T("ssa_food"))
    with ms3: st.metric(T("annual_loss"), "$4B+", T("world_bank"))
    with ms4: st.metric(T("market_pen"), "$2B+", T("rev_opp"))

# ────────────────────────────────────────────────────────────────
# TAB 3: ROUTE MAP
# ────────────────────────────────────────────────────────────────
with tab3:
    st.markdown(f'<div class="sec-label">{T("route_title")} · {city}, {country_name} {C["flag"]}</div>', unsafe_allow_html=True)

    city_coords    = C["city_coords"]
    map_buyers_db  = C.get("map_buyers", {})
    road_alerts_db = C.get("road_alerts", {})

    flat, flon     = city_coords.get(city, (9.032, 38.747))
    map_buyers_now = map_buyers_db.get(city, list(map_buyers_db.values())[0] if map_buyers_db else [])
    alerts         = road_alerts_db.get(city, [])

    tile = "CartoDB dark_matter" if dark else "CartoDB positron"
    m    = folium.Map(location=[flat, flon], zoom_start=9, tiles=tile)

    # Farmer marker
    folium.Marker(
        [flat, flon],
        popup=folium.Popup(
            f"<b>📍 {city}, {country_name}</b><br>"
            f"{crop} · {quantity}kg<br>"
            f"{C['farmer_name']}<br>"
            f"Risk: {spoilage['risk'].upper()}<br>"
            f"Waste: {spoilage['waste_pct']}%",
            max_width=220
        ),
        tooltip=f"👨🏾‍🌾 {C['farmer_name']} — {T('farmer')}",
        icon=folium.Icon(color="orange", icon="home", prefix="fa")
    ).add_to(m)

    # Buyer markers and route lines
    buyer_colors = {"best": "green", "cold": "blue", None: "gray"}
    for b in map_buyers_now[:3]:
        col = buyer_colors[b["tag"]]
        price_usd = b["price"] / usd_rate
        label_tag = f" — {T('best_match')}" if b["tag"]=="best" else (f" — {T('cold_storage')}" if b["tag"]=="cold" else "")
        folium.Marker(
            [b["lat"], b["lon"]],
            popup=folium.Popup(
                f"<b>{b['name']}</b>{label_tag}<br>"
                f"{currency} {b['price']}/kg (${price_usd:.2f} USD)<br>"
                f"{b['km']}km away<br>"
                f"Revenue: {currency} {b['price']*quantity:,}",
                max_width=240
            ),
            tooltip=f"🏪 {b['name']} — {currency} {b['price']}/kg",
            icon=folium.Icon(color=col, icon="shopping-cart", prefix="fa")
        ).add_to(m)

        line_color = "#4BBF7A" if b["tag"]=="best" else ("#6BACDE" if b["tag"]=="cold" else "#888888")
        folium.PolyLine(
            [[flat, flon], [b["lat"], b["lon"]]],
            color=line_color,
            weight=3 if b["tag"]=="best" else 1.5,
            opacity=0.9 if b["tag"]=="best" else 0.45,
            dash_array=None if b["tag"]=="best" else "8 8"
        ).add_to(m)

    # Road alert markers
    for a in alerts:
        folium.Marker(
            [a["lat"], a["lon"]],
            popup=folium.Popup(f"<b>{a['msg']}</b><br>{a['detail']}", max_width=220),
            tooltip=a["msg"],
            icon=folium.Icon(
                color="red" if a["type"]=="flood" else "green",
                icon="exclamation-triangle" if a["type"]=="flood" else "check",
                prefix="fa"
            )
        ).add_to(m)

    # Legend
    leg_bg = "#0F0F0A" if dark else "#FFFFFF"
    leg_t  = "#F5F0E8" if dark else "#0F0F0A"
    m.get_root().html.add_child(folium.Element(f"""
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
         background:{leg_bg};border:1px solid rgba(255,255,255,0.12);
         border-radius:12px;padding:14px 18px;font-family:sans-serif;
         font-size:12px;color:{leg_t};box-shadow:0 4px 20px rgba(0,0,0,0.3)">
      <div style="font-weight:700;margin-bottom:10px;color:#E8A84C;font-size:13px">FreshRoute {C["flag"]}</div>
      <div style="margin-bottom:5px">🟠 {T("farmer")}: {C["farmer_name"]}</div>
      <div style="color:#4BBF7A;margin-bottom:5px">🟢 {T("best_match")}</div>
      <div style="color:#6BACDE;margin-bottom:5px">🔵 {T("cold_storage")}</div>
      <div style="margin-bottom:8px">⚪ Other buyers</div>
      <div style="color:#D64936;margin-bottom:5px">🔴 Road alert</div>
      <div style="color:#4BBF7A">✅ Safe route</div>
    </div>"""))

    # Render map and side panel
    mc, mi = st.columns([3, 1])
    with mc:
        st_folium(m, width=None, height=450, returned_objects=[])
    with mi:
        alert_html = ""
        for a in alerts:
            if a["type"] == "flood":
                alert_html += f'<div style="background:rgba(214,73,54,0.1);border:1px solid rgba(214,73,54,0.3);border-radius:10px;padding:11px;margin-bottom:8px"><div style="font-size:11px;font-weight:600;color:#FF7B6B">{a["msg"]}</div><div style="font-size:11px;color:{MUTED};margin-top:3px">{a["detail"]}</div></div>'
            else:
                alert_html += f'<div style="background:rgba(75,191,122,0.08);border:1px solid rgba(75,191,122,0.2);border-radius:10px;padding:11px;margin-bottom:8px"><div style="font-size:11px;font-weight:600;color:{FRESH}">{a["msg"]}</div><div style="font-size:11px;color:{MUTED};margin-top:3px">{a["detail"]}</div></div>'

        buyer_panel = "".join([
            f'<div style="padding:9px 0;border-bottom:1px solid {LINE};font-size:12px">'
            f'<span style="color:{TEXT};font-weight:600">{b["name"]}</span><br>'
            f'<span style="color:{MUTED}">{b["km"]}km · {currency} {b["price"]}/kg</span>'
            f'<span style="color:{MUTED}"> (${b["price"]/usd_rate:.2f})</span></div>'
            for b in map_buyers_now[:3]
        ])

        st.markdown(f"""<div class="fr-card" style="height:450px;overflow-y:auto">
            <div class="sec-label">{T("route_intel")}</div>
            <div style="margin-bottom:12px">
                <div style="font-size:13px;font-weight:600;color:{TEXT}">📍 {city}, {country_name}</div>
                <div style="font-size:12px;color:{MUTED};margin-top:2px">{crop} · {quantity}kg · {C['farmer_name']}</div>
                <div style="margin-top:6px"><span class="stat-pill {'pill-red' if spoilage['risk'] in ['critical','high'] else 'pill-gold' if spoilage['risk']=='moderate' else 'pill-green'}">{spoilage['risk'].upper()}</span></div>
            </div>
            {alert_html}
            <div class="sec-label" style="margin-top:10px">{T("nearest_buyers")}</div>
            {buyer_panel}
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════

st.markdown(f"<hr style='border:none;border-top:1px solid {LINE};margin:24px 0 12px'>", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)
with f1: st.markdown(f"<div style='font-size:11px;color:{MUTED}'>{T('built_for')} <strong style='color:{TEXT}'>ITU × WFF 2026</strong></div>", unsafe_allow_html=True)
with f2: st.markdown(f"<div style='font-size:11px;color:{MUTED}'><strong style='color:{TEXT}'>40%</strong> {T('fao_stat')}</div>", unsafe_allow_html=True)
with f3: st.markdown(f"<div style='font-size:11px;color:{MUTED}'><strong style='color:{TEXT}'>500M+</strong> {T('farmers_global')}</div>", unsafe_allow_html=True)
with f4: st.markdown(f"<div style='font-size:11px;color:{MUTED}'><strong style='color:{TEXT}'>1.5%</strong> {T('fee_note')}</div>", unsafe_allow_html=True)

# Flag stripe at bottom
fc = C["flag_colors"]
st.markdown(f'<div class="flag-stripe" style="margin-top:8px"><div style="flex:1;background:{fc[0]}"></div><div style="flex:1;background:{fc[1]}"></div><div style="flex:1;background:{fc[2]}"></div></div>', unsafe_allow_html=True)

if auto_refresh:
    time.sleep(300)
    st.rerun()