import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURACIÓN Y MOTOR DE FECHAS
# ==========================================

st.set_page_config(page_title="Agenda Tributaria 2026", layout="wide", page_icon="🗓️")

# Definimos los días festivos clave de Colombia 2026 para que el cálculo sea preciso
# (Lista simplificada para el cálculo de días hábiles bimport streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURACIÓN Y UTILIDADES
# ==========================================
st.set_page_config(page_title="Hub Tributario 2026", layout="wide", page_icon="🏢")

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
# 2. LOGICA NACIONAL (DIAN)
# ==========================================
def get_national_calendar(last_digit, last_two_digits):
    calendar = []
    
    # Reglas Generales (1 dígito) - Fechas de inicio aproximadas
    rules = [
        {"impuesto": "Retención en la Fuente (DIAN)", "periodo": "Enero", "start": "2026-02-10"},
        {"impuesto": "Retención en la Fuente (DIAN)", "periodo": "Febrero", "start": "2026-03-10"},
        {"impuesto": "IVA Bimestral (DIAN)", "periodo": "Bimestre 1", "start": "2026-03-10"},
        {"impuesto": "Renta Personas Jurídicas (DIAN)", "periodo": "1ra Cuota", "start": "2026-05-11"},
    ]
    
    digit_map = {1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 0:9}
    idx = digit_map[int(last_digit)]
    
    for rule in rules:
        dates = get_business_days(rule['start'], num_days=10)
        calendar.append({
            "Jurisdicción": "🇨🇴 Nacional",
            "Impuesto": rule['impuesto'],
            "Periodo": rule['periodo'],
            "Fecha": dates[idx],
            "Detalle": "Regla General"
        })
        
    return calendar

# ==========================================
# 3. LOGICA DEPARTAMENTAL (ATLÁNTICO)
# ==========================================
def get_atlantico_calendar():
    # Basado en la Resolución 000476 de 2025 [cite: 424, 426]
    calendar = []
    
    # Impuesto de Registro [cite: 491, 492]
    fechas_registro = [
        ("Enero", "2026-02-16"), ("Febrero", "2026-03-16"), ("Marzo", "2026-04-15"),
        ("Abril", "2026-05-15"), ("Mayo", "2026-06-16"), ("Junio", "2026-07-15")
    ]
    for per, fecha in fechas_registro:
        calendar.append({
            "Jurisdicción": "🌊 Atlántico",
            "Impuesto": "Impuesto de Registro",
            "Periodo": per,
            "Fecha": pd.to_datetime(fecha),
            "Detalle": "Fecha Fija"
        })

    # Tasa de Seguridad y Convivencia [cite: 509, 511]
    fechas_seguridad = [
        ("Enero", "2026-02-18"), ("Febrero", "2026-03-18"), ("Marzo", "2026-04-20")
    ]
    for per, fecha in fechas_seguridad:
        calendar.append({
            "Jurisdicción": "🌊 Atlántico",
            "Impuesto": "Tasa Seguridad y Convivencia",
            "Periodo": per,
            "Fecha": pd.to_datetime(fecha),
            "Detalle": "Fecha Fija"
        })

    # Estampillas Departamentales (Anual) 
    calendar.append({
        "Jurisdicción": "🌊 Atlántico",
        "Impuesto": "Estampillas Departamentales",
        "Periodo": "Anual 2026",
        "Fecha": pd.to_datetime("2027-01-31"),
        "Detalle": "Declaración Consolidada"
    })
    
    return calendar

# ==========================================
# 4. LOGICA DISTRITAL (BARRANQUILLA)
# ==========================================
def get_barranquilla_calendar(last_digit):
    # Basado en Resolución DSH 003 de 2025 [cite: 534]
    calendar = []
    digit = int(last_digit)
    
    # --- A. ICA ANUAL  ---
    # Tabla especifica: 0->15 Feb, 9->16 Feb...
    ica_map = {
        0: "2027-02-15", 9: "2027-02-16", 8: "2027-02-17", 7: "2027-02-18",
        6: "2027-02-19", 5: "2027-02-22", 4: "2027-02-23", 3: "2027-02-24",
        2: "2027-02-25", 1: "2027-02-26"
    }
    calendar.append({
        "Jurisdicción": "🏙️ Barranquilla",
        "Impuesto": "ICA (Industria y Comercio)",
        "Periodo": "Anual 2026",
        "Fecha": pd.to_datetime(ica_map[digit]),
        "Detalle": "Régimen Común"
    })
    
    # --- B. PREDIAL UNIFICADO  ---
    predial_fechas = [
        ("Con Descuento 10%", "2026-03-27"),
        ("Con Descuento 5%", "2026-05-29"),
        ("Sin Descuento (Límite)", "2026-06-30")
    ]
    for desc, fecha in predial_fechas:
        calendar.append({
            "Jurisdicción": "🏙️ Barranquilla",
            "Impuesto": "Impuesto Predial",
            "Periodo": "Vigencia 2026",
            "Fecha": pd.to_datetime(fecha),
            "Detalle": desc
        })

    # --- C. RETE-ICA BIMESTRAL (Ejemplo)  ---
    # Ejemplo Bimestre Ene-Feb (Vence Marzo). 
    # Tabla source 595: Digitos 0-9 -> 13/16 Mar. Digito 1 -> 27 Mar.
    # Implementación simplificada para demo:
    if digit in [0, 9]:
        f_mar = "2026-03-13" if digit == 0 else "2026-03-16"
    elif digit == 8: f_mar = "2026-03-17"
    elif digit == 7: f_mar = "2026-03-18"
    elif digit in [6, 5, 4]: f_mar = "2026-03-20" # Simplificado, tabla real varía por día
    elif digit in [3, 2]: f_mar = "2026-03-25"
    else: f_mar = "2026-03-27" # Digito 1

    calendar.append({
        "Jurisdicción": "🏙️ Barranquilla",
        "Impuesto": "Rete-ICA Bimestral",
        "Periodo": "Ene-Feb",
        "Fecha": pd.to_datetime(f_mar),
        "Detalle": "Agentes Retenedores"
    })
    
    return calendar

# ==========================================
# 5. INTERFAZ PRINCIPAL
# ==========================================

st.title("🗓️ Hub Tributario: Nacional, Atlántico y Barranquilla")
st.markdown("""
Consulta unificada de obligaciones tributarias para 2026. 
Normativa: **DIAN**, **Gobernación del Atlántico** [Res. 000476/25] y **Alcaldía de Barranquilla** [Res. DSH 003/25].
""")

# --- FILTROS ---
col1, col2 = st.columns([1, 2])
with col1:
    nit_input = st.text_input("NIT (Sin dígito de verificación)", placeholder="Ej: 800123456")

with col2:
    jurisdicciones = st.multiselect(
        "Seleccione Jurisdicciones:",
        ["Nacional (DIAN)", "Atlántico (Gobernación)", "Barranquilla (Distrito)"],
        default=["Nacional (DIAN)", "Atlántico (Gobernación)", "Barranquilla (Distrito)"]
    )

if nit_input and nit_input.isdigit():
    last_digit = int(nit_input[-1])
    last_two = nit_input[-2:]
    
    full_calendar = []
    
    # --- CONSTRUCCIÓN DE DATOS ---
    if "Nacional (DIAN)" in jurisdicciones:
        full_calendar.extend(get_national_calendar(last_digit, last_two))
        
    if "Atlántico (Gobernación)" in jurisdicciones:
        # Atlántico no depende del NIT (generalmente), pero lo incluimos si se selecciona
        full_calendar.extend(get_atlantico_calendar())
        
    if "Barranquilla (Distrito)" in jurisdicciones:
        full_calendar.extend(get_barranquilla_calendar(last_digit))
    
    # --- VISUALIZACIÓN ---
    if full_calendar:
        df = pd.DataFrame(full_calendar)
        df = df.sort_values(by="Fecha")
        
        st.divider()
        st.subheader(f"Resultados para NIT terminado en {last_digit}")
        
        # Iterar filas para crear tarjetas
        for i, row in df.iterrows():
            fecha_dt = row['Fecha']
            dias_restantes = (fecha_dt - datetime.now()).days + 1
            
            # Colores por jurisdicción
            color_border = "#ccc"
            if "Nacional" in row['Jurisdicción']: color_border = "#003366" # Azul oscuro DIAN
            elif "Atlántico" in row['Jurisdicción']: color_border = "#FF9900" # Naranja Gob
            elif "Barranquilla" in row['Jurisdicción']: color_border = "#009933" # Verde Bquilla
            
            # Semáforo de tiempo
            estado_icon = "🟢"
            if dias_restantes < 0: estado_icon = "🔴 Vencido"
            elif dias_restantes < 15: estado_icon = "🟠 Próximo"
            
            st.markdown(f"""
            <div style="
                background-color: white; 
                padding: 15px; 
                border-radius: 8px; 
                border-left: 6px solid {color_border};
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:bold; color:{color_border};">{row['Jurisdicción']}</span>
                    <span style="background-color:#eee; padding:2px 8px; border-radius:4px; font-size:0.9em;">
                        {estado_icon} ({dias_restantes} días)
                    </span>
                </div>
                <h3 style="margin:5px 0 0 0; font-size:18px;">{row['Impuesto']}</h3>
                <p style="margin:0; color:#555;">{row['Periodo']} - <i>{row['Detalle']}</i></p>
                <hr style="margin:8px 0;">
                <div style="font-size:16px; font-weight:bold;">
                    📅 Vence: {fecha_dt.strftime('%d de %B, %Y')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.info("Selecciona al menos una jurisdicción para ver los resultados.")

elif nit_input:
    st.error("El NIT debe ser numérico.")ancarios)
HOLIDAYS_2026 = [
    "2026-01-01", "2026-01-12", "2026-03-23", "2026-04-02", "2026-04-03", 
    "2026-05-01", "2026-05-18", "2026-06-08", "2026-06-15", "2026-06-29", 
    "2026-07-20", "2026-08-07", "2026-08-17", "2026-10-12", "2026-11-02", 
    "2026-11-16", "2026-12-08", "2026-12-25"
]

def get_business_days(start_date_str, num_days=10):
    """
    Genera una lista de 'num_days' días hábiles a partir de una fecha de inicio.
    Salta fines de semana y festivos definidos.
    """
    start_date = pd.to_datetime(start_date_str)
    dates = []
    current_date = start_date
    
    while len(dates) < num_days:
        # Si es sábado (5) o domingo (6) o festivo, avanzar
        if current_date.weekday() >= 5 or current_date.strftime("%Y-%m-%d") in HOLIDAYS_2026:
            current_date += timedelta(days=1)
            continue
        dates.append(current_date)
        current_date += timedelta(days=1)
        
    return dates

# ==========================================
# 2. GENERADOR DE CALENDARIO COMPLETO (BASE DE DATOS)
# ==========================================
# Aquí definimos SOLO la fecha de inicio del Dígito 1 para cada obligación.
# El sistema calculará el resto (Dígitos 2,3...0) automáticamente.

CALENDAR_RULES = [
    # --- RETENCIÓN EN LA FUENTE (Mensual) ---
    {"impuesto": "Retención en la Fuente", "periodo": "Enero", "start": "2026-02-10"},
    {"impuesto": "Retención en la Fuente", "periodo": "Febrero", "start": "2026-03-10"},
    {"impuesto": "Retención en la Fuente", "periodo": "Marzo", "start": "2026-04-07"}, # Ajustado por Semana Santa
    {"impuesto": "Retención en la Fuente", "periodo": "Abril", "start": "2026-05-11"},
    {"impuesto": "Retención en la Fuente", "periodo": "Mayo", "start": "2026-06-09"}, # Festivo el 8
    {"impuesto": "Retención en la Fuente", "periodo": "Junio", "start": "2026-07-07"},
    {"impuesto": "Retención en la Fuente", "periodo": "Julio", "start": "2026-08-11"}, # Festivo el 7
    {"impuesto": "Retención en la Fuente", "periodo": "Agosto", "start": "2026-09-08"},
    {"impuesto": "Retención en la Fuente", "periodo": "Septiembre", "start": "2026-10-06"},
    {"impuesto": "Retención en la Fuente", "periodo": "Octubre", "start": "2026-11-10"},
    {"impuesto": "Retención en la Fuente", "periodo": "Noviembre", "start": "2026-12-10"},
    {"impuesto": "Retención en la Fuente", "periodo": "Diciembre", "start": "2027-01-13"},

    # --- IVA BIMESTRAL ---
    {"impuesto": "IVA Bimestral", "periodo": "Bimestre 1 (Ene-Feb)", "start": "2026-03-10"},
    {"impuesto": "IVA Bimestral", "periodo": "Bimestre 2 (Mar-Abr)", "start": "2026-05-11"},
    {"impuesto": "IVA Bimestral", "periodo": "Bimestre 3 (May-Jun)", "start": "2026-07-07"},
    {"impuesto": "IVA Bimestral", "periodo": "Bimestre 4 (Jul-Ago)", "start": "2026-09-08"},
    {"impuesto": "IVA Bimestral", "periodo": "Bimestre 5 (Sep-Oct)", "start": "2026-11-10"},
    {"impuesto": "IVA Bimestral", "periodo": "Bimestre 6 (Nov-Dic)", "start": "2027-01-13"},

    # --- RENTA PERSONAS JURÍDICAS ---
    {"impuesto": "Renta Personas Jurídicas", "periodo": "1ra Cuota / Declaración", "start": "2026-05-11"},
    {"impuesto": "Renta Personas Jurídicas", "periodo": "2da Cuota", "start": "2026-07-07"},
    
    # --- RENTA GRANDES CONTRIBUYENTES ---
    {"impuesto": "Renta Grandes Contribuyentes", "periodo": "1ra Cuota", "start": "2026-02-10"},
    {"impuesto": "Renta Grandes Contribuyentes", "periodo": "2da Cuota / Declaración", "start": "2026-04-07"},
    {"impuesto": "Renta Grandes Contribuyentes", "periodo": "3ra Cuota", "start": "2026-06-09"},
]

def generate_full_calendar(nit_last_digit):
    """
    Crea la lista personalizada de fechas para un NIT específico.
    """
    my_calendar = []
    
    # 1. Procesar impuestos de 1 dígito (Regla general: 1 al 0)
    # El orden de vencimiento estándar DIAN es: 1, 2, 3, 4, 5, 6, 7, 8, 9, 0
    # Si mi NIT termina en 1, me toca el día 0. Si termina en 0, me toca el día 9.
    
    digit_map = {1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 0:9}
    day_index = digit_map[nit_last_digit]
    
    for rule in CALENDAR_RULES:
        dates = get_business_days(rule['start'], num_days=10)
        due_date = dates[day_index]
        
        my_calendar.append({
            "Impuesto": rule['impuesto'],
            "Periodo": rule['periodo'],
            "Fecha": due_date,
            "Categoria": "General / PJ / GC"
        })
        
    return pd.DataFrame(my_calendar)

def generate_natural_person_calendar(nit_last_two):
    """
    Genera fechas para Renta Personas Naturales (Regla de 2 dígitos)
    Inicio aprox: 11 Agosto 2026. Avanza 1 día por cada par de dígitos.
    """
    start_date_pn = "2026-08-11"
    # Generamos suficientes días hábiles para cubrir del 01 al 00 (50 días hábiles)
    dates_pn = get_business_days(start_date_pn, num_days=60)
    
    # NIT 01-02 -> Día 0
    # NIT 99-00 -> Día 49
    # Convertir NIT '00' a 100 para la matemática
    val = int(nit_last_two)
    if val == 0: val = 100
    
    # Índice: (Valor - 1) dividido en 2 (división entera)
    # Ej: 01 -> (1-1)//2 = 0. 02 -> (2-1)//2 = 0.
    day_index = (val - 1) // 2
    
    if day_index < len(dates_pn):
        due_date = dates_pn[day_index]
        return [{
            "Impuesto": "Renta Personas Naturales", 
            "Periodo": "Declaración Anual", 
            "Fecha": due_date,
            "Categoria": "Solo Personas Naturales"
        }]
    return []

# ==========================================
# 3. INTERFAZ DE USUARIO (UI)
# ==========================================

st.title("🗓️ Planificador Fiscal Anual 2026")
st.markdown("""
Esta herramienta proyecta **todas las obligaciones del año** para tu NIT, 
calculando los días hábiles automáticamente según el calendario DIAN.
""")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    nit_input = st.text_input("Ingresa tu NIT completo (Sin dígito de verificación)", placeholder="Ej: 900123456")

if nit_input and nit_input.isdigit():
    # --- LÓGICA DE CÁLCULO ---
    last_digit = int(nit_input[-1])
    last_two = nit_input[-2:]
    
    # 1. Generar calendario general (IVA, Rete, Renta PJ)
    df_general = generate_full_calendar(last_digit)
    
    # 2. Generar fecha de Persona Natural (Si aplica)
    pn_data = generate_natural_person_calendar(last_two)
    df_pn = pd.DataFrame(pn_data)
    
    # 3. Unir todo
    df_final = pd.concat([df_general, df_pn], ignore_index=True)
    df_final = df_final.sort_values(by="Fecha")
    
    # --- VISUALIZACIÓN ---
    st.divider()
    st.subheader(f"📅 Calendario Completo para NIT terminado en {last_digit}")
    
    # Crear pestañas para mejor organización
    tab1, tab2 = st.tabs(["📋 Lista Cronológica", "📊 Vista por Impuesto"])
    
    with tab1:
        # Iterar para mostrar como lista bonita
        for i, row in df_final.iterrows():
            fecha_str = row['Fecha'].strftime("%Y-%m-%d")
            mes_str = row['Fecha'].strftime("%B")
            dia_str = row['Fecha'].strftime("%d")
            
            # Estilo condicional para fechas pasadas
            color = "#0056b3" # Azul default
            if row['Fecha'] < pd.Timestamp.now():
                color = "#6c757d" # Gris (pasado)
            
            with st.container():
                c1, c2 = st.columns([1, 4])
                with c1:
                    st.markdown(f"""
                    <div style="text-align:center; background-color:{color}; color:white; border-radius:5px; padding:5px;">
                        <span style="font-size:12px">{row['Fecha'].strftime('%b').upper()}</span><br>
                        <span style="font-size:24px; font-weight:bold">{dia_str}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.markdown(f"**{row['Impuesto']}**")
                    st.caption(f"{row['Periodo']} - ({row['Categoria']})")
                st.write("") # Espacio
                
    with tab2:
        # Tabla dinámica filtrable
        st.dataframe(
            df_final[['Fecha', 'Impuesto', 'Periodo', 'Categoria']].style.format({"Fecha": lambda t: t.strftime("%Y-%m-%d")}),
            use_container_width=True,
            hide_index=True
        )

elif nit_input:
    st.error("El NIT debe contener solo números.")

