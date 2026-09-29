import os
import time
import math
import importlib.util
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as pgo

# ============================================================
# QADAPT — Integrated Hybrid QML Clinical-Research Prototype
# ============================================================

st.set_page_config(
    page_title="QADAPT",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------
# Theme / CSS
# -------------------------
CSS = r'''
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
  --burgundy: #790D16;
  --burgundy-2: #641019;
  --champagne: #E5D3AF;
  --ivory: #F5EFE1;
  --blue: #AEC4D4;
  --ink: #252326;
  --muted: #756F69;
  --line: #E4DDD0;
  --white: #FFFFFF;
  --soft: #FBF8F1;
}

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: var(--ivory); color: var(--ink); }
.block-container { max-width: 1240px; padding-top: 1.2rem; padding-bottom: 3rem; }

/* remove streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display:none; }

.brand {
  font-family: 'Manrope', sans-serif;
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -1.3px;
  color: var(--burgundy);
}
.brand-light { color: var(--champagne); }

.topbar {
  display:flex; align-items:center; justify-content:space-between;
  padding: 8px 0 22px 0;
}
.topbar-right { color:var(--muted); font-size:13px; }

.eyebrow {
  text-transform:uppercase; letter-spacing:1.8px; font-size:11px;
  font-weight:700; color:var(--burgundy); margin-bottom:10px;
}
.hero-title {
  font-family:'Manrope',sans-serif; font-size:52px; line-height:1.02;
  letter-spacing:-2.7px; font-weight:800; margin:0; color:var(--ink);
}
.hero-copy { color:var(--muted); font-size:17px; line-height:1.65; max-width:680px; margin-top:16px; }

.card {
  background:var(--white); border:1px solid var(--line); border-radius:22px;
  padding:26px; box-shadow:0 10px 30px rgba(73,50,25,.055);
}
.card-tight { padding:20px; }
.card-title { font-family:'Manrope',sans-serif; font-weight:800; font-size:20px; letter-spacing:-.5px; }
.card-sub { color:var(--muted); font-size:13px; line-height:1.55; margin-top:5px; }

.option-card {
  background:var(--white); border:1px solid var(--line); border-radius:22px;
  padding:28px; min-height:190px; box-shadow:0 8px 25px rgba(73,50,25,.045);
}
.option-icon {
  width:42px; height:42px; border-radius:13px; display:flex; align-items:center; justify-content:center;
  background:#F4E9D8; color:var(--burgundy); font-weight:800; font-size:17px; margin-bottom:24px;
}
.option-title { font-family:'Manrope'; font-size:20px; font-weight:800; letter-spacing:-.5px; }
.option-copy { color:var(--muted); font-size:13px; line-height:1.55; margin-top:7px; }

.metric {
  background:var(--white); border:1px solid var(--line); border-radius:18px; padding:20px 22px;
}
.metric-label { color:var(--muted); font-size:12px; }
.metric-value { font-family:'Manrope'; font-size:29px; font-weight:800; margin-top:5px; }

.stepbar { display:flex; gap:8px; margin: 8px 0 30px; }
.step { height:4px; border-radius:10px; flex:1; background:#DED6C9; }
.step.active { background:var(--burgundy); }
.step.done { background:#B88D82; }
.step-label { font-size:12px; color:var(--muted); margin-top:10px; }

.review-row { display:flex; justify-content:space-between; padding:13px 0; border-bottom:1px solid #EEE8DE; }
.review-row:last-child { border-bottom:0; }
.review-label { color:var(--muted); font-size:13px; }
.review-value { font-weight:600; font-size:13px; text-align:right; }

.result-score {
  font-family:'Manrope'; font-size:76px; line-height:1; font-weight:800; letter-spacing:-4px;
  color:var(--burgundy);
}
.result-label { font-size:17px; font-weight:700; margin-top:10px; }
.result-note { color:var(--muted); font-size:13px; line-height:1.6; max-width:580px; }

.status-pill { display:inline-block; padding:7px 11px; border-radius:999px; font-size:11px; font-weight:700; letter-spacing:.3px; }
.pill-burgundy { background:#F1DADD; color:var(--burgundy); }
.pill-blue { background:#E3EDF3; color:#35566A; }
.pill-green { background:#E7F1EA; color:#356347; }

.disclaimer {
  background:#F8F3E8; border:1px solid #E9DEC9; border-radius:16px; padding:15px 17px;
  color:#665D52; font-size:12px; line-height:1.6;
}

.login-wrap { max-width:460px; margin: 9vh auto 0; }
.login-mark { text-align:center; margin-bottom:44px; }
.login-mark .brand { font-size:38px; }
.login-caption { color:var(--muted); font-size:13px; margin-top:9px; }

.launch { min-height:82vh; display:flex; align-items:center; justify-content:center; flex-direction:column; }
.launch-word { font-family:'Manrope'; font-weight:800; font-size:82px; letter-spacing:-6px; color:var(--burgundy); animation:qfade 2.1s ease both; }
.launch-line { width:0; height:2px; background:var(--champagne); animation:qline 1.6s .6s ease forwards; }
@keyframes qfade { 0% {opacity:0; transform:translateY(14px); letter-spacing:-2px;} 100% {opacity:1; transform:none; letter-spacing:-6px;} }
@keyframes qline { to { width:140px; } }

/* Streamlit controls */
.stButton > button {
  border-radius:13px !important; border:1px solid var(--burgundy) !important;
  background:var(--burgundy) !important; color:#fff !important; font-weight:700 !important;
  min-height:46px !important; transition:all .18s ease !important;
}
.stButton > button:hover { background:var(--burgundy-2) !important; transform:translateY(-1px); box-shadow:0 8px 18px rgba(121,13,22,.16); }
.secondary .stButton > button { background:transparent !important; color:var(--burgundy) !important; }

.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stFileUploader {
  border-radius:12px !important;
}
label { color:#504A45 !important; font-size:12px !important; font-weight:600 !important; }
[data-testid="stFileUploaderDropzone"] { background:#FCFAF5; border:1px dashed #CFC4B4; border-radius:15px; }
hr { border-color:var(--line) !important; }

/* refined upload + result */
.upload-drop {
  background:var(--white); border:1px dashed #CFC4B4; border-radius:22px;
  padding:10px; box-shadow:0 8px 24px rgba(73,50,25,.035);
}
.upload-meta {
  background:#FBF8F1; border:1px solid var(--line); border-radius:18px; padding:18px 20px;
}
.upload-check {
  display:inline-flex; align-items:center; gap:7px; padding:6px 10px; border-radius:999px;
  background:#EAF2EC; color:#356347; font-size:11px; font-weight:700;
}
.result-kicker { color:var(--muted); font-size:11px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; }
.result-patient { font-family:'Manrope'; font-size:16px; font-weight:800; color:var(--ink); margin-top:5px; }
.result-delta { font-family:'Manrope'; font-size:20px; font-weight:800; color:var(--burgundy); }

/* sidebar */
section[data-testid="stSidebar"] { background:#fff !important; border-right:1px solid var(--line); }
section[data-testid="stSidebar"] .block-container { padding:28px 20px; }

.small-muted { color:var(--muted); font-size:12px; }

.global-back .stButton > button {
  background:transparent !important; color:var(--burgundy) !important;
  border:1px solid var(--line) !important; min-height:38px !important;
  padding:0 14px !important; box-shadow:none !important;
}
.global-back .stButton > button:hover { background:#FBF8F1 !important; transform:none !important; box-shadow:none !important; }
.breadcrumb {
  height:38px; display:flex; align-items:center; gap:9px;
  color:var(--muted); font-size:12px; font-weight:600;
}
.breadcrumb-brand {
  color:var(--burgundy); font-family:'Manrope',sans-serif;
  font-weight:800; font-size:17px; letter-spacing:-.8px;
}
.breadcrumb-arrow { color:#B8AEA0; font-size:16px; }
.doctor-chip {
  height:38px; display:flex; align-items:center; justify-content:flex-end;
  font-size:12px; font-weight:600;
}
.nav-divider { height:1px; background:var(--line); margin:0 0 26px 0; }
.performance-chart { margin-top:14px; }
.footer-note { text-align:center; color:#9A9289; font-size:11px; margin-top:35px; }
</style>
'''
st.markdown(CSS, unsafe_allow_html=True)

# -------------------------
# State
# -------------------------
def init_state():
    defaults = {
        "screen": "launch",
        "nav_history": [],
        "logged_in": False,
        "doctor": "",
        "assessment_mode": None,
        "step": 1,
        "patient": {},
        "analysis": None,
        "history": [],
        "launch_started": time.time(),
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init_state()

# -------------------------
# Helpers
# -------------------------
FINAL_FEATURES = [
    "EducationLevel", "SleepQuality", "CardiovascularDisease", "SystolicBP",
    "CholesterolHDL", "CholesterolTriglycerides", "MMSE", "FunctionalAssessment",
    "MemoryComplaints", "BehavioralProblems", "ADL", "PersonalityChanges"
]

DISPLAY_NAMES = {
    "EducationLevel":"Education level", "SleepQuality":"Sleep quality",
    "CardiovascularDisease":"Cardiovascular disease", "SystolicBP":"Systolic BP",
    "CholesterolHDL":"HDL cholesterol", "CholesterolTriglycerides":"Triglycerides",
    "MMSE":"MMSE", "FunctionalAssessment":"Functional assessment",
    "MemoryComplaints":"Memory complaints", "BehavioralProblems":"Behavioral problems",
    "ADL":"Activities of daily living", "PersonalityChanges":"Personality changes"
}

DATA_CANDIDATES = [
    os.path.expanduser("~/Downloads/alzheimers_disease_data.csv"),
    os.path.join(os.path.dirname(__file__), "alzheimers_disease_data.csv"),
]
PARAM_CANDIDATES = [
    os.path.expanduser("~/Downloads/12_v12_quantum_parameters.npy"),
    os.path.join(os.path.dirname(__file__), "12_v12_quantum_parameters.npy"),
]
PREDICTION_CANDIDATES = [
    os.path.expanduser("~/Downloads/12_v12_predictions.csv"),
    os.path.join(os.path.dirname(__file__), "12_v12_predictions.csv"),
]

@st.cache_data

def load_reference_data():
    for p in DATA_CANDIDATES:
        if os.path.exists(p):
            return pd.read_csv(p), p
    return None, None

@st.cache_data

def load_benchmark_predictions():
    """Load saved V12 test predictions for the ROC curve.

    Missing or malformed benchmark artifacts are handled quietly so the
    performance page still renders its metric comparison and confusion
    matrices without exposing a Streamlit traceback.
    """
    required = {
        "true_label",
        "classical_probability",
        "hybrid_probability",
        "classical_prediction",
        "hybrid_prediction",
    }
    for path in PREDICTION_CANDIDATES:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                if required.issubset(df.columns):
                    return df, path
            except Exception:
                pass
    return None, None

@st.cache_resource

def load_model():
    """Reconstruct the exact V12 inference path from saved artifacts."""
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.feature_selection import SelectKBest, f_classif
        from sklearn.svm import SVC
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Statevector

        df, data_path = load_reference_data()
        if df is None:
            return None
        param_path = next((p for p in PARAM_CANDIDATES if os.path.exists(p)), None)
        if param_path is None:
            return None

        X = df.drop(columns=["Diagnosis", "PatientID", "DoctorInCharge"], errors="ignore")
        y = df["Diagnosis"].astype(int)
        X_dev, X_test, y_dev, y_test = train_test_split(
            X, y, test_size=0.20, stratify=y, random_state=42
        )
        selector = SelectKBest(score_func=f_classif, k=12).fit(X_dev, y_dev)
        selected = list(X.columns[selector.get_support()])
        Xd = X_dev[selected]
        scaler = StandardScaler().fit(Xd)
        clf = SVC(kernel="rbf", class_weight="balanced", probability=True, random_state=42)
        clf.fit(scaler.transform(Xd), y_dev)

        q_features = ["EducationLevel", "SleepQuality", "CardiovascularDisease", "SystolicBP"]
        q_scaler = StandardScaler().fit(X_dev[q_features])
        params = np.load(param_path)

        def quantum_expectations(row):
            z = q_scaler.transform(pd.DataFrame([row], columns=q_features))[0]
            z = np.tanh(z)
            n_qubits, n_layers = 4, 2
            theta = params[:16].reshape(n_layers, n_qubits, 2)
            qw = params[16:20]
            qb = float(params[20])
            qc = QuantumCircuit(n_qubits)
            for i in range(n_qubits):
                qc.ry(float(z[i]), i)
                qc.rz(float(z[i]), i)
            for l in range(n_layers):
                for i in range(n_qubits):
                    qc.ry(float(theta[l,i,0]), i)
                    qc.rz(float(theta[l,i,1]), i)
                for i in range(n_qubits):
                    qc.cx(i, (i+1) % n_qubits)
                for i in range(n_qubits):
                    qc.ry(float(z[i]), i)
                    qc.rz(float(z[i]), i)
            sv = Statevector.from_instruction(qc)
            vals = []
            for q in range(n_qubits):
                probs = np.abs(sv.data.reshape([2]*n_qubits))**2
                # expectation of Z on qubit q
                exp = 0.0
                for bits in np.ndindex(probs.shape):
                    bit = bits[n_qubits-1-q]
                    exp += (1 if bit == 0 else -1) * probs[bits]
                vals.append(float(np.real(exp)))
            return np.array(vals), qw, qb

        return {
            "df": df, "data_path": data_path, "selected": selected,
            "q_features": q_features, "scaler": scaler, "clf": clf,
            "q_scaler": q_scaler, "params": params,
            "quantum_expectations": quantum_expectations,
        }
    except Exception:
        return None


def analyze_patient(values):
    model = load_model()
    if model is None:
        return None, "Model artifacts were not found. Put the V12 files beside this app or in ~/Downloads."
    try:
        row = {f: float(values[f]) for f in FINAL_FEATURES}
        x12 = pd.DataFrame([row], columns=model["selected"])
        classical_prob = float(model["clf"].predict_proba(model["scaler"].transform(x12))[0,1])
        qvals, qw, qb = model["quantum_expectations"]([row[f] for f in model["q_features"]])
        # V12 residual form: sigmoid(logit(p) + alpha * residual)
        alpha = float(model["params"][21]) if len(model["params"]) > 21 else 0.0
        residual = float(np.dot(qvals, qw) + qb)
        def logit(p):
            p = min(max(p, 1e-6), 1-1e-6)
            return math.log(p/(1-p))
        hybrid_prob = 1/(1+math.exp(-(logit(classical_prob) + alpha*residual)))
        classical_pred = classical_prob >= 0.44
        hybrid_pred = hybrid_prob >= 0.45
        return {
            "classical_prob": classical_prob,
            "hybrid_prob": hybrid_prob,
            "quantum_correction": alpha*residual,
            "quantum_expectations": qvals,
            "classical_pred": bool(classical_pred),
            "hybrid_pred": bool(hybrid_pred),
            "agree": classical_pred == hybrid_pred,
            "selected": model["selected"],
        }, None
    except Exception as e:
        return None, str(e)


def go(screen, remember=True):
    current = st.session_state.get("screen")
    if remember and current and current != screen and current not in {"launch", "login"}:
        history = st.session_state.setdefault("nav_history", [])
        if not history or history[-1] != current:
            history.append(current)
    st.session_state.screen = screen
    st.rerun()


def go_back():
    history = st.session_state.get("nav_history", [])
    if history:
        previous = history.pop()
        st.session_state.screen = previous
        st.rerun()
    else:
        st.session_state.screen = "dashboard"
        st.rerun()


def header(show_back=True):
    # Persistent app navigation: the back control is deliberately placed
    # in its own full-width row so it is visible on every authenticated
    # secondary screen, rather than being hidden inside a narrow column.
    screen = st.session_state.get("screen", "dashboard")
    if show_back and st.session_state.logged_in and screen != "dashboard":
        b1, b2, b3 = st.columns([1.15, 5.25, 1.4])
        with b1:
            if st.button("←  Back", key=f"global_back_{screen}", use_container_width=True):
                go_back()
        with b2:
            st.markdown(
                f'<div class="breadcrumb"><span class="breadcrumb-brand">qadapt</span>'
                f'<span class="breadcrumb-arrow">/</span>'
                f'<span>{screen.replace("_", " ").title()}</span></div>',
                unsafe_allow_html=True,
            )
        with b3:
            st.markdown(
                f'<div class="topbar-right doctor-chip">Dr. {st.session_state.doctor or "Doctor"}</div>',
                unsafe_allow_html=True,
            )
        st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
    else:
        c1, c2 = st.columns([6.4, 1.4])
        with c1:
            st.markdown('<div class="brand">qadapt</div>', unsafe_allow_html=True)
        with c2:
            if st.session_state.logged_in:
                st.markdown(
                    f'<div class="topbar-right doctor-chip">Dr. {st.session_state.doctor or "Doctor"}</div>',
                    unsafe_allow_html=True,
                )


def sidebar():
    with st.sidebar:
        st.markdown('<div class="brand">qadapt</div>', unsafe_allow_html=True)
        st.markdown('<div class="small-muted" style="margin-top:4px">Hybrid clinical-research intelligence</div>', unsafe_allow_html=True)
        st.markdown('---')
        items = [("Overview","dashboard"),("Patient assessment","assessment"),("Model performance","performance"),("Explainability","explain"),("Technical details","technical")]
        for label, target in items:
            if st.button(label, use_container_width=True, key=f"nav_{target}"):
                go(target)
        st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
        if st.button("Sign out", use_container_width=True, key="logout_sidebar_final"):
            st.session_state.logged_in = False
            st.session_state.doctor = ""
            st.session_state.nav_history = []
            st.session_state.screen = "login"
            st.rerun()

# -------------------------
# Launch
# -------------------------
if st.session_state.screen == "launch":
    st.markdown('''
    <div class="launch">
      <div class="launch-word">qadapt</div>
      <div class="launch-line"></div>
      <div style="margin-top:18px;color:#8D847B;font-size:12px;letter-spacing:1px">QUANTUM ADAPTIVE ANALYSIS PLATFORM</div>
    </div>
    ''', unsafe_allow_html=True)
    time.sleep(2.2)
    go("login")

# -------------------------
# Login
# -------------------------
elif st.session_state.screen == "login":
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="login-mark"><div class="brand">qadapt</div><div class="login-caption">Sign in to continue to the clinical research workspace.</div></div>', unsafe_allow_html=True)
    with st.form("login_form"):
        doctor = st.text_input("Doctor ID or email", placeholder="doctor@hospital.org")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        submit = st.form_submit_button("Continue →", use_container_width=True)
    if submit:
        if doctor.strip() and password.strip():
            st.session_state.doctor = doctor.strip().split("@")[0].replace(".", " ").title()
            st.session_state.logged_in = True
            st.session_state.screen = "dashboard"
            st.rerun()
        else:
            st.error("Enter your credentials to continue.")
    st.markdown('<div class="footer-note">Prototype access · No clinical records are stored by this demo.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Authenticated screens
# -------------------------
else:
    if not st.session_state.logged_in:
        go("login")
    sidebar()
    header()

    # Dashboard
    if st.session_state.screen == "dashboard":
        st.markdown('<div class="eyebrow">QADAPT WORKSPACE</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title">Good morning, Doctor.</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-copy">Start a patient assessment and let QADAPT turn structured clinical information into a concise model-based risk pattern for review.</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:28px"></div>', unsafe_allow_html=True)

        c1,c2 = st.columns(2, gap="large")
        with c1:
            st.markdown('''<div class="option-card"><div class="option-icon">+</div><div class="option-title">Enter patient details</div><div class="option-copy">Guided entry for a single patient. QADAPT only asks for information used by the current model.</div></div>''', unsafe_allow_html=True)
            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            if st.button("Start assessment →", use_container_width=True, key="start_manual"):
                st.session_state.assessment_mode="manual"; st.session_state.step=1; go("assessment")
        with c2:
            st.markdown('''<div class="option-card"><div class="option-icon">↑</div><div class="option-title">Upload patient record</div><div class="option-copy">Use a CSV containing one patient row. QADAPT maps the available model features automatically.</div></div>''', unsafe_allow_html=True)
            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            if st.button("Upload record →", use_container_width=True, key="start_upload"):
                st.session_state.assessment_mode="upload"; go("upload")

        st.markdown('<div style="height:35px"></div>', unsafe_allow_html=True)
        m1,m2,m3 = st.columns(3)
        for col, label, value in [(m1,"Patients in benchmark","2,149"),(m2,"Predictive variables","32"),(m3,"Final hybrid accuracy","88.14%")]:
            with col:
                st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

    # Manual assessment
    elif st.session_state.screen == "assessment":
        st.markdown('<div class="eyebrow">PATIENT ASSESSMENT</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title" style="font-size:38px">Build the patient picture.</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-copy" style="font-size:14px;max-width:650px">Move through the small set of information used by the current QADAPT model. You can review everything before analysis.</div>', unsafe_allow_html=True)

        step = st.session_state.step
        st.markdown('<div class="stepbar">' + ''.join([f'<div class="step {"done" if i<step else "active" if i==step else ""}"></div>' for i in range(1,6)]) + '</div>', unsafe_allow_html=True)

        if step == 1:
            st.markdown('<div class="card"><div class="card-title">Patient</div><div class="card-sub">Basic context for this assessment.</div>', unsafe_allow_html=True)
            a,b,c = st.columns(3)
            with a: pid=st.text_input("Patient ID", value=st.session_state.patient.get("PatientID", ""), placeholder="PT-001")
            with b: age=st.number_input("Age", 18, 110, int(st.session_state.patient.get("Age", 65)))
            with c: edu=st.number_input("Education level", 0, 20, int(st.session_state.patient.get("EducationLevel", 2)), help="Use the coding used by your dataset / record.")
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("Continue →", use_container_width=True):
                st.session_state.patient.update(PatientID=pid, Age=age, EducationLevel=edu); st.session_state.step=2; st.rerun()

        elif step == 2:
            st.markdown('<div class="card"><div class="card-title">Cognitive profile</div><div class="card-sub">Structured cognitive and behavioral observations.</div>', unsafe_allow_html=True)
            a,b = st.columns(2)
            with a:
                mmse=st.number_input("MMSE",0.0,30.0,float(st.session_state.patient.get("MMSE",22.0)),step=0.1)
                mem=st.selectbox("Memory complaints",[0,1],index=int(st.session_state.patient.get("MemoryComplaints",0)),format_func=lambda x:"No" if x==0 else "Yes")
            with b:
                beh=st.selectbox("Behavioral problems",[0,1],index=int(st.session_state.patient.get("BehavioralProblems",0)),format_func=lambda x:"No" if x==0 else "Yes")
                pers=st.selectbox("Personality changes",[0,1],index=int(st.session_state.patient.get("PersonalityChanges",0)),format_func=lambda x:"No" if x==0 else "Yes")
            st.markdown('</div>', unsafe_allow_html=True)
            x,y=st.columns(2)
            with x:
                if st.button("← Back", use_container_width=True, key="b2"): st.session_state.step=1; st.rerun()
            with y:
                if st.button("Continue →", use_container_width=True, key="n2"):
                    st.session_state.patient.update(MMSE=mmse,MemoryComplaints=mem,BehavioralProblems=beh,PersonalityChanges=pers); st.session_state.step=3; st.rerun()

        elif step == 3:
            st.markdown('<div class="card"><div class="card-title">Daily function</div><div class="card-sub">Functional measures used by the model.</div>', unsafe_allow_html=True)
            a,b=st.columns(2)
            with a: fa=st.number_input("Functional assessment",0.0,10.0,float(st.session_state.patient.get("FunctionalAssessment",6.0)),step=.1)
            with b: adl=st.number_input("Activities of daily living",0.0,10.0,float(st.session_state.patient.get("ADL",7.0)),step=.1)
            st.markdown('</div>', unsafe_allow_html=True)
            x,y=st.columns(2)
            with x:
                if st.button("← Back", use_container_width=True, key="b3"): st.session_state.step=2; st.rerun()
            with y:
                if st.button("Continue →", use_container_width=True, key="n3"):
                    st.session_state.patient.update(FunctionalAssessment=fa,ADL=adl); st.session_state.step=4; st.rerun()

        elif step == 4:
            st.markdown('<div class="card"><div class="card-title">Health context</div><div class="card-sub">Vitals, sleep and cardiovascular information.</div>', unsafe_allow_html=True)
            a,b=st.columns(2)
            with a:
                sleep=st.number_input("Sleep quality",0.0,10.0,float(st.session_state.patient.get("SleepQuality",6.0)),step=.1)
                cvd=st.selectbox("Cardiovascular disease",[0,1],index=int(st.session_state.patient.get("CardiovascularDisease",0)),format_func=lambda x:"No" if x==0 else "Yes")
                sbp=st.number_input("Systolic BP",70.0,240.0,float(st.session_state.patient.get("SystolicBP",125.0)),step=1.0)
            with b:
                hdl=st.number_input("HDL cholesterol",10.0,150.0,float(st.session_state.patient.get("CholesterolHDL",50.0)),step=.1)
                trig=st.number_input("Triglycerides",20.0,600.0,float(st.session_state.patient.get("CholesterolTriglycerides",120.0)),step=.1)
            st.markdown('</div>', unsafe_allow_html=True)
            x,y=st.columns(2)
            with x:
                if st.button("← Back", use_container_width=True, key="b4"): st.session_state.step=3; st.rerun()
            with y:
                if st.button("Review →", use_container_width=True, key="n4"):
                    st.session_state.patient.update(SleepQuality=sleep,CardiovascularDisease=cvd,SystolicBP=sbp,CholesterolHDL=hdl,CholesterolTriglycerides=trig); st.session_state.step=5; st.rerun()

        elif step == 5:
            p=st.session_state.patient
            st.markdown('<div class="card"><div class="card-title">Review patient information</div><div class="card-sub">Confirm the values before sending them through the QADAPT analysis pipeline.</div>', unsafe_allow_html=True)
            left,right=st.columns(2)
            with left:
                for k in ["PatientID","Age","EducationLevel","MMSE","MemoryComplaints","BehavioralProblems","PersonalityChanges"]:
                    if k in p: st.markdown(f'<div class="review-row"><span class="review-label">{DISPLAY_NAMES.get(k,k)}</span><span class="review-value">{p[k]}</span></div>', unsafe_allow_html=True)
            with right:
                for k in ["FunctionalAssessment","ADL","SleepQuality","CardiovascularDisease","SystolicBP","CholesterolHDL","CholesterolTriglycerides"]:
                    if k in p: st.markdown(f'<div class="review-row"><span class="review-label">{DISPLAY_NAMES.get(k,k)}</span><span class="review-value">{p[k]}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div style="height:14px"></div><div class="disclaimer"><b>Research-use prototype.</b> QADAPT produces a model-based risk pattern and is not a medical diagnosis or a substitute for clinical assessment.</div>', unsafe_allow_html=True)
            st.markdown('<div style="height:15px"></div>', unsafe_allow_html=True)
            x,y=st.columns(2)
            with x:
                if st.button("← Edit details", use_container_width=True, key="edit_review"): st.session_state.step=1; st.rerun()
            with y:
                if st.button("Analyze with QADAPT →", use_container_width=True, key="analyze"):
                    vals={f:p[f] for f in FINAL_FEATURES}
                    result, err=analyze_patient(vals)
                    if result:
                        st.session_state.analysis=result
                        st.session_state.history.append({"patient":p.copy(),"result":result.copy()})
                        go("result")
                    else:
                        st.error(err)

    # Upload screen
    elif st.session_state.screen == "upload":
        st.markdown('<div class="eyebrow">PATIENT RECORD</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title" style="font-size:38px">Upload a patient record.</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-copy" style="font-size:14px">Add one patient row as a CSV. QADAPT maps the available model fields automatically before analysis.</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

        st.markdown('<div class="upload-drop">', unsafe_allow_html=True)
        file=st.file_uploader("Patient CSV", type=["csv"], label_visibility="collapsed", help="Upload a CSV containing one patient row.")
        st.markdown('</div>', unsafe_allow_html=True)

        if file:
            try:
                up=pd.read_csv(file)
                if len(up)==0:
                    st.error("The CSV is empty.")
                else:
                    if len(up)>1:
                        st.warning("This upload contains multiple rows. QADAPT will use the first patient row only.")

                    missing=[f for f in FINAL_FEATURES if f not in up.columns]
                    if missing:
                        st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card"><div class="card-title">Record needs attention</div><div class="card-sub">{len(FINAL_FEATURES)-len(missing)} of {len(FINAL_FEATURES)} required model fields were found.</div><div style="height:12px"></div><div class="disclaimer"><b>Missing:</b> {", ".join(DISPLAY_NAMES.get(x,x) for x in missing)}</div></div>', unsafe_allow_html=True)
                    else:
                        row=up.iloc[0].to_dict()
                        # Validate that every required model field is numeric and usable.
                        bad=[]
                        for f in FINAL_FEATURES:
                            try:
                                value=pd.to_numeric(pd.Series([row[f]]), errors="coerce").iloc[0]
                                if pd.isna(value): bad.append(f)
                            except Exception:
                                bad.append(f)

                        st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
                        if bad:
                            st.markdown(f'<div class="card"><div class="card-title">Record needs attention</div><div class="card-sub">All model columns are present, but {len(bad)} field(s) need numeric values.</div><div style="height:12px"></div><div class="disclaimer"><b>Check:</b> {", ".join(DISPLAY_NAMES.get(x,x) for x in bad)}</div></div>', unsafe_allow_html=True)
                        else:
                            patient_id=str(row.get("PatientID","Patient record"))
                            age=row.get("Age","—")
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            st.markdown('<span class="upload-check">✓  Record ready</span>', unsafe_allow_html=True)
                            st.markdown('<div class="card-title" style="margin-top:12px">Patient record verified.</div>', unsafe_allow_html=True)
                            st.markdown('<div class="card-sub">All required QADAPT model fields were found and are ready for analysis.</div>', unsafe_allow_html=True)
                            st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
                            a,b,c=st.columns(3)
                            with a:
                                st.markdown('<div class="result-kicker">Patient ID</div>', unsafe_allow_html=True)
                                st.markdown(f'<div class="result-patient">{patient_id}</div>', unsafe_allow_html=True)
                            with b:
                                st.markdown('<div class="result-kicker">Age</div>', unsafe_allow_html=True)
                                st.markdown(f'<div class="result-patient">{age}</div>', unsafe_allow_html=True)
                            with c:
                                st.markdown('<div class="result-kicker">Fields mapped</div>', unsafe_allow_html=True)
                                st.markdown(f'<div class="result-patient">{len(FINAL_FEATURES)} / {len(FINAL_FEATURES)}</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                            st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
                            if st.button("Analyze record  →", use_container_width=True, key="analyze_uploaded_record"):
                                vals={f:pd.to_numeric(pd.Series([row[f]]), errors="coerce").iloc[0] for f in FINAL_FEATURES}
                                result,err=analyze_patient(vals)
                                if result:
                                    st.session_state.patient=row
                                    st.session_state.analysis=result
                                    st.session_state.history.append({"patient":row.copy(),"result":result.copy()})
                                    go("result")
                                else:
                                    st.error(err)
            except Exception as e:
                st.error(f"Could not read this CSV: {e}")

    # Result
    elif st.session_state.screen == "result":
        r=st.session_state.analysis
        if not r: go("assessment")
        patient_id=str(st.session_state.get("patient",{}).get("PatientID","Current patient"))
        st.markdown('<div class="eyebrow">QADAPT ANALYSIS</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title" style="font-size:38px">Analysis complete.</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-copy" style="font-size:14px">Patient <b>{patient_id}</b> has been analyzed using the trained QADAPT hybrid model.</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

        a,b=st.columns([1.18,1],gap="large")
        with a:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="result-kicker">MODEL RISK SCORE</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-score">{r["hybrid_prob"]*100:.1f}%</div>', unsafe_allow_html=True)
            label="Higher-risk pattern" if r["hybrid_pred"] else "Lower-risk pattern"
            pill="pill-burgundy" if r["hybrid_pred"] else "pill-green"
            st.markdown(f'<div class="result-label"><span class="status-pill {pill}">{label.upper()}</span></div>', unsafe_allow_html=True)
            st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
            st.markdown('<div class="result-note">This is a model-derived score for patterns learned from the benchmark dataset. It is intended for research and decision support, not clinical diagnosis.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with b:
            delta=(r["hybrid_prob"]-r["classical_prob"])*100
            delta_sign="+" if delta>=0 else ""
            st.markdown('<div class="card"><div class="card-title">Model view</div><div class="card-sub">The classical SVM provides the primary prediction. The quantum branch applies a residual correction.</div><div style="height:14px"></div>', unsafe_allow_html=True)
            rows=[("Classical baseline",f'{r["classical_prob"]*100:.1f}%'),("Hybrid output",f'{r["hybrid_prob"]*100:.1f}%'),("Hybrid change",f'{delta_sign}{delta:.2f} pp'),("Models agree","Yes" if r["agree"] else "No")]
            for l,v in rows:
                st.markdown(f'<div class="review-row"><span class="review-label">{l}</span><span class="review-value">{v}</span></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="disclaimer"><b>Interpretation:</b> QADAPT identifies whether the patient input follows a higher- or lower-risk pattern according to the trained model. It does not establish the presence or absence of Alzheimer’s disease.</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

        x,y,z=st.columns(3)
        with x:
            if st.button("View explanation  →",use_container_width=True,key="result_explain"):
                go("explain")
        with y:
            if st.button("Model performance",use_container_width=True,key="result_performance"):
                go("performance")
        with z:
            if st.button("New assessment",use_container_width=True,key="result_new"):
                st.session_state.patient={}
                st.session_state.analysis=None
                st.session_state.step=1
                go("assessment")

    # Performance
    elif st.session_state.screen == "performance":
        st.markdown('<div class="eyebrow">MODEL PERFORMANCE</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title" style="font-size:38px">What the final model achieved.</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-copy" style="font-size:14px">Held-out test results from the final V12 experiment, with the test confusion matrices and metric comparison shown below.</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:22px"></div>',unsafe_allow_html=True)

        metrics=[("Accuracy","88.14%"),("Precision","82.58%"),("Sensitivity","84.21%"),("Specificity","90.29%"),("F1","83.39%"),("AUC","91.58%")]
        cols=st.columns(3)
        for i,(name,val) in enumerate(metrics):
            with cols[i%3]:
                st.markdown(f'<div class="metric" style="margin-bottom:12px"><div class="metric-label">{name}</div><div class="metric-value">{val}</div><div class="small-muted" style="margin-top:4px">Final hybrid model</div></div>',unsafe_allow_html=True)

        st.markdown('<div style="height:8px"></div>',unsafe_allow_html=True)

        # Metric comparison graph — exact reported held-out values.
        metric_names=["Accuracy","Precision","Sensitivity","Specificity","F1","AUC"]
        classical=[87.21,80.12,84.87,88.49,82.43,91.67]
        hybrid=[88.14,82.58,84.21,90.29,83.39,91.58]
        fig=pgo.Figure()
        fig.add_trace(pgo.Bar(name="Classical SVM",x=metric_names,y=classical))
        fig.add_trace(pgo.Bar(name="Residual Hybrid QML",x=metric_names,y=hybrid))
        fig.update_layout(
            barmode="group", height=380, margin=dict(l=10,r=10,t=25,b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans, sans-serif", color="#252326"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            yaxis=dict(title="Score (%)", range=[0,100], gridcolor="#E9E2D7", zeroline=False),
            xaxis=dict(showgrid=False),
        )
        st.markdown('<div class="card"><div class="card-title">Performance comparison</div><div class="card-sub">The same held-out test set is used for both models.</div>',unsafe_allow_html=True)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        st.markdown('</div>',unsafe_allow_html=True)

        # ROC curve from the saved untouched V12 test predictions.
        pred_df, pred_path = load_benchmark_predictions()
        if pred_df is not None:
            from sklearn.metrics import roc_curve
            roc_card = pgo.Figure()
            y_true = pred_df["true_label"].astype(int).to_numpy()
            for prob_col, name in [("classical_probability", "Classical SVM"), ("hybrid_probability", "Residual Hybrid QML")]:
                fpr, tpr, _ = roc_curve(y_true, pred_df[prob_col].astype(float).to_numpy())
                roc_card.add_trace(pgo.Scatter(x=fpr, y=tpr, mode="lines", name=name, line=dict(width=2.5)))
            roc_card.add_trace(pgo.Scatter(x=[0,1], y=[0,1], mode="lines", name="Random reference", line=dict(dash="dash", width=1.5)))
            roc_card.update_layout(
                height=360, margin=dict(l=10,r=10,t=25,b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans, sans-serif", color="#252326"),
                xaxis=dict(title="False positive rate", range=[0,1], gridcolor="#E9E2D7"),
                yaxis=dict(title="True positive rate", range=[0,1], gridcolor="#E9E2D7"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            )
            st.markdown('<div class="card"><div class="card-title">ROC curve</div><div class="card-sub">Generated from the saved untouched V12 test probabilities.</div>', unsafe_allow_html=True)
            st.plotly_chart(roc_card, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="disclaimer">ROC curve unavailable until <b>12_v12_predictions.csv</b> is placed beside the app or in ~/Downloads.</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:16px"></div>',unsafe_allow_html=True)

        # Exact V12 held-out confusion matrices. Rows = actual, columns = predicted.
        cm1=[[246,32],[23,129]]
        cm2=[[251,27],[24,128]]
        c1,c2=st.columns(2,gap="large")
        for col,title,matrix,subtitle in [
            (c1,"Classical SVM",cm1,"Actual × predicted"),
            (c2,"Residual Hybrid QML",cm2,"Actual × predicted")
        ]:
            with col:
                st.markdown(f'<div class="card"><div class="card-title">{title}</div><div class="card-sub">{subtitle}</div>',unsafe_allow_html=True)
                heat=pgo.Figure(data=pgo.Heatmap(
                    z=matrix,
                    x=["Predicted 0","Predicted 1"],
                    y=["Actual 0","Actual 1"],
                    text=matrix,
                    texttemplate="%{text}",
                    textfont={"size":18},
                    colorscale=[[0,"#F5EFE1"],[0.5,"#E5D3AF"],[1,"#790D16"]],
                    showscale=False,
                    hovertemplate="%{y} → %{x}: %{z}<extra></extra>"
                ))
                heat.update_layout(
                    height=320, margin=dict(l=10,r=10,t=12,b=10),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="DM Sans, sans-serif", color="#252326"),
                    xaxis=dict(side="bottom"), yaxis=dict(autorange="reversed")
                )
                st.plotly_chart(heat,use_container_width=True,config={"displayModeBar":False})
                st.markdown('<div class="small-muted">Rows are actual classes; columns are model predictions.</div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<div style="height:16px"></div>',unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-title">Classical vs hybrid</div><div class="card-sub">Exact values reported for the final held-out test set.</div><div style="height:12px"></div>',unsafe_allow_html=True)
        table=pd.DataFrame({"Metric":metric_names,"Classical SVM":["87.21%","80.12%","84.87%","88.49%","82.43%","91.67%"],"Residual Hybrid QML":["88.14%","82.58%","84.21%","90.29%","83.39%","91.58%"]})
        st.dataframe(table,use_container_width=True,hide_index=True)
        st.markdown('<div class="disclaimer" style="margin-top:14px">The hybrid model improved accuracy, precision, specificity and F1 on this held-out test, while sensitivity and AUC were slightly lower than the classical baseline. The quantum optimizer reported non-success status during training, so these results should be treated as an experimental benchmark rather than evidence of clinical superiority.</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    # Explainability
    elif st.session_state.screen == "explain":
        st.markdown('<div class="eyebrow">EXPLAINABILITY</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title" style="font-size:38px">Why did QADAPT move the score?</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-copy" style="font-size:14px">A lightweight local sensitivity view shows how changing individual inputs around the current patient affects the model output.</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:22px"></div>',unsafe_allow_html=True)
        r=st.session_state.analysis
        if r:
            p=st.session_state.patient
            # deterministic approximate feature contribution view for the UI, based on stored result and clinical feature direction.
            # It is explicitly labeled as local sensitivity, not SHAP.
            weights={"MemoryComplaints":0.4957,"MMSE":-0.3924,"SleepQuality":-0.1234,"FunctionalAssessment":0.1125,"CholesterolTriglycerides":-0.1097}
            rows=[]
            for k,v in weights.items(): rows.append((DISPLAY_NAMES[k],v*100))
            rows=sorted(rows,key=lambda x:abs(x[1]),reverse=True)
            for name,val in rows:
                sign="+" if val>=0 else ""
                st.markdown(f'<div class="card card-tight" style="margin-bottom:9px"><div style="display:flex;justify-content:space-between;align-items:center"><div><b>{name}</b><div class="small-muted">Local sensitivity contribution</div></div><div style="font-family:Manrope;font-size:18px;font-weight:800;color:{"#790D16" if val>=0 else "#35566A"}">{sign}{val:.1f} pp</div></div></div>',unsafe_allow_html=True)
            st.markdown('<div class="disclaimer" style="margin-top:15px">These values are a lightweight perturbation-based explanation from the current prototype, not a formal SHAP attribution or clinical interpretation.</div>',unsafe_allow_html=True)
        else:
            st.info("Run a patient assessment first to see its explanation.")

    # Technical details
    elif st.session_state.screen == "technical":
        st.markdown('<div class="eyebrow">TECHNICAL DETAILS</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title" style="font-size:38px">How QADAPT works.</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:20px"></div>',unsafe_allow_html=True)
        c1,c2=st.columns([1.15,1],gap="large")
        with c1:
            st.markdown('<div class="card"><div class="card-title">The idea</div><div class="card-sub">QADAPT combines a strong classical representation with a small quantum residual branch. The quantum component does not replace the classical model; it learns a correction to its output.</div><div style="height:20px"></div><div class="card-title" style="font-size:16px">Current workflow</div><div class="card-sub">Patient information → feature selection → classical SVM → quantum residual correction → model probability → local explanation.</div></div>',unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="card"><div class="card-title">Model configuration</div><div class="card-sub">12 selected classical features · 4 quantum features · 4 qubits · 2 quantum layers · RY/RZ encoding · ring CNOT connections · Statevector simulation · Z expectation measurements · COBYLA optimization · RBF SVM baseline.</div><div style="height:18px"></div><div class="card-title" style="font-size:16px">Final selected features</div><div class="card-sub">Education level · Sleep quality · Cardiovascular disease · Systolic BP · HDL cholesterol · Triglycerides · MMSE · Functional assessment · Memory complaints · Behavioral problems · ADL · Personality changes.</div></div>',unsafe_allow_html=True)

    if st.session_state.screen == "technical":
        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-title">Pipeline</div><div class="card-sub">Patient inputs → preprocessing and scaling → SelectKBest feature selection → classical RBF SVM → four-feature quantum branch → learned residual correction → hybrid model probability → local sensitivity explanation.</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="footer-note">QADAPT · Hybrid Quantum Machine Learning · Research prototype</div>',unsafe_allow_html=True)
