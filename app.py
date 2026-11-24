import io
import pandas as pd
import streamlit as st
import core
import export as pdf_export

st.set_page_config(page_title="BuildEstimator | Estimasi Material Bangunan", page_icon="🏗️", layout="wide")

# ------------------------------------------------------------------ tema
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] {font-family:'Inter',sans-serif;}
.stApp {color:#E6F0F3; background:
   radial-gradient(1200px 500px at 85% -10%, rgba(124,224,46,.14), transparent 60%),
   radial-gradient(900px 500px at -10% 110%, rgba(56,189,248,.10), transparent 60%),
   #0C171B;}
.block-container {max-width:1180px; padding-top:1.2rem; padding-bottom:4rem;}
header[data-testid="stHeader"] {background:transparent;}
h1,h2,h3 {font-family:'Rajdhani',sans-serif !important; letter-spacing:.5px;}

/* stepper */
.stepper {display:flex; gap:6px; margin:0 0 1.4rem 0;}
.stp {flex:1; text-align:center; padding:8px 2px 6px; border-radius:10px; background:#142329;
      border:1px solid #23404a; font-family:'Rajdhani'; font-weight:600; font-size:.78rem; color:#7e98a1;}
.stp b {display:block; font-size:1.15rem; line-height:1.1;}
.stp.done {background:#1d3a2a; border-color:#3d7a3f; color:#a6e58c;}
.stp.now {background:linear-gradient(135deg,#7CE02E,#2BD4A5); color:#06150b; border-color:#7CE02E;
          box-shadow:0 0 18px rgba(124,224,46,.45); transform:translateY(-2px);}
@media(max-width:700px){.stp span{display:none}}

/* cover */
.cover {position:relative; overflow:hidden; border-radius:22px; padding:3.2rem 2.4rem 2.6rem;
  background:
   linear-gradient(115deg, transparent 48%, rgba(255,255,255,.05) 48.4%, transparent 49%),
   linear-gradient(62deg, transparent 30%, rgba(255,255,255,.05) 30.4%, transparent 31%),
   linear-gradient(160deg, transparent 70%, rgba(255,255,255,.05) 70.4%, transparent 71%),
   linear-gradient(135deg,#1c2b30 0%,#22363c 55%,#183a2c 100%);
  border:1px solid #2f4a52; box-shadow:0 18px 50px rgba(0,0,0,.45);}
.cover:after {content:"🏗️"; position:absolute; right:26px; top:10px; font-size:9rem; opacity:.10; transform:rotate(14deg);}
.kicker {font-family:'Rajdhani'; letter-spacing:4px; color:#7CE02E; font-weight:700; font-size:.95rem;}
.cover h1 {font-family:'Rajdhani',sans-serif !important; font-size:4.6rem; line-height:.95; margin:.3rem 0 .2rem;
  letter-spacing:3px; background:linear-gradient(90deg,#fff,#c9ff9b 45%,#7CE02E); -webkit-background-clip:text; color:transparent;}
.cover h1 span {display:block; font-size:2rem; letter-spacing:6px; -webkit-text-fill-color:#6fdcf4;}
.cover p {color:#cfe3d4; font-size:1.05rem; max-width:620px;}
.pct {display:inline-block; margin-top:.8rem; padding:.35rem .9rem; border-radius:999px; background:#7CE02E; color:#07130A;
  font-family:'Rajdhani'; letter-spacing:2px; font-size:1.15rem; transform:rotate(-2deg);}
.cards {display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:14px; margin:1.3rem 0;}
.card {background:#142329; border:1px solid #23404a; border-radius:16px; padding:1.1rem 1.2rem;}
.card:hover {border-color:#7CE02E; transform:translateY(-3px); transition:.2s;}
.card .ic {font-size:1.8rem;} .card h4 {margin:.3rem 0 .2rem; font-family:'Rajdhani'; font-size:1.2rem; color:#EAF4E4;}
.card p {margin:0; color:#9db4ab; font-size:.9rem;}
.flow {display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:.6rem 0 0; color:#9db4ab; font-size:.9rem;}
.flow i {background:#142329; border:1px solid #2b4a52; border-radius:8px; padding:3px 10px; font-style:normal; color:#cfe9c8;}

/* page header */
.phead {display:flex; align-items:center; gap:16px; margin-bottom:.8rem;}
.pnum {font-family:'Rajdhani'; font-size:3.2rem; color:#07130A; background:#7CE02E; border-radius:16px; min-width:70px; height:70px;
  display:flex; align-items:center; justify-content:center; transform:rotate(-4deg); box-shadow:0 6px 0 #3d7a3f;}
.phead h2 {margin:0; font-size:2rem;} .phead small {color:#8fb0a0;}
.bubble {position:relative; background:#eaf6e2; color:#10241a; border-radius:16px; padding:.75rem 1rem; margin:.4rem 0 1.2rem 0;
  font-weight:500; border:2px solid #7CE02E; max-width:760px;}
.bubble:before {content:"CATATAN TEKNIS:"; font-family:'Rajdhani'; letter-spacing:1.5px; color:#2a8a2f; margin-right:6px;}

div[data-testid="stMetric"] {background:#142329; border:1px solid #23404a; padding:14px; border-radius:14px;}
div[data-testid="stMetricValue"] {color:#7CE02E; font-family:'Rajdhani';}
button[kind="primary"], .stDownloadButton button[kind="primary"] {color:#06150b !important; font-weight:700 !important;
   background:linear-gradient(135deg,#7CE02E,#2BD4A5) !important; border:none !important;}
button[kind="primary"]:hover {filter:brightness(1.08); transform:translateY(-1px);}
div[data-testid="stExpander"] {border:1px solid #23404a; border-radius:12px; background:#101e23;}
section[data-testid="stSidebar"] {background:#101f25; border-right:1px solid #31505a;}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] small {color:#D7E7EC !important;}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {color:#9FB8C1 !important;}
section[data-testid="stSidebar"] [data-testid="stRadio"] label {color:#D7E7EC !important;}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {color:#D7E7EC !important;}
.stButton button {border-radius:10px !important;}
.stepper button {font-size:.72rem !important; line-height:1.15 !important; padding:.45rem .15rem !important; min-height:3.25rem !important; white-space:normal !important;}
/* ===== KEBACAAN: warna eksplisit, tidak bergantung tema browser/Streamlit ===== */
.stApp label, .stApp [data-testid="stWidgetLabel"], .stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] p,
.stApp [data-testid="stMarkdownContainer"] p, .stApp [data-testid="stMarkdownContainer"] li {color:#DCEBE3;}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {color:#EAF4E4;}
.stApp .bubble {color:#10241a;}
.stApp .pct {color:#07130A;}
.stApp [data-testid="stMetricLabel"], .stApp [data-testid="stMetricLabel"] * {color:#B9D0C6 !important;}
.stApp [data-testid="stExpander"] summary, .stApp [data-testid="stExpander"] summary * {color:#EAF4E4 !important;}
.stApp button[data-baseweb="tab"] * {color:#CFE3D8 !important;}
.stApp button[data-baseweb="tab"][aria-selected="true"] * {color:#7CE02E !important;}

/* tombol: latar putih -> teks hitam */
.stApp div.stButton > button, .stApp div.stDownloadButton > button {background:#FFFFFF !important; border:1px solid #b9c9c1 !important;}
.stApp div.stButton > button *, .stApp div.stDownloadButton > button *,
section[data-testid="stSidebar"] div.stDownloadButton > button * {color:#10241A !important; -webkit-text-fill-color:#10241A !important;}
.stApp div.stButton > button:hover, .stApp div.stDownloadButton > button:hover {background:#E6F5D8 !important; border-color:#7CE02E !important;}
.stApp div.stButton > button[kind="primary"], .stApp div.stDownloadButton > button[kind="primary"],
.stApp div.stButton > button[data-testid="stBaseButton-primary"], .stApp div.stDownloadButton > button[data-testid="stBaseButton-primary"] {
   background:linear-gradient(135deg,#7CE02E,#2BD4A5) !important; border:none !important;}
.stApp div.stButton > button[kind="primary"] *, .stApp div.stDownloadButton > button[kind="primary"] *,
.stApp div.stButton > button[data-testid="stBaseButton-primary"] *, .stApp div.stDownloadButton > button[data-testid="stBaseButton-primary"] * {
   color:#06150B !important; -webkit-text-fill-color:#06150B !important;}
.stApp div.stButton > button:disabled, .stApp div.stDownloadButton > button:disabled {
   background:#24373E !important; border:1px solid #34505A !important; opacity:1 !important;}
.stApp div.stButton > button:disabled *, .stApp div.stDownloadButton > button:disabled * {
   color:#9DB3BB !important; -webkit-text-fill-color:#9DB3BB !important;}

/* kolom isian: latar putih -> teks hitam */
.stApp div[data-baseweb="input"], .stApp div[data-baseweb="base-input"],
.stApp div[data-baseweb="select"] > div, .stApp div[data-baseweb="textarea"] {background:#FFFFFF !important;}
.stApp input, .stApp textarea, .stApp div[data-baseweb="select"] * {color:#10241A !important; -webkit-text-fill-color:#10241A !important;}
.stApp [data-testid="stNumberInput"] button {background:#EEF3F0 !important;}
.stApp [data-testid="stNumberInput"] button svg {fill:#10241A !important; color:#10241A !important;}
div[data-baseweb="popover"] ul, div[data-baseweb="popover"] [role="listbox"], div[data-baseweb="menu"] {background:#FFFFFF !important;}
div[data-baseweb="popover"] li, div[data-baseweb="popover"] li * {color:#10241A !important; -webkit-text-fill-color:#10241A !important;}
div[data-baseweb="popover"] li:hover {background:#E6F5D8 !important;}

/* sidebar: kotak upload dan kotak info */
section[data-testid="stSidebar"] div[data-testid="stFileUploaderDropzone"] {background:#EAF1F4 !important; border:1px dashed #7a929b !important;}
section[data-testid="stSidebar"] div[data-testid="stFileUploaderDropzone"] *,
section[data-testid="stSidebar"] div[data-testid="stFileUploaderFile"] * {color:#10241A !important; -webkit-text-fill-color:#10241A !important;}
section[data-testid="stSidebar"] div[data-testid="stFileUploaderFile"] {background:#EAF1F4 !important; border-radius:8px; padding:2px 6px;}
.stApp div[data-testid="stAlert"], section[data-testid="stSidebar"] div[data-testid="stAlert"] {background:#EAF4FB !important; border:1px solid #9cc3dd !important; border-radius:12px;}
.stApp div[data-testid="stAlert"] *, section[data-testid="stSidebar"] div[data-testid="stAlert"] * {color:#10241A !important; -webkit-text-fill-color:#10241A !important;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------ data halaman
MODUL = {
    1: ("Persiapan & Tanah", "⛏️", "Tentukan dimensi galian, urugan pasir, dan lantai kerja berdasarkan gambar rencana."),
    2: ("Pondasi", "🪨", "Pilih jenis pondasi dan periksa ukuran serta volume setiap elemen pondasi."),
    3: ("Struktur Beton", "🏛️", "Hitung kebutuhan material sloof, kolom, balok, pelat, dan tangga."),
    4: ("Dinding", "🧱", "Masukkan luas dinding serta bukaan pintu dan jendela agar kebutuhan material lebih akurat."),
    5: ("Lantai", "◼️", "Masukkan luas lantai tiap tingkat untuk menghitung keramik dan bahan pemasangan."),
    6: ("Atap", "🏠", "Tentukan jenis atap, kemiringan, dan overstek sesuai desain bangunan."),
    7: ("Finishing", "🎨", "Hitung kebutuhan plester, plafon, pintu, jendela, dan pekerjaan finishing lainnya."),
    8: ("Utilitas", "💡", "Lengkapi estimasi kebutuhan material instalasi air, listrik, dan sanitasi."),
}
LABELS = ["Cover", "Identitas"] + [MODUL[i][0] for i in range(1, 9)] + ["Hasil"]
LAST = 10

# ------------------------------------------------------------------ state
S = st.session_state
_DEFAULTS = dict(
    db=lambda: core.DB.copy(), harga=lambda: core.HARGA.copy(), waste=lambda: dict(core.WASTE),
    mode_harga=lambda: "rata-rata", P=lambda: None, A=lambda: None, H=lambda: None, step=lambda: 0,
    draft=lambda: dict(nama="Rumah Contoh", pemilik="-", lantai=2, panjang=10.0, lebar=8.0, tinggi1=3.5,
                       tinggi2=3.5, pondasi="batu_kali", dinding="bata_merah", rangka_atap="baja_ringan",
                       penutup_atap="genteng_keramik", keramik="40x40", ker_p=50.0, ker_l=50.0),
)
for _k, _f in _DEFAULTS.items():       # tiap kunci diisi sendiri-sendiri agar sesi lama tidak error
    if _k not in S:
        S[_k] = _f()

def go(n):
    S.step = max(0, min(LAST, n))

def on_jump():
    pick = S.jump
    if pick >= 2 and S.P is None:
        S.flash = "Simpan identitas proyek dulu."
    elif pick == LAST and S.H is None:
        S.flash = "Hitung dulu dari modul 8."
    else:
        go(pick)

def sync_engine():
    core.DB = S.db.copy(); core.HARGA = S.harga.copy()
    core.WASTE = dict(S.waste); core.MODE_HARGA = S.mode_harga

def labelize(s):
    return str(s).replace("_", " ").capitalize()

def render_dict(d, prefix, depth=0):
    result = {}
    for k, v in d.items():
        path = f"{prefix}_{k}"
        if isinstance(v, dict):
            with st.expander(labelize(k), expanded=(depth < 1)):
                result[k] = render_dict(v, path, depth + 1)
        elif k == "jenis_atap":
            result[k] = st.selectbox(labelize(k), ["pelana", "perisai"], index=["pelana", "perisai"].index(v), key=path)
        elif isinstance(v, bool):
            result[k] = st.checkbox(labelize(k), value=v, key=path)
        elif isinstance(v, int):
            result[k] = st.number_input(labelize(k), value=int(v), step=1, min_value=0, key=path)
        elif isinstance(v, float):
            result[k] = st.number_input(labelize(k), value=float(v), step=0.1, min_value=0.0, format="%.3f", key=path)
        else:
            result[k] = st.text_input(labelize(k), value=str(v), key=path)
    return result

def make_excel():
    sync_engine()
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xw:
        pd.DataFrame(list(S.P.items()), columns=["Data", "Nilai"]).to_excel(xw, sheet_name="Identitas Proyek", index=False)
        pd.DataFrame(core.ratakan(S.A), columns=["Input", "Nilai"]).to_excel(xw, sheet_name="Data Input", index=False)
        core.tabel_volume(S.H).to_excel(xw, sheet_name="Rekap Pekerjaan", index=False)
        core.tabel_detail(S.H).to_excel(xw, sheet_name="Detail Material", index=False)
        core.rekap_material(S.H).to_excel(xw, sheet_name="Rekap Material", index=False)
        S.db.to_excel(xw, sheet_name="Database Koefisien", index=False)
        pd.DataFrame(list(S.waste.items()), columns=["Material", "Waste"]).to_excel(xw, sheet_name="Waste", index=False)
        S.harga.to_excel(xw, sheet_name="Harga Bahan", index=False)
    return buf.getvalue()

def stepper():
    cols = st.columns(len(LABELS), gap="small")
    for i, lab in enumerate(LABELS):
        with cols[i]:
            allowed = (i <= 1) or (S.P is not None and 2 <= i <= 9) or (i == LAST and S.H is not None)
            mark = "✓" if i < S.step else ("★" if i == LAST else str(i))
            if st.button(f"{mark}\\n{lab}", key=f"stepper_{i}",
                         type="primary" if i == S.step else "secondary",
                         disabled=not allowed, use_container_width=True):
                go(i)
                st.rerun()

def quick_navigation():
    st.markdown("#### Pintasan halaman")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("✏️ Edit identitas proyek", key="quick_identity", use_container_width=True):
            go(1); st.rerun()
    with c2:
        if st.button("📐 Edit pekerjaan", key="quick_work", disabled=S.P is None, use_container_width=True):
            go(2); st.rerun()
    with c3:
        if st.button("🧮 Lihat hasil", key="quick_result", disabled=S.H is None, use_container_width=True):
            go(LAST); st.rerun()
    with c4:
        if st.button("⌂ Kembali ke cover", key="quick_cover", use_container_width=True):
            go(0); st.rerun()

def page_head(num, title, sub, quip):
    st.markdown(f'<div class="phead"><div class="pnum">{num}</div><div><h2>{title}</h2><small>{sub}</small></div></div>'
                f'<div class="bubble">{quip}</div>', unsafe_allow_html=True)

def nav(next_label="Lanjut ➜", next_fn=None, disabled=False):
    st.write("")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if S.step > 0:
            st.button("⬅ Kembali", on_click=go, args=(S.step - 1,), use_container_width=True, key=f"back{S.step}")
    with c3:
        if next_fn is None:
            st.button(next_label, on_click=go, args=(S.step + 1,), type="primary", use_container_width=True,
                      key=f"next{S.step}", disabled=disabled)
        else:
            if st.button(next_label, type="primary", use_container_width=True, key=f"next{S.step}", disabled=disabled):
                next_fn()

# ------------------------------------------------------------------ sidebar
with st.sidebar:
    st.markdown("## 🏗️ Navigasi Proyek")
    st.caption("BUILD ESTIMATOR | ESTIMASI MATERIAL BANGUNAN")
    # Sinkronkan radio dengan halaman aktif SEBELUM widget dibuat, supaya tombol
    # Lanjut/Kembali/stepper/pintasan tidak "dibatalkan" oleh nilai lama radio.
    S["jump"] = S.step
    st.radio("Loncat ke laman", range(0, LAST + 1),
             format_func=lambda i: f"{i}. {LABELS[i]}" if i else "Cover",
             key="jump", on_change=on_jump)
    if S.get("flash"):
        st.warning(S.pop("flash"))
    st.markdown("---")
    st.markdown("**Database**")
    up = st.file_uploader("Impor database Excel", type=["xlsx"], key="db_upload")
    if up is not None:
        try:
            xls = pd.ExcelFile(up)
            if "KOEFISIEN_BAHAN" in xls.sheet_names:
                newdb = pd.read_excel(up, sheet_name="KOEFISIEN_BAHAN")
                if set(core.KOLOM_DB).issubset(newdb.columns):
                    S.db = newdb[list(core.KOLOM_DB)].copy()
            if "HARGA" in xls.sheet_names:
                newh = pd.read_excel(up, sheet_name="HARGA")
                req = ["material", "spesifikasi", "satuan", "harga_min", "harga_max", "sumber"]
                if set(req).issubset(newh.columns):
                    S.harga = newh[req].copy()
            st.success("Database terbaca.")
        except Exception as e:
            st.error(f"Gagal membaca database: {e}")
    try:
        st.download_button("Unduh template database", data=open("data/template_database_material.xlsx", "rb").read(),
                           file_name="template_database_material.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except FileNotFoundError:
        pass
    st.info("Koefisien awal masih asumsi prototipe. Verifikasi dengan AHSP/HSD sebelum dipakai untuk RAB.")

stepper()

# ------------------------------------------------------------------ 0 COVER
if S.step == 0:
    st.markdown("""
<div class="cover">
  <div class="kicker">CIVIL ENGINEERING • BUILDING ESTIMATOR</div>
  <h1>BUILD<br>ESTIMATOR<span>ESTIMASI MATERIAL BANGUNAN</span></h1>
  <p>Rencanakan kebutuhan material bangunan secara sistematis. Masukkan data proyekmu,
     isi 8 modul pekerjaan, lalu ambil laporannya dalam Excel dan PDF.</p>
  <div class="pct">RANCANG • HITUNG • EVALUASI</div>
</div>
<div class="cards">
  <div class="card"><div class="ic">📋</div><h4>Identitas Proyek</h4><p>Dimensi, jumlah lantai, jenis pondasi, dinding, atap, dan keramik.</p></div>
  <div class="card"><div class="ic">🧩</div><h4>8 Modul Pekerjaan</h4><p>Tanah, pondasi, beton, dinding, lantai, atap, finishing, utilitas.</p></div>
  <div class="card"><div class="ic">⚗️</div><h4>Database Editable</h4><p>Koefisien AHSP, harga bahan, dan waste bisa kamu atur sendiri.</p></div>
  <div class="card"><div class="ic">📦</div><h4>Output Excel & PDF</h4><p>Rekap volume, detail material, dan estimasi biaya siap unduh.</p></div>
</div>

""", unsafe_allow_html=True)
    st.write("")
    _, c, _ = st.columns([1, 1.2, 1])
    with c:
        st.button("🏗️  MULAI PERHITUNGAN", on_click=go, args=(1,), type="primary", use_container_width=True)
    st.caption("Hasil estimasi bukan pengganti gambar kerja, perhitungan struktur, survei lapangan, atau pemeriksaan tenaga ahli.")

# ------------------------------------------------------------------ 1 IDENTITAS
elif S.step == 1:
    page_head("01", "Identitas Proyek", "Langkah pertama: kenali bangunan yang akan dihitung",
              "Lengkapi identitas dan parameter dasar bangunan. Nilai awal modul akan disesuaikan dari data ini.")
    d = S.draft
    c1, c2, c3 = st.columns(3)
    with c1:
        d["nama"] = st.text_input("Nama proyek", value=d["nama"])
        d["pemilik"] = st.text_input("Pemilik", value=d["pemilik"])
        d["lantai"] = st.selectbox("Jumlah lantai", [1, 2], index=[1, 2].index(d["lantai"]))
    with c2:
        d["panjang"] = st.number_input("Panjang bangunan (m)", min_value=0.1, value=float(d["panjang"]), step=.5)
        d["lebar"] = st.number_input("Lebar bangunan (m)", min_value=0.1, value=float(d["lebar"]), step=.5)
        d["tinggi1"] = st.number_input("Tinggi lantai 1 (m)", min_value=0.1, value=float(d["tinggi1"]), step=.1)
    with c3:
        d["tinggi2"] = st.number_input("Tinggi lantai 2 (m)", min_value=0.1, value=float(d["tinggi2"]), step=.1,
                                       disabled=(d["lantai"] == 1))
        d["pondasi"] = st.selectbox("Jenis pondasi", core.PILIHAN["pondasi"], index=core.PILIHAN["pondasi"].index(d["pondasi"]))
        d["dinding"] = st.selectbox("Jenis dinding", core.PILIHAN["dinding"], index=core.PILIHAN["dinding"].index(d["dinding"]))
    c4, c5, c6 = st.columns(3)
    with c4:
        d["rangka_atap"] = st.selectbox("Rangka atap", core.PILIHAN["rangka_atap"], index=core.PILIHAN["rangka_atap"].index(d["rangka_atap"]))
    with c5:
        d["penutup_atap"] = st.selectbox("Penutup atap", core.PILIHAN["penutup_atap"], index=core.PILIHAN["penutup_atap"].index(d["penutup_atap"]))
    with c6:
        d["keramik"] = st.selectbox("Ukuran keramik", core.PILIHAN["keramik"], index=core.PILIHAN["keramik"].index(d["keramik"]))
    if d["keramik"] == "custom":
        x, y = st.columns(2)
        d["ker_p"] = x.number_input("Panjang keramik (cm)", min_value=.1, value=float(d["ker_p"]))
        d["ker_l"] = y.number_input("Lebar keramik (cm)", min_value=.1, value=float(d["ker_l"]))

    def simpan_identitas():
        try:
            P = {k: d[k] for k in ("nama", "pemilik", "lantai", "panjang", "lebar", "tinggi1", "tinggi2",
                                   "pondasi", "dinding", "rangka_atap", "penutup_atap", "keramik")}
            if d["keramik"] == "custom":
                P.update(keramik_p_cm=d["ker_p"], keramik_l_cm=d["ker_l"])
            P = core.validasi_proyek(P)
            if S.P != P:                      # input modul hanya dibuat ulang jika identitas berubah
                S.P = P; S.A = core.default_input(P); S.H = None
                for k in [k for k in S.keys() if str(k).startswith("mod")]:
                    del S[k]
            go(2)
        except Exception as e:
            st.error(str(e))
    nav("Simpan & ke Modul 1 ➜", simpan_identitas)

# ------------------------------------------------------------------ 2-9 MODUL
elif 2 <= S.step <= 9:
    i = S.step - 1
    nama, ikon, quip = MODUL[i]
    page_head(f"{i:02d}", f"Modul {i}: {nama} {ikon}", f"Proyek: {S.P['nama']}  •  Modul {i} dari 8", quip)
    st.caption("Nilai awal diturunkan dari identitas proyek. Periksa dan sesuaikan dengan gambar rencana dan kondisi lapangan.")
    key = f"m{i}"
    S.A[key] = render_dict(S.A[key], f"mod{i}")

    def hitung_semua():
        try:
            sync_engine()
            S.H = core.hitung(S.P, S.A)
            go(LAST)
        except Exception as e:
            S.H = None
            st.error(f"Perhitungan belum berhasil: {e}")
    if i < 8:
        nav(f"Lanjut ke Modul {i+1} ➜")
    else:
        nav("🔬 HITUNG SEMUA MODUL", hitung_semua)

# ------------------------------------------------------------------ 10 HASIL
else:
    page_head("★", "Hasil Estimasi", f"Proyek: {S.P['nama']}  •  Pemilik: {S.P['pemilik']}",
              "Perhitungan selesai. Unduh laporan Excel atau PDF dan verifikasi koefisien sebelum digunakan sebagai dasar RAB.")
    H = S.H
    rec = core.rekap_material(H)
    m1, m2, m3 = st.columns(3)
    m1.metric("Item pekerjaan", len(H.vol))
    m2.metric("Jenis material", len(rec))
    total = rec["biaya"].sum(min_count=1) if "biaya" in rec else None
    m3.metric("Estimasi biaya", "Belum tersedia" if (total is None or pd.isna(total)) else f"Rp {total:,.0f}".replace(",", "."))

    d1, d2 = st.columns(2)
    with d1:
        st.download_button("📗 Unduh laporan Excel", data=make_excel(), file_name="Laporan_BuildEstimator.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           type="primary", use_container_width=True)
    with d2:
        st.download_button("📕 Unduh laporan PDF", data=pdf_export.buat_pdf(S.P, H, rec),
                           file_name="Laporan_BuildEstimator.pdf", mime="application/pdf",
                           type="primary", use_container_width=True)
    st.write("")
    t1, t2, t3 = st.tabs(["Rekap pekerjaan", "Detail kebutuhan", "Rekap material & biaya"])
    with t1:
        st.dataframe(core.tabel_volume(H), use_container_width=True, hide_index=True)
    with t2:
        st.dataframe(core.tabel_detail(H), use_container_width=True, hide_index=True)
    with t3:
        st.dataframe(rec, use_container_width=True, hide_index=True)
        if rec["harga"].isna().all():
            st.warning("Harga bahan belum tersedia. Isi database harga agar estimasi biaya dapat dihitung.")

    with st.expander("⚗️ Pengaturan database (koefisien, harga, waste)"):
        dbtab, hargatab, wastetab = st.tabs(["Koefisien AHSP", "Harga bahan", "Waste"])
        with dbtab:
            edited = st.data_editor(S.db, use_container_width=True, num_rows="dynamic", key="editor_db")
            if st.button("Simpan perubahan koefisien"):
                S.db = edited.copy(); st.success("Tersimpan pada sesi ini. Hitung ulang untuk melihat dampaknya.")
        with hargatab:
            mode = st.selectbox("Metode pemilihan harga", ["min", "max", "rata-rata"],
                                index=["min", "max", "rata-rata"].index(S.mode_harga))
            S.mode_harga = mode
            editedh = st.data_editor(S.harga, use_container_width=True, num_rows="dynamic", key="editor_harga")
            if st.button("Simpan perubahan harga"):
                S.harga = editedh.copy(); st.success("Tersimpan pada sesi ini. Hitung ulang untuk melihat dampaknya.")
        with wastetab:
            wdf = pd.DataFrame([{"material": k, "waste": v} for k, v in S.waste.items()])
            editedw = st.data_editor(wdf, use_container_width=True, num_rows="dynamic", key="editor_waste")
            if st.button("Simpan perubahan waste"):
                try:
                    nw = {str(r["material"]): float(r["waste"]) for _, r in editedw.iterrows()}
                    if any(v < 0 for v in nw.values()):
                        raise ValueError("Waste tidak boleh negatif.")
                    S.waste = nw; st.success("Waste tersimpan pada sesi ini.")
                except Exception as e:
                    st.error(str(e))

    def hitung_ulang():
        try:
            sync_engine(); S.H = core.hitung(S.P, S.A); st.rerun()
        except Exception as e:
            st.error(str(e))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("⬅ Edit modul 8", on_click=go, args=(9,), use_container_width=True)
    with c2:
        if st.button("🔁 Hitung ulang", use_container_width=True):
            hitung_ulang()
    with c3:
        def baru():
            S.P = None; S.A = None; S.H = None; go(0)
        st.button("🧪 Proyek baru", on_click=baru, use_container_width=True)
    st.caption("BuildEstimator hanya alat estimasi awal. Bukan pengganti gambar kerja, hitungan struktur, survei, atau tenaga ahli.")


# Pintasan navigasi internal yang dapat digunakan dari setiap halaman
quick_navigation()
