import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================
st.set_page_config(page_title="Hub Tributario 2026", layout="wide", page_icon="🏛️")

# Estilos CSS para mejorar la tablas
st.markdown("""
<style>
    [data-testid="stExpander"] {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6f3ff;
        border-bottom: 2px solid #0068c9;
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
    
    # --- Renta PJ (Fuente: PDF 1) ---
    # Fechas base aproximadas para el dígito 1 extraídas del calendario
    renta_rules = [
        ("1ra Cuota", "2026-05-11"), 
        ("2da Cuota", "2026-07-07")
    ]
    for per, start in renta_rules:
        dates = get_business_days(start, 10)
        calendar.append({"Jurisdicción": "Nacional", "Impuesto": "Renta Personas Jurídicas", "Periodo": per, "Fecha": dates[idx]})

    # --- IVA Bimestral (Fuente: PDF 1) ---
    iva_rules = [
        ("Bimestre 1 (Ene-Feb)", "2026-03-10"),
        ("Bimestre 2 (Mar-Abr)", "2026-05-12"),
        ("Bimestre 3 (May-Jun)", "2026-07-08"), # Ajuste festivos
        ("Bimestre 4 (Jul-Ago)", "2026-09-08"),
        ("Bimestre 5 (Sep-Oct)", "2026-11-10"),
        ("Bimestre 6 (Nov-Dic)", "2027-01-13")
    ]
    for per, start in iva_rules:
        dates = get_business_days(start, 10)
        calendar.append({"Jurisdicción": "Nacional", "Impuesto": "IVA Bimestral", "Periodo": per, "Fecha": dates[idx]})

    # --- Retefuente (Fuente: PDF 1) ---
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
    # (Fuente: Resolución 000476 Atlántico)
    
    # Impuesto Registro (Fechas fijas mensuales - Muestra 6 meses)
    reg_fechas = [("Enero", "2026-02-16"), ("Febrero", "2026-03-16"), ("Marzo", "2026-04-15"),
                  ("Abril", "2026-05-15"), ("Mayo", "2026-06-16"), ("Junio", "2026-07-15"),
                  ("Julio", "2026-08-18"), ("Agosto", "2026-09-15"), ("Septiembre", "2026-10-15")]
    for per, f in reg_fechas:
        calendar.append({"Jurisdicción": "Atlántico", "Impuesto": "Impuesto de Registro", "Periodo": per, "Fecha": pd.to_datetime(f)})

    # Tasa Seguridad (Fechas fijas mensuales - Muestra 6 meses)
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
    
    # 1. ICA Anual (Fuente: Res DSH 003)
    ica_dates = {0: "2027-02-15", 9: "2027-02-16", 8: "2027-02-17", 7: "2027-02-18",
                 6: "2027-02-19", 5: "2027-02-22", 4: "2027-02-23", 3: "2027-02-24", 2: "2027-02-25", 1: "2027-02-26"}
    calendar.append({"Jurisdicción": "Barranquilla", "Impuesto": "ICA (Industria y Comercio)", "Periodo": "Anual 2026", "Fecha": pd.to_datetime(ica_dates[d])})

    # 2. Predial
    calendar.append({"Jurisdicción": "Barranquilla", "Impuesto": "Predial Unificado", "Periodo": "Desc. 10%", "Fecha": pd.to_datetime("2026-03-27")})
    calendar.append({"Jurisdicción": "Barranquilla", "Impuesto": "Predial Unificado", "Periodo": "Desc. 5%", "Fecha": pd.to_datetime("2026-05-29")})
    calendar.append({"Jurisdicción": "Barranquilla", "Impuesto": "Predial Unificado", "Periodo": "Sin Descuento", "Fecha": pd.to_datetime("2026-06-30")})

    # 3. Rete-ICA Bimestral (Logica simplificada de ejemplo para demo)
    bimestres = [
        ("Ene-Feb", "2026-03-13"), ("Mar-Abr", "2026-05-15"), 
        ("May-Jun", "2026-07-17"), ("Jul-Ago", "2026-09-17"),
        ("Sep-Oct", "2026-11-17"), ("Nov-Dic", "2027-01-18")
    ]
    # Ajuste simple de días según dígito (simulación de la tabla compleja del PDF)
    offset = 0 if d in [0,9] else (2 if d in [8,7] else 4)
    
    for per, base in bimestres:
        f_base = pd.to_datetime(base)
        f_real = f_base + timedelta(days=offset) 
        # Ajuste fin de semana simple
        if f_real.weekday() >= 5: f_real += timedelta(days=2)
        
        calendar.append({"Jurisdicción": "Barranquilla", "Impuesto": "Rete-ICA", "Periodo": per, "Fecha": f_real})

    return calendar

# ==========================================
# 3. INTERFAZ DE USUARIO
# ==========================================

st.title("🗓️ Hub Tributario 2026: Vista Jerárquica")
st.write("Consulta organizada por **Jurisdicción > Impuesto > Fechas**.")

col_in, col_check = st.columns([1, 2])
with col_in:
    nit = st.text_input("Digite NIT (Sin dígito de verificación)", max_chars=15)

if nit and nit.isdigit():
    last_digit = int(nit[-1])
    
    # 1. Obtener todos los datos
    data_nac = get_national_calendar(last_digit)
    data_atl = get_atlantico_calendar()
    data_bar = get_barranquilla_calendar(last_digit)
    
    full_data = data_nac + data_atl + data_bar
    df_master = pd.DataFrame(full_data)
    
    # 2. Estructura visual: PESTAÑAS (Jurisdicción)
    tab_nac, tab_atl, tab_bar = st.tabs(["🇨🇴 Nacional (DIAN)", "🌊 Atlántico (Gobernación)", "🏙️ Barranquilla (Distrito)"])
    
    # Función auxiliar para renderizar contenido de cada pestaña
    def render_jurisdiction_tab(df, jurisdiction_name):
        subset = df[df['Jurisdicción'].str.contains(jurisdiction_name, case=False)]
        
        if subset.empty:
            st.info("No hay datos cargados para esta jurisdicción.")
            return

        # Agrupar por Impuesto (Nivel 2)
        unique_taxes = subset['Impuesto'].unique()
        
        for tax in unique_taxes:
            # Filtrar y ordenar por fecha (Nivel 3)
            df_tax = subset[subset['Impuesto'] == tax].copy()
            df_tax = df_tax.sort_values(by="Fecha")
            
            # Formatear fecha para mostrar
            df_tax['Fecha Vencimiento'] = df_tax['Fecha'].dt.strftime('%Y-%m-%d')
            df_tax['Día Semana'] = df_tax['Fecha'].dt.day_name().replace(
                'Monday', 'Lunes').replace('Tuesday', 'Martes').replace('Wednesday', 'Miércoles').replace(
                'Thursday', 'Jueves').replace('Friday', 'Viernes').replace('Saturday', 'Sábado').replace('Sunday', 'Domingo')
            
            # Calcular estado
            today = datetime.now()
            df_tax['Estado'] = df_tax['Fecha'].apply(
                lambda x: "🔴 Vencido" if x < today else ("🟠 Próximo" if (x - today).days < 30 else "🟢 A tiempo")
            )

            # Mostrar en Expander
            with st.expander(f"📌 {tax}", expanded=True):
                # Usar dataframe interactivo (No lista)
                st.dataframe(
                    df_tax[['Periodo', 'Fecha Vencimiento', 'Día Semana', 'Estado']],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Estado": st.column_config.TextColumn(
                            "Estado",
                            help="Estado del vencimiento",
                            width="small"
                        ),
                        "Fecha Vencimiento": st.column_config.DateColumn(
                            "Fecha Límite",
                            format="DD/MM/YYYY"
                        )
                    }
                )

    # 3. Renderizar cada pestaña
    with tab_nac:
        render_jurisdiction_tab(df_master, "Nacional")
        
    with tab_atl:
        render_jurisdiction_tab(df_master, "Atlántico")
        
    with tab_bar:
        render_jurisdiction_tab(df_master, "Barranquilla")

elif nit:
    st.error("El NIT debe ser numérico.")
