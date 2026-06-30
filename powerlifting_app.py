"""
╔══════════════════════════════════════════════════════════════╗
║          IRON PROTOCOL v3 — Powerlifting Training OS         ║
║   Layout 3 columnas · Accesorios científicos · RPE en vivo  ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import hashlib
from dataclasses import dataclass
from supabase import create_client, Client

st.set_page_config(page_title="Iron Protocol", page_icon="🏋️", layout="wide", initial_sidebar_state="expanded")

# ══════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:#0a0a0c;color:#e8e8e8;font-family:'Inter',sans-serif;}
[data-testid="stSidebar"]{background:#0f0f12;border-right:1px solid #1a1a20;}
/* ── Day column cards ── */
.day-col{background:#111116;border:1px solid #1e1e25;border-radius:14px;padding:1.2rem 1rem;height:100%;}
.day-title{font-family:'Space Grotesk',sans-serif;font-size:0.78rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.2rem;}
.day-phase{font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:1rem;padding-bottom:0.7rem;border-bottom:1px solid #1e1e25;}
/* ── Main lift block ── */
.main-lift-block{background:#0d0d10;border:1px solid #1e1e25;border-radius:10px;padding:0.9rem 1rem;margin-bottom:0.8rem;}
.lift-name{font-family:'Space Grotesk',sans-serif;font-size:0.95rem;font-weight:700;margin-bottom:0.5rem;}
.set-row{display:flex;align-items:center;gap:0.5rem;padding:0.3rem 0;border-bottom:1px solid #141418;font-size:0.82rem;}
.set-row:last-child{border-bottom:none;}
.set-num{color:#444;width:28px;flex-shrink:0;}
.set-reps{color:#888;width:45px;flex-shrink:0;}
.set-pct{color:#ccc;width:50px;flex-shrink:0;}
.set-kg{font-family:'Space Grotesk',sans-serif;font-weight:700;color:#ff4d1c;width:65px;flex-shrink:0;}
/* ── RPE chip ── */
.rpe-chip{display:inline-flex;align-items:center;justify-content:center;width:32px;height:18px;border-radius:4px;font-size:0.65rem;font-weight:700;flex-shrink:0;}
.rpe-easy  {background:#1a2a1a;color:#4caf50;border:1px solid #2d4a2d;}
.rpe-medium{background:#2a1f0a;color:#ff9800;border:1px solid #4a3000;}
.rpe-hard  {background:#2a1010;color:#ef5350;border:1px solid #4a1818;}
/* ── Accessory slot ── */
.acc-slot{background:#0d0d10;border:1px dashed #242428;border-radius:8px;padding:0.7rem 0.9rem;margin-bottom:0.5rem;}
.acc-slot-label{font-size:0.65rem;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.3rem;}
.acc-cat-push  {color:#64b5f6;}
.acc-cat-pull  {color:#4caf50;}
.acc-cat-hinge {color:#ff9800;}
.acc-cat-quad  {color:#ab47bc;}
.acc-cat-core  {color:#f06292;}
.acc-cat-shoulder{color:#26c6da;}
/* ── RPE live feedback ── */
.rpe-feedback{border-radius:8px;padding:0.6rem 0.9rem;font-size:0.8rem;margin-top:0.4rem;line-height:1.5;}
.rpe-ok    {background:#0f1a0f;border:1px solid #2d4a2d;border-left:3px solid #4caf50;color:#a5d6a7;}
.rpe-warn  {background:#1a1000;border:1px solid #4a3000;border-left:3px solid #ff9800;color:#ffcc80;}
.rpe-danger{background:#1a0808;border:1px solid #4a1818;border-left:3px solid #ef5350;color:#ef9a9a;}
/* ── Badges ── */
.badge{display:inline-block;font-size:0.62rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;padding:0.12rem 0.5rem;border-radius:4px;}
.badge-accum  {background:#1a2a1a;color:#4caf50;border:1px solid #2d4a2d;}
.badge-intens {background:#2a1a0a;color:#ff9800;border:1px solid #4a2d00;}
.badge-deload {background:#1a1a2a;color:#64b5f6;border:1px solid #1a2a4a;}
/* ── Metric cards ── */
.mc{background:#111116;border:1px solid #1e1e25;border-radius:10px;padding:0.9rem 1rem;text-align:center;}
.mc-label{font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;color:#555;margin-bottom:0.2rem;}
.mc-val{font-family:'Space Grotesk',sans-serif;font-size:1.8rem;font-weight:700;color:#ff4d1c;line-height:1;}
.mc-unit{font-size:0.75rem;color:#666;margin-top:0.1rem;}
/* ── Section header ── */
.sh{font-family:'Space Grotesk',sans-serif;font-size:0.8rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#555;border-bottom:1px solid #1a1a20;padding-bottom:0.35rem;margin:1.2rem 0 0.8rem 0;}
/* ── Buttons ── */
.stButton>button{background:#ff4d1c;color:#fff;font-weight:700;font-size:0.8rem;letter-spacing:0.06em;text-transform:uppercase;border:none;border-radius:6px;padding:0.45rem 1rem;transition:background 0.15s;}
.stButton>button:hover{background:#e63d0f;}
/* ── Tabs ── */
div[data-testid="stTabs"] button{color:#666;font-weight:600;font-size:0.8rem;letter-spacing:0.06em;text-transform:uppercase;}
div[data-testid="stTabs"] button[aria-selected="true"]{color:#ff4d1c;border-bottom-color:#ff4d1c;}
/* ── Inputs ── */
div[data-testid="stNumberInput"] input,div[data-testid="stTextInput"] input{background:#111116!important;color:#e8e8e8!important;border:1px solid #1e1e25!important;}
/* ── Table ── */
.tbl{width:100%;border-collapse:collapse;font-size:0.82rem;}
.tbl th{background:#0a0a0c;color:#555;text-transform:uppercase;font-size:0.65rem;letter-spacing:0.1em;padding:0.4rem 0.6rem;border-bottom:1px solid #1a1a20;text-align:left;}
.tbl td{padding:0.4rem 0.6rem;border-bottom:1px solid #141418;color:#bbb;}
.tbl tr:last-child td{border-bottom:none;}
.kg-hi{font-family:'Space Grotesk',sans-serif;font-weight:700;color:#ff4d1c;}
/* ── Login ── */
.login-err{background:#1a0808;border:1px solid #4a1818;border-left:3px solid #ef5350;border-radius:6px;padding:0.6rem 0.9rem;font-size:0.82rem;color:#ef5350;margin-bottom:1rem;}
.user-badge{display:inline-flex;align-items:center;gap:0.4rem;background:#16161c;border:1px solid #222228;border-radius:20px;padding:0.22rem 0.65rem;font-size:0.78rem;color:#888;}
.udot{width:7px;height:7px;border-radius:50%;background:#ff4d1c;display:inline-block;}
hr{border-color:#1a1a20;}
.lift-pill{display:inline-block;padding:0.05rem 0.45rem;border-radius:10px;font-size:0.7rem;font-weight:700;margin-right:3px;}
.sq{background:#1a2a1a;color:#4caf50;}.bp{background:#1a1a2a;color:#64b5f6;}.dl{background:#2a1a0a;color:#ff9800;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  SUPABASE
# ══════════════════════════════════════════════════════════════
@st.cache_resource
def get_supabase() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
supabase = get_supabase()

# ══════════════════════════════════════════════════════════════
#  AUTH
# ══════════════════════════════════════════════════════════════
def _hash(pw): return hashlib.sha256(pw.encode()).hexdigest()

def verify_login(username, password):
    try:
        res = supabase.table("users").select("username,display_name,password_hash").eq("username", username.strip().lower()).single().execute()
        u = res.data
        if not u: return None, "Usuario no encontrado."
        if u["password_hash"] != _hash(password): return None, "Contraseña incorrecta."
        return u["display_name"], None
    except Exception as e:
        return None, f"Error de conexión: {e}"

# ══════════════════════════════════════════════════════════════
#  PERSISTENCE
# ══════════════════════════════════════════════════════════════
def _default():
    return {"one_rm":{"Squat":0.0,"Bench Press":0.0,"Deadlift":0.0},
            "template":"DUP","pct_overrides":{},"recommendations":{},"acc_selections":{}}

def load_user_data(username):
    try:
        res = supabase.table("user_data").select("one_rm,template,pct_overrides,recommendations,acc_selections").eq("username", username).single().execute()
        d = res.data
        if not d: return _default()
        base = _default()
        base.update({k: d[k] for k in base if d.get(k) is not None})
        return base
    except: return _default()

def save_user_data(username):
    try:
        supabase.table("user_data").upsert({
            "username": username,
            "one_rm": dict(st.session_state.one_rm),
            "template": st.session_state.template,
            "pct_overrides": dict(st.session_state.pct_overrides),
            "recommendations": dict(st.session_state.recommendations),
            "acc_selections": dict(st.session_state.acc_selections),
            "updated_at": "now()",
        }, on_conflict="username").execute()
    except Exception as e:
        st.toast(f"⚠ Error al guardar: {e}")

# ══════════════════════════════════════════════════════════════
#  SCIENTIFIC ACCESSORY LIBRARY
#  Categorías basadas en movimientos primales (Boyle, 2016)
#  y principios de fuerza general de Westside / Juggernaut
# ══════════════════════════════════════════════════════════════

# Cada slot define: categoría, función, por qué importa para SBD
ACC_SLOTS = {
    "Day A — Hypertrophy": [
        {"cat":"EMPUJE VERTICAL",   "color":"acc-cat-push",     "science":"Desarrolla deltoides anterior y tríceps largo — transferencia directa al Bench Press (Schoenfeld, 2010).",
         "options":["Press Militar con Barra","Press de Hombro con Mancuernas","Press Arnold","Push Press"]},
        {"cat":"TRACCIÓN VERTICAL", "color":"acc-cat-pull",     "science":"Fortalece dorsales y bíceps — fundamental para el setup del Deadlift y estabilidad en Bench (McGill, 2016).",
         "options":["Pull-Up / Dominadas con Peso","Jalón al Pecho (Agarre Ancho)","Pullover con Mancuerna","Chin-Up (Supino)"]},
        {"cat":"CUÁDRICEPS",        "color":"acc-cat-quad",     "science":"Hipertrofia unilateral de cuádriceps → mejora la salida del hoyo en Squat (Helms et al., 2017).",
         "options":["Bulgarian Split Squat","Prensa de Piernas (45°)","Hack Squat","Extensión de Cuádriceps","Step-Up con Mancuernas"]},
        {"cat":"ISQUIOTIBIALES",    "color":"acc-cat-hinge",    "science":"MEV de isquiotibiales crítico para proteger rodilla y potenciar Deadlift (Contreras & Schoenfeld, 2011).",
         "options":["Romanian Deadlift con Mancuernas","Nordic Curl","Curl de Piernas Acostado","Good Morning","Stiff-Leg Deadlift"]},
    ],
    "Day B — Strength": [
        {"cat":"EMPUJE HORIZONTAL", "color":"acc-cat-push",     "science":"Variante de pausa para construir fuerza en el punto de pegado del Bench (Taber et al., 2019).",
         "options":["Bench Press Pausa 2s (Variante)","Close-Grip Bench Press","Press con Mancuernas Inclinado","Dips Lastrados"]},
        {"cat":"TRACCIÓN HORIZONTAL","color":"acc-cat-pull",    "science":"Remo horizontal → equilibrio escapular y fuerza de retracción clave para el Bench Press (Cressey, 2012).",
         "options":["Barbell Row (Pendlay)","Chest-Supported Row","Remo en Polea Baja","Remo con Mancuerna 1 Brazo","Cable Row"]},
        {"cat":"BISAGRA DE CADERA", "color":"acc-cat-hinge",    "science":"Variantes de bisagra cargan los erectores y glúteos — principal limitante en Deadlift pesado (Contreras, 2014).",
         "options":["Hip Thrust con Barra","Rack Pull (por encima rodillas)","Sumo Deadlift (variante técnica)","Kettlebell Swing","Block Pull"]},
        {"cat":"CORE ANTI-ROTACIÓN","color":"acc-cat-core",     "science":"Rigidez de núcleo = transmisión de fuerza eficiente. Esencial para Squat y Deadlift (McGill, 2010).",
         "options":["Pallof Press","Ab Wheel Rollout","Plancha Cargada","Farmer's Walk","Suitcase Carry"]},
    ],
    "Day C — Power": [
        {"cat":"EXPLOSIVIDAD TREN INF.","color":"acc-cat-quad", "science":"Velocidad de desarrollo de fuerza (RFD) — entrena el sistema nervioso para aplicar fuerza más rápido (Zatsiorsky, 2003).",
         "options":["Box Squat con Bandas (velocidad)","Jump Squat (BW o ligero)","Box Jump","Trap Bar Jump"]},
        {"cat":"TRACCIÓN EXPLOSIVA", "color":"acc-cat-hinge",   "science":"Snatch-grip y remo explosivo mejoran la aceleración de la barra en Deadlift (Cormie et al., 2011).",
         "options":["Romanian Deadlift Snatch-Grip","Power Clean (técnica)","Remo Explosivo en Polea","Kettlebell Deadlift Saltado"]},
        {"cat":"HOMBRO / ESTABILIDAD","color":"acc-cat-shoulder","science":"Manguito rotador y estabilizadores escapulares — previenen lesión y mantienen arco en Bench (Reinold, 2014).",
         "options":["Face Pull con Cuerda","Rotación Externa con Banda","Elevación Lateral (3×15)","YTW en Banco Inclinado","Band Pull-Apart"]},
        {"cat":"GRIP / ANTEBRAZO",  "color":"acc-cat-pull",     "science":"La fuerza de agarre es el limitante más subestimado en Deadlift pesado (Haff & Triplett, 2016).",
         "options":["Farmer's Walk Pesado","Wrist Curl con Barra","Dead Hang Lastrado","Plate Pinch","Towel Pull-Up"]},
    ],
}

# Sets/reps recomendados por categoría (evidencia: Schoenfeld 2010, Israetel 2019)
ACC_PRESCRIPTION = {
    "EMPUJE VERTICAL":    {"sets":3,"reps":"8–12","rpe":7,"note":"Hipertrofia funcional — mantener técnica estricta."},
    "TRACCIÓN VERTICAL":  {"sets":3,"reps":"8–12","rpe":7,"note":"Superar ratio 1:1 empuje/tracción para salud escapular."},
    "CUÁDRICEPS":         {"sets":3,"reps":"10–15","rpe":7,"note":"Volumen alto de cuádriceps → transferencia al Squat."},
    "ISQUIOTIBIALES":     {"sets":3,"reps":"8–12","rpe":7,"note":"Trabajo excéntrico enfatizado para prevención de lesiones."},
    "EMPUJE HORIZONTAL":  {"sets":3,"reps":"5–8","rpe":8,"note":"Intensidad moderada-alta — patrón específico al Bench."},
    "TRACCIÓN HORIZONTAL":{"sets":4,"reps":"8–10","rpe":7,"note":"Volumen alto de remo para equilibrar el Bench pesado."},
    "BISAGRA DE CADERA":  {"sets":3,"reps":"6–10","rpe":8,"note":"Carga progresiva — glúteos y erectores para Deadlift."},
    "CORE ANTI-ROTACIÓN": {"sets":3,"reps":"10–15","rpe":6,"note":"Rigidez, no movimiento. Respiración y bracing."},
    "EXPLOSIVIDAD TREN INF.":{"sets":4,"reps":"3–5","rpe":7,"note":"Velocidad máxima de ejecución — no sacrificar RFD."},
    "TRACCIÓN EXPLOSIVA": {"sets":3,"reps":"3–5","rpe":7,"note":"Aceleración máxima, carga ligera (40–60% 1RM)."},
    "HOMBRO / ESTABILIDAD":{"sets":3,"reps":"12–20","rpe":6,"note":"Alta repetición, baja carga — salud articular."},
    "GRIP / ANTEBRAZO":   {"sets":3,"reps":"AMRAP/tiempo","rpe":8,"note":"Hasta fallo controlado — fuerza de agarre específica."},
}

# ══════════════════════════════════════════════════════════════
#  DATA MODELS
# ══════════════════════════════════════════════════════════════
LIFTS = ["Squat","Bench Press","Deadlift"]

@dataclass
class SetConfig:
    pct: float; sets: int; reps: int; rpe_target: int

@dataclass
class Exercise:
    name: str; lift: str; sets_config: list; notes: str = ""

@dataclass
class TrainingDay:
    label: str; exercises: list; acc_key: str = ""

@dataclass
class Week:
    number: int; phase: str; days: list; volume_note: str = ""

# ══════════════════════════════════════════════════════════════
#  TEMPLATE BUILDERS
# ══════════════════════════════════════════════════════════════
def build_dup_template():
    dup = [
        {"Squat":[(67,4,8,7),(75,3,5,8),(80,3,3,8)],"Bench Press":[(65,4,8,7),(73,3,5,8),(78,3,3,8)],"Deadlift":[(65,3,6,7),(73,3,4,8),(80,2,3,8)]},
        {"Squat":[(70,4,8,7),(77,3,5,8),(82,3,3,8)],"Bench Press":[(68,4,8,7),(75,3,5,8),(80,3,3,8)],"Deadlift":[(68,3,6,7),(76,3,4,8),(82,2,3,8)]},
        {"Squat":[(72,4,6,8),(80,3,4,8),(85,3,2,9)],"Bench Press":[(70,4,6,8),(78,3,4,8),(83,3,2,9)],"Deadlift":[(70,3,5,8),(79,3,3,8),(85,2,2,9)]},
        {"Squat":[(60,3,5,6),(65,3,3,6),(68,2,2,7)],"Bench Press":[(58,3,5,6),(63,3,3,6),(66,2,2,7)],"Deadlift":[(58,2,4,6),(63,2,3,6),(66,1,2,7)]},
    ]
    phases = ["Accumulation","Accumulation","Intensification","Deload"]
    vol_notes = ["Alto volumen, intensidad moderada. Construir capacidad de trabajo.",
                 "Incremento de volumen. Precisión técnica clave.",
                 "Volumen baja, intensidad sube. Cargas cerca del máximo.",
                 "Recuperación activa. Restaurar disposición neurológica."]
    day_keys = ["Day A — Hypertrophy","Day B — Strength","Day C — Power"]
    day_labels = ["Día A — Hipertrofia","Día B — Fuerza","Día C — Potencia"]
    weeks = []
    for wi in range(4):
        days = []
        for di, (dkey, dlabel) in enumerate(zip(day_keys, day_labels)):
            exs = []
            for lift in LIFTS:
                pct, sets, reps, rpe = dup[wi][lift][di]
                exs.append(Exercise(lift, lift, [SetConfig(pct,1,reps,rpe)]*sets, f"{reps} reps × {sets} series @ {pct}% 1RM"))
            days.append(TrainingDay(dlabel, exs, dkey))
        weeks.append(Week(wi+1, phases[wi], days, vol_notes[wi]))
    return weeks

def build_linear_template():
    lin = [
        {"Squat":(75,4,5,7),"Bench Press":(73,4,5,7),"Deadlift":(75,3,5,7)},
        {"Squat":(80,3,4,8),"Bench Press":(78,3,4,8),"Deadlift":(80,3,4,8)},
        {"Squat":(85,3,3,8),"Bench Press":(83,3,3,8),"Deadlift":(85,2,3,8)},
        {"Squat":(62,2,3,6),"Bench Press":(60,2,3,6),"Deadlift":(60,2,2,6)},
    ]
    phases = ["Accumulation","Intensification","Intensification","Deload"]
    vol_notes = ["Semana base. Ajustar técnica, construir base de fatiga.",
                 "Incremento de carga. 4×4 — estímulo denso y potente.",
                 "Triples pesados. Intensidades cerca de competencia.",
                 "Deload — clearar fatiga antes de nuevo bloque."]
    weeks = []
    for wi in range(4):
        sched = lin[wi]
        exs = []
        for lift in LIFTS:
            pct, sets, reps, rpe = sched[lift]
            exs.append(Exercise(lift, lift, [SetConfig(pct,1,reps,rpe)]*sets, f"{sets}×{reps} @ {pct}% | RPE {rpe}"))
        # Linear uses Day B slots for accessories
        weeks.append(Week(wi+1, phases[wi], [TrainingDay("Sesión SBD Completa", exs, "Day B — Strength")], vol_notes[wi]))
    return weeks

# ══════════════════════════════════════════════════════════════
#  MATH
# ══════════════════════════════════════════════════════════════
def epley(w,r): return w if r==1 else w*(1+r/30)
def brzycki(w,r): return w if r==1 else w*(36/(37-r))
def weighted_1rm(w,r): return round(0.6*epley(w,r)+0.4*brzycki(w,r),1)
def pct_to_kg(orm,pct): return round((orm*pct/100)/2.5)*2.5

# ══════════════════════════════════════════════════════════════
#  RPE LIVE FEEDBACK ENGINE
#  Basado en: Tuchscherer (2008), Helms et al. (2016),
#             Zourdos et al. (2016) — RIR-based autoregulation
# ══════════════════════════════════════════════════════════════
def rpe_live_feedback(rpe_actual: float, rpe_target: int, rir: int, completed: bool) -> dict:
    delta = rpe_actual - rpe_target
    if not completed and rpe_actual >= 10:
        return {"cls":"rpe-danger","icon":"🛑","title":"FALLO — Deload Adaptativo",
                "adj_pct":-7.5,"adj_text":"Reducir carga −7.5%",
                "msg":"Fallo absoluto detectado. Reducir carga inmediatamente. Próxima sesión: técnica ligera ≤75% 1RM. La fatiga acumulada está enmascarando el fitness real."}
    elif not completed and rpe_actual >= 9:
        return {"cls":"rpe-danger","icon":"⚠","title":"Series Incompletas — Mantener",
                "adj_pct":-2.5,"adj_text":"Mantener o reducir −2.5%",
                "msg":f"RPE {rpe_actual:.1f} con series incompletas. No aumentar carga. Revisar sueño (target >7h), calorías y volumen semanal total."}
    elif completed and rpe_actual < (rpe_target - 1.5):
        inc = 5.0 if rir >= 4 else 2.5
        return {"cls":"rpe-ok","icon":"✅","title":f"Muy Submaximal — Aumentar +{inc}%",
                "adj_pct":inc,"adj_text":f"Aumentar carga +{inc}%",
                "msg":f"RPE {rpe_actual:.1f} vs objetivo RPE {rpe_target} — {rir} RIR restantes. Reserva significativa. Estímulo insuficiente para la adaptación planificada. Aumentar próxima sesión."}
    elif completed and rpe_actual <= (rpe_target + 0.5):
        return {"cls":"rpe-ok","icon":"🎯","title":"En Target — Progresión Planificada",
                "adj_pct":2.5,"adj_text":"Continuar +2.5% planificado",
                "msg":f"RPE {rpe_actual:.1f} ≈ objetivo RPE {rpe_target}. Alineación perfecta con la periodización. Proceder con el incremento semanal programado."}
    elif completed and rpe_actual <= (rpe_target + 1.5):
        return {"cls":"rpe-warn","icon":"⚡","title":"Ligeramente Alto — Mantener Peso",
                "adj_pct":0,"adj_text":"Mantener misma carga",
                "msg":f"RPE {rpe_actual:.1f} levemente por encima del objetivo. No aumentar carga esta semana. Evaluar calidad del sueño y nutrición peri-entreno."}
    else:
        return {"cls":"rpe-danger","icon":"🔴","title":"Sobrepaso — Reducir Volumen",
                "adj_pct":-2.5,"adj_text":"Reducir carga −2.5% o bajar 1 serie",
                "msg":f"RPE {rpe_actual:.1f} significativamente por encima del objetivo RPE {rpe_target}. Señal de fatiga acumulada o mala recuperación. Reducir carga o volumen en la próxima sesión."}

def full_recommendation(lift, rpe_actual, rir, completed, phase):
    fb = rpe_live_feedback(rpe_actual, 8, rir, completed)
    return {"verdict": "ok" if "ok" in fb["cls"] else "warn" if "warn" in fb["cls"] else "danger",
            "title": fb["title"], "text": fb["msg"], "action": fb["adj_text"], "adj_pct": fb["adj_pct"]}

# ══════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════
for k, v in [("authenticated",False),("current_user",None),("display_name",None),("login_error","")]:
    if k not in st.session_state: st.session_state[k] = v

# ══════════════════════════════════════════════════════════════
#  LOGIN
# ══════════════════════════════════════════════════════════════
def render_login():
    _, col, _ = st.columns([1,1.1,1])
    with col:
        st.markdown("""
        <div style='text-align:center;padding-top:3.5rem;'>
          <div style='font-family:Space Grotesk,sans-serif;font-size:2.6rem;font-weight:900;color:#e8e8e8;letter-spacing:-0.03em;'>
            🏋 <span style='color:#ff4d1c;'>IRON</span> PROTOCOL
          </div>
          <div style='font-size:0.7rem;color:#333;letter-spacing:0.18em;text-transform:uppercase;margin:0.4rem 0 2.5rem;'>
            Powerlifting Training OS · Acceso Privado
          </div>
        </div>""", unsafe_allow_html=True)
        if st.session_state.login_error:
            st.markdown(f"<div class='login-err'>⚠ {st.session_state.login_error}</div>", unsafe_allow_html=True)
        username = st.text_input("Usuario", placeholder="usuario1 / usuario2", key="lu")
        password = st.text_input("Contraseña", type="password", placeholder="••••••••", key="lp")
        st.markdown("<div style='margin-top:0.4rem;'></div>", unsafe_allow_html=True)
        if st.button("Ingresar →", use_container_width=True):
            dn, err = verify_login(username, password)
            if err:
                st.session_state.login_error = err; st.rerun()
            else:
                uname = username.strip().lower()
                data  = load_user_data(uname)
                st.session_state.update({
                    "authenticated":True,"current_user":uname,"display_name":dn,
                    "login_error":"","one_rm":data["one_rm"],"template":data["template"],
                    "pct_overrides":data["pct_overrides"],"recommendations":data["recommendations"],
                    "acc_selections":data.get("acc_selections",{}),
                    "weeks": build_dup_template() if data["template"]=="DUP" else build_linear_template(),
                    "active_page":"Program",
                })
                st.rerun()

# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════
def rpe_chip(rpe):
    cls = "rpe-easy" if rpe<=7 else "rpe-medium" if rpe<=8.5 else "rpe-hard"
    return f"<span class='rpe-chip {cls}'>RPE{int(rpe) if rpe==int(rpe) else rpe}</span>"

PHASE_BADGE = {"Accumulation":"badge-accum","Intensification":"badge-intens","Deload":"badge-deload","Peak":"badge-deload"}

def render_main_lift(ex, wk_idx, d_idx, ex_idx, username):
    orm = st.session_state.one_rm.get(ex.lift, 0)
    cfg = ex.sets_config[0]
    pill = {"Squat":"sq","Bench Press":"bp","Deadlift":"dl"}.get(ex.lift,"")
    st.markdown(f"""
    <div class='main-lift-block'>
      <div class='lift-name'>
        <span class='lift-pill {pill}'>{ex.lift.upper()}</span>
        <span style='font-size:0.72rem;color:#555;margin-left:6px;'>{ex.notes}</span>
      </div>
    """, unsafe_allow_html=True)

    changed = False
    for s_idx in range(len(ex.sets_config)):
        key = f"pct_{username}_{wk_idx}_{d_idx}_{ex_idx}_{s_idx}"
        if key not in st.session_state.pct_overrides:
            st.session_state.pct_overrides[key] = float(cfg.pct)

        col_set, col_reps, col_pct, col_kg, col_rpe_input = st.columns([0.6,0.8,1.3,1.2,1.5])
        with col_set:
            st.markdown(f"<div style='padding-top:8px;font-size:0.8rem;color:#444;'>S{s_idx+1}</div>", unsafe_allow_html=True)
        with col_reps:
            st.markdown(f"<div style='padding-top:8px;font-size:0.82rem;color:#888;'>{cfg.reps} reps</div>", unsafe_allow_html=True)
        with col_pct:
            new_pct = st.number_input("pct",min_value=30.0,max_value=110.0,
                value=float(st.session_state.pct_overrides[key]),step=2.5,
                key=key,label_visibility="collapsed")
            if new_pct != st.session_state.pct_overrides[key]:
                st.session_state.pct_overrides[key] = new_pct; changed = True
        with col_kg:
            if orm > 0:
                kg = pct_to_kg(orm, st.session_state.pct_overrides[key])
                st.markdown(f"<div style='padding-top:6px;font-family:Space Grotesk,sans-serif;font-weight:700;color:#ff4d1c;font-size:1rem;'>{kg:.1f} kg</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='padding-top:8px;font-size:0.75rem;color:#333;'>set 1RM</div>", unsafe_allow_html=True)
        with col_rpe_input:
            rpe_key = f"rpe_live_{username}_{wk_idx}_{d_idx}_{ex_idx}_{s_idx}"
            if rpe_key not in st.session_state:
                st.session_state[rpe_key] = float(cfg.rpe_target)
            rpe_real = st.number_input("RPE real",min_value=5.0,max_value=10.0,
                value=st.session_state[rpe_key],step=0.5,
                key=rpe_key,label_visibility="collapsed",
                help="RPE real de esta serie")

    st.markdown("</div>", unsafe_allow_html=True)

    # Live RPE feedback for the whole exercise (last set RPE)
    last_rpe_key = f"rpe_live_{username}_{wk_idx}_{d_idx}_{ex_idx}_{len(ex.sets_config)-1}"
    rpe_real_val = st.session_state.get(last_rpe_key, float(cfg.rpe_target))
    if rpe_real_val != float(cfg.rpe_target):
        fb = rpe_live_feedback(rpe_real_val, cfg.rpe_target, max(0, int(10 - rpe_real_val)), rpe_real_val < 10)
        st.markdown(f"""
        <div class='rpe-feedback {fb["cls"]}'>
          <strong>{fb["icon"]} {fb["title"]}</strong> — {fb["adj_text"]}<br>
          <span style='font-size:0.76rem;opacity:0.85;'>{fb["msg"]}</span>
        </div>""", unsafe_allow_html=True)

    if changed: save_user_data(username)

def render_accessory_slot(slot, day_key, slot_idx, username):
    sel_key = f"acc_{username}_{day_key}_{slot_idx}"
    saved = st.session_state.acc_selections.get(sel_key, slot["options"][0])
    presc = ACC_PRESCRIPTION.get(slot["cat"], {"sets":3,"reps":"10","rpe":7,"note":""})

    st.markdown(f"""
    <div class='acc-slot'>
      <div class='acc-slot-label {slot["color"]}'>{slot["cat"]}</div>
      <div style='font-size:0.7rem;color:#444;margin-bottom:0.5rem;line-height:1.4;'>{slot["science"]}</div>
    """, unsafe_allow_html=True)

    chosen = st.selectbox(
        f"Ejercicio — {slot['cat']}",
        options=slot["options"],
        index=slot["options"].index(saved) if saved in slot["options"] else 0,
        key=f"sel_{sel_key}",
        label_visibility="collapsed",
    )
    if chosen != st.session_state.acc_selections.get(sel_key):
        st.session_state.acc_selections[sel_key] = chosen
        save_user_data(username)

    st.markdown(f"""
      <div style='margin-top:0.4rem;display:flex;gap:0.8rem;align-items:center;'>
        <span style='font-size:0.72rem;color:#555;'>{presc["sets"]} series × {presc["reps"]} reps</span>
        {rpe_chip(presc["rpe"])}
        <span style='font-size:0.68rem;color:#444;'>{presc["note"]}</span>
      </div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════
def render_app():
    username     = st.session_state.current_user
    display_name = st.session_state.display_name

    # ── Sidebar ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style='padding:0.5rem 0 0.8rem;'>
          <div style='font-family:Space Grotesk,sans-serif;font-size:1.3rem;font-weight:700;color:#e8e8e8;'>
            🏋 <span style='color:#ff4d1c;'>IRON</span> PROTOCOL
          </div>
          <div style='margin-top:0.5rem;'><span class='user-badge'><span class='udot'></span>{display_name}</span></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<div class='sh'>1RMs Activos</div>", unsafe_allow_html=True)
        for lift, color in [("Squat","#4caf50"),("Bench Press","#64b5f6"),("Deadlift","#ff9800")]:
            v = st.session_state.one_rm[lift]
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:0.3rem 0;border-bottom:1px solid #151518;font-size:0.83rem;'><span style='color:#666;'>{lift}</span><span style='font-family:Space Grotesk,sans-serif;font-weight:700;color:{color};'>{'—' if v==0 else f'{v:.1f} kg'}</span></div>", unsafe_allow_html=True)

        total = sum(st.session_state.one_rm.values())
        if total > 0:
            st.markdown(f"<div style='text-align:center;margin-top:0.6rem;padding:0.5rem;background:#0f0f12;border:1px solid #1a1a20;border-radius:6px;'><div style='font-size:0.6rem;color:#444;text-transform:uppercase;letter-spacing:0.1em;'>Total PL</div><div style='font-family:Space Grotesk,sans-serif;font-size:1.5rem;font-weight:700;color:#ff4d1c;'>{total:.1f} kg</div></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='sh'>Navegación</div>", unsafe_allow_html=True)
        for icon, pg in [("📅","Program"),("📊","Calculator"),("📈","Progress"),("🗂️","Templates")]:
            if st.button(f"{icon}  {pg}", key=f"nav_{pg}", use_container_width=True):
                st.session_state.active_page = pg; st.rerun()
        st.markdown("---")
        if st.button("🚪  Cerrar sesión", use_container_width=True):
            save_user_data(username)
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

    page = st.session_state.get("active_page","Program")
    st.markdown(f"""
    <div style='font-family:Space Grotesk,sans-serif;font-size:2rem;font-weight:700;letter-spacing:-0.02em;color:#e8e8e8;margin-bottom:0.1rem;'>
      <span style='color:#ff4d1c;'>Iron</span> Protocol
      <span style='font-size:0.9rem;font-weight:400;color:#444;margin-left:0.5rem;'>/ {page}</span>
    </div>
    <div style='font-size:0.72rem;color:#444;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:1.2rem;'>
      Powerlifting Training OS · {display_name}
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    # ════════════════════════════════════════════════════════
    #  PROGRAM PAGE — 3 column day layout
    # ════════════════════════════════════════════════════════
    if page == "Program":
        weeks = st.session_state.weeks
        missing = [l for l in LIFTS if st.session_state.one_rm[l]==0]
        if missing:
            st.warning(f"⚠ 1RM no configurado para: **{', '.join(missing)}** — ve a Calculadora.")

        week_tabs = st.tabs([f"Semana {w.number}" for w in weeks])
        for wk_idx, (wk, tab) in enumerate(zip(weeks, week_tabs)):
            with tab:
                bc = PHASE_BADGE.get(wk.phase,"badge-accum")
                st.markdown(f"<span class='badge {bc}'>{wk.phase}</span><span style='font-size:0.78rem;color:#555;margin-left:0.6rem;'>{wk.volume_note}</span>", unsafe_allow_html=True)
                st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)

                # ── 3 column layout for DUP (1 col for linear)
                num_days = len(wk.days)
                day_cols = st.columns(num_days, gap="medium")

                for d_idx, (day, dcol) in enumerate(zip(wk.days, day_cols)):
                    with dcol:
                        day_colors = ["#4caf50","#64b5f6","#ff9800"]
                        dc = day_colors[d_idx % len(day_colors)]
                        st.markdown(f"""
                        <div style='border-top:3px solid {dc};background:#111116;border-radius:0 0 12px 12px;
                                    padding:1rem;margin-bottom:0.5rem;min-height:500px;'>
                          <div style='font-family:Space Grotesk,sans-serif;font-size:0.75rem;font-weight:700;
                                      letter-spacing:0.12em;text-transform:uppercase;color:{dc};
                                      margin-bottom:0.8rem;padding-bottom:0.5rem;border-bottom:1px solid #1a1a20;'>
                            {day.label}
                          </div>
                        """, unsafe_allow_html=True)

                        # Main lifts
                        st.markdown("<div style='font-size:0.65rem;color:#444;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;'>⬛ Levantamientos Principales</div>", unsafe_allow_html=True)
                        for ex_idx, ex in enumerate(day.exercises):
                            render_main_lift(ex, wk_idx, d_idx, ex_idx, username)

                        st.markdown("</div>", unsafe_allow_html=True)

                        # Accessories below each column
                        slots = ACC_SLOTS.get(day.acc_key, [])
                        if slots:
                            st.markdown(f"<div style='font-size:0.65rem;color:{dc};text-transform:uppercase;letter-spacing:0.1em;margin:0.8rem 0 0.4rem;'>⬜ Accesorios Científicos</div>", unsafe_allow_html=True)
                            for slot_idx, slot in enumerate(slots):
                                render_accessory_slot(slot, day.acc_key, slot_idx, username)

    # ════════════════════════════════════════════════════════
    #  CALCULATOR
    # ════════════════════════════════════════════════════════
    elif page == "Calculator":
        st.markdown("<div style='font-size:0.85rem;color:#666;margin-bottom:1.5rem;'>Promedio ponderado Epley 60% / Brzycki 40% — optimizado para rangos de Powerlifting.</div>", unsafe_allow_html=True)
        cf, cr = st.columns([1,1], gap="large")
        with cf:
            st.markdown("<div class='sh'>Input</div>", unsafe_allow_html=True)
            ls = st.selectbox("Movimiento", LIFTS, key="cl")
            wc, rc = st.columns(2)
            with wc: weight = st.number_input("Peso (kg)", 1.0, 500.0, 100.0, 2.5, key="cw")
            with rc: reps   = st.number_input("Reps", 1, 20, 5, 1, key="cr")
            st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
            if st.button("⚡ Calcular 1RM", use_container_width=True):
                st.session_state["calc_result"] = {"lift":ls,"weight":weight,"reps":reps,
                    "epley":epley(weight,reps),"brzycki":brzycki(weight,reps),"avg":weighted_1rm(weight,reps)}
            if "calc_result" in st.session_state:
                r = st.session_state.calc_result
                st.markdown("<div class='sh'>Resultados</div>", unsafe_allow_html=True)
                for col, lbl, val in zip(st.columns(3),["Epley","Brzycki","Prom. Ponderado"],[r["epley"],r["brzycki"],r["avg"]]):
                    with col:
                        st.markdown(f"<div class='mc'><div class='mc-label'>{lbl}</div><div class='mc-val'>{val:.1f}</div><div class='mc-unit'>kg</div></div>", unsafe_allow_html=True)
                st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
                if st.button(f"💾 Guardar {r['avg']:.1f} kg como 1RM — {r['lift']}", use_container_width=True):
                    st.session_state.one_rm[r["lift"]] = r["avg"]
                    save_user_data(username)
                    st.success(f"✅ {r['lift']} 1RM → {r['avg']:.1f} kg guardado en Supabase.")
        with cr:
            st.markdown("<div class='sh'>Tabla de Porcentajes</div>", unsafe_allow_html=True)
            base = st.session_state.one_rm.get(ls,0)
            if "calc_result" in st.session_state and st.session_state.calc_result.get("lift")==ls:
                base = st.session_state.calc_result["avg"]
            if base > 0:
                rows = [{"% 1RM":f"{p}%","Carga (kg)":f"{pct_to_kg(base,p):.1f}",
                         "Zona":("Calentamiento" if p<=60 else "Hipertrofia" if p<=72 else "Fuerza" if p<=82 else "Intensificación" if p<=90 else "Pico")}
                        for p in [50,55,60,65,70,75,77.5,80,82.5,85,87.5,90,92.5,95,100]]
                st.markdown(pd.DataFrame(rows).to_html(index=False,classes="tbl",border=0), unsafe_allow_html=True)
            else:
                st.info("Calcula un 1RM para ver la tabla.")
            st.markdown("<div class='sh'>Override Manual</div>", unsafe_allow_html=True)
            for lift in LIFTS:
                cur = float(st.session_state.one_rm[lift])
                nv  = st.number_input(f"{lift} 1RM (kg)", 0.0, 500.0, cur, 2.5, key=f"m_{lift}")
                if nv != cur:
                    st.session_state.one_rm[lift] = nv; save_user_data(username)

    # ════════════════════════════════════════════════════════
    #  PROGRESS
    # ════════════════════════════════════════════════════════
    elif page == "Progress":
        weeks = st.session_state.weeks
        st.markdown("<div style='font-size:0.85rem;color:#666;margin-bottom:1.5rem;'>Motor de auto-regulación. Registra tu RPE real post-sesión y el sistema ajusta cargas para la próxima semana.</div>", unsafe_allow_html=True)
        wk_opts = {f"Semana {w.number} — {w.phase}": w for w in weeks}
        cw = wk_opts[st.selectbox("Semana a evaluar", list(wk_opts.keys()))]
        st.markdown(f"<div style='background:#111116;border:1px solid #1e1e25;border-radius:8px;padding:0.7rem 1rem;margin-bottom:1rem;font-size:0.82rem;color:#666;'><strong style='color:#ccc;'>{cw.phase}</strong> — {cw.volume_note}</div>", unsafe_allow_html=True)

        for lift in LIFTS:
            pc = {"Squat":"#4caf50","Bench Press":"#64b5f6","Deadlift":"#ff9800"}[lift]
            with st.expander(f"{lift}", expanded=True):
                c1,c2,c3 = st.columns(3)
                with c1:
                    rv = st.slider("RPE Real",5.0,10.0,8.0,0.5,key=f"rp_{cw.number}_{lift}_{username}")
                    rp = (rv-5)/5*100
                    rc2 = "#4caf50" if rv<=7 else "#ff9800" if rv<=9 else "#ef5350"
                    st.markdown(f"<div style='height:5px;background:#1a1a20;border-radius:3px;margin-top:4px;'><div style='width:{rp}%;height:5px;background:{rc2};border-radius:3px;'></div></div><div style='font-size:0.68rem;color:#555;margin-top:2px;'>RPE {rv:.1f}</div>", unsafe_allow_html=True)
                with c2:
                    ri = st.selectbox("RIR",[0,1,2,3,4,5],key=f"ri_{cw.number}_{lift}_{username}")
                with c3:
                    comp = st.radio("Series completadas",["Sí","No"],key=f"co_{cw.number}_{lift}_{username}",horizontal=True)=="Sí"
                rk = f"rec_{cw.number}_{lift}"
                if st.button(f"Analizar {lift}", key=f"ab_{rk}_{username}", use_container_width=True):
                    st.session_state.recommendations[rk] = full_recommendation(lift, rv, ri, comp, cw.phase)
                    save_user_data(username)
                if rk in st.session_state.recommendations:
                    rec = st.session_state.recommendations[rk]
                    cls = rec["verdict"]
                    bc2  = {"ok":"#0f1a0f","warn":"#1a1000","danger":"#1a0808"}[cls]
                    blc = {"ok":"#4caf50","warn":"#ff9800","danger":"#ef5350"}[cls]
                    tc  = {"ok":"#4caf50","warn":"#ff9800","danger":"#ef5350"}[cls]
                    st.markdown(f"<div style='background:{bc2};border:1px solid #222;border-left:3px solid {blc};border-radius:8px;padding:0.9rem 1rem;margin-top:0.5rem;'><div style='font-weight:700;font-size:0.85rem;color:{tc};margin-bottom:0.3rem;'>{rec['title']}</div><div style='font-size:0.8rem;color:#999;line-height:1.5;'>{rec['text']}</div><div style='margin-top:0.5rem;font-family:Space Grotesk,sans-serif;font-weight:700;font-size:0.9rem;color:{tc};'>{rec['action']}</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='sh'>Total Powerlifting</div>", unsafe_allow_html=True)
        mc_cols = st.columns(4)
        for i,(lift,color) in enumerate(zip(LIFTS,["#4caf50","#64b5f6","#ff9800"])):
            v = st.session_state.one_rm[lift]
            with mc_cols[i]:
                st.markdown(f"<div class='mc'><div class='mc-label'>{lift}</div><div class='mc-val' style='color:{color};'>{'—' if v==0 else f'{v:.1f}'}</div><div class='mc-unit'>kg</div></div>", unsafe_allow_html=True)
        total = sum(st.session_state.one_rm.values())
        with mc_cols[3]:
            st.markdown(f"<div class='mc'><div class='mc-label'>Total PL</div><div class='mc-val'>{total:.1f if total>0 else '—'}</div><div class='mc-unit'>kg</div></div>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    #  TEMPLATES
    # ════════════════════════════════════════════════════════
    elif page == "Templates":
        st.markdown("<div style='font-size:0.85rem;color:#666;margin-bottom:1.5rem;'>Selecciona un sistema de periodización científico. Los 1RMs se preservan al cambiar de plantilla.</div>", unsafe_allow_html=True)
        tpls = {
            "DUP":{"name":"Periodización Ondulante Diaria","abbr":"DUP",
                   "desc":"3 días/semana con estímulos rotativos (hipertrofia, fuerza, potencia). Maximiza frecuencia y especificidad. Zourdos & Apel (2010).",
                   "tags":["3×/sem","Alta Frecuencia","Intermedio–Avanzado"],"stats":{"Sesiones":3,"Semanas":4,"Intensidad":"65–90%"}},
            "Linear":{"name":"Bloque de Intensificación Lineal","abbr":"LP",
                      "desc":"Progresión clásica lineal. Ideal para base de fuerza o peaking pre-competencia. Método de esfuerzo máximo (Zatsiorsky, 2003).",
                      "tags":["2–3×/sem","Frecuencia Moderada","Principiante–Inter."],"stats":{"Sesiones":"2–3","Semanas":4,"Intensidad":"75–95%"}},
        }
        for tk, tpl in tpls.items():
            ia = st.session_state.template == tk
            c1,c2 = st.columns([2,1],gap="large")
            with c1:
                ab = "<span style='font-size:0.68rem;color:#ff4d1c;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;'>● ACTIVA</span>" if ia else ""
                st.markdown(f"<div style='background:#111116;border:1px solid {'#ff4d1c' if ia else '#1e1e25'};border-radius:12px;padding:1.2rem 1.4rem;'><div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:0.5rem;'><div style='font-family:Space Grotesk,sans-serif;font-size:1.8rem;font-weight:900;color:#ff4d1c;opacity:{'1' if ia else '0.35'};'>{tpl['abbr']}</div><div><div style='font-family:Space Grotesk,sans-serif;font-size:1rem;font-weight:700;margin-bottom:0.1rem;'>{tpl['name']}</div>{ab}</div></div><div style='font-size:0.82rem;color:#666;line-height:1.5;margin-bottom:0.5rem;'>{tpl['desc']}</div><div>{''.join(f'<span style=display:inline-block;font-size:0.62rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:0.1rem 0.4rem;border-radius:3px;margin-right:4px;background:#16161c;color:#666;border:1px solid #222;>{t}</span>' for t in tpl['tags'])}</div></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div style='background:#111116;border:1px solid #1e1e25;border-radius:10px;padding:0.9rem 1rem;'>{''.join(f'<div style=display:flex;justify-content:space-between;padding:0.3rem 0;border-bottom:1px solid #141418;font-size:0.82rem;><span style=color:#555;>{k}</span><span style=font-weight:700;color:#ccc;>{v}</span></div>' for k,v in tpl['stats'].items())}</div>", unsafe_allow_html=True)
            if not ia:
                if st.button(f"📥 Cargar {tpl['abbr']}", key=f"lt_{tk}_{username}"):
                    st.session_state.template = tk
                    st.session_state.weeks = build_dup_template() if tk=="DUP" else build_linear_template()
                    st.session_state.pct_overrides = {}; st.session_state.recommendations = {}
                    save_user_data(username)
                    st.success(f"✅ {tpl['name']} cargada.")
            else:
                st.markdown("<div style='font-size:0.82rem;color:#4caf50;padding:0.3rem 0;'>✓ Activa</div>", unsafe_allow_html=True)
            st.markdown("---")

        st.markdown("<div class='sh'>Base Científica — Categorías de Accesorios</div>", unsafe_allow_html=True)
        cats = [
            ("Empuje Vertical","Deltoides anterior + tríceps largo. Transferencia al Bench Press y estabilidad overhead.","#64b5f6"),
            ("Tracción Vertical","Dorsales + bíceps. Setup del Deadlift, estabilidad escapular en Bench.","#4caf50"),
            ("Tracción Horizontal","Retractores escapulares. Equilibrio muscular esencial para el Bench pesado.","#4caf50"),
            ("Bisagra de Cadera","Glúteos + erectores. Limitante primario en el Deadlift pesado.","#ff9800"),
            ("Cuádriceps","Fuerza unilateral de cuádriceps. Salida del hoyo en el Squat.","#ab47bc"),
            ("Core Anti-Rotación","Rigidez de núcleo = transmisión de fuerza eficiente en SBD.","#f06292"),
            ("Hombro / Estabilidad","Manguito rotador. Prevención de lesiones, mantiene arco en Bench.","#26c6da"),
            ("Grip / Antebrazo","Fuerza de agarre — limitante subestimado en Deadlift sin straps.","#ff7043"),
        ]
        gc = st.columns(4)
        for i,(name,desc,color) in enumerate(cats):
            with gc[i%4]:
                st.markdown(f"<div style='background:#111116;border:1px solid #1e1e25;border-top:2px solid {color};border-radius:8px;padding:0.7rem 0.8rem;margin-bottom:0.5rem;'><div style='font-size:0.72rem;font-weight:700;color:{color};text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3rem;'>{name}</div><div style='font-size:0.72rem;color:#555;line-height:1.4;'>{desc}</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════
if not st.session_state.authenticated:
    render_login()
else:
    render_app()
