import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================
st.set_page_config(page_title="Hub Tributario 2026", layout="wide", page_icon="🏛️")

# Estilos CSS
st.markdown("""
<style>
    [data-testid="stExpander"] {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px 15px;
        font-size: 14px;
        flex-grow: 1;
        text-align: center;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6f3ff;
        border-bottom: 2px solid #0068c9;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

HOLIDAYS_2026 = [
    "2026-01-01", "2026-01-12", "2026-03-23", "2026-04-02", "2026-04-03", 
    "2026-05-01", "2026-05-18", "2026-06-08", "2026-06-15", "2026-06-29", 
    "2026-07-20", "2026-08-07", "2026-08-17", "2026-10-12", "2026-11-02", 
    "2026-11-16", "2026-12-08", "2026-12-25"
]

def get_business_days(start_date_str, num_days=10):
    start_date = pd.to_datetime(start_date_str)
    dates = []
    current_date = start_date
    while len(dates) < num_days:
        if current_date.weekday() >= 5 or current_date.strftime("%Y-%m-%d") in HOLIDAYS_2026:
            current_date += timedelta(days=1)
            continue
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates

# ==========================================
# 2. MOTORES DE CÁLCULO (Data Generators)
# ==========================================

def get_national_calendar(last_digit):
    calendar = []
    idx = {1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 0:9}[int(last_digit)]
    
    # Renta PJ
    renta_rules = [("1ra Cuota", "2026-05-11"), ("2da Cuota", "2026-07-07")]
    for per, start in renta_rules:
        dates = get_business_days(start, 10)
        calendar.append({"Jurisdicción": "Nacional", "Impuesto": "Renta Personas Jurídicas", "Periodo": per, "Fecha": dates[idx]})

    # IVA
    iva_rules = [
        ("Bimestre 1 (Ene-Feb)", "2026-03-10"), ("Bimestre 2 (Mar-Abr)", "2026-05-12"),
        ("Bimestre 3 (May-Jun)", "2026-07-08"), ("Bimestre 4 (Jul-Ago)", "2026-09-08"),
        ("Bimestre 5 (Sep-Oct)", "2026-11-10"), ("Bimestre 6 (Nov-Dic)", "2027-01-13")
    ]
    for per, start in iva_rules:
        dates = get_business_days(start, 10)
        calendar.append({"Jurisdicción": "Nacional", "Impuesto": "IVA Bimestral", "Periodo": per, "Fecha": dates[idx]})

    # Retefuente
    rete_rules = [
        ("Enero", "2026-02-10"), ("Febrero", "2026-03-10"), ("Marzo", "2026-04-07"),
        ("Abril", "2026-05-11"), ("Mayo", "2026-06-09"), ("Junio", "2026-07-07"),
        ("Julio", "2026-08-11"), ("Agosto", "2026-09-08"), ("Septiembre", "2026-10-06"),
        ("Octubre", "2026-11-10"), ("Noviembre", "2026-12-10"), ("Diciembre", "2027-01-13")
    ]
    for per, start in rete_rules:
        dates = get_business_days(start, 10)
        calendar.append({"Jurisdicción": "Nacional", "Impuesto": "Retención en la Fuente", "Periodo": per, "Fecha": dates[idx]})

    return calendar

def get_atlantico_calendar():
    calendar = []
    # Registro
    reg_fechas = [("Enero", "2026-02-16"), ("Febrero", "2026-03-16"), ("Marzo", "2026-04-15"),
                  ("Abril", "2026-05-15"), ("Mayo", "2026-06-16"), ("Junio", "2026-07-15"),
                  ("Julio", "2026-08-18"), ("Agosto", "2026-09-15"), ("Septiembre", "2026-10-15")]
    for per, f in reg_fechas:
        calendar.append({"Jurisdicción": "Atlántico", "Impuesto": "Impuesto de Registro", "Periodo": per, "Fecha": pd.to_datetime(f)})

    # Tasa Seguridad
    seg_fechas = [("Enero", "2026-02-18"), ("Febrero", "2026-03-18"), ("Marzo", "2026-04-20"),
                  ("Abril", "2026-05-19"), ("Mayo", "2026-06-18"), ("Junio", "2026-07-21")]
    for per, f in seg_fechas:
        calendar.append({"Jurisdicción": "Atlántico", "Impuesto": "Tasa Seguridad", "Periodo": per, "Fecha": pd.to_datetime(f)})

    # Estampillas
    calendar.append({"Jurisdicción": "Atlántico", "Impuesto": "Estampillas", "Periodo": "Anual 2026", "Fecha": pd.to_datetime("2027-01-31")})
    return calendar

def get_barranquilla_calendar(last_digit):
    calendar = []
    d = int(last_digit)
    
    # ICA
    ica_dates = {0: "2027-02-15", 9: "2027-02-16", 8: "2027-02-17", 7: "2027-02-18",
                 6: "2027-02-19", 5: "2027-02-22", 4: "2027-02-23", 3: "2027-02-24", 2: "2027-02-25", 1: "2027-02-26"}
    calendar.append({"Jurisdicción": "Barranquilla", "Impuesto": "ICA (Industria y Comercio)", "Periodo": "Anual 2026", "Fecha": pd.to_datetime(ica_dates[d])})

    # Predial
    calendar.append({"Jurisdicción": "Barranquilla", "Impuesto": "Predial Unificado", "Periodo": "Desc. 10%", "Fecha": pd.to_datetime("2026-03-27")})
    calendar.append({"Jurisdicción": "Barranquilla", "Impuesto": "Predial Unificado", "Periodo": "Desc. 5%", "Fecha": pd.to_datetime("2026-05-29")})
    calendar.append({"Jurisdicción": "Barranquilla", "Impuesto": "Predial Unificado", "Periodo": "Sin Descuento", "Fecha": pd.to_datetime("2026-06-30")})

    # Rete-ICA (Simulado)
    bimestres = [("Ene-Feb", "2026-03-13"), ("Mar-Abr", "2026-05-15"), ("May-Jun", "2026-07-17"), ("Jul-Ago", "2026-09-17"), ("Sep-Oct", "2026-11-17"), ("Nov-Dic", "2027-01-18")]
    offset = 0 if d in [0,9] else (2 if d in [8,7] else 4)
    for per, base in bimestres:
        f_real = pd.to_datetime(base) + timedelta(days=offset)
        if f_real.weekday() >= 5: f_real += timedelta(days=2)
        calendar.append({"Jurisdicción": "Barranquilla", "Impuesto": "Rete-ICA", "Periodo": per, "Fecha": f_real})

    return calendar

def get_candelaria_calendar(last_digit):
    calendar = []
    d = int(last_digit)
    
    # Predial
    calendar.append({"Jurisdicción": "Candelaria", "Impuesto": "Predial Unificado", "Periodo": "Desc. 20% (Pronto Pago)", "Fecha": pd.to_datetime("2026-03-31")})
    calendar.append({"Jurisdicción": "Candelaria", "Impuesto": "Predial Unificado", "Periodo": "Desc. 15%", "Fecha": pd.to_datetime("2026-05-31")})
    calendar.append({"Jurisdicción": "Candelaria", "Impuesto": "Predial Unificado", "Periodo": "Desc. 10%", "Fecha": pd.to_datetime("2026-06-30")})

    # ICA Anual
    calendar.append({"Jurisdicción": "Candelaria", "Impuesto": "ICA Anual (Vigencia 2025)", "Periodo": "Declaración y Pago", "Fecha": pd.to_datetime("2026-02-27")})

    # Rete-ICA Bimestral
    fechas_rete = {
        0: ["2026-03-16", "2026-05-15", "2026-07-13", "2026-09-14", "2026-11-17", "2027-01-12"],
        1: ["2026-03-17", "2026-05-19", "2026-07-14", "2026-09-15", "2026-11-18", "2027-01-13"],
        2: ["2026-03-18", "2026-05-20", "2026-07-15", "2026-09-16", "2026-11-19", "2027-01-14"],
        3: ["2026-03-19", "2026-05-21", "2026-07-16", "2026-09-17", "2026-11-20", "2027-01-15"],
        4: ["2026-03-20", "2026-05-22", "2026-07-17", "2026-09-18", "2026-11-23", "2027-01-18"],
        5: ["2026-03-24", "2026-05-25", "2026-07-21", "2026-09-21", "2026-11-24", "2027-01-19"],
        6: ["2026-03-25", "2026-05-26", "2026-07-22", "2026-09-22", "2026-11-25", "2027-01-20"],
        7: ["2026-03-26", "2026-05-27", "2026-07-23", "2026-09-23", "2026-11-26", "2027-01-21"],
        8: ["2026-03-27", "2026-05-28", "2026-07-24", "2026-09-24", "2026-11-27", "2027-01-22"],
        9: ["2026-03-30", "2026-05-29", "2026-07-27", "2026-09-25", "2026-11-30", "2027-01-25"],
    }
    bimestres = ["Ene-Feb", "Mar-Abr", "May-Jun", "Jul-Ago", "Sep-Oct", "Nov-Dic"]
    
    mis_fechas = fechas_rete[d]
    for i, fecha in enumerate(mis_fechas):
        calendar.append({"Jurisdicción": "Candelaria", "Impuesto": "Rete-ICA Bimestral", "Periodo": bimestres[i], "Fecha": pd.to_datetime(fecha)})

    return calendar

def get_soledad_calendar(last_digit):
    calendar = []
    d = int(last_digit)
    
    # ICA Anual
    calendar.append({"Jurisdicción": "Soledad", "Impuesto": "ICA Anual (Vigencia 2025)", "Periodo": "Anual", "Fecha": pd.to_datetime("2026-02-27")})
    calendar.append({"Jurisdicción": "Soledad", "Impuesto": "ICA Anual (Vigencia 2026)", "Periodo": "Anual", "Fecha": pd.to_datetime("2027-02-26")})

    # Predial
    calendar.append({"Jurisdicción": "Soledad", "Impuesto": "Predial Unificado", "Periodo": "Desc. 5%", "Fecha": pd.to_datetime("2026-05-31")})
    calendar.append({"Jurisdicción": "Soledad", "Impuesto": "Predial Unificado", "Periodo": "Límite Sin Intereses", "Fecha": pd.to_datetime("2026-06-30")})

    # Medios Magnéticos
    medios_map = {1:"2026-05-25", 2:"2026-05-25", 3:"2026-05-26", 4:"2026-05-26", 5:"2026-05-27", 6:"2026-05-27", 7:"2026-05-28", 8:"2026-05-28", 9:"2026-05-29", 0:"2026-05-29"}
    calendar.append({"Jurisdicción": "Soledad", "Impuesto": "Medios Magnéticos", "Periodo": "Reporte Anual", "Fecha": pd.to_datetime(medios_map[d])})

    # Rete-ICA Régimen Común (Bimestral)
    if d in [1,2]: idx_grp = 0
    elif d in [3,4]: idx_grp = 1
    elif d in [5,6]: idx_grp = 2
    elif d in [7,8]: idx_grp = 3
    else: idx_grp = 4
    
    rete_common_dates = [
        ["2026-03-09", "2026-05-11", "2026-07-13", "2026-09-11", "2026-11-09", "2027-01-12"], 
        ["2026-03-10", "2026-05-12", "2026-07-14", "2026-09-14", "2026-11-10", "2027-01-13"], 
        ["2026-03-11", "2026-05-13", "2026-07-15", "2026-09-15", "2026-11-11", "2027-01-14"], 
        ["2026-03-12", "2026-05-14", "2026-07-16", "2026-09-16", "2026-11-12", "2027-01-15"], 
        ["2026-03-13", "2026-05-15", "2026-07-17", "2026-09-17", "2026-11-13", "2027-01-18"]
    ]
    bimestres = ["Ene-Feb", "Mar-Abr", "May-Jun", "Jul-Ago", "Sep-Oct", "Nov-Dic"]
    
    mis_fechas = rete_common_dates[idx_grp]
    for i, fecha in enumerate(mis_fechas):
        calendar.append({"Jurisdicción": "Soledad", "Impuesto": "Rete-ICA (Régimen Común)", "Periodo": bimestres[i], "Fecha": pd.to_datetime(fecha)})

    return calendar

def get_malambo_calendar(last_digit):
    # Malambo NO usa último dígito en sus tablas principales, fecha única para todos.
    # Fuente: Resolución 2051 del 2025
    calendar = []
    
    # --- 1. ICA Anual ---
    # Fuente: Artículo Primero (Vigencia 2025)
    calendar.append({"Jurisdicción": "Malambo", "Impuesto": "ICA Anual (Vigencia 2025)", "Periodo": "Anual", "Fecha": pd.to_datetime("2026-03-27")})

    # --- 2. Anticipo ICA Mensual (Régimen Común y Grandes Contribuyentes) ---
    # Fuente: Artículo Segundo. Fechas fijas para todos.
    anticipo_fechas = [
        ("Enero", "2026-02-09"), ("Febrero", "2026-03-09"), ("Marzo", "2026-04-10"),
        ("Abril", "2026-05-08"), ("Mayo", "2026-06-09"), ("Junio", "2026-07-09"),
        ("Julio", "2026-08-10"), ("Agosto", "2026-09-08"), ("Septiembre", "2026-10-08"),
        ("Octubre", "2026-11-09"), ("Noviembre", "2026-12-09"), ("Diciembre", "2027-01-08")
    ]
    for per, f in anticipo_fechas:
        calendar.append({"Jurisdicción": "Malambo", "Impuesto": "Anticipo ICA Mensual", "Periodo": per, "Fecha": pd.to_datetime(f)})

    # --- 3. Rete-ICA Mensual ---
    # Fuente: Artículo Tercero. Fechas fijas para todos.
    rete_fechas = [
        ("Enero", "2026-02-12"), ("Febrero", "2026-03-13"), ("Marzo", "2026-04-13"),
        ("Abril", "2026-05-12"), ("Mayo", "2026-06-12"), ("Junio", "2026-07-13"),
        ("Julio", "2026-08-13"), ("Agosto", "2026-09-11"), ("Septiembre", "2026-10-13"),
        ("Octubre", "2026-11-13"), ("Noviembre", "2026-12-11"), ("Diciembre", "2027-01-13")
    ]
    for per, f in rete_fechas:
        calendar.append({"Jurisdicción": "Malambo", "Impuesto": "Rete-ICA Mensual", "Periodo": per, "Fecha": pd.to_datetime(f)})

    # --- 4. ICA Simplificado Preferencial (Bimestral) ---
    # Fuente: Artículo Cuarto. Fechas fijas.
    simp_fechas = [
        ("Bimestre 1", "2026-03-05"), ("Bimestre 2", "2026-05-05"), ("Bimestre 3", "2026-07-07"),
        ("Bimestre 4", "2026-09-07"), ("Bimestre 5", "2026-11-06"), ("Bimestre 6", "2027-01-07")
    ]
    for per, f in simp_fechas:
        calendar.append({"Jurisdicción": "Malambo", "Impuesto": "ICA Simplificado", "Periodo": per, "Fecha": pd.to_datetime(f)})

    # --- 5. Predial Unificado ---
    # Fuente: Artículo Quinto y Parágrafo 1
    calendar.append({"Jurisdicción": "Malambo", "Impuesto": "Predial Unificado", "Periodo": "Desc. 15%", "Fecha": pd.to_datetime("2026-01-31")})
    calendar.append({"Jurisdicción": "Malambo", "Impuesto": "Predial Unificado", "Periodo": "Desc. 10%", "Fecha": pd.to_datetime("2026-03-31")})
    calendar.append({"Jurisdicción": "Malambo", "Impuesto": "Predial Unificado", "Periodo": "Desc. 5% / Límite Sin Intereses", "Fecha": pd.to_datetime("2026-05-31")})

    return calendar

# ==========================================
# 3. INTERFAZ DE USUARIO
# ==========================================

st.title("🗓️ Hub Tributario 2026: Vista Jerárquica")
st.markdown("Consulta organizada por **Jurisdicción > Impuesto > Fechas**.")
st.caption("Normativa: Nación, Atlántico, Barranquilla, Soledad, Candelaria y **Malambo**.")

col_in, col_check = st.columns([1, 2])
with col_in:
    nit = st.text_input("Digite NIT (Sin dígito de verificación)", max_chars=15)

if nit and nit.isdigit():
    last_digit = int(nit[-1])
    
    # 1. Obtener todos los datos
    data_nac = get_national_calendar(last_digit)
    data_atl = get_atlantico_calendar()
    data_bar = get_barranquilla_calendar(last_digit)
    data_can = get_candelaria_calendar(last_digit)
    data_sol = get_soledad_calendar(last_digit)
    data_mal = get_malambo_calendar(last_digit) # ¡Nuevo!
    
    full_data = data_nac + data_atl + data_bar + data_can + data_sol + data_mal
    df_master = pd.DataFrame(full_data)
    
    # 2. Estructura visual: PESTAÑAS (Ahora son 6)
    tabs = st.tabs([
        "🇨🇴 Nación", 
        "🌊 Atlántico", 
        "🏙️ B/quilla", 
        "✈️ Soledad",
        "🏭 Malambo",
        "🏘️ Candelaria"
    ])
    
    # Función de renderizado
    def render_jurisdiction_tab(df, jurisdiction_name):
        subset = df[df['Jurisdicción'].str.contains(jurisdiction_name, case=False)]
        
        if subset.empty:
            st.info("No hay datos cargados para esta jurisdicción.")
            return

        unique_taxes = subset['Impuesto'].unique()
        
        for tax in unique_taxes:
            df_tax = subset[subset['Impuesto'] == tax].copy()
            df_tax = df_tax.sort_values(by="Fecha")
            
            df_tax['Fecha Vencimiento'] = df_tax['Fecha'].dt.strftime('%Y-%m-%d')
            df_tax['Día Semana'] = df_tax['Fecha'].dt.day_name().replace(
                'Monday', 'Lunes').replace('Tuesday', 'Martes').replace('Wednesday', 'Miércoles').replace(
                'Thursday', 'Jueves').replace('Friday', 'Viernes').replace('Saturday', 'Sábado').replace('Sunday', 'Domingo')
            
            today = datetime.now()
            df_tax['Estado'] = df_tax['Fecha'].apply(
                lambda x: "🔴 Vencido" if x < today else ("🟠 Próximo" if (x - today).days < 30 else "🟢 A tiempo")
            )

            with st.expander(f"📌 {tax}", expanded=True):
                st.dataframe(
                    df_tax[['Periodo', 'Fecha Vencimiento', 'Día Semana', 'Estado']],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Estado": st.column_config.TextColumn("Estado", width="small"),
                        "Fecha Vencimiento": st.column_config.DateColumn("Fecha Límite", format="DD/MM/YYYY")
                    }
                )

    # 3. Renderizar cada pestaña
    with tabs[0]: render_jurisdiction_tab(df_master, "Nacional")
    with tabs[1]: render_jurisdiction_tab(df_master, "Atlántico")
    with tabs[2]: render_jurisdiction_tab(df_master, "Barranquilla")
    with tabs[3]: render_jurisdiction_tab(df_master, "Soledad")
    with tabs[4]: render_jurisdiction_tab(df_master, "Malambo")
    with tabs[5]: render_jurisdiction_tab(df_master, "Candelaria")

elif nit:
    st.error("El NIT debe ser numérico.")
