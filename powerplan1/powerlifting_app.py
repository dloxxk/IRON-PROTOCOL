"""
╔══════════════════════════════════════════════════════════════╗
║          IRON PROTOCOL — Powerlifting Training Manager        ║
║    Multi-User · Supabase · Streamlit Community Cloud         ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import hashlib
import json
from dataclasses import dataclass
from supabase import create_client, Client

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Iron Protocol",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────────────────────────

DARK_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=Space+Grotesk:wght@400;700&display=swap');
  html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0d0f; color: #e8e8e8; font-family: 'Inter', sans-serif;
  }
  [data-testid="stSidebar"] { background-color: #111114; border-right: 1px solid #1f1f24; }
  .app-title { font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 700; letter-spacing: -0.03em; color: #e8e8e8; line-height: 1.1; margin-bottom: 0.1rem; }
  .app-subtitle { font-size: 0.82rem; color: #666; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 1.6rem; }
  .accent { color: #ff4d1c; }
  .section-header { font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: #aaa; border-bottom: 1px solid #1f1f24; padding-bottom: 0.4rem; margin-bottom: 1rem; margin-top: 1.4rem; }
  .metric-card { background: #14141a; border: 1px solid #1f1f24; border-radius: 10px; padding: 1rem 1.2rem; text-align: center; }
  .metric-label { font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: #666; margin-bottom: 0.25rem; }
  .metric-value { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: #ff4d1c; line-height: 1; }
  .metric-unit { font-size: 0.8rem; color: #888; margin-top: 0.15rem; }
  .week-card { background: #111114; border: 1px solid #1f1f24; border-radius: 12px; padding: 1.1rem 1.3rem; margin-bottom: 0.8rem; }
  .week-badge { display: inline-block; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.15rem 0.55rem; border-radius: 4px; margin-bottom: 0.5rem; }
  .badge-accum  { background: #1a2a1a; color: #4caf50; border: 1px solid #2d4a2d; }
  .badge-intens { background: #2a1a0a; color: #ff9800; border: 1px solid #4a2d00; }
  .badge-deload { background: #1a1a2a; color: #64b5f6; border: 1px solid #1a2a4a; }
  .badge-peak   { background: #2a0a0a; color: #ef5350; border: 1px solid #4a1a1a; }
  .rec-box { background: #0f1a0f; border: 1px solid #2d4a2d; border-left: 3px solid #4caf50; border-radius: 8px; padding: 1rem 1.2rem; margin-top: 0.8rem; }
  .rec-box.warn   { background: #1a0f00; border-color: #4a2d00; border-left-color: #ff9800; }
  .rec-box.danger { background: #1a0808; border-color: #4a1a1a; border-left-color: #ef5350; }
  .rec-title { font-weight: 700; font-size: 0.88rem; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.4rem; }
  .rec-ok  { color: #4caf50; } .rec-warn { color: #ff9800; } .rec-bad { color: #ef5350; }
  .styled-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
  .styled-table th { background: #0d0d0f; color: #666; text-transform: uppercase; font-size: 0.7rem; letter-spacing: 0.1em; padding: 0.5rem 0.8rem; border-bottom: 1px solid #1f1f24; text-align: left; }
  .styled-table td { padding: 0.45rem 0.8rem; border-bottom: 1px solid #191919; color: #ccc; }
  .styled-table tr:last-child td { border-bottom: none; }
  .styled-table tr:hover td { background: #141418; }
  .kg-cell { font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #ff4d1c; font-size: 1rem; }
  div[data-testid="stNumberInput"] input, div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] select { background-color: #14141a !important; color: #e8e8e8 !important; border: 1px solid #1f1f24 !important; }
  .stButton > button { background-color: #ff4d1c; color: #fff; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.06em; text-transform: uppercase; border: none; border-radius: 6px; padding: 0.5rem 1.2rem; transition: background 0.15s; }
  .stButton > button:hover { background-color: #e63d0f; }
  div[data-testid="stTabs"] button { color: #888; font-weight: 600; font-size: 0.82rem; letter-spacing: 0.06em; text-transform: uppercase; }
  div[data-testid="stTabs"] button[aria-selected="true"] { color: #ff4d1c; border-bottom-color: #ff4d1c; }
  hr { border-color: #1f1f24; }
  .lift-pill { display: inline-block; padding: 0.05rem 0.5rem; border-radius: 12px; font-size: 0.75rem; font-weight: 700; margin-right: 4px; }
  .squat-pill { background: #1a2a1a; color: #4caf50; }
  .bench-pill { background: #1a1a2a; color: #64b5f6; }
  .dead-pill  { background: #2a1a0a; color: #ff9800; }
  .spacer { margin-top: 1rem; }
  .rpe-bar-wrap { height: 6px; background: #1a1a1f; border-radius: 3px; margin-top: 4px; }
  .rpe-bar { height: 6px; border-radius: 3px; }
  .tag { display: inline-block; font-size: 0.65rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; padding: 0.12rem 0.45rem; border-radius: 3px; margin-right: 4px; margin-top: 8px; background: #1a1a1f; color: #888; border: 1px solid #2a2a2f; }
  .template-card { background: #111114; border: 1px solid #1f1f24; border-radius: 12px; padding: 1.2rem 1.4rem; height: 100%; }
  .template-name { font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.3rem; }
  .template-desc { font-size: 0.82rem; color: #888; line-height: 1.5; }
  .user-badge { display: inline-flex; align-items: center; gap: 0.4rem; background: #1a1a1f; border: 1px solid #2a2a2f; border-radius: 20px; padding: 0.25rem 0.7rem; font-size: 0.8rem; color: #aaa; }
  .user-dot { width: 8px; height: 8px; border-radius: 50%; background: #ff4d1c; display: inline-block; }
  .login-error { background: #1a0808; border: 1px solid #4a1a1a; border-left: 3px solid #ef5350; border-radius: 6px; padding: 0.6rem 0.9rem; font-size: 0.82rem; color: #ef5350; margin-bottom: 1rem; }
  .save-indicator { font-size: 0.72rem; color: #4caf50; text-align: right; margin-top: 2px; }
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SUPABASE CLIENT  (credentials from st.secrets)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_resource
def get_supabase() -> Client:
    url  = st.secrets["SUPABASE_URL"]
    key  = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase()

# ─────────────────────────────────────────────────────────────────────────────
#  AUTH HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def verify_login(username: str, password: str):
    """
    Returns (display_name, None) on success, (None, error_msg) on failure.
    Queries Supabase users table.
    """
    try:
        res = (
            supabase.table("users")
            .select("username, display_name, password_hash")
            .eq("username", username.strip().lower())
            .single()
            .execute()
        )
        user = res.data
        if not user:
            return None, "Usuario no encontrado."
        if user["password_hash"] != _hash(password):
            return None, "Contraseña incorrecta."
        return user["display_name"], None
    except Exception as e:
        return None, f"Error de conexión: {e}"

# ─────────────────────────────────────────────────────────────────────────────
#  PERSISTENT DATA HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def load_user_data(username: str) -> dict:
    """Load user's training data from Supabase."""
    try:
        res = (
            supabase.table("user_data")
            .select("one_rm, template, pct_overrides, recommendations")
            .eq("username", username)
            .single()
            .execute()
        )
        d = res.data
        if not d:
            return _default_data()
        return {
            "one_rm":          d.get("one_rm")          or {"Squat": 0.0, "Bench Press": 0.0, "Deadlift": 0.0},
            "template":        d.get("template")         or "DUP",
            "pct_overrides":   d.get("pct_overrides")    or {},
            "recommendations": d.get("recommendations")  or {},
        }
    except Exception:
        return _default_data()

def _default_data() -> dict:
    return {
        "one_rm":          {"Squat": 0.0, "Bench Press": 0.0, "Deadlift": 0.0},
        "template":        "DUP",
        "pct_overrides":   {},
        "recommendations": {},
    }

def save_user_data(username: str):
    """Upsert current session training data to Supabase."""
    try:
        payload = {
            "username":        username,
            "one_rm":          dict(st.session_state.one_rm),
            "template":        st.session_state.template,
            "pct_overrides":   dict(st.session_state.pct_overrides),
            "recommendations": dict(st.session_state.recommendations),
            "updated_at":      "now()",
        }
        supabase.table("user_data").upsert(payload, on_conflict="username").execute()
    except Exception as e:
        st.toast(f"⚠ Error al guardar: {e}", icon="⚠")

# ─────────────────────────────────────────────────────────────────────────────
#  DATA MODELS
# ─────────────────────────────────────────────────────────────────────────────

LIFTS = ["Squat", "Bench Press", "Deadlift"]

@dataclass
class SetConfig:
    pct: float
    sets: int
    reps: int
    rpe_target: int

@dataclass
class Exercise:
    name: str
    lift: str
    sets_config: list
    notes: str = ""

@dataclass
class TrainingDay:
    label: str
    exercises: list

@dataclass
class Week:
    number: int
    phase: str
    days: list
    volume_note: str = ""

# ─────────────────────────────────────────────────────────────────────────────
#  TEMPLATE BUILDERS
# ─────────────────────────────────────────────────────────────────────────────

def build_dup_template():
    dup_schedule = [
        {"Squat":[(67,4,8,7),(75,3,5,8),(80,3,3,8)],"Bench Press":[(65,4,8,7),(73,3,5,8),(78,3,3,8)],"Deadlift":[(65,3,6,7),(73,3,4,8),(80,2,3,8)]},
        {"Squat":[(70,4,8,7),(77,3,5,8),(82,3,3,8)],"Bench Press":[(68,4,8,7),(75,3,5,8),(80,3,3,8)],"Deadlift":[(68,3,6,7),(76,3,4,8),(82,2,3,8)]},
        {"Squat":[(72,4,6,8),(80,3,4,8),(85,3,2,9)],"Bench Press":[(70,4,6,8),(78,3,4,8),(83,3,2,9)],"Deadlift":[(70,3,5,8),(79,3,3,8),(85,2,2,9)]},
        {"Squat":[(60,3,5,6),(65,3,3,6),(68,2,2,7)],"Bench Press":[(58,3,5,6),(63,3,3,6),(66,2,2,7)],"Deadlift":[(58,2,4,6),(63,2,3,6),(66,1,2,7)]},
    ]
    day_labels = ["Day A — Hypertrophy Focus","Day B — Strength Focus","Day C — Power / Peaking"]
    phases = ["Accumulation","Accumulation","Intensification","Deload"]
    vol_notes = [
        "High volume, moderate intensity. Build work capacity.",
        "Moderate volume increase. Technical precision is key.",
        "Volume drops, intensity spikes. Approach near-maximal loads.",
        "Active recovery. Reduce load & volume. Restore readiness.",
    ]
    accessories = {
        "Day A — Hypertrophy Focus":[
            Exercise("Bulgarian Split Squat","Accessory",[SetConfig(0,3,10,7)],"Unilateral quad/glute development"),
            Exercise("Dumbbell Romanian Deadlift","Accessory",[SetConfig(0,3,10,7)],"Hamstring accessory"),
            Exercise("Dumbbell Incline Press","Accessory",[SetConfig(0,3,10,7)],"Chest accessory volume"),
        ],
        "Day B — Strength Focus":[
            Exercise("Pause Squat (2s)","Accessory",[SetConfig(0,3,3,8)],"Paused at bottom — strength out of hole"),
            Exercise("Close-Grip Bench Press","Accessory",[SetConfig(0,3,5,8)],"Tricep strength carryover"),
            Exercise("Barbell Row","Accessory",[SetConfig(0,4,6,7)],"Upper back — essential for bench & deadlift"),
        ],
        "Day C — Power / Peaking":[
            Exercise("Box Squat (light)","Accessory",[SetConfig(0,3,2,7)],"Speed work — rate of force development"),
            Exercise("Weighted Pull-Up","Accessory",[SetConfig(0,3,5,8)],"Lat strength — deadlift setup"),
            Exercise("Overhead Press","Accessory",[SetConfig(0,3,5,8)],"Shoulder stability for bench"),
        ],
    }
    weeks = []
    for wk_idx in range(4):
        days = []
        sched = dup_schedule[wk_idx]
        for d_idx, d_label in enumerate(day_labels):
            exs = []
            for lift in LIFTS:
                pct, sets, reps, rpe = sched[lift][d_idx]
                exs.append(Exercise(lift,lift,[SetConfig(pct,1,reps,rpe)]*sets,f"{reps} reps × {sets} sets @ {pct}% 1RM"))
            exs.extend(accessories[d_label])
            days.append(TrainingDay(d_label, exs))
        weeks.append(Week(wk_idx+1, phases[wk_idx], days, vol_notes[wk_idx]))
    return weeks

def build_linear_template():
    linear_schedule = [
        {"Squat":(75,4,5,7),"Bench Press":(73,4,5,7),"Deadlift":(75,3,5,7)},
        {"Squat":(80,3,4,8),"Bench Press":(78,3,4,8),"Deadlift":(80,3,4,8)},
        {"Squat":(85,3,3,8),"Bench Press":(83,3,3,8),"Deadlift":(85,2,3,8)},
        {"Squat":(62,2,3,6),"Bench Press":(60,2,3,6),"Deadlift":(60,2,2,6)},
    ]
    phases = ["Accumulation","Intensification","Intensification","Deload"]
    vol_notes = [
        "Foundation week. Dial in technique, build fatigue base.",
        "Load increases. 4×4 — dense, powerful training stimulus.",
        "Heavy triples. Near-competition intensities. Stay technical.",
        "Deload — clear fatigue before assessment or next block.",
    ]
    accessory_pool = [
        Exercise("Leg Press","Accessory",[SetConfig(0,3,10,7)],"Quad hypertrophy without spinal load"),
        Exercise("Chest-Supported Row","Accessory",[SetConfig(0,3,8,7)],"Upper back without fatigue carryover"),
        Exercise("Tricep Pushdown","Accessory",[SetConfig(0,3,12,7)],"Elbow extension hypertrophy"),
    ]
    weeks = []
    for wk_idx in range(4):
        sched = linear_schedule[wk_idx]
        exs = []
        for lift in LIFTS:
            pct, sets, reps, rpe = sched[lift]
            exs.append(Exercise(lift,lift,[SetConfig(pct,1,reps,rpe)]*sets,f"{sets}×{reps} @ {pct}% 1RM | RPE target {rpe}"))
        if wk_idx < 3:
            exs.extend(accessory_pool[:3])
        weeks.append(Week(wk_idx+1, phases[wk_idx],[TrainingDay("Full SBD Session", exs)],vol_notes[wk_idx]))
    return weeks

# ─────────────────────────────────────────────────────────────────────────────
#  1RM MATH
# ─────────────────────────────────────────────────────────────────────────────

def epley(w, r):
    return w if r == 1 else w * (1 + r / 30)

def brzycki(w, r):
    return w if r == 1 else w * (36 / (37 - r))

def weighted_1rm(w, r):
    return round(0.6 * epley(w, r) + 0.4 * brzycki(w, r), 1)

def pct_to_kg(orm, pct):
    return round((orm * pct / 100) / 2.5) * 2.5

# ─────────────────────────────────────────────────────────────────────────────
#  AUTO-REGULATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def generate_recommendation(lift, rpe_actual, rir, completed, week_phase):
    if not completed and rpe_actual >= 10:
        return {"verdict":"danger","title":"⚠ Overreach Detected — Adaptive Deload",
                "text":f"Absolute failure o RPE 10 en {lift}. Reducir volumen 30%, próxima sesión ≤75% 1RM. La fatiga está enmascarando el fitness.","action":"DELOAD"}
    elif not completed and rpe_actual >= 9:
        return {"verdict":"warn","title":"⚡ Near-Failure — Maintain & Monitor",
                "text":f"{lift}: series incompletas @ RPE {rpe_actual:.1f}. Mantener peso. Revisar sueño, nutrición y volumen semanal.","action":"MAINTAIN"}
    elif completed and rpe_actual < 7:
        inc = 5.0 if rpe_actual < 6 else 2.5
        return {"verdict":"ok","title":f"✅ Submaximal — Aumentar Carga {inc}%",
                "text":f"{lift}: todas las series completadas @ RPE {rpe_actual:.1f}, {rir} RIR restantes. Reserva significativa detectada. Aumentar ~{inc}%.","action":f"+{inc}%"}
    elif completed and rpe_actual <= 8.5:
        return {"verdict":"ok","title":"✅ On Target — Continuar Progresión Planificada",
                "text":f"{lift}: RPE {rpe_actual:.1f}, {rir} RIR. Alineación perfecta con el objetivo. Proceder con el peso planificado.","action":"PLANNED +2.5%"}
    elif completed and rpe_actual <= 9.5:
        return {"verdict":"warn","title":"⚡ Alto Esfuerzo — Mantener Peso",
                "text":f"{lift}: completado @ RPE {rpe_actual:.1f} — señal de fatiga acumulada alta. NO aumentar carga. Re-evaluar próxima semana.","action":"MAINTAIN"}
    else:
        return {"verdict":"warn","title":"⚡ Esfuerzo Máximo — Recuperar",
                "text":f"{lift}: series completadas @ RPE absoluto {rpe_actual:.1f}. Mantener peso, priorizar recuperación. 2 semanas consecutivas → deload.","action":"MAINTAIN"}

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE BOOTSTRAP
# ─────────────────────────────────────────────────────────────────────────────

for k, v in [("authenticated", False), ("current_user", None),
             ("display_name", None), ("login_error", "")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
#  LOGIN SCREEN
# ─────────────────────────────────────────────────────────────────────────────

def render_login():
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("""
        <div style='text-align:center; padding-top:3rem;'>
          <div style='font-family:Space Grotesk,sans-serif; font-size:2.4rem; font-weight:900; color:#e8e8e8; letter-spacing:-0.03em;'>
            🏋 <span style='color:#ff4d1c;'>IRON</span> PROTOCOL
          </div>
          <div style='font-size:0.72rem; color:#444; letter-spacing:0.16em; text-transform:uppercase; margin-bottom:2.5rem; margin-top:0.3rem;'>
            Powerlifting Training OS · Acceso privado
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.login_error:
            st.markdown(f"<div class='login-error'>⚠ {st.session_state.login_error}</div>", unsafe_allow_html=True)

        username = st.text_input("Usuario", placeholder="usuario1 / usuario2", key="login_user")
        password = st.text_input("Contraseña", type="password", placeholder="••••••••", key="login_pass")
        st.markdown("<div style='margin-top:0.3rem;'></div>", unsafe_allow_html=True)

        if st.button("Ingresar →", use_container_width=True):
            display_name, error = verify_login(username, password)
            if error:
                st.session_state.login_error = error
                st.rerun()
            else:
                uname = username.strip().lower()
                data  = load_user_data(uname)
                st.session_state.authenticated  = True
                st.session_state.current_user   = uname
                st.session_state.display_name   = display_name
                st.session_state.login_error    = ""
                st.session_state.one_rm         = data["one_rm"]
                st.session_state.template       = data["template"]
                st.session_state.pct_overrides  = data["pct_overrides"]
                st.session_state.recommendations= data["recommendations"]
                st.session_state.weeks          = (
                    build_dup_template() if data["template"] == "DUP"
                    else build_linear_template()
                )
                st.session_state.active_page    = "Calculator"
                st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────────────────────────────────────

def render_app():
    username     = st.session_state.current_user
    display_name = st.session_state.display_name

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style='padding:0.5rem 0 1rem 0;'>
          <div style='font-family:Space Grotesk,sans-serif; font-size:1.4rem; font-weight:700; color:#e8e8e8;'>
            🏋 <span style='color:#ff4d1c;'>IRON</span> PROTOCOL
          </div>
          <div style='margin-top:0.6rem;'>
            <span class='user-badge'><span class='user-dot'></span>{display_name}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<div class='section-header'>Active 1RMs</div>", unsafe_allow_html=True)
        for lift, color in [("Squat","#4caf50"),("Bench Press","#64b5f6"),("Deadlift","#ff9800")]:
            val = st.session_state.one_rm[lift]
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;padding:0.35rem 0;border-bottom:1px solid #1a1a1f;font-size:0.85rem;'>
              <span style='color:#888;'>{lift}</span>
              <span style='font-family:Space Grotesk,sans-serif;font-weight:700;color:{color};'>{"—" if val==0 else f"{val:.1f} kg"}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Navegación</div>", unsafe_allow_html=True)
        for icon, pg in [("📊","Calculator"),("📅","Program"),("📈","Progress"),("🗂️","Templates")]:
            if st.button(f"{icon}  {pg}", key=f"nav_{pg}", use_container_width=True):
                st.session_state.active_page = pg
                st.rerun()

        st.markdown("---")
        if st.button("🚪  Cerrar sesión", use_container_width=True):
            save_user_data(username)
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        st.markdown("<div style='font-size:0.65rem;color:#2a2a2a;text-align:center;margin-top:0.5rem;'>☁ Supabase · Datos persistentes</div>", unsafe_allow_html=True)

    # ── Header ────────────────────────────────────────────────────────────────
    page = st.session_state.get("active_page", "Calculator")
    st.markdown(f"""
    <div class='app-title'><span class='accent'>Iron</span> Protocol
      <span style='font-size:1rem;font-weight:400;color:#555;margin-left:0.5rem;'>/ {page}</span>
    </div>
    <div class='app-subtitle'>Powerlifting Training OS · {display_name} · SBD Focus</div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # ═════════════════════════════════════════════════════════════════════════
    #  CALCULATOR
    # ═════════════════════════════════════════════════════════════════════════
    if page == "Calculator":
        st.markdown("<div style='font-size:0.88rem;color:#888;margin-bottom:1.5rem;'>Calculadora 1RM — promedio ponderado Epley 60% / Brzycki 40%, optimizado para Powerlifting.</div>", unsafe_allow_html=True)
        col_form, col_results = st.columns([1,1], gap="large")

        with col_form:
            st.markdown("<div class='section-header'>Input</div>", unsafe_allow_html=True)
            lift_sel = st.selectbox("Movimiento", LIFTS, key="calc_lift")
            w_col, r_col = st.columns(2)
            with w_col:
                weight = st.number_input("Peso levantado (kg)", min_value=1.0, max_value=500.0, value=100.0, step=2.5, key="calc_weight")
            with r_col:
                reps = st.number_input("Repeticiones", min_value=1, max_value=20, value=5, step=1, key="calc_reps")

            st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
            if st.button("⚡ Calcular 1RM", use_container_width=True):
                st.session_state["calc_result"] = {
                    "lift":lift_sel,"weight":weight,"reps":reps,
                    "epley":epley(weight,reps),"brzycki":brzycki(weight,reps),"avg":weighted_1rm(weight,reps)
                }

            if "calc_result" in st.session_state:
                r = st.session_state.calc_result
                st.markdown("<div class='section-header'>Resultados</div>", unsafe_allow_html=True)
                for col, label, val in zip(st.columns(3),["Epley","Brzycki","Prom. Ponderado"],[r["epley"],r["brzycki"],r["avg"]]):
                    with col:
                        st.markdown(f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{val:.1f}</div><div class='metric-unit'>kg</div></div>", unsafe_allow_html=True)
                st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
                if st.button(f"💾 Guardar {r['avg']:.1f} kg como 1RM de {r['lift']}", use_container_width=True):
                    st.session_state.one_rm[r["lift"]] = r["avg"]
                    save_user_data(username)
                    st.success(f"✅ {r['lift']} 1RM guardado: **{r['avg']:.1f} kg** — sincronizado con Supabase.")

        with col_results:
            st.markdown("<div class='section-header'>Tabla de Porcentajes</div>", unsafe_allow_html=True)
            base = st.session_state.one_rm.get(lift_sel, 0)
            if "calc_result" in st.session_state and st.session_state.calc_result.get("lift") == lift_sel:
                base = st.session_state.calc_result["avg"]
            if base > 0:
                rows = [{"% 1RM":f"{pct}%","Carga (kg)":f"{pct_to_kg(base,pct):.1f}",
                         "Uso":("Calentamiento" if pct<=60 else "Volumen/Hiper." if pct<=72 else "Fuerza/Acum." if pct<=82 else "Intensificación" if pct<=90 else "Pico/Competencia")}
                        for pct in [50,55,60,65,70,75,77.5,80,82.5,85,87.5,90,92.5,95,100]]
                st.markdown(pd.DataFrame(rows).to_html(index=False,classes="styled-table",border=0), unsafe_allow_html=True)
            else:
                st.info("Calcula o ingresa un 1RM para ver la tabla.")

            st.markdown("<div class='section-header'>1RM Manual</div>", unsafe_allow_html=True)
            for lift in LIFTS:
                cur = float(st.session_state.one_rm[lift])
                new_val = st.number_input(f"{lift} 1RM (kg)", min_value=0.0, max_value=500.0, value=cur, step=2.5, key=f"manual_{lift}")
                if new_val != cur:
                    st.session_state.one_rm[lift] = new_val
                    save_user_data(username)

    # ═════════════════════════════════════════════════════════════════════════
    #  PROGRAM
    # ═════════════════════════════════════════════════════════════════════════
    elif page == "Program":
        weeks = st.session_state.weeks
        st.markdown(f"<div style='font-size:0.85rem;color:#888;margin-bottom:1rem;'>Plantilla activa: <strong style='color:#ccc;'>{st.session_state.template}</strong> · Bloque de {len(weeks)} semanas · Modifica los % — los kg se recalculan en tiempo real.</div>", unsafe_allow_html=True)

        missing = [l for l in LIFTS if st.session_state.one_rm[l] == 0]
        if missing:
            st.warning(f"⚠ 1RM no configurado para: **{', '.join(missing)}**. Ve a Calculadora.")

        PHASE_BADGE = {"Accumulation":"badge-accum","Intensification":"badge-intens","Deload":"badge-deload","Peak":"badge-peak"}
        week_tabs = st.tabs([f"Semana {w.number} — {w.phase}" for w in weeks])

        for wk_idx, (wk, tab) in enumerate(zip(weeks, week_tabs)):
            with tab:
                st.markdown(f"<span class='week-badge {PHASE_BADGE.get(wk.phase,'badge-accum')}'>{wk.phase}</span><span style='font-size:0.82rem;color:#666;margin-left:0.5rem;'>{wk.volume_note}</span>", unsafe_allow_html=True)

                for d_idx, day in enumerate(wk.days):
                    st.markdown(f"<div style='font-family:Space Grotesk,sans-serif;font-size:0.95rem;font-weight:700;color:#aaa;margin:1.2rem 0 0.7rem 0;letter-spacing:0.05em;text-transform:uppercase;'>{day.label}</div>", unsafe_allow_html=True)

                    for ex_idx, ex in enumerate(day.exercises):
                        is_main = ex.lift in LIFTS
                        orm_val = st.session_state.one_rm.get(ex.lift, 0)
                        pill_map = {"Squat":"<span class='lift-pill squat-pill'>SQUAT</span>","Bench Press":"<span class='lift-pill bench-pill'>BENCH</span>","Deadlift":"<span class='lift-pill dead-pill'>DEAD</span>"}
                        pill_html = pill_map.get(ex.lift,"") if is_main else "<span style='font-size:0.72rem;color:#555;text-transform:uppercase;'>accesorio</span>"
                        st.markdown(f"<div style='display:flex;align-items:center;gap:0.5rem;margin-bottom:0.3rem;'><span style='font-weight:700;font-size:0.92rem;color:{'#e8e8e8' if is_main else '#aaa'};'>{ex.name}</span>{pill_html}</div><div style='font-size:0.76rem;color:#555;margin-bottom:0.5rem;'>{ex.notes}</div>", unsafe_allow_html=True)

                        if is_main:
                            unique_set = ex.sets_config[0]
                            num_sets   = len(ex.sets_config)
                            hdr_cols   = st.columns([1.2,1.2,1.2,1.2,1.5])
                            for hdr, col in zip(["Set","Reps","% 1RM","RPE Obj.","Carga (kg)"], hdr_cols):
                                col.markdown(f"<div style='font-size:0.7rem;color:#555;text-transform:uppercase;padding-bottom:4px;'>{hdr}</div>", unsafe_allow_html=True)

                            changed = False
                            for s_idx in range(num_sets):
                                key = f"pct_{username}_{wk_idx}_{d_idx}_{ex_idx}_{s_idx}"
                                if key not in st.session_state.pct_overrides:
                                    st.session_state.pct_overrides[key] = float(unique_set.pct)
                                cols = st.columns([1.2,1.2,1.2,1.2,1.5])
                                cols[0].markdown(f"<div style='padding-top:8px;font-size:0.88rem;color:#666;'>Set {s_idx+1}</div>", unsafe_allow_html=True)
                                cols[1].markdown(f"<div style='padding-top:8px;font-size:0.88rem;color:#ccc;'>{unique_set.reps}</div>", unsafe_allow_html=True)
                                with cols[2]:
                                    new_pct = st.number_input("% 1RM",min_value=30.0,max_value=110.0,
                                        value=float(st.session_state.pct_overrides[key]),
                                        step=2.5, key=key, label_visibility="collapsed")
                                    if new_pct != st.session_state.pct_overrides[key]:
                                        st.session_state.pct_overrides[key] = new_pct
                                        changed = True
                                cols[3].markdown(f"<div style='padding-top:8px;font-size:0.88rem;color:#ff9800;'>RPE {unique_set.rpe_target}</div>", unsafe_allow_html=True)
                                with cols[4]:
                                    if orm_val > 0:
                                        kg = pct_to_kg(orm_val, st.session_state.pct_overrides[key])
                                        st.markdown(f"<div style='padding-top:6px;'><span class='kg-cell'>{kg:.1f} kg</span></div>", unsafe_allow_html=True)
                                    else:
                                        st.markdown("<div style='padding-top:8px;font-size:0.8rem;color:#444;'>Set 1RM</div>", unsafe_allow_html=True)
                            if changed:
                                save_user_data(username)
                        else:
                            cfg = ex.sets_config[0]
                            st.markdown(f"<div style='background:#0f0f12;border:1px solid #191919;border-radius:6px;padding:0.4rem 0.8rem;font-size:0.82rem;color:#666;display:inline-block;'>{len(ex.sets_config)} series × {cfg.reps} reps @ RPE {cfg.rpe_target}</div>", unsafe_allow_html=True)

                        st.markdown("<div style='margin-bottom:0.8rem;'></div>", unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    #  PROGRESS
    # ═════════════════════════════════════════════════════════════════════════
    elif page == "Progress":
        weeks = st.session_state.weeks
        st.markdown("<div style='font-size:0.88rem;color:#888;margin-bottom:1.5rem;'>Motor de auto-regulación basado en ciencia. Ingresa tus métricas reales — el sistema recomienda ajustes por levantamiento.</div>", unsafe_allow_html=True)

        week_options = {f"Semana {w.number} — {w.phase}": w for w in weeks}
        current_week = week_options[st.selectbox("Evaluar semana", list(week_options.keys()))]
        st.markdown(f"<div class='week-card' style='margin-top:0.5rem;'><div style='font-size:0.82rem;color:#888;'><strong style='color:#ccc;'>Fase {current_week.phase}</strong> — {current_week.volume_note}</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Evaluación por Levantamiento</div>", unsafe_allow_html=True)

        for lift in LIFTS:
            pill_cls = {"Squat":"squat-pill","Bench Press":"bench-pill","Deadlift":"dead-pill"}[lift]
            with st.expander(f"  {lift}", expanded=True):
                st.markdown(f"<span class='lift-pill {pill_cls}'>{lift.upper()}</span>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                with c1:
                    rpe_val = st.slider("RPE Alcanzado",5.0,10.0,8.0,0.5,key=f"rpe_{current_week.number}_{lift}_{username}")
                    rpe_pct = (rpe_val - 5) / 5 * 100
                    rpe_color = "#4caf50" if rpe_val<=7 else "#ff9800" if rpe_val<=9 else "#ef5350"
                    st.markdown(f"<div class='rpe-bar-wrap'><div class='rpe-bar' style='width:{rpe_pct}%;background:{rpe_color};'></div></div><div style='font-size:0.7rem;color:#666;margin-top:2px;'>RPE {rpe_val:.1f}</div>", unsafe_allow_html=True)
                with c2:
                    rir_val = st.selectbox("RIR (Reps en Recámara)",[0,1,2,3,4,5],key=f"rir_{current_week.number}_{lift}_{username}")
                with c3:
                    completed = st.radio("¿Series completadas?",["Sí","No"],key=f"comp_{current_week.number}_{lift}_{username}",horizontal=True)=="Sí"

                rec_key = f"rec_{current_week.number}_{lift}"
                if st.button(f"Generar Recomendación — {lift}", key=f"btn_{rec_key}_{username}", use_container_width=True):
                    rec = generate_recommendation(lift, rpe_val, rir_val, completed, current_week.phase)
                    st.session_state.recommendations[rec_key] = rec
                    save_user_data(username)

                if rec_key in st.session_state.recommendations:
                    rec = st.session_state.recommendations[rec_key]
                    cls = rec["verdict"]
                    box_cls   = {"ok":"","warn":"warn","danger":"danger"}[cls]
                    title_cls = {"ok":"rec-ok","warn":"rec-warn","danger":"rec-bad"}[cls]
                    a_color   = "#4caf50" if cls=="ok" else "#ff9800" if cls=="warn" else "#ef5350"
                    st.markdown(f"<div class='rec-box {box_cls}'><div class='rec-title {title_cls}'>{rec['title']}</div><div style='font-size:0.83rem;color:#aaa;line-height:1.55;'>{rec['text']}</div><div style='margin-top:0.6rem;'><span style='font-size:0.72rem;font-weight:700;text-transform:uppercase;color:#555;'>Acción:</span><span style='font-family:Space Grotesk,sans-serif;font-weight:700;font-size:0.88rem;color:{a_color};margin-left:0.4rem;'>{rec['action']}</span></div></div>", unsafe_allow_html=True)

        st.markdown("<div class='section-header'>Total Powerlifting</div>", unsafe_allow_html=True)
        for i, (lift, color) in enumerate(zip(LIFTS,["#4caf50","#64b5f6","#ff9800"])):
            val = st.session_state.one_rm[lift]
            with st.columns(3)[i]:
                st.markdown(f"<div class='metric-card'><div class='metric-label'>{lift}</div><div class='metric-value' style='color:{color};'>{'—' if val==0 else f'{val:.1f}'}</div><div class='metric-unit'>kg 1RM</div></div>", unsafe_allow_html=True)
        total = sum(st.session_state.one_rm.values())
        if total > 0:
            st.markdown(f"<div style='text-align:center;margin-top:1rem;padding:0.8rem;background:#111114;border:1px solid #1f1f24;border-radius:8px;'><div style='font-size:0.72rem;color:#555;text-transform:uppercase;letter-spacing:0.1em;'>Total Powerlifting</div><div style='font-family:Space Grotesk,sans-serif;font-size:2.4rem;font-weight:700;color:#ff4d1c;'>{total:.1f} kg</div></div>", unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    #  TEMPLATES
    # ═════════════════════════════════════════════════════════════════════════
    elif page == "Templates":
        st.markdown("<div style='font-size:0.88rem;color:#888;margin-bottom:1.5rem;'>Selecciona un sistema de entrenamiento científico. Cambiar plantilla preserva tus 1RMs.</div>", unsafe_allow_html=True)
        templates = {
            "DUP":{"name":"Periodización Ondulante Diaria (DUP)","abbr":"DUP",
                   "desc":"3×/semana con días rotativos: hipertrofia, fuerza, potencia. Maximiza frecuencia y especificidad. Zourdos & Apel (2010).",
                   "tags":["3×/semana","Alta Frecuencia","Intermedio–Avanzado","4 Semanas"],
                   "stats":{"Sesiones/sem":3,"Semanas":4,"Intensidad":"65–90%"}},
            "Linear":{"name":"Bloque de Intensificación Lineal","abbr":"LP",
                      "desc":"Progresión clásica semanal. Ideal para base de fuerza o pico pre-competencia. Método de esfuerzo máximo de Zatsiorsky.",
                      "tags":["2–3×/semana","Frecuencia Moderada","Principiante–Intermedio","4 Semanas"],
                      "stats":{"Sesiones/sem":"2–3","Semanas":4,"Intensidad":"75–95%"}},
        }
        for tpl_key, tpl in templates.items():
            is_active = st.session_state.template == tpl_key
            border = "border-color:#ff4d1c;" if is_active else ""
            c1, c2 = st.columns([2,1], gap="large")
            with c1:
                active_badge = "<span style='font-size:0.7rem;color:#ff4d1c;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;'>● Activa</span>" if is_active else ""
                st.markdown(f"<div class='template-card' style='{border}'><div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:0.5rem;'><div style='font-family:Space Grotesk,sans-serif;font-size:2rem;font-weight:900;color:#ff4d1c;opacity:{'1' if is_active else '0.4'};'>{tpl['abbr']}</div><div><div class='template-name'>{tpl['name']}</div>{active_badge}</div></div><div class='template-desc'>{tpl['desc']}</div><div>{''.join(f'<span class=tag>{t}</span>' for t in tpl['tags'])}</div></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='week-card' style='margin-top:0;'><div class='metric-label' style='margin-bottom:0.8rem;'>Stats</div>{''.join(f'<div style=display:flex;justify-content:space-between;padding:0.3rem 0;border-bottom:1px solid #191919;font-size:0.82rem;><span style=color:#666;>{k}</span><span style=font-weight:700;color:#ccc;>{v}</span></div>' for k,v in tpl['stats'].items())}</div>", unsafe_allow_html=True)
            if not is_active:
                if st.button(f"📥 Cargar {tpl['abbr']}", key=f"load_{tpl_key}_{username}"):
                    st.session_state.template = tpl_key
                    st.session_state.weeks = build_dup_template() if tpl_key=="DUP" else build_linear_template()
                    st.session_state.pct_overrides = {}
                    st.session_state.recommendations = {}
                    save_user_data(username)
                    st.success(f"✅ {tpl['name']} cargada y guardada en Supabase.")
            else:
                st.markdown("<div style='font-size:0.82rem;color:#4caf50;padding:0.4rem 0;'>✓ Plantilla activa</div>", unsafe_allow_html=True)
            st.markdown("---")

        st.markdown("<div class='section-header'>Principios Científicos</div>", unsafe_allow_html=True)
        for title, body in [
            ("Especificidad (SAID)","Las adaptaciones son específicas a las demandas impuestas. Entrena los levantamientos de competencia con frecuencia y cargas representativas."),
            ("Sobrecarga Progresiva","El estímulo debe aumentar con el tiempo. La app aplica incrementos sistémicos de % cada semana."),
            ("Auto-Regulación (RPE/RIR)","La disposición diaria varía. RPE y RIR permiten ajustar la intensidad según el rendimiento real."),
            ("Supercompensación","La fatiga debe gestionarse (deload) para que el fitness se exprese. El deload no es opcional — ahí se consolidan las ganancias."),
            ("Volumen MEV→MAV→MRV","Inicia en el Volumen Mínimo Efectivo, acumula hasta el Máximo Adaptativo, y descarga antes del Máximo Recuperable."),
        ]:
            st.markdown(f"<div style='background:#111114;border:1px solid #1a1a1f;border-radius:8px;padding:0.8rem 1rem;margin-bottom:0.6rem;'><div style='font-weight:700;font-size:0.85rem;color:#ccc;margin-bottom:0.25rem;'>{title}</div><div style='font-size:0.8rem;color:#666;line-height:1.55;'>{body}</div></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  ROUTER
# ─────────────────────────────────────────────────────────────────────────────

if not st.session_state.authenticated:
    render_login()
else:
    render_app()
