"""
╔══════════════════════════════════════════════════════════════╗
║          IRON PROTOCOL — Powerlifting Training Manager        ║
║    Full-Stack Powerlifting Science + Session Management       ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import math
from dataclasses import dataclass, field
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG & CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Iron Protocol",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DARK_CSS = """
<style>
  /* ── Base ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=Space+Grotesk:wght@400;700&display=swap');

  html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0d0f;
    color: #e8e8e8;
    font-family: 'Inter', sans-serif;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background-color: #111114;
    border-right: 1px solid #1f1f24;
  }

  /* ── Top bar title ── */
  .app-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #e8e8e8;
    line-height: 1.1;
    margin-bottom: 0.1rem;
  }
  .app-subtitle {
    font-size: 0.82rem;
    color: #666;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.6rem;
  }
  .accent { color: #ff4d1c; }

  /* ── Section headers ── */
  .section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #aaa;
    border-bottom: 1px solid #1f1f24;
    padding-bottom: 0.4rem;
    margin-bottom: 1rem;
    margin-top: 1.4rem;
  }

  /* ── Metric cards ── */
  .metric-card {
    background: #14141a;
    border: 1px solid #1f1f24;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
  }
  .metric-label {
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 0.25rem;
  }
  .metric-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #ff4d1c;
    line-height: 1;
  }
  .metric-unit {
    font-size: 0.8rem;
    color: #888;
    margin-top: 0.15rem;
  }

  /* ── Week cards ── */
  .week-card {
    background: #111114;
    border: 1px solid #1f1f24;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
  }
  .week-badge {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.15rem 0.55rem;
    border-radius: 4px;
    margin-bottom: 0.5rem;
  }
  .badge-accum  { background: #1a2a1a; color: #4caf50; border: 1px solid #2d4a2d; }
  .badge-intens { background: #2a1a0a; color: #ff9800; border: 1px solid #4a2d00; }
  .badge-deload { background: #1a1a2a; color: #64b5f6; border: 1px solid #1a2a4a; }
  .badge-peak   { background: #2a0a0a; color: #ef5350; border: 1px solid #4a1a1a; }

  /* ── Recommendation box ── */
  .rec-box {
    background: #0f1a0f;
    border: 1px solid #2d4a2d;
    border-left: 3px solid #4caf50;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-top: 0.8rem;
  }
  .rec-box.warn {
    background: #1a0f00;
    border-color: #4a2d00;
    border-left-color: #ff9800;
  }
  .rec-box.danger {
    background: #1a0808;
    border-color: #4a1a1a;
    border-left-color: #ef5350;
  }
  .rec-title {
    font-weight: 700;
    font-size: 0.88rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
  }
  .rec-ok    { color: #4caf50; }
  .rec-warn  { color: #ff9800; }
  .rec-bad   { color: #ef5350; }

  /* ── Table ── */
  .styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
  }
  .styled-table th {
    background: #0d0d0f;
    color: #666;
    text-transform: uppercase;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    padding: 0.5rem 0.8rem;
    border-bottom: 1px solid #1f1f24;
    text-align: left;
  }
  .styled-table td {
    padding: 0.45rem 0.8rem;
    border-bottom: 1px solid #191919;
    color: #ccc;
  }
  .styled-table tr:last-child td { border-bottom: none; }
  .styled-table tr:hover td { background: #141418; }
  .kg-cell {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    color: #ff4d1c;
    font-size: 1rem;
  }

  /* ── Streamlit element overrides ── */
  div[data-testid="stNumberInput"] input,
  div[data-testid="stTextInput"] input,
  div[data-testid="stSelectbox"] select {
    background-color: #14141a !important;
    color: #e8e8e8 !important;
    border: 1px solid #1f1f24 !important;
  }
  .stButton > button {
    background-color: #ff4d1c;
    color: #fff;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1.2rem;
    transition: background 0.15s;
  }
  .stButton > button:hover { background-color: #e63d0f; }
  .stButton > button:active { background-color: #cc3600; }

  div[data-testid="stTabs"] button {
    color: #888;
    font-weight: 600;
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #ff4d1c;
    border-bottom-color: #ff4d1c;
  }

  hr { border-color: #1f1f24; }

  .stAlert { background: #111114 !important; border-color: #1f1f24 !important; }
  .stSuccess { border-left-color: #4caf50 !important; }
  .stWarning { border-left-color: #ff9800 !important; }
  .stError   { border-left-color: #ef5350 !important; }

  /* ── Sidebar nav links ── */
  .nav-item {
    display: block;
    padding: 0.55rem 0.8rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
    color: #888;
    cursor: pointer;
    margin-bottom: 2px;
    transition: all 0.12s;
  }
  .nav-item:hover, .nav-item.active {
    background: #1a1a1f;
    color: #e8e8e8;
  }
  .nav-item.active { border-left: 2px solid #ff4d1c; color: #ff4d1c; }

  /* ── Template card ── */
  .template-card {
    background: #111114;
    border: 1px solid #1f1f24;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    height: 100%;
    transition: border-color 0.15s;
  }
  .template-card:hover { border-color: #333; }
  .template-card.selected { border-color: #ff4d1c; }
  .template-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
  }
  .template-desc { font-size: 0.82rem; color: #888; line-height: 1.5; }
  .tag {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.12rem 0.45rem;
    border-radius: 3px;
    margin-right: 4px;
    margin-top: 8px;
    background: #1a1a1f;
    color: #888;
    border: 1px solid #2a2a2f;
  }
  .lift-pill {
    display: inline-block;
    padding: 0.05rem 0.5rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-right: 4px;
  }
  .squat-pill  { background: #1a2a1a; color: #4caf50; }
  .bench-pill  { background: #1a1a2a; color: #64b5f6; }
  .dead-pill   { background: #2a1a0a; color: #ff9800; }
  .spacer { margin-top: 1rem; }

  /* ── RPE indicator ── */
  .rpe-bar-wrap { height: 6px; background: #1a1a1f; border-radius: 3px; margin-top: 4px; }
  .rpe-bar { height: 6px; border-radius: 3px; }
</style>
"""

st.markdown(DARK_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  DATA MODELS & CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

LIFTS = ["Squat", "Bench Press", "Deadlift"]

@dataclass
class SetConfig:
    pct: float  # % of 1RM
    sets: int
    reps: int
    rpe_target: int

@dataclass
class Exercise:
    name: str
    lift: str  # "Squat" | "Bench Press" | "Deadlift" | "Accessory"
    sets_config: list[SetConfig]
    notes: str = ""

@dataclass
class TrainingDay:
    label: str       # e.g. "Day A — Squat Focus"
    exercises: list[Exercise]

@dataclass
class Week:
    number: int
    phase: str  # "Accumulation" | "Intensification" | "Deload" | "Peak"
    days: list[TrainingDay]
    volume_note: str = ""

# ─── Template A: Daily Undulating Periodization (DUP) ────────────────────────

def build_dup_template() -> list[Week]:
    """
    DUP — 4-week block: 3×/week full SBD with rotating intensity
    Week 1-2: Accumulation (hypertrophy + strength days)
    Week 3:   Intensification
    Week 4:   Deload
    """
    weeks = []

    # Percentages per week per day-type
    # (hypertrophy_day, strength_day, power_day)
    dup_schedule = [
        # Wk1
        {
            "Squat":       [(67, 4, 8, 7), (75, 3, 5, 8), (80, 3, 3, 8)],
            "Bench Press": [(65, 4, 8, 7), (73, 3, 5, 8), (78, 3, 3, 8)],
            "Deadlift":    [(65, 3, 6, 7), (73, 3, 4, 8), (80, 2, 3, 8)],
        },
        # Wk2
        {
            "Squat":       [(70, 4, 8, 7), (77, 3, 5, 8), (82, 3, 3, 8)],
            "Bench Press": [(68, 4, 8, 7), (75, 3, 5, 8), (80, 3, 3, 8)],
            "Deadlift":    [(68, 3, 6, 7), (76, 3, 4, 8), (82, 2, 3, 8)],
        },
        # Wk3 — Intensification
        {
            "Squat":       [(72, 4, 6, 8), (80, 3, 4, 8), (85, 3, 2, 9)],
            "Bench Press": [(70, 4, 6, 8), (78, 3, 4, 8), (83, 3, 2, 9)],
            "Deadlift":    [(70, 3, 5, 8), (79, 3, 3, 8), (85, 2, 2, 9)],
        },
        # Wk4 — Deload
        {
            "Squat":       [(60, 3, 5, 6), (65, 3, 3, 6), (68, 2, 2, 7)],
            "Bench Press": [(58, 3, 5, 6), (63, 3, 3, 6), (66, 2, 2, 7)],
            "Deadlift":    [(58, 2, 4, 6), (63, 2, 3, 6), (66, 1, 2, 7)],
        },
    ]

    day_labels = [
        "Day A — Hypertrophy Focus",
        "Day B — Strength Focus",
        "Day C — Power / Peaking",
    ]
    phases = ["Accumulation", "Accumulation", "Intensification", "Deload"]
    vol_notes = [
        "High volume, moderate intensity. Build work capacity.",
        "Moderate volume increase. Technical precision is key.",
        "Volume drops, intensity spikes. Approach near-maximal loads.",
        "Active recovery. Reduce load & volume. Restore readiness.",
    ]

    accessories = {
        "Day A — Hypertrophy Focus": [
            Exercise("Bulgarian Split Squat", "Accessory",
                     [SetConfig(0, 3, 10, 7)], "Unilateral quad/glute development"),
            Exercise("Dumbbell Romanian Deadlift", "Accessory",
                     [SetConfig(0, 3, 10, 7)], "Hamstring accessory"),
            Exercise("Dumbbell Incline Press", "Accessory",
                     [SetConfig(0, 3, 10, 7)], "Chest accessory volume"),
        ],
        "Day B — Strength Focus": [
            Exercise("Pause Squat (2s)", "Accessory",
                     [SetConfig(0, 3, 3, 8)], "Paused at bottom — builds strength out of hole"),
            Exercise("Close-Grip Bench Press", "Accessory",
                     [SetConfig(0, 3, 5, 8)], "Tricep strength carryover to full competition bench"),
            Exercise("Barbell Row", "Accessory",
                     [SetConfig(0, 4, 6, 7)], "Upper back — essential for bench and deadlift"),
        ],
        "Day C — Power / Peaking": [
            Exercise("Box Squat (light)", "Accessory",
                     [SetConfig(0, 3, 2, 7)], "Speed work — rate of force development"),
            Exercise("Weighted Pull-Up", "Accessory",
                     [SetConfig(0, 3, 5, 8)], "Lat strength — critical for deadlift setup"),
            Exercise("Overhead Press", "Accessory",
                     [SetConfig(0, 3, 5, 8)], "Shoulder stability for bench press"),
        ],
    }

    for wk_idx in range(4):
        days = []
        sched = dup_schedule[wk_idx]
        for d_idx, d_label in enumerate(day_labels):
            exercises = []
            for lift in LIFTS:
                pct, sets, reps, rpe = sched[lift][d_idx]
                exercises.append(
                    Exercise(
                        name=lift,
                        lift=lift,
                        sets_config=[SetConfig(pct, 1, reps, rpe)] * sets,
                        notes=f"Competition stance — {reps} reps × {sets} sets @ {pct}% 1RM",
                    )
                )
            exercises.extend(accessories[d_label])
            days.append(TrainingDay(label=d_label, exercises=exercises))

        weeks.append(Week(
            number=wk_idx + 1,
            phase=phases[wk_idx],
            days=days,
            volume_note=vol_notes[wk_idx],
        ))

    return weeks


# ─── Template B: Linear Periodization Intensification Block ──────────────────

def build_linear_template() -> list[Week]:
    """
    Classic Linear Periodization — intensification block.
    Progressively heavier each week; volume decreases.
    """
    # (pct, sets, reps, rpe_target)
    linear_schedule = [
        {"Squat": (75, 4, 5, 7), "Bench Press": (73, 4, 5, 7), "Deadlift": (75, 3, 5, 7)},
        {"Squat": (80, 3, 4, 8), "Bench Press": (78, 3, 4, 8), "Deadlift": (80, 3, 4, 8)},
        {"Squat": (85, 3, 3, 8), "Bench Press": (83, 3, 3, 8), "Deadlift": (85, 2, 3, 8)},
        {"Squat": (62, 2, 3, 6), "Bench Press": (60, 2, 3, 6), "Deadlift": (60, 2, 2, 6)},
    ]
    phases = ["Accumulation", "Intensification", "Intensification", "Deload"]
    vol_notes = [
        "Foundation week. Moderate % — dial in technique, build fatigue base.",
        "Load increases. 4×4 — dense, powerful training stimulus.",
        "Heavy triples. Near-competition intensities. Stay technical.",
        "Deload — clear fatigue before assessment or next block.",
    ]

    linear_accessory_pool = [
        Exercise("Leg Press", "Accessory",
                 [SetConfig(0, 3, 10, 7)], "Quad hypertrophy without spinal load"),
        Exercise("Chest-Supported Row", "Accessory",
                 [SetConfig(0, 3, 8, 7)], "Upper back without fatigue carryover"),
        Exercise("Tricep Pushdown", "Accessory",
                 [SetConfig(0, 3, 12, 7)], "Elbow extension hypertrophy"),
        Exercise("Face Pulls", "Accessory",
                 [SetConfig(0, 3, 15, 6)], "Shoulder health & external rotation"),
    ]

    weeks = []
    for wk_idx in range(4):
        sched = linear_schedule[wk_idx]
        exercises = []
        for lift in LIFTS:
            pct, sets, reps, rpe = sched[lift]
            exercises.append(
                Exercise(
                    name=lift,
                    lift=lift,
                    sets_config=[SetConfig(pct, 1, reps, rpe)] * sets,
                    notes=f"{sets}×{reps} @ {pct}% 1RM | RPE target {rpe}",
                )
            )
        # Add accessories on all weeks except deload (simplified)
        if wk_idx < 3:
            exercises.extend(linear_accessory_pool[:3])

        weeks.append(Week(
            number=wk_idx + 1,
            phase=phases[wk_idx],
            days=[TrainingDay(label="Full SBD Session", exercises=exercises)],
            volume_note=vol_notes[wk_idx],
        ))

    return weeks


# ─────────────────────────────────────────────────────────────────────────────
#  1RM CALCULATION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def epley(weight: float, reps: int) -> float:
    if reps == 1:
        return weight
    return weight * (1 + reps / 30)

def brzycki(weight: float, reps: int) -> float:
    if reps == 1:
        return weight
    return weight * (36 / (37 - reps))

def weighted_1rm(weight: float, reps: int) -> float:
    """Powerlifting-focused weighted average: 60% Epley + 40% Brzycki"""
    e = epley(weight, reps)
    b = brzycki(weight, reps)
    return round(0.6 * e + 0.4 * b, 1)

def pct_to_kg(one_rm: float, pct: float) -> float:
    """Round to nearest 2.5 kg — realistic plate increments"""
    raw = one_rm * pct / 100
    return round(raw / 2.5) * 2.5


# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "one_rm": {"Squat": 0.0, "Bench Press": 0.0, "Deadlift": 0.0},
        "template": "DUP",
        "weeks": build_dup_template(),
        "active_page": "Calculator",
        # Dynamic percentages per (week, day, exercise, set)
        "pct_overrides": {},
        # Progress recommendations per (week, lift)
        "rec_inputs": {},
        "recommendations": {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────────────────────────────────────
#  PROGRESS RECOMMENDATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def generate_recommendation(lift: str, rpe_actual: float, rir: int, completed: bool, week_phase: str) -> dict:
    """
    Science-based auto-regulation logic:
    - RPE < target → increase load
    - RPE on target (8-9) → maintain planned progression
    - RPE 10 / failure → reduce or deload
    """
    if not completed and rpe_actual >= 10:
        return {
            "verdict": "danger",
            "title": "⚠ Overreach Detected — Adaptive Deload",
            "text": (
                f"Absolute failure or RPE 10 on {lift}. "
                "Protocol: hold all loads, reduce volume by 30%, and treat next session "
                "as a technical deload (≤ 75% 1RM). Fatigue is masking fitness — recovery is the priority."
            ),
            "action": "DELOAD",
        }
    elif not completed and rpe_actual >= 9:
        return {
            "verdict": "warn",
            "title": "⚡ Near-Failure — Maintain & Monitor",
            "text": (
                f"{lift}: incomplete sets with RPE {rpe_actual:.1f}. "
                "Keep the same weight next session. Do not increase load. "
                "Prioritise sleep, nutrition and review total weekly volume."
            ),
            "action": "MAINTAIN",
        }
    elif completed and rpe_actual < 7:
        pct_inc = 5.0 if rpe_actual < 6 else 2.5
        return {
            "verdict": "ok",
            "title": f"✅ Submaximal — Increase Load by {pct_inc}%",
            "text": (
                f"{lift}: all sets completed with RPE {rpe_actual:.1f} and {rir} RIR remaining. "
                f"Significant reserve detected. Increase working weight by "
                f"~{pct_inc}% (or the nearest 2.5 kg increment) in the next session. "
                "High RIR indicates the stimulus was insufficient for the planned adaptation."
            ),
            "action": f"+{pct_inc}%",
        }
    elif completed and rpe_actual <= 8.5:
        return {
            "verdict": "ok",
            "title": "✅ On Target — Continue Planned Progression",
            "text": (
                f"{lift}: RPE {rpe_actual:.1f} with {rir} RIR. "
                "Performance aligns perfectly with the periodization target. "
                "Proceed with the next planned session weight as programmed."
            ),
            "action": "PLANNED +2.5%",
        }
    elif completed and rpe_actual <= 9.5:
        return {
            "verdict": "warn",
            "title": "⚡ High Effort — Maintain Weight",
            "text": (
                f"{lift}: all reps completed but RPE {rpe_actual:.1f} indicates high accumulated fatigue. "
                "Do NOT increase load. Hold the same percentage and re-evaluate next week. "
                "Consider adding a light technique session before the next heavy day."
            ),
            "action": "MAINTAIN",
        }
    else:  # RPE 10, completed
        return {
            "verdict": "warn",
            "title": "⚡ Max Effort — Hold & Recover",
            "text": (
                f"{lift}: sets completed at RPE {rpe_actual:.1f} — absolute maximum. "
                "Do not increase load. Maintain weight and focus on recovery quality. "
                "If this occurs 2 weeks consecutively, initiate a deload week."
            ),
            "action": "MAINTAIN",
        }


# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1.2rem 0;'>
      <div style='font-family: Space Grotesk, sans-serif; font-size:1.5rem; font-weight:700; color:#e8e8e8;'>
        🏋 <span style='color:#ff4d1c;'>IRON</span> PROTOCOL
      </div>
      <div style='font-size:0.68rem; color:#444; letter-spacing:0.12em; text-transform:uppercase; margin-top:2px;'>
        Powerlifting Training OS
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Active 1RMs display
    st.markdown("<div class='section-header'>Active 1RMs</div>", unsafe_allow_html=True)
    for lift, emoji in [("Squat", "🟢"), ("Bench Press", "🔵"), ("Deadlift", "🟠")]:
        val = st.session_state.one_rm[lift]
        color = "#4caf50" if lift == "Squat" else "#64b5f6" if lift == "Bench Press" else "#ff9800"
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; padding:0.35rem 0;
                    border-bottom:1px solid #1a1a1f; font-size:0.85rem;'>
          <span style='color:#888;'>{lift}</span>
          <span style='font-family:Space Grotesk,sans-serif; font-weight:700; color:{color};'>
            {"—" if val == 0 else f"{val:.1f} kg"}
          </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    # ── Navigation
    st.markdown("<div class='section-header'>Navigation</div>", unsafe_allow_html=True)
    pages = [
        ("📊", "Calculator", "1RM & Weight Estimator"),
        ("📅", "Program", "Weekly Schedule"),
        ("📈", "Progress", "Auto-Regulation"),
        ("🗂️", "Templates", "Routine Templates"),
    ]
    for icon, page, desc in pages:
        active_cls = "active" if st.session_state.active_page == page else ""
        if st.button(f"{icon}  {page}", key=f"nav_{page}", use_container_width=True):
            st.session_state.active_page = page
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.68rem; color:#333; text-align:center; line-height:1.7;'>
      Built with Sports Science principles<br>
      DUP · Linear · Auto-Regulation<br>
      <span style='color:#ff4d1c;'>●</span> Session state persisted
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN HEADER
# ─────────────────────────────────────────────────────────────────────────────

page = st.session_state.active_page

st.markdown(f"""
<div class='app-title'>
  <span class='accent'>Iron</span> Protocol
  <span style='font-size:1rem; font-weight:400; color:#555; margin-left:0.5rem;'>/ {page}</span>
</div>
<div class='app-subtitle'>Powerlifting Training Management System · SBD Focus</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────

if page == "Calculator":
    st.markdown("""
    <div style='font-size:0.88rem; color:#888; margin-bottom:1.5rem;'>
    Enter the weight you lifted and the reps achieved. The estimator uses a weighted average
    of the <strong style='color:#ccc;'>Epley</strong> and <strong style='color:#ccc;'>Brzycki</strong>
    formulas optimised for Powerlifting intensities (sub-10 rep ranges).
    </div>
    """, unsafe_allow_html=True)

    col_form, col_results = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown("<div class='section-header'>Input</div>", unsafe_allow_html=True)

        lift_sel = st.selectbox("Movement", LIFTS, key="calc_lift")
        w_col, r_col = st.columns(2)
        with w_col:
            weight = st.number_input("Weight lifted (kg)", min_value=1.0, max_value=500.0,
                                     value=100.0, step=2.5, key="calc_weight")
        with r_col:
            reps = st.number_input("Reps completed", min_value=1, max_value=20,
                                   value=5, step=1, key="calc_reps")

        st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)

        if st.button("⚡ Calculate 1RM", use_container_width=True):
            st.session_state["calc_result"] = {
                "lift": lift_sel,
                "weight": weight,
                "reps": reps,
                "epley": epley(weight, reps),
                "brzycki": brzycki(weight, reps),
                "avg": weighted_1rm(weight, reps),
            }

        if "calc_result" in st.session_state:
            r = st.session_state.calc_result
            st.markdown("<div class='section-header'>Results</div>", unsafe_allow_html=True)

            cols = st.columns(3)
            for col, label, val in [
                (cols[0], "Epley", r["epley"]),
                (cols[1], "Brzycki", r["brzycki"]),
                (cols[2], "Weighted Avg", r["avg"]),
            ]:
                with col:
                    st.markdown(f"""
                    <div class='metric-card'>
                      <div class='metric-label'>{label}</div>
                      <div class='metric-value'>{val:.1f}</div>
                      <div class='metric-unit'>kg</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

            if st.button(f"💾 Save {r['avg']:.1f} kg as {r['lift']} 1RM", use_container_width=True):
                st.session_state.one_rm[r["lift"]] = r["avg"]
                st.success(f"✅ {r['lift']} 1RM set to **{r['avg']:.1f} kg** — all program weights updated.")

    with col_results:
        st.markdown("<div class='section-header'>Percentage Table</div>", unsafe_allow_html=True)

        calc_base_orm = st.session_state.one_rm.get(lift_sel, 0)
        if "calc_result" in st.session_state:
            calc_base_orm = st.session_state.calc_result["avg"]

        if calc_base_orm > 0:
            rows = []
            for pct in [50, 55, 60, 65, 70, 75, 77.5, 80, 82.5, 85, 87.5, 90, 92.5, 95, 100]:
                rows.append({
                    "% 1RM": f"{pct}%",
                    "Load (kg)": f"{pct_to_kg(calc_base_orm, pct):.1f}",
                    "Usage": (
                        "Warm-up / Technique" if pct <= 60 else
                        "Volume / Hypertrophy" if pct <= 72 else
                        "Strength / Accumulation" if pct <= 82 else
                        "Intensification" if pct <= 90 else
                        "Peak / Competition"
                    ),
                })

            df = pd.DataFrame(rows)
            st.markdown(df.to_html(index=False, classes="styled-table", border=0), unsafe_allow_html=True)
        else:
            st.info("Calculate or set a 1RM to see the load table.")

        st.markdown("<div class='section-header'>Manual 1RM Override</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.8rem; color:#666; margin-bottom:0.6rem;'>Set a known competition or tested 1RM directly.</div>", unsafe_allow_html=True)
        for lift in LIFTS:
            cur = st.session_state.one_rm[lift]
            new_val = st.number_input(f"{lift} 1RM (kg)", min_value=0.0, max_value=500.0,
                                      value=float(cur), step=2.5, key=f"manual_{lift}")
            if new_val != cur:
                st.session_state.one_rm[lift] = new_val


# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: PROGRAM
# ─────────────────────────────────────────────────────────────────────────────

elif page == "Program":
    weeks = st.session_state.weeks
    template_name = st.session_state.template

    st.markdown(f"""
    <div style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>
      Active template: <strong style='color:#ccc;'>{template_name}</strong> ·
      {len(weeks)}-Week Block ·
      Modify percentages inline — weights update in real time from your saved 1RMs.
    </div>
    """, unsafe_allow_html=True)

    # Check 1RMs
    missing = [l for l in LIFTS if st.session_state.one_rm[l] == 0]
    if missing:
        st.warning(f"⚠ 1RM not set for: **{', '.join(missing)}**. Go to Calculator → set 1RMs for live kg calculations.")

    # Week tabs
    week_tabs = st.tabs([f"Week {w.number} — {w.phase}" for w in weeks])

    PHASE_BADGE = {
        "Accumulation": "badge-accum",
        "Intensification": "badge-intens",
        "Deload": "badge-deload",
        "Peak": "badge-peak",
    }

    for wk_idx, (wk, tab) in enumerate(zip(weeks, week_tabs)):
        with tab:
            badge_cls = PHASE_BADGE.get(wk.phase, "badge-accum")
            st.markdown(f"""
            <span class='week-badge {badge_cls}'>{wk.phase}</span>
            <span style='font-size:0.82rem; color:#666; margin-left:0.5rem;'>{wk.volume_note}</span>
            """, unsafe_allow_html=True)

            for d_idx, day in enumerate(wk.days):
                st.markdown(f"""
                <div style='font-family: Space Grotesk, sans-serif; font-size:0.95rem;
                            font-weight:700; color:#aaa; margin:1.2rem 0 0.7rem 0;
                            letter-spacing:0.05em; text-transform:uppercase;'>
                  {day.label}
                </div>
                """, unsafe_allow_html=True)

                for ex_idx, ex in enumerate(day.exercises):
                    is_main = ex.lift in LIFTS
                    orm_val = st.session_state.one_rm.get(ex.lift, 0)

                    lift_color = {
                        "Squat": "#4caf50",
                        "Bench Press": "#64b5f6",
                        "Deadlift": "#ff9800",
                    }.get(ex.lift, "#888")

                    st.markdown(f"""
                    <div style='display:flex; align-items:center; gap:0.5rem; margin-bottom:0.3rem;'>
                      <span style='font-weight:700; font-size:0.92rem; color:{"#e8e8e8" if is_main else "#aaa"};'>
                        {ex.name}
                      </span>
                      {"<span class='lift-pill squat-pill'>SQUAT</span>" if ex.lift == "Squat" and is_main else ""}
                      {"<span class='lift-pill bench-pill'>BENCH</span>" if ex.lift == "Bench Press" and is_main else ""}
                      {"<span class='lift-pill dead-pill'>DEAD</span>" if ex.lift == "Deadlift" and is_main else ""}
                      {"<span style='font-size:0.72rem; color:#555; text-transform:uppercase; letter-spacing:0.08em;'>accessory</span>" if not is_main else ""}
                    </div>
                    <div style='font-size:0.76rem; color:#555; margin-bottom:0.5rem;'>{ex.notes}</div>
                    """, unsafe_allow_html=True)

                    if is_main:
                        # One row per set with editable %
                        set_cols = st.columns([1.2, 1.2, 1.2, 1.2, 1.5])
                        set_cols[0].markdown("<div style='font-size:0.7rem; color:#555; text-transform:uppercase; padding-bottom:4px;'>Set</div>", unsafe_allow_html=True)
                        set_cols[1].markdown("<div style='font-size:0.7rem; color:#555; text-transform:uppercase; padding-bottom:4px;'>Reps</div>", unsafe_allow_html=True)
                        set_cols[2].markdown("<div style='font-size:0.7rem; color:#555; text-transform:uppercase; padding-bottom:4px;'>% 1RM</div>", unsafe_allow_html=True)
                        set_cols[3].markdown("<div style='font-size:0.7rem; color:#555; text-transform:uppercase; padding-bottom:4px;'>RPE Target</div>", unsafe_allow_html=True)
                        set_cols[4].markdown("<div style='font-size:0.7rem; color:#555; text-transform:uppercase; padding-bottom:4px;'>Load (kg)</div>", unsafe_allow_html=True)

                        # Collect sets (they repeat in sets_config)
                        unique_set = ex.sets_config[0]  # All sets same config
                        num_sets = len(ex.sets_config)

                        for s_idx in range(num_sets):
                            key = f"pct_{wk_idx}_{d_idx}_{ex_idx}_{s_idx}"
                            if key not in st.session_state.pct_overrides:
                                st.session_state.pct_overrides[key] = float(unique_set.pct)

                            cols = st.columns([1.2, 1.2, 1.2, 1.2, 1.5])
                            with cols[0]:
                                st.markdown(f"<div style='padding-top:8px; font-size:0.88rem; color:#666;'>Set {s_idx+1}</div>", unsafe_allow_html=True)
                            with cols[1]:
                                st.markdown(f"<div style='padding-top:8px; font-size:0.88rem; color:#ccc;'>{unique_set.reps}</div>", unsafe_allow_html=True)
                            with cols[2]:
                                new_pct = st.number_input(
                                    "% 1RM",
                                    min_value=30.0, max_value=110.0,
                                    value=st.session_state.pct_overrides[key],
                                    step=2.5,
                                    key=key,
                                    label_visibility="collapsed",
                                )
                                st.session_state.pct_overrides[key] = new_pct
                            with cols[3]:
                                st.markdown(f"<div style='padding-top:8px; font-size:0.88rem; color:#ff9800;'>RPE {unique_set.rpe_target}</div>", unsafe_allow_html=True)
                            with cols[4]:
                                if orm_val > 0:
                                    kg = pct_to_kg(orm_val, new_pct)
                                    st.markdown(f"<div style='padding-top:6px;'><span class='kg-cell'>{kg:.1f} kg</span></div>", unsafe_allow_html=True)
                                else:
                                    st.markdown("<div style='padding-top:8px; font-size:0.8rem; color:#444;'>Set 1RM</div>", unsafe_allow_html=True)
                    else:
                        # Accessory — just show set/rep scheme
                        cfg = ex.sets_config[0]
                        st.markdown(f"""
                        <div style='background:#0f0f12; border:1px solid #191919; border-radius:6px;
                                    padding:0.4rem 0.8rem; font-size:0.82rem; color:#666; display:inline-block;'>
                          {len(ex.sets_config)} sets × {cfg.reps} reps @ RPE {cfg.rpe_target}
                          <span style='color:#444; margin-left:0.5rem;'>| Load: self-selected / RPE-based</span>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("<div style='margin-bottom:0.8rem;'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: PROGRESS
# ─────────────────────────────────────────────────────────────────────────────

elif page == "Progress":
    weeks = st.session_state.weeks

    st.markdown("""
    <div style='font-size:0.88rem; color:#888; margin-bottom:1.5rem;'>
      Auto-regulation engine. Input your real session metrics — the system applies evidence-based
      logic to recommend your next week's adjustments per lift.
    </div>
    """, unsafe_allow_html=True)

    week_options = {f"Week {w.number} — {w.phase}": w for w in weeks}
    selected_week_label = st.selectbox("Evaluate week", list(week_options.keys()))
    current_week = week_options[selected_week_label]

    st.markdown(f"""
    <div class='week-card' style='margin-top:0.5rem;'>
      <div style='font-size:0.82rem; color:#888;'>
        <strong style='color:#ccc;'>{current_week.phase} Phase</strong> —
        {current_week.volume_note}
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Session Evaluation per Lift</div>", unsafe_allow_html=True)

    for lift in LIFTS:
        lift_color = {"Squat": "#4caf50", "Bench Press": "#64b5f6", "Deadlift": "#ff9800"}[lift]
        pill_cls = {"Squat": "squat-pill", "Bench Press": "bench-pill", "Deadlift": "dead-pill"}[lift]

        with st.expander(f"  {lift}", expanded=True):
            st.markdown(f"<span class='lift-pill {pill_cls}'>{lift.upper()}</span>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                rpe_key = f"rpe_{current_week.number}_{lift}"
                rpe_val = st.slider(
                    "RPE Achieved",
                    min_value=5.0, max_value=10.0, value=8.0, step=0.5,
                    key=rpe_key,
                    help="Rating of Perceived Exertion (6=easy, 10=absolute max/failed)"
                )
                # RPE bar
                rpe_pct = (rpe_val - 5) / 5 * 100
                rpe_color = "#4caf50" if rpe_val <= 7 else "#ff9800" if rpe_val <= 9 else "#ef5350"
                st.markdown(f"""
                <div class='rpe-bar-wrap'>
                  <div class='rpe-bar' style='width:{rpe_pct}%; background:{rpe_color};'></div>
                </div>
                <div style='font-size:0.7rem; color:#666; margin-top:2px;'>RPE {rpe_val:.1f}</div>
                """, unsafe_allow_html=True)

            with c2:
                rir_key = f"rir_{current_week.number}_{lift}"
                rir_val = st.selectbox(
                    "Reps in Reserve (RIR)",
                    options=[0, 1, 2, 3, 4, 5],
                    key=rir_key,
                    help="How many more reps could you have done on your hardest set?"
                )

            with c3:
                comp_key = f"comp_{current_week.number}_{lift}"
                completed = st.radio(
                    "All sets completed?",
                    options=["Yes", "No"],
                    key=comp_key,
                    horizontal=True,
                ) == "Yes"

            rec_key = f"rec_{current_week.number}_{lift}"
            if st.button(f"Generate Recommendation — {lift}", key=f"btn_{rec_key}", use_container_width=True):
                rec = generate_recommendation(lift, rpe_val, rir_val, completed, current_week.phase)
                st.session_state.recommendations[rec_key] = rec

            if rec_key in st.session_state.recommendations:
                rec = st.session_state.recommendations[rec_key]
                cls = rec["verdict"]
                box_cls = {"ok": "", "warn": "warn", "danger": "danger"}[cls]
                title_cls = {"ok": "rec-ok", "warn": "rec-warn", "danger": "rec-bad"}[cls]
                st.markdown(f"""
                <div class='rec-box {box_cls}'>
                  <div class='rec-title {title_cls}'>{rec["title"]}</div>
                  <div style='font-size:0.83rem; color:#aaa; line-height:1.55;'>{rec["text"]}</div>
                  <div style='margin-top:0.6rem;'>
                    <span style='font-size:0.72rem; font-weight:700; letter-spacing:0.1em;
                                 text-transform:uppercase; color:#555;'>Action:</span>
                    <span style='font-family: Space Grotesk, sans-serif; font-weight:700;
                                 font-size:0.88rem; color:{
                                   "#4caf50" if cls=="ok" else "#ff9800" if cls=="warn" else "#ef5350"
                                 }; margin-left:0.4rem;'>{rec["action"]}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Overall Block Progress</div>", unsafe_allow_html=True)

    # Simple 1RM tracking chart
    orm_data = st.session_state.one_rm
    has_any = any(v > 0 for v in orm_data.values())

    if has_any:
        chart_data = {k: [v] for k, v in orm_data.items() if v > 0}
        df_chart = pd.DataFrame(chart_data, index=["Current 1RM"])
        st.markdown("""
        <div style='font-size:0.8rem; color:#666; margin-bottom:0.5rem;'>
          Current saved 1RMs — update these after testing to track block-to-block progress.
        </div>
        """, unsafe_allow_html=True)

        metrics = st.columns(3)
        for i, lift in enumerate(LIFTS):
            val = orm_data[lift]
            with metrics[i]:
                color = {"Squat": "#4caf50", "Bench Press": "#64b5f6", "Deadlift": "#ff9800"}[lift]
                st.markdown(f"""
                <div class='metric-card'>
                  <div class='metric-label'>{lift}</div>
                  <div class='metric-value' style='color:{color};'>{"—" if val==0 else f"{val:.1f}"}</div>
                  <div class='metric-unit'>kg 1RM</div>
                </div>
                """, unsafe_allow_html=True)

        total = sum(orm_data.values())
        if total > 0:
            st.markdown(f"""
            <div style='text-align:center; margin-top:1rem; padding:0.8rem; background:#111114;
                        border:1px solid #1f1f24; border-radius:8px;'>
              <div style='font-size:0.72rem; color:#555; text-transform:uppercase;
                          letter-spacing:0.1em;'>Total (Powerlifting Total)</div>
              <div style='font-family: Space Grotesk, sans-serif; font-size:2.4rem;
                          font-weight:700; color:#ff4d1c;'>{total:.1f} kg</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Set your 1RMs in the Calculator tab to track your powerlifting total.")


# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: TEMPLATES
# ─────────────────────────────────────────────────────────────────────────────

elif page == "Templates":
    st.markdown("""
    <div style='font-size:0.88rem; color:#888; margin-bottom:1.5rem;'>
      Select a pre-configured scientific training system. Loading a template resets the
      current program while preserving your 1RMs and session history.
    </div>
    """, unsafe_allow_html=True)

    templates = {
        "DUP": {
            "name": "Daily Undulating Periodization",
            "abbr": "DUP",
            "desc": (
                "Train each lift 3× per week with rotating stimuli — "
                "hypertrophy, strength, and power days within the same week. "
                "Backed by research from Zourdos & Apel (2010). Optimal for intermediates "
                "seeking to maximise frequency and specificity simultaneously."
            ),
            "tags": ["3×/week", "High Frequency", "Intermediate–Advanced", "4 Weeks"],
            "stats": {"Sessions/week": 3, "Weeks": 4, "Intensity range": "65–90%"},
            "science": (
                "DUP exploits the principle of conjugate variation: by rotating intensity "
                "daily, the athlete avoids accommodation while maintaining high specificity. "
                "The hypertrophy day builds structural adaptation; the strength day trains "
                "neuromuscular efficiency; the power day peaking protocols optimise rate of "
                "force development."
            ),
        },
        "Linear": {
            "name": "Linear Intensification Block",
            "abbr": "LP",
            "desc": (
                "Classic periodization with a single weekly training frequency per lift, "
                "progressively increasing intensity across 4 weeks. "
                "Ideal for building a strength base or for competition peaking phases. "
                "Based on Zatsiorsky's maximal effort method."
            ),
            "tags": ["1–2×/week", "Lower Frequency", "Beginner–Intermediate", "4 Weeks"],
            "stats": {"Sessions/week": "2–3", "Weeks": 4, "Intensity range": "75–95%"},
            "science": (
                "Linear progression exploits the principle of progressive overload in its "
                "purest form. By increasing the load systematically each week, the athlete "
                "creates a predictable overreaching stimulus. The deload week dissipates "
                "accumulated fatigue, allowing fitness to express fully — a technique "
                "central to Supercompensation theory."
            ),
        },
    }

    current_tpl = st.session_state.template

    for tpl_key, tpl in templates.items():
        is_active = current_tpl == tpl_key
        selected_css = "border-color: #ff4d1c;" if is_active else ""

        c1, c2 = st.columns([2, 1], gap="large")
        with c1:
            st.markdown(f"""
            <div class='template-card' style='{selected_css}'>
              <div style='display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;'>
                <div style='font-family: Space Grotesk, sans-serif; font-size:2rem; font-weight:900;
                            color:#ff4d1c; opacity:{"1" if is_active else "0.4"};'>{tpl["abbr"]}</div>
                <div>
                  <div class='template-name'>{tpl["name"]}</div>
                  {"<span style='font-size:0.7rem; color:#ff4d1c; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;'>● Active</span>" if is_active else ""}
                </div>
              </div>
              <div class='template-desc'>{tpl["desc"]}</div>
              <div>{"".join(f"<span class='tag'>{t}</span>" for t in tpl["tags"])}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class='week-card' style='margin-top:0;'>
              <div class='metric-label' style='margin-bottom:0.8rem;'>Quick Stats</div>
              {"".join(f'''
              <div style='display:flex; justify-content:space-between; padding:0.3rem 0;
                          border-bottom:1px solid #191919; font-size:0.82rem;'>
                <span style='color:#666;'>{k}</span>
                <span style='font-weight:700; color:#ccc;'>{v}</span>
              </div>
              ''' for k, v in tpl["stats"].items())}
            </div>
            """, unsafe_allow_html=True)

        with st.expander(f"Science behind {tpl['name']}"):
            st.markdown(f"<div style='font-size:0.84rem; color:#999; line-height:1.65;'>{tpl['science']}</div>", unsafe_allow_html=True)

        if not is_active:
            if st.button(f"📥 Load {tpl['abbr']} Template", key=f"load_{tpl_key}", use_container_width=False):
                st.session_state.template = tpl_key
                if tpl_key == "DUP":
                    st.session_state.weeks = build_dup_template()
                else:
                    st.session_state.weeks = build_linear_template()
                # Reset per-set overrides (1RMs preserved)
                st.session_state.pct_overrides = {}
                st.session_state.recommendations = {}
                st.success(f"✅ {tpl['name']} loaded. Head to **Program** to view your schedule.")
        else:
            st.markdown(f"""
            <div style='font-size:0.82rem; color:#4caf50; padding:0.4rem 0; margin-bottom:0.5rem;'>
              ✓ Currently active
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

    # ── Scientific principles reference
    st.markdown("<div class='section-header'>Core Training Science Principles</div>", unsafe_allow_html=True)

    principles = [
        ("Specificity (SAID)", "Adaptations are specific to the demands imposed. Train the competition lifts frequently and with competition-representative loads."),
        ("Progressive Overload", "The training stimulus must increase over time to drive continued adaptation. This app enforces systematic % increases each week."),
        ("Auto-Regulation (RPE/RIR)", "Daily readiness varies. RPE and RIR allow intensity to fluctuate with actual performance, avoiding both under- and over-training."),
        ("Supercompensation", "Fatigue must be managed (deload week) to allow fitness to express. The deload is not optional — it's when gains are realised."),
        ("Volume Progression", "MEV → MAV → MRV. Start at Minimum Effective Volume, accumulate to Maximum Adaptive Volume, then deload before Maximal Recoverable Volume."),
    ]

    for title, body in principles:
        st.markdown(f"""
        <div style='background:#111114; border:1px solid #1a1a1f; border-radius:8px;
                    padding:0.8rem 1rem; margin-bottom:0.6rem;'>
          <div style='font-weight:700; font-size:0.85rem; color:#ccc; margin-bottom:0.25rem;'>{title}</div>
          <div style='font-size:0.8rem; color:#666; line-height:1.55;'>{body}</div>
        </div>
        """, unsafe_allow_html=True)
